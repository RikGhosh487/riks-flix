import os
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

base_dir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DB_URI")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
CORS(app)  # Enable CORS for all routes


# initialize the database
def init_database(app: Flask) -> SQLAlchemy:
    return SQLAlchemy(app)


# initialize marshmallow
def init_marshmallow(app: Flask) -> Marshmallow:
    return Marshmallow(app)


# exported objects from __file__
db = init_database(app)
ma = init_marshmallow(app)
