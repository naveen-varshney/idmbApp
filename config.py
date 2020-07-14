# Define the application directory
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

MONGO_DB_HOST = os.getenv("MONGODB_URI") or "localhost"
MONGO_DB_NAME = os.getenv("DB_NAME") or "imdbmovie"


class BaseConfig:
    """Base configuration."""

    SECRET_KEY = os.getenv("SECRET_KEY", "my_precious")
    DEBUG = False
    MONGODB_SETTINGS = {
        "db": MONGO_DB_NAME,
        "host": MONGO_DB_HOST,
    }


class DevelopmentConfig(BaseConfig):
    """Development configuration."""

    DEBUG = True


class TestingConfig(BaseConfig):
    """Testing configuration."""

    DEBUG = True
    TESTING = True


class ProductionConfig(BaseConfig):
    """Production configuration."""

    DEBUG = False
