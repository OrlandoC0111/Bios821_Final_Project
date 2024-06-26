"""Test netflix_utils file."""

import csv
import os
import sqlite3

import pytest
from netflix_utils import (
    common_genre,
    filter_titles,
    parse_data,
    rating_warning,
)

DB_NAME = "netflix.db"


def populate_test_database(db_name: str) -> None:
    """Populate the test database with sample data."""
    netflix_titles_table = [
        [
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
        [
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
            "Geralt of Rivia, a mutated monster-hunter for hire.",
        ],
        [
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
            "When a young boy disappears, his mother, a police chief.",
        ],
        [
            "s3",
            "Movie",
            "The Irishman",
            "Martin Scorsese",
            "Robert De Niro, Al Pacino, Joe Pesci",
            "United States",
            "2019-11-27",
            "2019",
            "R",
            "209 min",
            "Biography, Crime, Drama",
            "An aging hitman recalls his time with the mob.",
        ],
        [
            "s4",
            "Movie",
            "The Dark Knight",
            "Christopher Nolan",
            "Christian Bale, Heath Ledger, Aaron Eckhart",
            "United States",
            "2020-03-15",
            "2008",
            "PG-13",
            "152 min",
            "Action, Crime, Drama",
            "When the menace known as the Joker wreaks havoc.",
        ],
    ]

    conn = sqlite3.connect(db_name)
    c = conn.cursor()

    # Create table (if not already created)
    c.execute(
        """CREATE TABLE IF NOT EXISTS netflix_titles (
            show_id TEXT,
            type TEXT,
            title TEXT PRIMARY KEY,
            director TEXT,
            cast TEXT,
            country TEXT,
            date_added TEXT,
            release_year TEXT,
            rating TEXT,
            duration TEXT,
            listed_in TEXT,
            description TEXT
        )"""
    )

    # Insert Netflix titles data
    for title_data in netflix_titles_table[1:]:
        c.execute(
            """INSERT OR REPLACE INTO netflix_titles (
                show_id, type, title, director, cast, country,
                date_added, release_year, rating, duration,
                listed_in, description
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            title_data,
        )

    conn.commit()
    conn.close()


def test_parse_data() -> None:
    """Test parse_data() function."""
    if os.path.exists(DB_NAME):
        os.remove(DB_NAME)
    netflix_titles_table = [
        [
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
        [
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
            "Geralt of Rivia, a mutated monster-hunter for hire, "
            "journeys toward his destiny in a turbulent world "
            "where people often prove more wicked than beasts.",
        ],
        [
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
            "When a young boy disappears, his mother, a police chief, and his "
            "friends must confront terrifying supernatural forces in order"
            " to get him back.",
        ],
        [
            "s3",
            "Movie",
            "The Irishman",
            "Martin Scorsese",
            "Robert De Niro, Al Pacino, Joe Pesci",
            "United States",
            "2019-11-27",
            "2019",
            "R",
            "209 min",
            "Biography, Crime, Drama",
            "An aging hitman recalls his time with the mob and intersecting"
            "events with his friend, Jimmy Hoffa, through the 1950-70s.",
        ],
        [
            "s4",
            "Movie",
            "The Dark Knight",
            "Christopher Nolan",
            "Christian Bale, Heath Ledger, Aaron Eckhart",
            "United States",
            "2020-03-15",
            "2008",
            "PG-13",
            "152 min",
            "Action, Crime, Drama",
            "When the menace known as the Joker wreaks havoc.",
        ],
    ]
    # Write the sample data to a temporary CSV file
    temp_file = "temp_netflix_data.csv"
    with open(temp_file, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(netflix_titles_table)

    # Write the sample data to a temporary CSV file
    temp_file = "temp_netflix_data.csv"
    with open(temp_file, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(netflix_titles_table)

    # Call the parse_data function with the temporary CSV file
    result = parse_data(temp_file)

    # Create the expected dictionary from the netflix_titles_table
    expected_dict = {
        "Column_Name": netflix_titles_table[0],
        "The Witcher": netflix_titles_table[1],
        "Stranger Things": netflix_titles_table[2],
        "The Irishman": netflix_titles_table[3],
        "The Dark Knight": netflix_titles_table[4],
    }

    # Assert the returned dictionary matches the expected dictionary
    assert result == expected_dict


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
            "Geralt of Rivia, a mutated monster-hunter for hire.",
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
            "When a young boy disappears, his mother, a police chief.",
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
            "A family saga with a supernatural twist.",
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
            "An anthology series exploring a twisted.",
        ],
    }

    # Test case 1: Filter by country and rating
    filters = {"country": "United States", "rating": "TV-MA"}
    expected_output = ["The Witcher"]
    actual_output = filter_titles(netflix_titles, **filters)
    assert actual_output == expected_output, (
        f"Test case 1 failed: Expected {expected_output},"
        f"but got {actual_output}"
    )

    # Test case 2: Filter by type and release_year
    filters = {"type": "TV Show", "release_year": "2016"}
    expected_output = ["Stranger Things"]
    actual_output = filter_titles(netflix_titles, **filters)
    assert actual_output == expected_output, (
        f"Test case 2 failed: Expected {expected_output}, "
        f"but got {actual_output}"
    )

    # Test case 3: Filter with no matches
    filters = {"country": "France"}
    expected_output = []
    actual_output = filter_titles(netflix_titles, **filters)
    assert actual_output == expected_output, (
        f"Test case 3 failed: Expected {expected_output},"
        f"but got {actual_output}"
    )


def test_rating_warning() -> None:
    """Test rating_warning() function."""
    if os.path.exists(DB_NAME):
        os.remove(DB_NAME)
    populate_test_database(DB_NAME)
    # Test cases
    test_cases = [
        # Suitable for kids
        ("The Dark Knight", 14, "Bravo! Your kids can watch this movie!"),
        ("Stranger Things", 16, "Bravo! Your kids can watch this movie!"),
        # Need parental guidance
        ("The Dark Knight", 13, "Look out! We suggest parental guidance."),
        ("The Irishman", 17, "Look out! We suggest parental guidance."),
        # Not suitable for kids
        (
            "The Irishman",
            10,
            "Sorry, your kids are not suitable for this movie.",
        ),
        (
            "The Witcher",
            14,
            "Sorry, your kids are not suitable for this movie.",
        ),
        # Non-existent movie
        ("Non-existent Movie", 10, ValueError),
    ]

    # Iterate through test cases
    for movie_name, kid_age, expected_result in test_cases:
        if expected_result == ValueError:
            with pytest.raises(ValueError):
                rating_warning(DB_NAME, movie_name, kid_age)
        else:
            assert (
                rating_warning(DB_NAME, movie_name, kid_age) == expected_result
            )


def test_common_genre() -> None:
    """Test common_genre function for various edge cases."""
    if os.path.exists(DB_NAME):
        os.remove(DB_NAME)
    populate_test_database(DB_NAME)

    # Test for the most common genres from 2015 to 2020 where genres overlap
    expected_genres = sorted(["Drama"])
    actual_genres = sorted(common_genre(2015, 2020, DB_NAME))
    assert (
        actual_genres == expected_genres
    ), f"Expected genres {expected_genres} but got {actual_genres}."

    # Test for no movies in the period from 1900 to 1901
    with pytest.raises(ValueError) as excinfo:
        common_genre(1900, 1901, DB_NAME)
    assert "There are no movies released in this period" in str(excinfo.value)

    # Test for invalid input where start year is greater than end year
    with pytest.raises(ValueError) as excinfo:
        common_genre(2021, 2020, DB_NAME)
    assert "Start year must be earlier than or equal to end year" in str(
        excinfo.value
    )


if __name__ == "__main__":
    pytest.main([__file__])
