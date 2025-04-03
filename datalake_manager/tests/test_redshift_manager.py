from unittest.mock import MagicMock

import pytest

from datalake_manager.config import REDSHIFT_MSG_METRIC, REDSHIFT_TRACE_METRIC
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
