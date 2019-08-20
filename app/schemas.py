from marshmallow import Schema, fields, validates, ValidationError

from app.models import User


class UserSchema(Schema):
    id = fields.Number(dump_only=True)
    email = fields.Email(required=True)
    username = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)
    registered_at = fields.DateTime(dump_only=True)


class UserLoginSchema(Schema):
    email = fields.Str(required=True)
    password = fields.Str(required=True)
