#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import datetime
import json
import logging
import sys
import traceback
from functools import wraps
from time import time

import graypy
import requests
import urllib3
from pebble import concurrent

import config

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def send_request(
    url, json=None, params=None, method: str = "post", headers: dict = None, timeout: int = 10, chunk_size: int = 100,
):
    """
    Helper function for calling other API, will timed out after waiting for `timeout` second
    """
    method = method.lower()
    assert method in ["post", "get", "put", "delete"], f"Method {method} not supported!"
    start = time()
    with requests.Session() as sess:
        request_method = getattr(sess, method)
        r = request_method(url, params=params, json=json, verify=False, headers=headers, stream=True, timeout=timeout,)
        body = []
        for chunk in r.iter_content(chunk_size):
            body.append(chunk)
            if time() > (start + timeout):
                raise TimeoutError()
        content = b"".join(body)
        r._content = content
        r._content_consumed = False
    return r


def timing(f):
    """
    Decorator function to add time elapsed
    """

    @wraps(f)
    def wrapper(*args, **kwargs):
        start = time()
        result = f(*args, **kwargs)
        end = time()
        time_elapsed = round(end - start, 2)
        if isinstance(result, tuple):
            return (*result, time_elapsed)
        return result, time_elapsed

    return wrapper


###logging
logger_manager = {}


def get_logger(name, include_datetime=True):
    global logger_manager
    now = datetime.datetime.now()
    if include_datetime:
        filename = "logs/{}_{}.txt".format(now.strftime("%Y%m%d"), name)
    else:
        filename = "logs/{}.txt".format(name)

    if filename not in logger_manager:

        # create logger
        logger = logging.getLogger(name)
        logger.setLevel(logging.INFO)

        # create handler for stdout
        stdout_handler = logging.StreamHandler(sys.stdout)
        stdout_handler.setLevel(logging.INFO)
        logger.addHandler(stdout_handler)

        # create handler for file
        file_handler = logging.FileHandler(filename)
        logger.addHandler(file_handler)

        # create handler for graylog
        graylog_handler = graypy.GELFTcpHandler(config.SERVICE_GRAYLOG_IP, config.SERVICE_GRAYLOG_PORT)
        graylog_handler.setLevel(logging.INFO)
        logger.addHandler(graylog_handler)

        # add format
        format_string = "[%(asctime)s][%(name)s][%(levelname)s]: %(message)s"
        formatter = logging.Formatter(format_string)
        file_handler.setFormatter(formatter)
        stdout_handler.setFormatter(formatter)

        logger_manager[filename] = logger
    return logger_manager[filename]


###threading
def format_exception(e):
    exception_list = traceback.format_stack()
    exception_list = exception_list[:-2]
    exception_list.extend(traceback.format_tb(sys.exc_info()[2]))
    exception_list.extend(traceback.format_exception_only(sys.exc_info()[0], sys.exc_info()[1]))

    exception_str = "Traceback (most recent call last):\n"
    exception_str += "".join(exception_list)
    # Removing the last \n
    exception_str = exception_str[:-1]
    return exception_str


error_logger = get_logger("error", False)


def print_exception(future):
    error = future.exception()
    if error is not None:
        error_data = {
            "service": config.SERVICE_NAME,
            "message": "Background job fail!",
            "environment": config.ENVIRONMENT,
            "stacktrace": format_exception(error),
        }
        error_logger.error(json.dumps(error_data))


def run_background_job(function, return_result=False, callback=None, **params):
    wrapper_function = concurrent.thread(function)
    result = wrapper_function(**params)
    result.add_done_callback(print_exception)
    if callback is not None:
        result.add_done_callback(callback)
    if return_result:
        return result
