from app_init import db


# Directors model
class Director(db.Model):
    __tablename__ = "directors"
    __table_args__ = (db.UniqueConstraint("slug", name="uq_directors_slug"),)

    # primary key
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(255), nullable=False)
    biography = db.Column(db.Text)

    # urls
    photo_url = db.Column(db.Text)
    imdb_id = db.Column(db.Text)

    # secondary identifier
    slug = db.Column(db.String(255), unique=True)

    # timestamps
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(
        db.DateTime, server_default=db.func.now(), onupdate=db.func.now()
    )

    def __init__(
        self,
        name: str,
        biography: str,
        photo_url: str,
        imdb_id: str,
        slug: str,
    ) -> None:

        # populate fields
        self.name = name
        self.biography = biography
        self.photo_url = photo_url
        self.imdb_id = imdb_id
        self.slug = slug

    def __repr__(self):
        return f"<Director {self.name}>"
