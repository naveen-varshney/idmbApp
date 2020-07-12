import os 
from flask import Flask
from flask_mongoengine import MongoEngine
from .api.v1.movies.handler import movie_views
app = Flask(__name__)

MONGO_DB_HOST = os.getenv("MONGODB_URI") or "localhost"
MONGO_DB_NAME = os.getenv("DB_NAME") or "imdbmovie"
app.config['MONGODB_SETTINGS'] = {
    "db": MONGO_DB_NAME,
    "host": MONGO_DB_HOST,
}
app.register_blueprint(movie_views)

db = MongoEngine(app)

pymongo_db = None


def get_pymongo_client():
    global pymongo_db
    if pymongo_db is None:
        pymongo_client = MongoClient(MONGO_DB_HOST)
        pymongo_db = pymongo_client[MONGO_DB_NAME]
    return pymongo_db