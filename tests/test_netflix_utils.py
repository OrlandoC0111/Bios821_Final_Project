"""Test netflix_utils file."""

import csv
import os
import sqlite3

import pytest

from netflix_utils import filter_titles, parse_data

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
            "Geralt of Rivia, a mutated monster-hunter for hire, journeys toward his destiny in a turbulent world where people often prove more wicked than beasts.",
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
            "When a young boy disappears, his mother, a police chief, and his friends must confront terrifying supernatural forces in order to get him back.",
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
            "An aging hitman recalls his time with the mob and the intersecting events with his friend, Jimmy Hoffa, through the 1950-70s.",
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
            "When the menace known as the Joker wreaks havoc and chaos on the people of Gotham, Batman must accept one of the greatest psychological and physical tests of his ability to fight injustice.",
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
            "Geralt of Rivia, a mutated monster-hunter for hire, journeys toward his destiny in a turbulent world where people often prove more wicked than beasts.",
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
            "When a young boy disappears, his mother, a police chief, and his friends must confront terrifying supernatural forces in order to get him back.",
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
            "An aging hitman recalls his time with the mob and the intersecting events with his friend, Jimmy Hoffa, through the 1950-70s.",
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
            "When the menace known as the Joker wreaks havoc and chaos on the people of Gotham, Batman must accept one of the greatest psychological and physical tests of his ability to fight injustice.",
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

    # Test case 3: Filter with no matches
    filters = {"country": "France"}
    expected_output = []
    actual_output = filter_titles(netflix_titles, **filters)
    assert (
        actual_output == expected_output
    ), f"Test case 3 failed: Expected {expected_output}, but got {actual_output}"



def test_rating_warning() -> None:
    """Test rating_warning() function."""
    if os.path.exists(DB_NAME):
        os.remove(DB_NAME)
    populate_test_database(DB_NAME)
