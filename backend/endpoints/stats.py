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


def fetch_movie_by_order(order):
    """
    Fetch a movie based on the specified order.

    Args:
        order: SQLAlchemy order clause to apply to the query.

    Returns:
        Movie instance or None if no movie is found.
    """
    movie = db.session.query(Movie).order_by(order).first()

    return (
        {
            "title": movie.title,
            "year": movie.release_year,
            "id": movie.id,
            "slug": movie.slug,
            "poster_url": movie.poster_url,
        }
        if movie
        else None
    )


def fetch_top_rated_movies(limit: int = 10):
    """
    Fetch top-rated movies.

    Args:
        limit (int): Number of top-rated movies to fetch. Defaults to 10.

    Returns:
        list: A list of dictionaries containing movie details.
    """
    return [
        {
            "title": movie.title,
            "rating": round(float(movie.rating), 2),
            "id": movie.id,
            "slug": movie.slug,
            "poster_url": movie.poster_url,
        }
        for movie in db.session.query(Movie)
        .filter(Movie.rating != None)
        .order_by(Movie.rating.desc())
        .limit(limit)
        .all()
    ]


def fetch_length_brackets():
    """
    Fetch the distribution of movie durations in length brackets.

    Returns:
        dict: A dictionary with duration brackets as keys and counts as values.
    """
    return dict(
        db.session.query(
            case(
                (Movie.duration < 90, "< 90 min"),
                (Movie.duration.between(90, 120), "90-120 min"),
                (Movie.duration.between(120, 150), "120-150 min"),
                (Movie.duration > 150, "> 150 min"),
                else_="Unknown",
            ).label("length_group"),
            func.count(Movie.id),
        )
        .group_by("length_group")
        .all()
    )


def fetch_avg_rating_by_year():
    """
    Fetch average movie ratings grouped by release year.

    Returns:
        dict: A dictionary with years as keys and average ratings as values.
    """
    return {
        year: round(float(avg), 2)
        for year, avg in db.session.query(Movie.release_year, func.avg(Movie.rating))
        .filter(Movie.rating != None)
        .group_by(Movie.release_year)
        .order_by(Movie.release_year)
        .all()
    }


def fetch_movie_stats():
    """
    Fetch statistics about movies
    """

    try:
        return {
            "total": db.session.query(func.count(Movie.id)).scalar(),
            "movies_by_year": dict(
                db.session.query(Movie.release_year, func.count(Movie.id))
                .group_by(Movie.release_year)
                .order_by(Movie.release_year)
                .all()
            ),
            "oldest_movie": fetch_movie_by_order(Movie.release_year.asc()),
            "newest_movie": fetch_movie_by_order(Movie.release_year.desc()),
            "average_duration": round(
                float(db.session.query(func.avg(Movie.duration)).scalar() or 0), 2
            ),
            "median_duration": db.session.query(
                func.percentile_cont(0.5).within_group(Movie.duration)
            ).scalar()
            or 0,
            "longest_movie": fetch_movie_by_order(Movie.duration.desc()),
            "shortest_movie": fetch_movie_by_order(Movie.duration.asc()),
            "mpaa_distribution": dict(
                db.session.query(Movie.mpaa_rating, func.count(Movie.id))
                .group_by(Movie.mpaa_rating)
                .all()
            ),
            "top_ratind_movies": fetch_top_rated_movies(),
            "length_brackets": fetch_length_brackets(),
            "average_rating_by_year": fetch_avg_rating_by_year(),
        }
    except Exception as e:
        print(f"Error fetching movie stats: {e}", file=sys.stderr)
        return None


@stats.route("/stats", methods=["GET"])
def get_stats():
    """Get statistics about movies, actors, genres, and directors in the database.

    Returns:
        dict: A dictionary containing the status and statistics data.
    """
    stats = dict()

    movie_stats = fetch_movie_stats()
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
