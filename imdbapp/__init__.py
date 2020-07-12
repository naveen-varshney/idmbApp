import os
from pymongo import MongoClient
from flask import Flask
from flask_mongoengine import MongoEngine
from flask_login import LoginManager


MONGO_DB_HOST = os.getenv("MONGODB_URI") or "localhost"
MONGO_DB_NAME = os.getenv("DB_NAME") or "imdbmovie"
db = MongoEngine()

# login manager settings
login_manager = LoginManager()
login_manager.session_protection = "strong"
login_manager.needs_refresh_message = (
    "To protect your account, please re-authenticate to access this page."
)
login_manager.needs_refresh_message_category = "info"


def create_app():
    """Initialize the core application."""
    app = Flask(__name__, instance_relative_config=False)
    app.config["MONGODB_SETTINGS"] = {
        "db": MONGO_DB_NAME,
        "host": MONGO_DB_HOST,
    }

    with app.app_context():
        # Initialize Plugins
        db.init_app(app)
        login_manager.init_app(app)

        # Register Blueprints
        from .api.v1.movies.handler import movie_views
        from .api.v1.users.handler import user_views

        app.register_blueprint(movie_views)
        app.register_blueprint(user_views)
        return app


pymongo_db = None


def get_pymongo_client():
    global pymongo_db
    if pymongo_db is None:
        pymongo_client = MongoClient(MONGO_DB_HOST)
        pymongo_db = pymongo_client[MONGO_DB_NAME]
    return pymongo_db
