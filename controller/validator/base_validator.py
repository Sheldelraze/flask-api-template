import time

from marshmallow import (EXCLUDE, Schema, ValidationError, fields, utils,
                         validate)

from exception import error

not_blank = validate.Length(min=1, error="Field cannot be blank")


class BaseSchema(Schema):
    event_timestamp = fields.Float(required=True, default=time.time)
    user_id = fields.Str(required=True, validate=not_blank)

    def load(self, *args, **kwargs):
        try:
            return super().load(*args, **kwargs)
        except ValidationError as err:
            raise error.InvalidRequest(data=err.messages)
