from models.movies import Movie
from flask import Blueprint, request
from schema.genres_schema import genres_schema
from schema.actors_schema import actors_schema
from schema.directors_schema import directors_schema
from schema.movies_schema import movies_schema, movie_schema
from utils import (
    query_pages,
    query_by_id,
    parse_exact_filters,
    apply_exact_filters,
    parse_range_filters,
    apply_range_filters,
    apply_search_filters,
    parse_sort_parameters,
    query_relations_by_id,
    parse_pagination_parameters,
)


movies = Blueprint("movies", __name__)


@movies.route("/movies", methods=["GET"])
def get_movies() -> dict:
    """
    Get a list of movies with pagination.

    Returns:
        dict: A dictionary containing the status and data of the query.
    """

    EXACT_FILTERS = [
        Movie.release_year,
        Movie.mpaa_rating,
    ]

    RANGE_FILTERS = [
        Movie.duration,
        Movie.release_year,
        Movie.rating,
    ]

    SEARCH_FIELDS = [
        Movie.title,
    ]

    SORT_FIELDS = [
        Movie.title,
        Movie.release_year,
        Movie.duration,
        Movie.rating,
    ]

    page_info = parse_pagination_parameters(request.args)
    sort_info = parse_sort_parameters(request.args, SORT_FIELDS)
    exact_filters = parse_exact_filters(request.args, EXACT_FILTERS)
    range_filters = parse_range_filters(request.args, RANGE_FILTERS)
    search_info = request.args.get("search", None)

    base_query = Movie.query
    if search_info is not None:
        base_query = apply_search_filters(base_query, search_info, SEARCH_FIELDS)
    base_query = apply_exact_filters(base_query, exact_filters)
    base_query = apply_range_filters(base_query, range_filters)
    base_query = base_query.order_by(
        sort_info if sort_info is not None else Movie.id, Movie.id
    )

    result = query_pages(base_query, movies_schema, page_info)

    if result["status"] == "success":
        result["data"]["movies"] = result["data"].pop("instances")

    return result


@movies.route("/movies/<string:id>", methods=["GET"])
def get_movie(id: str) -> dict:
    result = query_by_id(Movie, id, movie_schema)

    if result["status"] == "success":
        result["data"]["movie"] = result["data"].pop("instance")

    return result


@movies.route("/movies/<string:id>/actors", methods=["GET"])
def get_movie_actors(id: str) -> dict:
    result = query_relations_by_id(Movie, id, "actors", actors_schema)

    return result


@movies.route("/movies/<string:id>/directors", methods=["GET"])
def get_movie_directors(id: str) -> dict:
    result = query_relations_by_id(Movie, id, "directors", directors_schema)

    return result


@movies.route("/movies/<string:id>/genres", methods=["GET"])
def get_movie_genres(id: str) -> dict:
    result = query_relations_by_id(Movie, id, "genres", genres_schema)

    return result
