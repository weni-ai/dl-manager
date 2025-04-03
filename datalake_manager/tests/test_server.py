from unittest.mock import MagicMock

import pytest
from google.protobuf.json_format import ParseDict

import datalake_manager.server.proto.msgs_pb2 as msgs_pb2
import datalake_manager.server.proto.traces_pb2 as traces_pb2
from datalake_manager.clients.redshift_client import RedshiftClient
from datalake_manager.redshift_manager import RedshiftManager
from datalake_manager.server.server import DatalakeManagerService


@pytest.fixture
def mock_redshift():
    mock = MagicMock(spec=RedshiftManager)
    mock.client = MagicMock(spec=RedshiftClient)
    mock.client.send.return_value = {"status": "success"}
    return mock


@pytest.fixture
def service(mock_redshift):
    return DatalakeManagerService(redshift=mock_redshift)


def test_insert_data_success(service, mock_redshift):
    request = msgs_pb2.InsertRequest(path="test_table")
    request.data.update(ParseDict({"field": "test_value"}, request.data))

    context = MagicMock()
    response = service.InsertData(request, context)

    mock_redshift.insert.assert_called_once_with("test_table", {"field": "test_value"})
    assert response.status == "success"


def test_insert_data_failure(service, mock_redshift):
    mock_redshift.insert.side_effect = Exception("DB error")

    request = msgs_pb2.InsertRequest(path="test_table")
    request.data.update(ParseDict({"field": "test_value"}, request.data))

    context = MagicMock()
    response = service.InsertData(request, context)

    mock_redshift.insert.assert_called_once()
    assert response.status == "error"


def test_insert_trace_data_success(service, mock_redshift):
    request = traces_pb2.InsertTraceRequest(path="trace_table")
    request.data.update(ParseDict({"trace_field": "trace_value"}, request.data))

    context = MagicMock()
    response = service.InsertTraceData(request, context)

    mock_redshift.insert_trace.assert_called_once_with(
        "trace_table", {"trace_field": "trace_value"}
    )
    assert response.status == "success"


def test_insert_trace_data_failure(service, mock_redshift):
    mock_redshift.insert_trace.side_effect = Exception("DB error")

    request = traces_pb2.InsertTraceRequest(path="trace_table")
    request.data.update(ParseDict({"trace_field": "trace_value"}, request.data))

    context = MagicMock()
    response = service.InsertTraceData(request, context)

    mock_redshift.insert_trace.assert_called_once()
    assert response.status == "error"
