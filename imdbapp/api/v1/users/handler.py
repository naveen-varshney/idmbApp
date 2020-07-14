import json
from flask import request, jsonify, Blueprint, make_response
from flask.views import MethodView
from mongoengine.errors import ValidationError, DoesNotExist
from imdbapp.api.models import User
from imdbapp.api.v1.users.schema import UserSchema

user_views = Blueprint("users", __name__, url_prefix="/api/v1/users")


@user_views.route("/")
def users():
    users = User.objects
    return jsonify(UserSchema(many=True).dump(users))


class RegisterAPI(MethodView):
    """
    User Registration Resource
    """

    def post(self):
        # get the post data
        data = request.json
        try:
            validated_data = UserSchema().load(data)
        except ValidationError as err:
            return make_response(jsonify({"message": err.errors})), 422
        # check if user already exists
        user = User.objects.filter(email=validated_data.get("email")).first()
        if not user:
            try:
                user = User.create_user(
                    name=validated_data["name"],
                    email=validated_data["email"],
                    password=validated_data["password"],
                )
                user.is_admin = validated_data["is_admin"]
                user.save()

                # generate the auth token
                auth_token = user.encode_auth_token(user.id)
                response_data = {
                    "status": "success",
                    "message": "Successfully registered.",
                    "auth_token": auth_token.decode(),
                }
                return make_response(jsonify(response_data)), 201
            except Exception as e:
                response_data = {
                    "status": "fail",
                    "message": "Some error occurred. Please try again.",
                }
                return make_response(jsonify(response_data)), 401
        else:
            response_data = {
                "status": "fail",
                "message": "User already exists. Please Log in.",
            }
            return make_response(jsonify(response_data)), 202


class LoginAPI(MethodView):
    """
    User Login Resource
    """

    def post(self):
        # get the post data
        post_data = request.json
        try:
            # fetch the user data
            user = User.objects.filter(email=post_data.get("email")).first()
            if user and user.check_password(user.password, post_data.get("password")):
                auth_token = user.encode_auth_token(user.id)
                if auth_token:
                    response_data = {
                        "status": "success",
                        "message": "Successfully logged in.",
                        "auth_token": auth_token.decode(),
                    }
                    return make_response(jsonify(response_data)), 200
            else:
                response_data = {"status": "fail", "message": "User does not exist."}
                return make_response(jsonify(response_data)), 404
        except Exception as e:
            response_data = {"status": "fail", "message": "Try again"}
            return make_response(jsonify(response_data)), 500


class UserAPI(MethodView):
    """
    User Resource
    """

    def get(self):
        # get the auth token
        auth_header = request.headers.get("Authorization")
        if auth_header:
            try:
                auth_token = auth_header.split(" ")[1]
            except IndexError:
                response_data = {"status": "fail", "message": "Bearer token malformed."}
                return make_response(jsonify(response_data)), 401
        else:
            auth_token = ""
        if auth_token:
            resp = User.decode_auth_token(auth_token)
            if not isinstance(resp, str):
                user = User.query.filter_by(id=resp).first()
                response_data = {
                    "status": "success",
                    "data": {
                        "user_id": user.id,
                        "email": user.email,
                        "admin": user.is_admin,
                        "registered_on": user.id.generation_time.astimezone().strftime(
                            "%d-%m-%yT%H:%M"
                        ),
                    },
                }
                return make_response(jsonify(response_data)), 200
            response_data = {"status": "fail", "message": resp}
            return make_response(jsonify(response_data)), 401
        else:
            response_data = {"status": "fail", "message": "Provide a valid auth token."}
            return make_response(jsonify(response_data)), 401


class LogoutAPI(MethodView):
    """
    Logout Resource
    """

    def post(self):
        # get auth token
        auth_header = request.headers.get("Authorization")
        if auth_header:
            auth_token = auth_header.split(" ")[1]
        else:
            auth_token = ""
        if auth_token:
            resp = User.decode_auth_token(auth_token)
            if not isinstance(resp, str):
                # mark the token as blacklisted
                blacklist_token = BlacklistToken(token=auth_token)
                try:
                    # insert the token
                    db.session.add(blacklist_token)
                    db.session.commit()
                    response_data = {
                        "status": "success",
                        "message": "Successfully logged out.",
                    }
                    return make_response(jsonify(response_data)), 200
                except Exception as e:
                    response_data = {"status": "fail", "message": e}
                    return make_response(jsonify(response_data)), 200
            else:
                response_data = {"status": "fail", "message": resp}
                return make_response(jsonify(response_data)), 401
        else:
            response_data = {"status": "fail", "message": "Provide a valid auth token."}
            return make_response(jsonify(response_data)), 403


# define the API resources
registration_view = RegisterAPI.as_view("register_api")
login_view = LoginAPI.as_view("login_api")
user_view = UserAPI.as_view("user_api")
logout_view = LogoutAPI.as_view("logout_api")

# add Rules for API Endpoints
user_views.add_url_rule("/register", view_func=registration_view, methods=["POST"])
user_views.add_url_rule("/login", view_func=login_view, methods=["POST"])
user_views.add_url_rule("/status", view_func=user_view, methods=["GET"])
user_views.add_url_rule("/auth/logout", view_func=logout_view, methods=["POST"])
