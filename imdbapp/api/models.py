from werkzeug.security import generate_password_hash, check_password_hash
from mongoengine import fields, Document
from flask_login import UserMixin


class BaseDocument(Document):
    """
    Abstract model which contains all the common fields.
    """

    active = fields.BooleanField(default=True)
    modified = fields.DateTimeField()

    meta = {"abstract": True}


class User(UserMixin, BaseDocument):
    name = fields.StringField()
    email = fields.EmailField(required=True)
    password = fields.StringField()
    is_admin = fields.BooleanField(default=False)

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

    # applying search index on name and director field
    meta = {
        "indexes": [
            {
                "fields": ["$name", "$director"],
                "default_language": "english",
                "weights": {"name": 10, "director": 5},
            }
        ]
    }

    def __str__(self):
        return f"Name - {self.name} : Director - {self.director}"

    def __repr__(self):
        return f"<{self.name} : {self.director}>"
