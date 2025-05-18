from app_init import ma
from models.directors import Director


# Director Schema
class DirectorSchema(ma.Schema):
    class Meta:
        model = Director
        fields = (
            "id",
            "name",
            "biography",
            "photo_url",
            "imdb_id",
            "slug",
        )
        ordered = True


# Directors Schema
class DirectorsSchema(ma.Schema):
    class Meta:
        model = Director
        fields = (
            "id",
            "name",
            "photo_url",
            "slug",
        )
        ordered = True


director_schema = DirectorSchema()
directors_schema = DirectorsSchema(many=True)
