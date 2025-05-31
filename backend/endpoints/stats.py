import sys
from app_init import db
from utils import Status
from flask import Blueprint
from models.movies import Movie
from models.actors import Actor
from models.genres import Genre
from sqlalchemy import func, case
from models.directors import Director
from models.associations import movie_genres, movie_actors, movie_directors

stats = Blueprint("stats", __name__)


@stats.route("/stats", methods=["GET"])
def get_stats():
    """Get statistics about movies, actors, genres, and directors in the database.

    Returns:
        dict: A dictionary containing the status and statistics data.
    """
    stats = dict()

    movie_stats = dict()
    actor_stats = dict()
    director_stats = dict()

    if movie_stats:
        stats["movie_stats"] = movie_stats
    if actor_stats:
        stats["actor_stats"] = actor_stats
    if director_stats:
        stats["director_stats"] = director_stats

    return {
        **Status.SUCCESS.value,
        "data": stats,
    }
