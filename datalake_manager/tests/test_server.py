from unittest.mock import MagicMock

import grpc
import pytest
from google.protobuf.json_format import ParseDict
from google.protobuf.timestamp_pb2 import Timestamp

import datalake_manager.server.proto.commerce_webhook.commerce_webhook_pb2 as commerce_webhook_pb2
import datalake_manager.server.proto.events.events_pb2 as events_pb2
import datalake_manager.server.proto.msgs.msgs_pb2 as msgs_pb2
import datalake_manager.server.proto.traces.traces_pb2 as traces_pb2
from datalake_manager.clients.redshift_client import RedshiftClient
from datalake_manager.redshift_manager import RedshiftManager
from datalake_manager.server.interceptors import RateLimiterInterceptor
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


def test_insert_event_data_success(service, mock_redshift):
    timestamp = Timestamp()
    timestamp.FromJsonString("2023-10-26T10:00:00Z")
    request = events_pb2.InsertEventRequest(
        event_name="test_event",
        key="test_key",
        date=timestamp,
        project="test_project",
        contact_urn="tel:+123456789",
        value_type=events_pb2.VALUE_TYPE_STRING,
        value=events_pb2.ValueData(string_value="test_value"),
    )
    context = MagicMock()
    response = service.InsertEventData(request, context)
    expected_data = {
        "event_name": "test_event",
        "key": "test_key",
        "date": "2023-10-26T10:00:00Z",
        "project": "test_project",
        "contact_urn": "tel:+123456789",
        "value_type": "string",
        "value": "test_value",
        "metadata": {},
    }
    mock_redshift.insert_event.assert_called_once_with(expected_data)
    assert response.status == "success"


def test_insert_event_data_failure(service, mock_redshift):
    mock_redshift.insert_event.side_effect = Exception("DB error")
    request = events_pb2.InsertEventRequest(event_name="test_event")
    context = MagicMock()
    response = service.InsertEventData(request, context)
    mock_redshift.insert_event.assert_called_once()
    assert response.status == "error"


def test_insert_commerce_webhook_data_success(service, mock_redshift):
    from google.protobuf.struct_pb2 import Struct
    from google.protobuf.timestamp_pb2 import Timestamp

    timestamp = Timestamp()
    timestamp.FromJsonString("2023-10-26T10:00:00Z")
    data_struct = Struct()
    data_struct.update({"order_id": "123"})
    request = commerce_webhook_pb2.InsertCommerceWebhookRequest(
        status=1,
        template="order_confirmation",
        template_variables=Struct(),
        contact_urn="tel:+123456789",
        error=Struct(),
        data=data_struct,
        date=timestamp,
        project="test_project",
    )
    context = MagicMock()
    response = service.InsertCommerceWebhookData(request, context)
    expected_data = {
        "status": 1,
        "template": "order_confirmation",
        "template_variables": {},
        "contact_urn": "tel:+123456789",
        "error": {},
        "data": {"order_id": "123"},
        "date": "2023-10-26T10:00:00Z",
        "project": "test_project",
    }
    mock_redshift.insert_commerce_webhook.assert_called_once_with(expected_data)
    assert response.status == "success"


def test_insert_commerce_webhook_data_failure(service, mock_redshift):
    mock_redshift.insert_commerce_webhook.side_effect = Exception("DB error")
    request = commerce_webhook_pb2.InsertCommerceWebhookRequest(status=1)
    context = MagicMock()
    response = service.InsertCommerceWebhookData(request, context)
    mock_redshift.insert_commerce_webhook.assert_called_once()
    assert response.status == "error"


def test_rate_limiter_interceptor():
    # Configure the interceptor with a low limit for a specific service
    service_limits = {"events.DatalakeManagerService": "2/second"}
    interceptor = RateLimiterInterceptor(
        default_rate_limit="10/second", service_rate_limits=service_limits
    )

    # Mock the gRPC handler details for the "events" service
    handler_details_events = MagicMock()
    handler_details_events.method = "/events.DatalakeManagerService/InsertEventData"

    # Mock the gRPC handler details for another service (which will use the default limit)
    handler_details_other = MagicMock()
    handler_details_other.method = "/other.Service/SomeMethod"

    # Mock the continuation function that gRPC calls to proceed
    continuation = MagicMock()
    continuation.return_value = "OK"  # Simulate a successful RPC call

    # --- Test "events" service limit ---
    # First two calls should succeed
    assert interceptor.intercept_service(continuation, handler_details_events) == "OK"
    assert interceptor.intercept_service(continuation, handler_details_events) == "OK"

    # The third call should be rate-limited and return an abort handler
    abort_handler = interceptor.intercept_service(continuation, handler_details_events)
    mock_context = MagicMock()

    # The returned handler, when called by gRPC, aborts the request.
    # We call it directly by accessing its `unary_unary` method to test this.
    abort_handler.unary_unary(None, mock_context)

    # Check that the context was aborted with the correct status and message
    mock_context.abort.assert_called_once()
    assert mock_context.abort.call_args[0][0] == grpc.StatusCode.RESOURCE_EXHAUSTED
    assert (
        "Rate limit for service events.DatalakeManagerService exceeded"
        in mock_context.abort.call_args[0][1]
    )

    # Ensure the original continuation was not called for the blocked request
    assert continuation.call_count == 2

    # --- Test default service limit ---
    # This call to a different service should succeed as it has its own limit bucket
    assert interceptor.intercept_service(continuation, handler_details_other) == "OK"
    assert continuation.call_count == 3
