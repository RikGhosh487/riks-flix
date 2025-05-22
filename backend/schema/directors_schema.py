from app_init import ma
from models.directors import Director


# Director Schema
class DirectorSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Director
        load_instance = True
        include_relationships = True
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
class DirectorsSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Director
        load_instance = True
        fields = (
            "id",
            "name",
            "photo_url",
            "slug",
        )
        ordered = True


director_schema = DirectorSchema()
directors_schema = DirectorsSchema(many=True)
