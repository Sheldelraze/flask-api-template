# -*- coding: utf-8 -*-

import json

import flasgger
import flask
from marshmallow import EXCLUDE

from controller.validator import sample_validator
from service import sample_service

sample_app = flask.Blueprint("sample_app", __name__)

# service
s_service = sample_service.SampleService()

# validator
get_sample_validator = sample_validator.GetSampleSchema(unknown=EXCLUDE)
post_sample_validator = sample_validator.PostSampleSchema(unknown=EXCLUDE)


def make_response(data, time_elapsed):
    response = flask.jsonify(
        {
            "time_elapsed": time_elapsed,
            "data": data,
            "message": {"internalMessage": "", "error_code": 0, "success": True},
        }
    )
    return response, 200


@sample_app.route("/sample", methods=["GET"])
@flasgger.swag_from("docs/get_sample_question.yml", endpoint="sample_app.get_practice_sample")
def get_practice_sample():
    args = get_sample_validator.load(flask.request.args)
    data, time_elapsed = s_service.get_sample(**args)
    return make_response(data, time_elapsed)


@sample_app.route("/sample", methods=["POST"])
@flasgger.swag_from("docs/post_practice_sample.yml", endpoint="sample_app.post_practice_sample")
def post_practice_sample():
    dataDict = json.loads(flask.request.data.decode("utf-8"))
    args = post_sample_validator.load(dataDict)
    data, time_elapsed = s_service.post_sample(**args)
    return make_response(data, time_elapsed)


# TODO: Delete this later
@sample_app.route("/error", methods=["GET"])
def get_unknown_error():
    data, time_elapsed = s_service.get_custom_error()
    return make_response(data, time_elapsed)
