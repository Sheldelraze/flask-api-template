from marshmallow import EXCLUDE, fields, validate

from controller.validator import base_validator

not_blank = validate.Length(min=1, error="Field cannot be blank")


class GetSampleSchema(base_validator.BaseSchema):
    class Meta:
        unknown = EXCLUDE  # ignore undefined field

    params_one = fields.Str(required=True, validate=not_blank)
    params_two = fields.Int(required=True)


class PostSampleSchema(base_validator.BaseSchema):
    class Meta:
        unknown = EXCLUDE  # ignore undefined field

    params_three = fields.Int(required=True)
    params_four = fields.Str(required=True)
