from app_init import db

movie_genres = db.Table(
    "movie_genres",
    db.Column("movie_id", db.Integer, db.ForeignKey("movies.id"), primary_key=True),
    db.Column("genre_id", db.Integer, db.ForeignKey("genres.id"), primary_key=True),
    db.Column("created_at", db.DateTime, server_default=db.func.now()),
    db.Column(
        "updated_at", db.DateTime, server_default=db.func.now(), onupdate=db.func.now()
    ),
)

movie_actors = db.Table(
    "movie_actors",
    db.Column("movie_id", db.Integer, db.ForeignKey("movies.id"), primary_key=True),
    db.Column("actor_id", db.Integer, db.ForeignKey("actors.id"), primary_key=True),
    db.Column("created_at", db.DateTime, server_default=db.func.now()),
    db.Column(
        "updated_at", db.DateTime, server_default=db.func.now(), onupdate=db.func.now()
    ),
)

movie_directors = db.Table(
    "movie_directors",
    db.Column("movie_id", db.Integer, db.ForeignKey("movies.id"), primary_key=True),
    db.Column(
        "director_id", db.Integer, db.ForeignKey("directors.id"), primary_key=True
    ),
    db.Column("created_at", db.DateTime, server_default=db.func.now()),
    db.Column(
        "updated_at", db.DateTime, server_default=db.func.now(), onupdate=db.func.now()
    ),
)
