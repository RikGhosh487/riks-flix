from app_init import db


class Genre(db.Model):
    __tablename__ = "genres"
    __table_args__ = (db.UniqueConstraint("slug", name="uq_genres_slug"),)

    # primary key
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(255), nullable=False)

    # secondary identifier
    slug = db.Column(db.String(255), unique=True)

    # timestamps
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(
        db.DateTime, server_default=db.func.now(), onupdate=db.func.now()
    )

    def __init__(self, name: str, slug: str) -> None:
        # populate fields
        self.name = name
        self.slug = slug

    def __repr__(self):
        return f"<Genre {self.name}>"
