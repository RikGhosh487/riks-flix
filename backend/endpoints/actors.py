from flask import Blueprint
from models.actors import Actor
from utils import query_pages, query_by_id
from schema.actors_schema import actors_schema, actor_schema

actors = Blueprint("actors", __name__)


@actors.route("/actors", methods=["GET"])
def get_actors() -> dict:
    base_query = Actor.query

    result = query_pages(base_query, actors_schema)

    if result["status"] == "success":
        result["data"]["actors"] = result["data"].pop("instances")

    return result


@actors.route("/actors/<string:id>", methods=["GET"])
def get_actor(id: str) -> dict:
    result = query_by_id(Actor, id, actor_schema)

    if result["status"] == "success":
        result["data"]["actor"] = result["data"].pop("instance")

    return result
