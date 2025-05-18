import os
import sys
import requests
from dotenv import load_dotenv
from utils import create_json_file, create_slug


# Load environment variables from .env file
load_dotenv()

# Get the API key and URL from the environment
api_key = os.getenv("TMDB_API_KEY")
api_url = os.getenv("TMDB_API_URL")

headers = {"accept": "application/json", "Authorization": f"Bearer {api_key}"}


def search_movie(title: str, year: int = None) -> dict:
    """
    Search for a movie by title using the TMDB API.
    Args:
        title (str): The title of the movie to search for.
        year (int, optional): The release year of the movie to search for.
    Returns:
        dict: A dictionary containing the movie details if found, otherwise None.
    """
    url = f"{api_url}/search/movie"
    params = {"query": title, "language": "en-US"}
    if year:
        params["year"] = year

    # Make the API request
    response = requests.get(url, headers=headers, params=params)
    data = response.json()

    if not data["results"]:
        return None

    # Try to find an exact title match (case-insensitive)
    for movie in data["results"]:
        if movie["title"].lower() == title.lower():
            return movie

    # If no exact match is found, return the first result
    return data["results"][0]


def search_person(name: str, known_for: str) -> dict:
    """
    Search for a person by name using the TMDB API.
    Args:
        name (str): The name of the person to search for.
        known_for (str): The department the person is known for.
    Returns:
        dict: A dictionary containing the person details if found, otherwise None.
    """
    url = f"{api_url}/search/person"
    params = {"query": name, "language": "en-US", "include_adult": "true", "page": 1}

    # Make the API request
    response = requests.get(url, headers=headers, params=params)
    data = response.json()

    if not data["results"]:
        return None

    # Try to find an exact name match (case-insensitive)
    for person in data["results"]:
        if (
            person["name"].lower() == name.lower()
            and person["known_for_department"] == known_for
        ):
            return person

    # If no exact match is found, return the first result
    return data["results"][0]


def get_movie_details(movie_id: int) -> dict:
    """
    Get detailed information about a movie using its ID.
    Args:
        movie_id (int): The ID of the movie to retrieve details for.
    Returns:
        dict: A dictionary containing detailed information about the movie.
    """
    url = f"{api_url}/movie/{movie_id}"
    params = {
        "language": "en-US",
        "append_to_response": "credits,images,videos,release_dates",
    }
    response = requests.get(url, headers=headers, params=params)

    return response.json()


def get_person_details(person_id: int) -> dict:
    """
    Get detailed information about a person using their ID.
    Args:
        person_id (int): The ID of the person to retrieve details for.
    Returns:
        dict: A dictionary containing detailed information about the person.
    """
    url = f"{api_url}/person/{person_id}"
    params = {"language": "en-US", "append_to_response": "movie_credits"}
    response = requests.get(url, headers=headers, params=params)

    return response.json()


def extract_person_info(data: dict) -> dict:
    """
    Extract relevant person information from the TMDB API response.
    Args:
        data (dict): The TMDB API response containing person details.
    Returns:
        dict: A dictionary containing the person's information.
    """
    person_data = {
        "name": data.get("name"),
        "biography": data.get("biography"),
        "photo_url": data.get("profile_path") if data.get("profile_path") else None,
        "imdb_id": data.get("imdb_id") if data.get("imdb_id") else None,
        "slug": create_slug(data.get("name")),
    }

    return person_data


def get_person_info(name: str, known_for: str) -> dict:
    """
    Get person information by name.
    Args:
        name (str): The name of the person to retrieve information for.
        known_for (str): The department the person is known for.
    Returns:
        dict: A dictionary containing the person's information.
    """

    person = search_person(name, known_for)
    if not person:
        return {"error": "Person not found"}
    person_id = person["id"]
    data = get_person_details(person_id)
    return extract_person_info(data)


