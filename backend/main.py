import os
from app_init import app
from endpoints.movies import movies
from endpoints.actors import actors
from endpoints.directors import directors

# Register all blueprints
app.register_blueprint(movies, url_prefix="/api/v1")
app.register_blueprint(actors, url_prefix="/api/v1")
app.register_blueprint(directors, url_prefix="/api/v1")


@app.route("/")
def hello_world():
    name = os.getenv("NAME", "Riks Flix")
    return "Welcome to {name} Backend!\n".format(name=name)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.getenv("PORT", 8080)))
