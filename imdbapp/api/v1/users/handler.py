import json
from flask import request, jsonify, Blueprint
from imdbapp.api.models import User
from imdbapp.api.v1.users.schema import UserSchema

user_views = Blueprint("users", __name__, url_prefix="/api/v1/users")


@user_views.route("/")
def users():
    users = User.objects
    return jsonify(UserSchema(many=True).dump(users))


@user_views.route("/register", methods=["POST"])
def register_user():
    data = request.json
    validated_data = UserSchema().load(data)
    user = User.create_user(
        name=validated_data["name"],
        email=validated_data["email"],
        password=validated_data["password"],
    )
    user.is_admin = validated_data["is_admin"]
    user.save()
    return jsonify(UserSchema(many=True).dump(users))
