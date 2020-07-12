import json
from flask import Blueprint,jsonify,request
from mongoengine.errors import ValidationError,DoesNotExist
from imdbapp.api.models import Movie
from .schema import MovieSchema

movie_views = Blueprint("movies", __name__, url_prefix="/api/v1/movies")

@movie_views.route("/",methods=["GET"])
def movie_list():
    search = request.args.get('name')
    movies = Movie.objects
    if search:
        movies = movies.search_text(search).order_by("$text_score")
    return jsonify(json.loads(movies.to_json()))



@movie_views.route("/create", methods=["POST"])
def create_movie():
    data = request.json
    try:
        validated_data = MovieSchema.load(data)
    except ValidationError as err:
        return {"errors": err.messages}, 422

    movies = Movie.objects.create
    if search:
        movies = movies.search_text(search).order_by("$text_score")
    return jsonify(json.loads(movies.to_json()))



@movie_views.route("/<mov_id>/update", methods=["POST"])
def update_movie(mov_id):
    data = request.json
    try:
        validated_data = MovieSchema.load(data)
    except ValidationError as err:
        return {"errors": err.messages}, 422

    Movie.objects.create(**validated_data)
    return jsonify({"success":"Movie created successfully"})



@movie_views.route("/<mov_id>/delete", methods=["DELETE"])
def delete_movie(mov_id):
    try:
        Movie.objects.get(id=mov_id).delete()
    except DoesNotExist as err:
        return {"message": "movie does not exists"},404
    except DoesNotExist as err:
        return {"message": "movie does not exists"},404
    
    return jsonify({"success":True})