def extract_movie_info(data: dict) -> tuple:
    """
    Extract relevant movie information from the TMDB API response.
    Args:
        data (dict): The TMDB API response containing movie details.
    Returns:
        tuple: A tuple containing the movie information, directors, and actors.
    """

    # Get YouTube trailer
    trailers = [
        video
        for video in data["videos"]["results"]
        if video["site"] == "YouTube" and video["type"] == "Trailer"
    ]
    # trailers_url = f"https://www.youtube.com/watch?v={trailers[0]["key"]}" if trailers else None
    trailers_url = trailers[0]["key"] if trailers else None

    # Get MPAA rating
    release_dates = data.get("release_dates", {}).get("results", [{}])
    for release_date in release_dates:
        if release_date.get("iso_3166_1") == "US":  # Check for US release
            for date in release_date.get("release_dates", []):
                if date.get("certification") != "":
                    mpaa_rating = date["certification"]
                    break
            break

    release_year = (
        int(data.get("release_date", "").split("-")[0])
        if data.get("release_date")
        else None
    )

    # Finalized movie information
    movie_data = {
        "title": data.get("title"),
        "release_year": release_year,
        "duration": data.get("runtime"),
        "tagline": data.get("tagline"),
        "description": data.get("overview"),
        "rating": data.get("vote_average"),
        "mpaa_rating": mpaa_rating,
        # prefix : https://image.tmdb.org/t/p/original
        "poster_url": data.get("poster_path") if data.get("poster_path") else None,
        "page_img_url": (
            data.get("backdrop_path") if data.get("backdrop_path") else None
        ),
        "trailer_url": trailers_url,
        "slug": create_slug(data.get("title"), context={"year": release_year}),
    }

    # Get genres
    movie_genres = []
    genres = data.get("genres", [])

    for genre in genres:
        movie_genres.append(
            {"movie_slug": movie_data["slug"], "genre_slug": create_slug(genre["name"])}
        )

    # Get director(s)
    movie_directors = []
    directors = [
        crew["name"] for crew in data["credits"]["crew"] if crew["job"] == "Director"
    ]

    for director in directors:
        director_slug = create_slug(director)

        if director_slug not in directors_map:
            director_data = get_person_info(director, "Directing")
            if "error" in director_data:
                continue

            directors_map[director_slug] = director_data

        movie_directors.append(
            {"movie_slug": movie_data["slug"], "director_slug": director_slug}
        )

    # Get actor(s) - top 5 cast members
    movie_actors = []
    cast = [actor["name"] for actor in data["credits"]["cast"][:5]]

    for actor in cast:

        actor_slug = create_slug(actor)

        if actor_slug not in actors_map:
            actor_data = get_person_info(actor, "Acting")
            if "error" in actor_data:
                continue
            actors_map[actor_slug] = actor_data

        movie_actors.append(
            {"movie_slug": movie_data["slug"], "actor_slug": actor_slug}
        )

    return movie_data, movie_genres, movie_directors, movie_actors


def get_movie_info(title: str, year: int = None) -> dict:
    """
    Get movie information by title.
    Args:
        title (str): The title of the movie to retrieve information for.
        year (int, optional): The release year of the movie to retrieve information for.
    Returns:
        dict: A dictionary containing the movie information.
    """
    movie = search_movie(title, year)
    if not movie:
        return {"error": "Movie not found"}

    movie_id = movie["id"]
    data = get_movie_details(movie_id)
    return extract_movie_info(data)


def parse_query_input(input_line):
    """
    Parse a single line of input into a query dictionary.
    Args:
        input_line (str): The input line containing the movie title and optional year.
    Returns:
        dict: A dictionary containing the parsed title and year.
    """
    parts = input_line.strip().split("@")
    if len(parts) == 2:
        return {"title": parts[0].strip(), "year": int(parts[1])}
    elif len(parts) == 1 and parts[0] != "":
        return {"title": parts[0].strip()}
    return None


if __name__ == "__main__":
    """
    This script processes movie queries, retrieves movie and person information from the TMDB API, and saves the data into JSON files. It supports both interactive input and input redirection. The script uses the TMDB API to:
    - Search for movies and people
    - Extract relevant information
    - Store the data in JSON files
    """
    queries: list[dict] = list()
    directors_map: dict[str, dict] = dict()
    actors_map: dict[str, dict] = dict()

    if os.isatty(sys.stdin.fileno()):
        # Interactive input
        query_input = input().strip()
        query = parse_query_input(query_input)
        if query:
            queries.append(query)
    else:
        # Input redirected
        lines = sys.stdin.readlines()

        for line in lines:
            query = parse_query_input(line)
            if query:
                queries.append(query)

    # Process each query
    movie_list = []
    movie_genres_list = []
    directors_list = []
    movie_directors_list = []
    actors_list = []
    movie_actors_list = []

    for query in queries:
        data = get_movie_info(query["title"], query.get("year"))
        if "error" in data[0]:
            print(f"Skipping Query: {query["title"]}. Reason: {data[0]["error"]}")
            continue

        movie_list.append(data[0])
        movie_genres_list.extend(data[1])
        movie_directors_list.extend(data[2])
        movie_actors_list.extend(data[3])

    directors_list = list(directors_map.values())
    actors_list = list(actors_map.values())

    # Create the JSON file with the movies
    create_json_file("movies.tmp.json", movie_list)

    # Create the JSON file with the movie_genres
    create_json_file("movie_genres.tmp.json", movie_genres_list)

    # Create the JSON file with the movie_directors
    create_json_file("movie_directors.tmp.json", movie_directors_list)

    # Create the JSON file with the directors
    create_json_file("directors.tmp.json", directors_list)

    # Create the JSON file with the movie_actors
    create_json_file("movie_actors.tmp.json", movie_actors_list)

    # Create the JSON file with the actors
    create_json_file("actors.tmp.json", actors_list)
