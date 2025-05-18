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


def slugify(text: str) -> str:
    """
    Convert a string to a URL-friendly slug.
    Args:
        text (str): The string to be converted to a slug.
    Returns:
        str: The slugified version of the string.
    """
    # Normalize the string to remove accents and special characters
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("utf-8")
    text = text.strip().lower()     # Convert to lowercase and strip whitespace
    text = re.sub(r"[^a-z0-9]+", "-", text)  # Replace spaces and consecutive whitespace with a single hyphen
    text = re.sub(r"-+", "-", text)  # Replace consecutive hyphens with a single hyphen
    text = re.sub(r"^-|-$", "", text)  # Remove leading and trailing hyphens
    return text


def create_slug(base: str, context: dict = None) -> str:
    """
    Create a slug from the given title.
    Args:
        base (str): The title to be slugified.
        context (dict, optional): Additional context for slug creation. Defaults to None.
    Returns:
        str: The slugified version of the title.
    """
    slug_parts = [slugify(base)]

    if context:
        for _, val in context.items():
            slug_parts.append(slugify(val if isinstance(val, str) else str(val)))

    slug = "-".join(slug_parts)

    return slug