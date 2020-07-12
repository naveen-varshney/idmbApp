from marshmallow import Schema, ValidationError, fields, validate, validates_schema


class NonEmptyStringField(fields.String):
    """
    Custom Field that validate for empty values and deserializes to remove extra(leading/trailing) whitespace
    """
    def _validate(self, value):
        if not value.strip() and self.required:
            raise ValidationError("Field cannot be empty.")
        return super(NonEmptyStringField, self)._validate(value)