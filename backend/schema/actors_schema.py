from app_init import ma
from models.actors import Actor


# Actor Schema
class ActorSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Actor
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


# Actors Schema
class ActorsSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Actor
        load_instance = True
        fields = (
            "id",
            "name",
            "photo_url",
            "slug",
        )
        ordered = True


actor_schema = ActorSchema()
actors_schema = ActorsSchema(many=True)
