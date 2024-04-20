"""Netflix data analysis."""

import csv
import sqlite3
from typing import Dict, List, Union


def parse_data(netflix_data: str) -> Dict[str, List[str]]:
    """Parse local file into database, then retrieve everything."""
    # Connect to the database (or create it if it doesn't exist)
    conn = sqlite3.connect("netflix.db")
    cursor = conn.cursor()

    # Create a table to store the data
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS netflix_titles
                      (show_id TEXT, type TEXT, title TEXT PRIMARY KEY, 
                      director TEXT,cast TEXT, country TEXT, date_added TEXT, 
                      release_year TEXT,rating TEXT, duration TEXT, 
                      listed_in TEXT, description TEXT)"""
    )

    # Open the CSV file and read the data
    with open(netflix_data) as file:
        csv_reader = csv.reader(file)
        headers = next(csv_reader)  # Read the header row

        # Insert the data into the database
        for row in csv_reader:
            cursor.execute(
                """INSERT OR REPLACE INTO netflix_titles
                              (show_id, type, title, director, cast, country,
                               date_added, release_year, rating, duration,
                               listed_in, description)
                              VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                row,
            )

    # Commit the changes and close the database connection
    conn.commit()
    conn.close()

    # Retrieve the data from the database
    conn = sqlite3.connect("netflix.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM netflix_titles")
    data = cursor.fetchall()

    # Close the database connection
    conn.close()

    # Convert the data into the desired dictionary format
    result = {}
    column_names = headers

    for row in data:
        title = row[2]  # Get the title from the third column
        values = list(row)  # Get all columns as values, including the title
        result[title] = values

    result["Column_Name"] = column_names

    return result


def rating_warning(netflix_db: str, movie_name: str, kid_age: int) -> str:
    """Determine if a movie is suitable for a specific aged kid to watch.

    Args:
        netflix_db (str): Path to the Netflix SQLite database.
        movie_name (str): Name of the movie to check.
        kid_age (int): Age of the kid.

    Returns:
        str: A suggestion for the kid based on the movie rating and kid's age.
             Possible suggestions: 'Suitable', 'Parental Guidance Suggested',
             'Sorry, your kids are not suitable for this movie'.

    Raises:
        ValueError: If the kid's age is not strictly greater than 0
        or the movie rating is not found.
    """
    # Validate input: kid's age should be strictly greater than 0
    if kid_age <= 0:
        raise ValueError("Kid's age must be strictly greater than 0.")

    # Connect to the SQLite database
    conn = sqlite3.connect(netflix_db)
    cursor = conn.cursor()

    # Retrieve the rating of the movie from the database
    cursor.execute(
        "SELECT rating FROM netflix_titles " "WHERE title=?", (movie_name,)
    )
    row = cursor.fetchone()
    conn.close()
    if row is None:
        raise ValueError("Movie rating not found.")
    # Movie not found in the database

    rating = row[0]

    # Determine the minimum age for the movie based on its rating
    if rating == "TV-MA" or rating == "R" or rating == "NC-17":
        minimum_age = 17
    elif rating == "TV-14":
        minimum_age = 14
    elif rating == "TV-PG":
        minimum_age = 8
    elif (
        rating == "G"
        or rating == "TV-G"
        or rating == "TV-Y"
        or rating == "TV-Y7"
        or rating == "TV-Y7-FV"
    ):
        minimum_age = 0
    elif rating == "PG":
        minimum_age = 8
    elif rating == "PG-13":
        minimum_age = 13
    else:
        raise ValueError(
            "Unknown rating or unrated movie. "
            "Please check your input ratings again."
        )

    # Unknown or unhandled rating

    # Compare the minimum age with the kid's age and provide suggestion
    if kid_age > minimum_age:
        return "Bravo! Your kids can watch this movie!"
    elif kid_age == minimum_age:
        return "Look out! We suggest parental guidance."
    else:
        return "Sorry, your kids are not suitable for this movie."


def filter_titles(
    netflix_titles: Dict[str, List[str]], **filters: Union[str, List[str]]
) -> List[str]:
    """Search for title that comply with the filter requirement."""
    filtered_titles = []
    column_names = netflix_titles["Column_Name"]

    for title, values in netflix_titles.items():
        if title == "Column_Name":
            continue

        match = True
        for key, value in filters.items():
            if key in column_names:
                index = column_names.index(key)
                if values[index]:  # Check if the value is not empty
                    if isinstance(value, list):
                        if values[index] not in value:
                            match = False
                            break
                    else:
                        if values[index] != value:
                            match = False
                            break
                else:
                    match = False
                    break

        if match:
            filtered_titles.append(title)

    return filtered_titles


def common_genre(start_year: int, end_year: int, netflix_db: str) -> List[str]:
    """Determine the most common genre in a date range.

    Args:
        start_year (int): The start year of the period to analyze.
        end_year (int): The end year of the period to analyze.
        netflix_db (str): Path to the SQLite database file.

    Returns:
        list[str]: The most common genre in the date range.

    Raises:
        ValueError: If start_year is greater than end_year.
    """
    # Connect to the SQLite database
    conn = sqlite3.connect(netflix_db)
    cursor = conn.cursor()

    # Validate input: if start date is later than the end date.
    if start_year > end_year:
        raise ValueError(
            "Start year must be earlier than or equal to end year."
        )

    # Retrieve the movies and shows from the database
    cursor.execute(
        """SELECT title, release_year, listed_in FROM netflix_titles"""
    )
    movies = cursor.fetchall()
    conn.close()
    if not movies:
        raise ValueError("There are no movies released in this period")

    genre_count: Dict[str, int] = {}
    for _title, release_year, genres in movies:
        if start_year <= int(release_year) <= end_year:
            for genre in genres.split(", "):
                if genre in genre_count:
                    genre_count[genre] += 1
                else:
                    genre_count[genre] = 1

    # Determine the most common genre
    if not genre_count:
        raise ValueError("There are no movies released in this period")

    max_count = max(genre_count.values())
    most_genres = [
        genre for genre, count in genre_count.items() if count == max_count
    ]

    return most_genres
