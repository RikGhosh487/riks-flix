import sys
from app_init import db
from utils import Status
from flask import Blueprint
from models.movies import Movie
from models.actors import Actor
from models.genres import Genre
from collections import defaultdict
from models.directors import Director
from sqlalchemy import func, case, distinct
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


def fetch_actor_career_spans():
    """
    Fetch the career spans of actors.

    Returns:
        list: A list of Actor instances with their career spans.
    """
    return (
        db.session.query(
            Actor.id,
            Actor.name,
            Actor.photo_url,
            Actor.slug,
            func.min(Movie.release_year).label("first_year"),
            func.max(Movie.release_year).label("last_year"),
        )
        .join(movie_actors, Actor.id == movie_actors.c.actor_id)
        .join(Movie, movie_actors.c.movie_id == Movie.id)
        .group_by(Actor.id)
        .having(func.count(Movie.id) > 1)
        .all()
    )


def fetch_most_frequent_actors(limit: int = 10):
    """
    Fetch the most frequently appearing actors in movies.

    Args:
        limit (int): Number of top actors to fetch. Defaults to 10.

    Returns:
        list: A list of dictionaries containing actor details and their movie counts.
    """
    return [
        {
            "name": actor.name,
            "movie_count": count,
            "id": actor.id,
            "slug": actor.slug,
            "photo_url": actor.photo_url,
        }
        for actor, count in db.session.query(
            Actor, func.count(movie_actors.c.movie_id).label("movie_count")
        )
        .join(movie_actors, Actor.id == movie_actors.c.actor_id)
        .group_by(Actor.id)
        .order_by(func.count(movie_actors.c.movie_id).desc())
        .limit(limit)
        .all()
    ]


def format_longest_career_actor(actor):
    """
    Format the longest career actor's details.

    Args:
        actor (Actor): The actor with the longest career span.

    Returns:
        dict: A dictionary containing the actor's details.
    """

    return (
        {
            "name": actor.name,
            "career_span": actor.last_year - actor.first_year,
            "from": actor.first_year,
            "to": actor.last_year,
            "id": actor.id,
            "slug": actor.slug,
            "photo_url": actor.photo_url,
        }
        if actor
        else None
    )


def fetch_most_prolific_directors(limit: int = 10):
    """
    Fetch the most prolific directors based on the number of movies directed.

    Args:
        limit (int): Number of top directors to fetch. Defaults to 10.

    Returns:
        list: A list of dictionaries containing director details and their movie counts.
    """
    return [
        {
            "name": director.name,
            "movie_count": count,
            "id": director.id,
            "slug": director.slug,
            "photo_url": director.photo_url,
        }
        for director, count in db.session.query(
            Director, func.count(movie_directors.c.movie_id).label("movie_count")
        )
        .join(movie_directors, Director.id == movie_directors.c.director_id)
        .group_by(Director.id)
        .order_by(func.count(movie_directors.c.movie_id).desc())
        .limit(limit)
        .all()
    ]


def fetch_highest_avg_rated_directors(limit: int = 10):
    """
    Fetch directors with the highest average movie ratings.

    Args:
        limit (int): Number of top directors to fetch. Defaults to 10.

    Returns:
        list: A list of dictionaries containing director details and their average ratings.
    """
    subq = (
        db.session.query(
            Director.id,
            Director.name,
            Director.slug,
            Director.photo_url,
            func.avg(Movie.rating).label("avg_rating"),
            func.count(Movie.id).label("movie_count"),
        )
        .join(movie_directors, Director.id == movie_directors.c.director_id)
        .join(Movie, movie_directors.c.movie_id == Movie.id)
        .filter(Movie.rating != None)
        .group_by(Director.id)
        .having(func.count(Movie.id) >= 3)
        .subquery()
    )

    return [
        {
            "name": name,
            "avg_rating": round(float(avg_rating), 2),
            "movie_count": movie_count,
            "id": id,
            "slug": slug,
            "photo_url": photo_url,
        }
        for name, avg_rating, movie_count, id, slug, photo_url in db.session.query(
            subq.c.name,
            subq.c.avg_rating,
            subq.c.movie_count,
            subq.c.id,
            subq.c.slug,
            subq.c.photo_url,
        )
        .order_by(subq.c.avg_rating.desc())
        .limit(limit)
        .all()
    ]


