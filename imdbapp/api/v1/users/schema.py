from marshmallow import Schema, fields, validate
from imdbapp.api.schema import NonEmptyStringField


class UserSchema(Schema):
    name = NonEmptyStringField(required=True)
    email = fields.Str(
        required=True, validate=validate.Email(error="Not a valid email address")
    )
    password = fields.Str(
        required=True, validate=[validate.Length(min=6, max=36)], load_only=True
    )
    is_admin = fields.Boolean(default=False)
