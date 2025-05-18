from app_init import ma
from models.actors import Actor


# Actor Schema
class ActorSchema(ma.Schema):
    class Meta:
        model = Actor
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
class ActorsSchema(ma.Schema):
    class Meta:
        model = Actor
        fields = (
            "id",
            "name",
            "photo_url",
            "slug",
        )
        ordered = True


actor_schema = ActorSchema()
actors_schema = ActorsSchema(many=True)
