import os
import requests
from dotenv import load_dotenv
from utils import create_json_file, create_slug


# load environment variables from .env file
load_dotenv()

# Get the API key and URL from the environment
api_key = os.getenv('TMDB_API_KEY')
api_url = os.getenv('TMDB_API_URL')

url = f"{api_url}/genre/movie/list?language=en"

headers = {
    "accept": "application/json",
    "Authorization": f"Bearer {api_key}"
}


response = requests.get(url, headers=headers)
response_json = response.json()


if response.status_code == 200:
    genres = response_json.get('genres', [])
    
    if genres:
        for genre in genres:
            genre['slug'] = create_slug(genre['name'])
            genre.pop('id', None)

        # Create the JSON file with the genres
        file_path = os.path.join(os.path.dirname(__file__), 'genres.tmp.json')
        create_json_file(file_path, genres)
        print(f"Genres JSON file created at {file_path}")

else:
    print(f"Error: {response.status_code}")
    print(response_json)