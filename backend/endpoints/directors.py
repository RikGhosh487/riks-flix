from flask import Blueprint, request
from models.directors import Director
from schema.directors_schema import directors_schema, director_schema
from utils import query_pages, query_by_id, parse_pagination_parameters

directors = Blueprint("directors", __name__)


@directors.route("/directors", methods=["GET"])
def get_actors() -> dict:
    """
    Get a list of directors with pagination.

    Returns:
        dict: A dictionary containing the status and data of the query.
    """

    page_info = parse_pagination_parameters(request.args)

    base_query = Director.query

    result = query_pages(base_query, directors_schema, page_info)

    if result["status"] == "success":
        result["data"]["actors"] = result["data"].pop("instances")

    return result


@directors.route("/directors/<string:id>", methods=["GET"])
def get_actor(id: str) -> dict:
    result = query_by_id(Director, id, director_schema)

    if result["status"] == "success":
        result["data"]["actor"] = result["data"].pop("instance")

    return result
