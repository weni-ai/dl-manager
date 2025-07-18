from unittest.mock import MagicMock

import pytest

from datalake_manager.config import (
    REDSHIFT_COMMERCE_WEBHOOK_METRIC,
    REDSHIFT_EVENT_METRIC,
    REDSHIFT_MSG_METRIC,
    REDSHIFT_TRACE_METRIC,
)
from datalake_manager.redshift_manager import RedshiftManager


@pytest.fixture
def mock_redshift_client():
    mock_client = MagicMock()
    mock_client.send.return_value = {"status": "success"}
    return mock_client


@pytest.fixture
def redshift_manager(mock_redshift_client):
    manager = RedshiftManager()
    manager.client = mock_redshift_client
    return manager


def test_insert_calls_client_send(redshift_manager, mock_redshift_client):
    path = "test_table"
    data = [{"field": "test_value"}]

    response = redshift_manager.insert(path, data)

    mock_redshift_client.send.assert_called_once_with(
        {"name": REDSHIFT_MSG_METRIC, "kind": path, "fields": data}
    )

    assert response == {"status": "success"}


def test_insert_trace_calls_client_send(redshift_manager, mock_redshift_client):
    path = "test_table"
    data = [{"field": "test_value"}]

    response = redshift_manager.insert_trace(path, data)

    mock_redshift_client.send.assert_called_once_with(
        {"name": REDSHIFT_TRACE_METRIC, "kind": path, "fields": data}
    )

    assert response == {"status": "success"}


def test_insert_event_calls_client_send(redshift_manager, mock_redshift_client):
    event_data = {
        "event_name": "test_event",
        "key": "test_key",
        "date": "2023-10-27T10:00:00Z",
        "project": "test_project",
        "contact_urn": "tel:+123456789",
        "value": "test_value",
        "value_type": "string",
        "metadata": {"source": "test"},
    }

    response = redshift_manager.insert_event(event_data)

    expected_payload = {
        "name": REDSHIFT_EVENT_METRIC,
        "event_name": "test_event",
        "key": "test_key",
        "date": "2023-10-27T10:00:00Z",
        "project": "test_project",
        "contact_urn": "tel:+123456789",
        "value": "test_value",
        "value_type": "string",
        "metadata": {"source": "test"},
    }

    mock_redshift_client.send.assert_called_once_with(expected_payload)
    assert response == {"status": "success"}


def test_insert_commerce_webhook_calls_client_send(
    redshift_manager, mock_redshift_client
):
    commerce_webhook_data = {
        "status": 1,
        "template": "order_confirmation",
        "template_variables": {"var1": "value1"},
        "contact_urn": "tel:+123456789",
        "error": {},
        "data": {"order_id": "123"},
        "date": "2023-10-26T10:00:00Z",
        "project": "test_project",
        "request": {"req": "info"},
        "response": {"res": "info"},
        "agent": "agent_007",
    }

    response = redshift_manager.insert_commerce_webhook(commerce_webhook_data)

    expected_payload = {
        "name": REDSHIFT_COMMERCE_WEBHOOK_METRIC,
        "status": 1,
        "template": "order_confirmation",
        "template_variables": {"var1": "value1"},
        "contact_urn": "tel:+123456789",
        "error": {},
        "data": {"order_id": "123"},
        "date": "2023-10-26T10:00:00Z",
        "project": "test_project",
        "request": {"req": "info"},
        "response": {"res": "info"},
        "agent": "agent_007",
    }

    mock_redshift_client.send.assert_called_once_with(expected_payload)
    assert response == {"status": "success"}
