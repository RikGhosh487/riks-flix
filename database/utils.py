import json

def create_json_file(file_path: str, data: list[dict]) -> None:
    """
    Create a JSON file at the specified path with the given data.
    
    Args:
        file_path (str): The path where the JSON file will be created.
        data (list[dict]): The data to be written to the JSON file.
    """

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
    
    # Remove special characters and replace spaces with hyphens
    slug = title.lower().replace(" ", "-").replace("'", "").replace("\"", "")
    
    # Remove any remaining special characters
    slug = "".join(e for e in slug if e.isalnum() or e == "-")
    
    return slug