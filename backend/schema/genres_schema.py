from app_init import ma
from models.genres import Genre


# Genre Schema
class GenreSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Genre
        load_instance = True
        include_relationship = True
        fields = (
            "id",
            "name",
            "slug",
        )
        ordered = True


# Genres Schema
class GenresSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Genre
        load_instance = True
        fields = (
            "id",
            "name",
            "slug",
        )
        ordered = True


genre_schema = GenreSchema()
genres_schema = GenresSchema(many=True)
