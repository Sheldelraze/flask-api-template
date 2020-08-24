import json
import time
from urllib.parse import urlencode

import pytest

import config
from server import app

app.testing = True
client = app.test_client()

user_id = "its_me_unittest"


@pytest.fixture(scope="function")
def clean_up():
    print("start function")

    yield

    print("Cleaning database...")
    # k_service.practice_session.delete_many(dict(user_id=user_id))
    # k_service.practice_history.delete_many(dict(user_id=user_id))


def test_base_url(clean_up):
    response = client.get("/")
    data = json.loads(response.get_data(as_text=True))
    assert response.status_code == 200
    assert data["service_name"] == config.SERVICE_NAME


@pytest.mark.repeat(2)  # repeat test 2 times
def test_get_sample(clean_up):
    params = {"user_id": user_id, "event_timestamp": time.time(), "params_one": "foo", "params_two": 69}
    params = urlencode(params)
    response = client.get("/sample?" + params)
    data = json.loads(response.get_data(as_text=True))
    assert "question" in data["data"]


def test_post_sample(clean_up):
    body = {"user_id": user_id, "event_timestamp": time.time(), "params_three": 420, "params_four": "bar"}
    response = client.post("/sample", data=json.dumps(body), content_type="application/json")
    data = json.loads(response.get_data(as_text=True))
    assert "answer" in data["data"]


# TODO: Delete this
def test_error():
    response = client.get("/error")
    data = json.loads(response.get_data(as_text=True))
    print("Error:", data)