def fetch_most_common_genres(limit: int = 10):
    """
    Fetch the most common genres in the database.

    Args:
        limit (int): Number of top genres to fetch. Defaults to 10.

    Returns:
        list: A list of dictionaries containing genre details and their movie counts.
    """
    return [
        {"name": name, "count": count}
        for name, count in db.session.query(
            Genre.name, func.count(movie_genres.c.movie_id)
        )
        .join(movie_genres, Genre.id == movie_genres.c.genre_id)
        .group_by(Genre.id)
        .order_by(func.count(movie_genres.c.movie_id).desc())
        .limit(limit)
        .all()
    ]


def fetch_popularity_over_time():
    """
    Fetch the popularity of genres over time.

    Returns:
        dict: A dictionary with years as keys and genre counts as values.
    """
    genre_popularity = (
        db.session.query(Genre.name, Movie.release_year, func.count(Movie.id))
        .join(movie_genres, Genre.id == movie_genres.c.genre_id)
        .join(Movie, movie_genres.c.movie_id == Movie.id)
        .group_by(Genre.name, Movie.release_year)
        .order_by(Genre.name, Movie.release_year)
        .all()
    )

    popularity_by_genre = defaultdict(dict)
    for genre, year, count in genre_popularity:
        popularity_by_genre[genre][year] = count

    return popularity_by_genre


def fetch_movie_stats():
    """
    Fetch statistics about movies

    Returns:
        dict: A dictionary containing various movie statistics.
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


def fetch_actor_stats():
    """
    Fetch statistics about actors.

    Returns:
        dict: A dictionary containing various actor statistics.
    """

    try:
        career_spans = fetch_actor_career_spans()
        longest_span_actor = (
            max(
                career_spans,
                key=lambda x: (x.last_year or 0) - (x.first_year or 0),
            )
            if career_spans
            else None
        )

        return {
            "total": db.session.query(func.count(Actor.id)).scalar(),
            "most_frequent_actors": fetch_most_frequent_actors(),
            "longest_career_actor": format_longest_career_actor(longest_span_actor),
        }
    except Exception as e:
        print(f"Error fetching actor stats: {e}", file=sys.stderr)
        return None


def fetch_director_stats():
    """
    Fetch statistics about directors.

    Returns:
        dict: A dictionary containing various director statistics.
    """
    try:
        return {
            "total": db.session.query(func.count(Director.id)).scalar(),
            "most_prolific": fetch_most_prolific_directors(),
            "highest_avg_rated": fetch_highest_avg_rated_directors(),
        }
    except Exception as e:
        print(f"Error fetching director stats: {e}", file=sys.stderr)
        return None


def fetch_genre_stats():
    """
    Fetch statistics about genres.

    Returns:
        dict: A dictionary containing various genre statistics.
    """
    try:
        return {
            "total": (
                db.session.query(func.count(distinct(Genre.id)))
                .join(movie_genres, Genre.id == movie_genres.c.genre_id)
                .join(Movie, movie_genres.c.movie_id == Movie.id)
                .scalar()
            ),
            "most_common": fetch_most_common_genres(5),
            "popularity_over_time": fetch_popularity_over_time(),
            "average_rating": (
                {
                    name: round(float(avg), 2)
                    for name, avg in (
                        db.session.query(Genre.name, func.avg(Movie.rating))
                        .join(movie_genres, Genre.id == movie_genres.c.genre_id)
                        .join(Movie, movie_genres.c.movie_id == Movie.id)
                        .filter(Movie.rating != None)
                        .group_by(Genre.name)
                        .order_by(Genre.name)
                        .all()
                    )
                }
            ),
        }
    except Exception as e:
        print(f"Error fetching genre stats: {e}", file=sys.stderr)
        return None


@stats.route("/stats", methods=["GET"])
def get_stats():
    """Get statistics about movies, actors, genres, and directors in the database.

    Returns:
        dict: A dictionary containing the status and statistics data.
    """
    stats = dict()

    movie_stats = fetch_movie_stats()
    actor_stats = fetch_actor_stats()
    director_stats = fetch_director_stats()
    genre_stats = fetch_genre_stats()

    if movie_stats:
        stats["movie_stats"] = movie_stats
    if actor_stats:
        stats["actor_stats"] = actor_stats
    if director_stats:
        stats["director_stats"] = director_stats
    if genre_stats:
        stats["genre_stats"] = genre_stats

    # if not stats were fetched return an error message
    if not stats:
        return {
            **Status.ERROR.value,
            "message": "Failed to fetch statistics",
        }

    return {
        **Status.SUCCESS.value,
        "data": stats,
    }
