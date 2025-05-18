import json
import argparse
from app_init import db, app
from sqlalchemy import MetaData
from models import Movie, Actor, Director, Genre


def drop_all_tables():
    """
    Reflects and drops all tables in the database.
    """
    with app.app_context():
        metadata = MetaData()
        metadata.reflect(bind=db.engine)  # Load all table info from the database
        metadata.drop_all(bind=db.engine)  # Drop all tables


def create_tables(drop_all: bool = False):
    """
    Creates all tables in the database.
    Args:
        drop_all (bool): If True, drops all tables before creating them.
    """
    with app.app_context():
        if drop_all:
            drop_all_tables()
        db.create_all()


def add_movies(verbose: bool = False):
    """
    Adds movies to the database from a JSON file.
    Args:
        verbose (bool): If True, enables verbose output for skipped entries.
    """
    with app.app_context():
        file = open("data/movies.tmp.json", "r", encoding="utf-8")
        data = json.load(file)

        # get all existing slugs in the DB to avoid duplicates
        existing_slugs = {slug for (slug,) in db.session.query(Movie.slug).all()}

        new_count = 0
        for movie in data:
            if movie.get("slug") in existing_slugs:
                if verbose:
                    print(
                        f"Movie with slug {movie['slug']} already exists. Skipping..."
                    )
                continue
            # create a new Movie object
            new_movie = Movie(**movie)
            db.session.add(new_movie)
            new_count += 1
        db.session.commit()
        file.close()

        print(f"{new_count} movies added to the database.")


def add_actors(verbose: bool = False):
    """
    Adds actors to the database from a JSON file.
    Args:
        verbose (bool): If True, enables verbose output for skipped entries.
    """
    with app.app_context():
        file = open("data/actors.tmp.json", "r", encoding="utf-8")
        data = json.load(file)

        # get all existing slugs in the DB to avoid duplicates
        existing_slugs = {slug for (slug,) in db.session.query(Actor.slug).all()}

        new_count = 0
        for actor in data:
            if actor.get("slug") in existing_slugs:
                if verbose:
                    print(
                        f"Actor with slug {actor['slug']} already exists. Skipping..."
                    )
                continue
            # create a new Actor object
            new_actor = Actor(**actor)
            db.session.add(new_actor)
            new_count += 1
        db.session.commit()
        file.close()

        print(f"{new_count} actors added to the database.")


def add_directors(verbose: bool = False):
    """
    Adds directors to the database from a JSON file.
    Args:
        verbose (bool): If True, enables verbose output for skipped entries.
    """
    with app.app_context():
        file = open("data/directors.tmp.json", "r", encoding="utf-8")
        data = json.load(file)

        # get all existing slugs in the DB to avoid duplicates
        existing_slugs = {slug for (slug,) in db.session.query(Director.slug).all()}

        new_count = 0
        for director in data:
            if director.get("slug") in existing_slugs:
                if verbose:
                    print(
                        f"Director with slug {director['slug']} already exists. Skipping..."
                    )
                continue
            # create a new Director object
            new_director = Director(**director)
            db.session.add(new_director)
            new_count += 1
        db.session.commit()
        file.close()

        print(f"{new_count} directors added to the database.")


def add_genres(verbose: bool = False):
    """
    Adds genres to the database from a JSON file.
    Args:
        verbose (bool): If True, enables verbose output for skipped entries.
    """
    with app.app_context():
        file = open("data/genres.tmp.json", "r", encoding="utf-8")
        data = json.load(file)

        # get all existing slugs in the DB to avoid duplicates
        existing_slugs = {slug for (slug,) in db.session.query(Genre.slug).all()}

        new_count = 0
        for genre in data:
            if genre.get("slug") in existing_slugs:
                if verbose:
                    print(
                        f"Genre with slug {genre['slug']} already exists. Skipping..."
                    )
                continue
            # create a new Genre object
            new_genre = Genre(**genre)
            db.session.add(new_genre)
            new_count += 1
        db.session.commit()
        file.close()

        print(f"{new_count} genres added to the database.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Populate the database with movie-related data."
    )
    parser.add_argument(
        "--drop-all",
        action="store_true",
        help="Drop all tables before creating them.",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose output for skipped entries.",
    )
    parser.add_argument(
        "--include-genres",
        action="store_true",
        help="Include genres when populating the database.",
    )

    args = parser.parse_args()

    create_tables(drop_all=args.drop_all)

    add_movies(verbose=args.verbose)
    add_actors(verbose=args.verbose)
    add_directors(verbose=args.verbose)

    # Add genres if the flag is set or if we dropped all tables
    if args.include_genres or args.drop_all:
        add_genres(verbose=args.verbose)
