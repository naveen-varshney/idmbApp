from flask import Flask
from flask_mongoengine import MongoEngine
from .api.v1.movies.handler import movie_views
app = Flask(__name__)

app.config['MONGODB_SETTINGS'] = {
    "db": "imdbmovie",
    "host": "localhost",
}
app.register_blueprint(movie_views)

db = MongoEngine(app)

pymongo_db = None


def get_pymongo_client():
    global pymongo_db
    if pymongo_db is None:
        pymongo_client = MongoClient(MONGODB_SETTINGS["localhost"])
        pymongo_db = pymongo_client[MONGODB_SETTINGS["db"]]
    return pymongo_db