from models.actors import Actor
from flask import Blueprint, request
from schema.actors_schema import actors_schema, actor_schema
from utils import (
    query_pages,
    query_by_id,
    apply_search_filters,
    parse_sort_parameters,
    parse_pagination_parameters,
)

actors = Blueprint("actors", __name__)


@actors.route("/actors", methods=["GET"])
def get_actors() -> dict:
    """
    Get a list of actors with pagination.

    Returns:
        dict: A dictionary containing the status and data of the query.
    """

    SEARCH_FIELDS = [
        Actor.name,
    ]

    SORT_FIELDS = [
        Actor.name,
    ]

    page_info = parse_pagination_parameters(request.args)
    sort_info = parse_sort_parameters(request.args, SORT_FIELDS)
    search_info = request.args.get("search", None)

    base_query = Actor.query
    if search_info is not None:
        base_query = apply_search_filters(base_query, search_info, SEARCH_FIELDS)
    base_query = base_query.order_by(
        sort_info if sort_info is not None else Actor.id, Actor.id
    )

    result = query_pages(base_query, actors_schema, page_info)

    if result["status"] == "success":
        result["data"]["actors"] = result["data"].pop("instances")

    return result


@actors.route("/actors/<string:id>", methods=["GET"])
def get_actor(id: str) -> dict:
    result = query_by_id(Actor, id, actor_schema)

    if result["status"] == "success":
        result["data"]["actor"] = result["data"].pop("instance")

    return result
