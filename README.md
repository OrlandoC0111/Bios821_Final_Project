# Bios821_Final_Project - A Search Engine of Netflix

Welcome to the Search Engine of Netflix! This is a brief overview of the project, including 
setup instructions for end users and contributors.

## Setup/Installation Instructions

To use Netflix Project, follow these steps:

1. Clone the repository to your local machine.
2. Install the required dependencies by running `pip install -NAME`.
3. No local datasets required. You can access large-scale datasets through SQLite Database.  

## Examples
### Functions and Demos:
#### -  **most_common_genre_in_date_range**
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

#### - **rating_warning**
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

1. Fork the repository.
2. Make your changes on a feature branch.
3. Submit a pull request with a clear description of your changes.
