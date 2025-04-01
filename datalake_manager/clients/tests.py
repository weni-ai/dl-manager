import json

import pytest
import requests
import requests_mock
from weni_datalake_sdk.clients.redshift_client import RedshiftClient

BASE_URL = "https://datalake.example.com/api"
HEADERS = {"Content-Type": "application/json"}
PAYLOAD = {"key": "value"}
EXPECTED_RESPONSE = {"status": "success"}


@pytest.fixture
def client():
    return RedshiftClient(BASE_URL, HEADERS)


def test_send_success(client):
    with requests_mock.Mocker() as mocker:
        mocker.post(BASE_URL, json=EXPECTED_RESPONSE, status_code=200)

        response = client.send(PAYLOAD)

        assert response == EXPECTED_RESPONSE
        assert mocker.called
        assert mocker.request_history[0].method == "POST"
        assert json.loads(mocker.request_history[0].text) == PAYLOAD


def test_send_failure(client):
    with requests_mock.Mocker() as mocker:
        mocker.post(BASE_URL, json={"error": "Bad Request"}, status_code=400)

        response = client.send(PAYLOAD)

        assert response == {"error": "Bad Request"}
        assert mocker.called
        assert mocker.request_history[0].method == "POST"


def test_send_timeout(client):
    with requests_mock.Mocker() as mocker:
        mocker.post(BASE_URL, exc=requests.exceptions.Timeout)

        with pytest.raises(requests.exceptions.Timeout):
            client.send(PAYLOAD)
