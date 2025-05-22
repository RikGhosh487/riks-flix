from app_init import ma
from models.movies import Movie


# Movie Schema
class MovieSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Movie
        load_instance = True
        include_relationship = True
        fields = (
            "id",
            "title",
            "release_year",
            "duration",
            "tagline",
            "description",
            "rating",
            "mpaa_rating",
            "poster_url",
            "page_img_url",
            "trailer_url",
            "slug",
        )
        ordered = True


# Movies Schema
class MoviesSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Movie
        load_instance = True
        fields = (
            "id",
            "title",
            "release_year",
            "duration",
            "rating",
            "mpaa_rating",
            "poster_url",
            "slug",
        )
        ordered = True


movie_schema = MovieSchema()
movies_schema = MoviesSchema(many=True)
