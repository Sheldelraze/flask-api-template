import json
from urllib.parse import urlsplit

import flask
import requests

import config
from exception import error
from helper import common_util

general_app = flask.Blueprint("general_app", __name__)
error_logger = common_util.get_logger("error", False)


@general_app.app_errorhandler(404)
def not_found(error):
    response = flask.jsonify({"message": error.description, "status_code": 404})
    return response, 400


@general_app.app_errorhandler(500)
def server_error(error):
    stacktrace = common_util.format_exception(error)

    # log error
    data = {
        "service": config.SERVICE_NAME,
        "stacktrace": stacktrace,
        "url": flask.request.url,
        "environment": config.ENVIRONMENT,
    }
    if flask.request.method == "POST":
        data["body"] = flask.request.data.decode("utf-8")
    elif flask.request.method == "GET":
        data["args"] = dict(flask.request.args)
    error_logger.error(json.dumps(data))

    response = flask.jsonify(
        {
            **data,
            "message": {"internalMessage": str(error), "error_code": 69420, "success": False,},
            "status_code": 500,
        }
    )
    return response, 500


@general_app.app_errorhandler(error.Error)
def custom_error_handler(error):
    response_data = error.data

    # log  error
    data = {
        "service": config.SERVICE_NAME,
        "message": error.message,
        "data": response_data,
        "url": flask.request.url,
        "status_code": error.status_code,
        "environment": config.ENVIRONMENT,
    }
    if flask.request.method == "POST":
        data["body"] = flask.request.data.decode("utf-8")
    elif flask.request.method == "GET":
        data["args"] = dict(flask.request.args)
    error_logger.error(json.dumps(data))

    response = flask.jsonify(
        {
            "message": {"success": False, "error_code": error.code, "internalMessage": error.message,},
            "data": response_data,
            "result": [],
        }
    )
    return response, error.status_code


@general_app.route("/tos")
def hello():
    return flask.redirect("https://www.youtube.com/watch?v=dQw4w9WgXcQ", code=302)


def get_api_infor():
    api_infor = {
        "service_knightmare": check_status(config.SERVICE_KNIGHTMARE_IP),
    }
    return api_infor


@general_app.route("/", methods=["GET"])
def status_check():
    response = flask.jsonify(
        {"service_name": config.SERVICE_NAME, "status": get_api_infor(), "environment": config.ENVIRONMENT}
    )
    return response, 200


def check_status(url, timeout=3):
    if url is None or not url:
        return {"ip": None, "status": "fail", "message": "IP not configured"}
    status = None
    status_code = None
    clean_url = urlsplit(url)
    base_ip = "{}://{}".format(clean_url.scheme, clean_url.netloc)
    with requests.Session() as sess:
        try:
            r = sess.get(base_ip, timeout=timeout)
        except (requests.exceptions.ConnectTimeout, requests.exceptions.ReadTimeout):
            return {
                "ip": url,
                "status": "fail",
                "message": "connection timeout ({}s)".format(timeout),
            }
        except requests.exceptions.ConnectionError as e:
            return {"base_ip": url, "status": "fail", "message": str(e)}
    if r.status_code == 200:
        status = "ok"
    else:
        status = "warning (base method GET for url at '/' not found)"
    status_code = r.status_code
    return {
        "ip": url,
        "status": status,
        "status_code": status_code,
    }
