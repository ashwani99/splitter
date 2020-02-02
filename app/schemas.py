from marshmallow import Schema, fields
from app.exceptions import ParseError, ValidationFailed

SCHEMA = '_schema'

class BaseSchema(Schema):
    class Meta:
        unknown = 'EXCLUDE'

    error_messages = {
        'type': 'Problems parsing JSON'
    }

    def handle_error(self, error, data, **kwargs):
        if SCHEMA in error.messages:
            raise ParseError(message=error.messages[SCHEMA])
        else:
            errors = []
            for key in error.messages:
                errors.append({ 'key': key, 'messages': error.messages.get(key) })
            raise ValidationFailed(errors=errors)


class UserSchema(BaseSchema):
    id = fields.Number(dump_only=True)
    email = fields.Email(required=True)
    username = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)
    registered_at = fields.DateTime(dump_only=True)


class UserLoginSchema(BaseSchema):
    email = fields.Str(required=True)
    password = fields.Str(required=True)
