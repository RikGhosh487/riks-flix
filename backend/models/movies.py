from app_init import db
from models.associations import movie_genres, movie_actors, movie_directors


# Movies model
class Movie(db.Model):
    __tablename__ = "movies"
    __table_args__ = (db.UniqueConstraint("slug", name="uq_movies_slug"),)

    # primary key
    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(255), nullable=False)
    release_year = db.Column(db.Integer)
    duration = db.Column(db.Integer)
    tagline = db.Column(db.String(255))
    description = db.Column(db.Text)
    rating = db.Column(db.Float)
    mpaa_rating = db.Column(db.String(10))

    # urls
    poster_url = db.Column(db.Text)
    page_img_url = db.Column(db.Text)
    trailer_url = db.Column(db.Text)

    # secondary identifier
    slug = db.Column(db.String(255), unique=True)

    # timestamps
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(
        db.DateTime, server_default=db.func.now(), onupdate=db.func.now()
    )

    # relationships
    genres = db.relationship("Genre", secondary=movie_genres, backref="movies")
    actors = db.relationship("Actor", secondary=movie_actors, backref="movies")
    directors = db.relationship("Director", secondary=movie_directors, backref="movies")

    def __init__(
        self,
        title: str,
        release_year: int,
        duration: int,
        tagline: str,
        description: str,
        rating: float,
        mpaa_rating: str,
        poster_url: str,
        page_img_url: str,
        trailer_url: str,
        slug: str,
    ) -> None:

        # populate fields
        self.title = title
        self.release_year = release_year
        self.duration = duration
        self.tagline = tagline
        self.description = description
        self.rating = rating
        self.mpaa_rating = mpaa_rating
        self.poster_url = poster_url
        self.page_img_url = page_img_url
        self.trailer_url = trailer_url
        self.slug = slug

    def __repr__(self) -> str:
        return f"<Movie {self.title}>"
