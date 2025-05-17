# Database Module for Riks-Flix

This directory contains the API query logic for managing and processing movie-related data in the **Riks-Flix** project. It handles interactions with external APIs (TMDB API), processes movie queries, and organizes data into structured formats for storage and future use.

---

## Features

- **Movie Query Processing**:
    - Parses user input to retrieve movie details from an external API (TMDB).
    - Supports both interactive input and input redirection for batch processing.

- **Data Extraction**:
    - Extracts detailed information about movies, including:
        - Title, release year, duration, tagline, and description.
        - Genres, directors, and top actors.
        - Ratings, trailers, and poster URLs.

- **Data Organization**:
    - Organizes extracted data into structured JSON files:
        - Movies
        - Genres
        - Directors
        - Actors
        - Relationships between movies and their genres, directors, and actors.

- **Error Handling**:
    - Skips invalid or incomplete queries with appropriate error messages.

---

## Directory Structure
```
database/
|---- get_movie.py # Main script for processing movie queries and extracting data.
|---- get_genres.py # Gets a list of supported genres from the external API
|---- utils.py # Utility functions for data processing
|---- db_schema.dbml # Contains the database schema for storing the data
|---- database_schema_diagram.jpeg # Diagram for the database schema and relations
|---- README.md # This file
```

---

## How to Use

### 1. **Run The Script**
To process movie queries, run the `get_movies.py` script:

```bash
python3 get_movie.py
```

- **Interactive Mode:** Enter movie queries one at a time in the format `title@year`.
- **Batch Mode:** Redirect a file containing multiple queries to the script:

```bash
cat queries.tmp.txt | python3 get_movie.py
```

### 2. Input Format
Each query should be in the format:
```title@year```

- Example:
```
Inception@2010
The Matrix@1999
```

### 3. Output
The script generates the following JSON files in the `\backend\data` directory:
- `movies.tmp.json`: Contains movie details.
- `movie_genres.tmp.json`: Maps movies to their genres.
- `movie_directors.tmp.json`: Maps movies to their directors.
- `directors.tmp.json`: Contans director details.
- `movie_actors.tmp.json`: Contains actor details.