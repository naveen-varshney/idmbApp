from flask import Blueprint, jsonify, request
from flask import current_app as app
from mongoengine.errors import ValidationError, DoesNotExist
from flask_login import login_required
from imdbapp.api.utils import only_admin
from imdbapp.api.models import Movie
from imdbapp.api.v1.movies.schema import MovieSchema
from .schema import MovieSchema

movie_views = Blueprint("movies", __name__, url_prefix="/api/v1/movies")


@app.route("/", methods=["GET"])
@movie_views.route("/", methods=["GET"])
def movie_list():
    """
    get movie list
    """

    search = request.args.get("name")
    movies = Movie.objects
    if search:
        movies = movies.search_text(search).order_by("$text_score")
    return jsonify(MovieSchema(many=True).dump(movies))


@movie_views.route("/create", methods=["POST"])
@only_admin
def create_movie():
    data = request.json
    try:
        validated_data = MovieSchema().load(data)
    except ValidationError as err:
        return {"errors": err.messages}, 422

    Movie.objects.create(**validated_data)
    return jsonify(validated_data), 201


@movie_views.route("/<mov_id>/update", methods=["POST"])
def update_movie(mov_id):
    data = request.json
    try:
        validated_data = MovieSchema().load(data)
    except ValidationError as err:
        return {"errors": err.messages}, 422

    user = Movie.objects.get(id=mov_id)
    user.update
    return jsonify({"success": "Movie updated successfully"})


@movie_views.route("/<mov_id>/delete", methods=["DELETE"])
def delete_movie(mov_id):
    try:
        Movie.objects.get(id=mov_id).delete()
    except DoesNotExist as err:
        return {"message": "movie does not exists"}, 404
    except DoesNotExist as err:
        return {"message": "movie does not exists"}, 404

    return jsonify({"success": True})
