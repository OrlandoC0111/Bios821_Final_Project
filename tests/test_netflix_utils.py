"""Test netflix_utils file."""

import pytest
from netflix_utils import parse_data


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
        "show_id", "type", "title", "director", "cast", "country", 
        "date_added", "release_year", "rating", "duration", "listed_in",
        "description"
    ]
    assert parsed_data["Column_Name"] == expected_columns
