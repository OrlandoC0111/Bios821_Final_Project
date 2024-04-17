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
