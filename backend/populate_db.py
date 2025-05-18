import json
from models import Movie
from app_init import db, app
from sqlalchemy import MetaData

def drop_all_tables():
    """
    Reflects and drops all tables in the database.
    """
    with app.app_context():
        metadata = MetaData()
        metadata.reflect(bind=db.engine)    # Load all table info from the database
        metadata.drop_all(bind=db.engine)   # Drop all tables

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

def add_movies():
    with app.app_context():
        file = open("data/movies.tmp.json", "r", encoding="utf-8")
        data = json.load(file)

        # get all existing slugs in the DB to avoid duplicates
        existing_slugs = {slug for (slug,) in db.session.query(Movie.slug).all()}

        new_count = 0
        for movie in data:
            if movie.get("slug") in existing_slugs:
                print(f"Movie with slug {movie['slug']} already exists. Skipping...")
                continue
            # create a new Movie object
            new_movie = Movie(**movie)
            db.session.add(new_movie)
            new_count += 1
        db.session.commit()
        file.close()

        print(f"{new_count} movies added to the database.")

if __name__ == "__main__":
    create_tables()
    add_movies()