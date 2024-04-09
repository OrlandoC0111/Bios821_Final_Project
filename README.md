# Bios821_Final_Project - A Search Engine of Netflix

Welcome to the Search Engine of Netflix!  
This project provides tools for simple analytical capabilities on a tabular dataset consisting over 8000 movies or TV shows available on Netflix.
- A table of listings of relevant informations - casts, directors, etc.: netflix_titles.csv: 
https://www.kaggle.com/datasets/shivamb/netflix-shows

This is a brief overview of the project, including setup instructions for end users and contributors.  

## Setup/Installation Instructions

To use Netflix Project, follow these steps:

1. Clone the repository to your local machine by using `git clone https://github.com/OrlandoC0111/Bios821_Final_Project.git`.  
2. No local datasets required. You can access large-scale datasets through SQLite Database.  

## Expected Input File Formats

The Netflix Data Analysis package expects input files in the following formats:

- netflix_titles: CSV (Comma-Separated Values) file with columns:
- 'show_id': Unique ID for every Movie / Tv Show
- 'type': Identifier - A Movie or TV Show
- 'title': Title of the Movie / Tv Show
- 'director': Director of the Movie
- 'cast': Actors involved in the movie / show
- 'country': Country where the movie / show was produced
- 'data_added': Date it was added on Netflix
- 'release_year': Actual Release year of the move / show
- 'rating': TV Rating of the movie / show
- 'duration': Total Duration - in minutes or number of seasons
- 'listed_in': Genere
- 'description': The summary description


## Project Plans:
### Functions and Demos:
#### **filter_title()**
The function filter_title() takes the data and return the title(s) of the Movie / TV show that comply with the filter requirement. This function should allow user to flexible filtering criteria.  
**Demo Code:**
```
filter_titles(netflix_titles, country=['United States', 'Canada'], rating='PG-13')
```

####  **most_common_genre_in_date_range**
This function analyzes the Netflix dataset to determine which movie genre was most frequently released in a given date range. The date range is specified with precise start and end dates, allowing for detailed analysis over specific periods.  

**Parameters:**
1. **start_date**: A string representing the start date of the period to analyze, formatted as **"YYYY-MM-DD"**.
2. **end_date**: A string representing the end date of the period to analyze, formatted as **"YYYY-MM-DD"**.
3. **dataframe**: The DataFrame containing Netflix titles, which includes columns for title type, release date, and genre.  

**Demo Code:**
```
genre, count = most_common_genre_in_date_range("2019-01-01", "2020-12-31", netflix_dataframe)
print(f"The most common genre was '{genre}' with {count} times.")
```

####  **rating_warning**
This function analyzes the Netflix dataset to determine if a specific movie or TV show given its title is allowed for specific aged kids to watch. Returns are bool.  

**Paramters:**
1. **Title_of_show:** A string representing the title of the movie or TV Show. Space is allowed.  
2. **age_of_kids:** An integer representing the age of the kids.  

**Demo Code:**
```
rating_warning("NAME OF SHOW" , age:int) -> bool
```

## Contributing

I welcome contributions to My Project! If you would like to contribute.
Please follow these guidelines:

1. Clone the repository:
git clone https://github.com/OrlandoC0111/Bios821_Final_Project.git
2. Create a branch for new feature.
3. Make your changes and ensure that the code passes all tests.
4. Submit a pull request describing your changes.


To run the tests locally, follow these steps:

1. Make sure you have the pytest package installed: pip install pytest
2. Run the tests using pytest:
pytest test_netflix.py
3. Ensure that all tests pass successfully.
