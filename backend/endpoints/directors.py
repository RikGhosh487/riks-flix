from flask import Blueprint, request
from models.directors import Director
from schema.directors_schema import directors_schema, director_schema
from utils import (
    query_pages,
    query_by_id,
    parse_sort_parameters,
    parse_pagination_parameters,
)

directors = Blueprint("directors", __name__)


@directors.route("/directors", methods=["GET"])
def get_actors() -> dict:
    """
    Get a list of directors with pagination.

    Returns:
        dict: A dictionary containing the status and data of the query.
    """

    SORT_FIELD = [
        Director.name,
    ]

    page_info = parse_pagination_parameters(request.args)
    sort_info = parse_sort_parameters(request.args, SORT_FIELD)

    base_query = Director.query

    base_query = base_query.order_by(
        sort_info if sort_info is not None else Director.id, Director.id
    )

    result = query_pages(base_query, directors_schema, page_info)

    if result["status"] == "success":
        result["data"]["directors"] = result["data"].pop("instances")

    return result


@directors.route("/directors/<string:id>", methods=["GET"])
def get_actor(id: str) -> dict:
    result = query_by_id(Director, id, director_schema)

    if result["status"] == "success":
        result["data"]["directors"] = result["data"].pop("instance")

    return result
