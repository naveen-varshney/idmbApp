import datetime
import jwt
from werkzeug.security import generate_password_hash, check_password_hash
from mongoengine import fields, Document
from flask_login import UserMixin
from flask import current_app as app


class BaseDocument(Document):
    """
    Abstract model which contains all the common fields.
    """

    active = fields.BooleanField(default=True)
    modified = fields.DateTimeField()

    meta = {"abstract": True}


class UserToken(BaseDocument):
    user = fields.ObjectIdField()
    token = fields.StringField(max_length=512, required=True)
    expires_in = fields.IntField(default=-1)

    meta = {"auto_create_index": False, "indexes": [{"fields": ["$token"]}]}

    def __str__(self):
        return f"{self.token} {self.expires_in}"

    @property
    def user_object(self):
        return User.objects.filter(id=self.user).first()


class User(UserMixin, BaseDocument):
    name = fields.StringField()
    email = fields.EmailField(required=True)
    password = fields.StringField()
    is_admin = fields.BooleanField(default=False)

    meta = {"auto_create_index": False, "indexes": [{"fields": ["$email"]}]}

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    @classmethod
    def create_user(cls, name, email, password):
        try:
            email_name, domain_part = email.strip().split("@", 1)
        except ValueError:
            pass
        else:
            email = "@".join([email_name.lower(), domain_part.lower()])

        user = User(name=name, email=email)
        user.set_password(password)
        return user

    def encode_auth_token(self, user_id):
        """
        Generates the Auth Token
        :return: string
        """
        try:
            payload = {
                "exp": datetime.datetime.utcnow()
                + datetime.timedelta(days=0, seconds=5),
                "iat": datetime.datetime.utcnow(),
                "sub": str(user_id),
            }
            return jwt.encode(payload, app.config.get("SECRET_KEY"), algorithm="HS256")
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        """
        Decodes the auth token
        :param auth_token:
        :return: integer|string
        """
        token = UserToken.objects.filter(token=auth_token).first()
        if not token:
            return "Invalid token."
        try:
            payload = jwt.decode(auth_token, app.config.get("SECRET_KEY"))
            return payload["sub"]
        except jwt.ExpiredSignatureError:
            return "Signature expired. Please log in again."
        except jwt.InvalidTokenError:
            return "Invalid token. Please log in again."

    def __str__(self):
        return f"{self.name} : {self.email}"

    def __repr__(self):
        return f"<{self.name} : {self.email}>"


class Movie(Document):
    name = fields.StringField(required=True)
    director = fields.StringField(required=True)
    categories = fields.ListField(fields.StringField())
    imdb_score = fields.FloatField()
    popularity_99 = fields.FloatField()
    added_by = fields.ObjectId()

    # applying search index on name and director field
    meta = {
        "auto_create_index": False,
        "indexes": [
            {
                "fields": ["$name", "$director"],
                "default_language": "english",
                "weights": {"name": 10, "director": 5},
            }
        ],
    }

    def __str__(self):
        return f"Name - {self.name} : Director - {self.director}"

    def __repr__(self):
        return f"<{self.name} : {self.director}>"
