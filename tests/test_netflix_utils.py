"""Test netflix_utils file."""

import pytest

from netflix_utils import filter_titles, parse_data


@pytest.fixture
def sample_netflix_data():
    """Fixture to provide the path to the sample Netflix data."""
    return "sample_data.csv"


def test_parse_data(sample_netflix_data):
    """Test parse_data function."""
    # Call the parse_data function with the sample Netflix data
    parsed_data = parse_data(sample_netflix_data)

    # Check if the parsed data contains the correct keys
    assert "Dick Johnson Is Dead" in parsed_data
    assert "Blood & Water" in parsed_data
    assert "Ganglands" in parsed_data

    # Check if the column names are correct
    expected_columns = [
        "show_id",
        "type",
        "title",
        "director",
        "cast",
        "country",
        "date_added",
        "release_year",
        "rating",
        "duration",
        "listed_in",
        "description",
    ]
    assert parsed_data["Column_Name"] == expected_columns


def test_filter_titles() -> None:
    """Test filter_titles() function."""
    # Create a sample Dict[str, List[str]] object
    netflix_titles = {
        "Column_Name": [
            "show_id",
            "type",
            "title",
            "director",
            "cast",
            "country",
            "date_added",
            "release_year",
            "rating",
            "duration",
            "listed_in",
            "description",
        ],
        "The Witcher": [
            "s1",
            "TV Show",
            "The Witcher",
            "Lauren Schmidt Hissrich",
            "Henry Cavill, Anya Chalotra, Freya Allan",
            "United States",
            "2019-12-20",
            "2019",
            "TV-MA",
            "2 Seasons",
            "Action, Adventure, Drama",
            "Geralt of Rivia, a mutated monster-hunter for hire, journeys toward his destiny in a turbulent world where people often prove more wicked than beasts.",
        ],
        "Stranger Things": [
            "s2",
            "TV Show",
            "Stranger Things",
            "The Duffer Brothers",
            "Millie Bobby Brown, Finn Wolfhard, Winona Ryder",
            "United States",
            "2016-07-15",
            "2016",
            "TV-14",
            "4 Seasons",
            "Drama, Fantasy, Horror",
            "When a young boy disappears, his mother, a police chief, and his friends must confront terrifying supernatural forces in order to get him back.",
        ],
        "Dark": [
            "s3",
            "TV Show",
            "Dark",
            "Baran bo Odar",
            "Louis Hofmann, Karoline Eichhorn, Lisa Vicari",
            "Germany",
            "2017-12-01",
            "2017",
            "TV-MA",
            "3 Seasons",
            "Crime, Drama, Mystery",
            "A family saga with a supernatural twist, set in a German town where the disappearance of two young children exposes the relationships among four families.",
        ],
        "Black Mirror": [
            "s4",
            "TV Show",
            "Black Mirror",
            "Charlie Brooker",
            "Jesse Plemons, Cristin Milioti, Jimmi Simpson",
            "United Kingdom",
            "2011-12-04",
            "2011",
            "TV-MA",
            "5 Seasons",
            "Drama, Science Fiction, Thriller",
            "An anthology series exploring a twisted, high-tech multiverse where humanity's greatest innovations and darkest instincts collide.",
        ],
    }

    # Test case 1: Filter by country and rating
    filters = {"country": "United States", "rating": "TV-MA"}
    expected_output = ["The Witcher"]
    actual_output = filter_titles(netflix_titles, **filters)
    assert (
        actual_output == expected_output
    ), f"Test case 1 failed: Expected {expected_output}, but got {actual_output}"

    # Test case 2: Filter by type and release_year
    filters = {"type": "TV Show", "release_year": "2016"}
    expected_output = ["Stranger Things"]
    actual_output = filter_titles(netflix_titles, **filters)
    assert (
        actual_output == expected_output
    ), f"Test case 2 failed: Expected {expected_output}, but got {actual_output}"

    # Test case 3: Filter by listed_in (single value)
    filters = {"listed_in": "Crime"}
    expected_output = ["Dark"]
    actual_output = filter_titles(netflix_titles, **filters)
    assert (
        actual_output == expected_output
    ), f"Test case 3 failed: Expected {expected_output}, but got {actual_output}"

    # Test case 4: Filter by listed_in (multiple values)
    filters = {"listed_in": ["Drama", "Science Fiction"]}
    expected_output = ["Black Mirror"]
    actual_output = filter_titles(netflix_titles, **filters)
    assert (
        actual_output == expected_output
    ), f"Test case 4 failed: Expected {expected_output}, but got {actual_output}"

    # Test case 5: Filter with no matches
    filters = {"country": "France"}
    expected_output = []
    actual_output = filter_titles(netflix_titles, **filters)
    assert (
        actual_output == expected_output
    ), f"Test case 5 failed: Expected {expected_output}, but got {actual_output}"

    print("All test cases passed!")
