import os
import re
import json
import unicodedata

def create_json_file(filename: str, data: list[dict]) -> None:
    """
    Create a JSON file at the specified path with the given data.
    
    Args:
        filename (str): The name of the JSON file to be created.
        data (list[dict]): The data to be written to the JSON file.
    """

    current_dir = os.path.dirname(__file__)
    parent_dir = os.path.dirname(current_dir)
    destination_dir = os.path.join(parent_dir, "backend", "data")

    if not os.path.exists(destination_dir):
        print(f"Directory {destination_dir} does not exist. Creating it.")
        os.makedirs(destination_dir)

    file_path = os.path.join(destination_dir, filename)

    with open(file_path, "w") as json_file:
        json.dump(data, json_file, indent=4)


def create_slug(title: str) -> str:
    """
    Create a slug from the given title.
    
    Args:
        title (str): The title to be converted to a slug.
        
    Returns:
        str: The slugified version of the title.
    """
    
    # Normalize the strng to remove accents and special characters
    title = unicodedata.normalize("NFKD", title).encode("ascii", "ignore").decode("utf-8")

    # Convert to lowercase and strip whitespace
    title = title.strip().lower()

    # Replace spaces and conesecutive whitespace with a single hyphen
    title = re.sub(r"\s+", "-", title)

    # Remove any non-alphanumeric characters (except hyphens)
    title = re.sub(r"[^\w-]", "", title)

    # Remove leading and trailing hyphens
    title = title.strip("-")

    return title