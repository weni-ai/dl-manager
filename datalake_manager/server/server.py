import os
from concurrent import futures

import grpc
from google.protobuf.json_format import MessageToDict

import datalake_manager.server.proto.commerce_webhook.commerce_webhook_pb2 as commerce_webhook_pb2
import datalake_manager.server.proto.commerce_webhook.commerce_webhook_pb2_grpc as commerce_webhook_pb2_grpc
import datalake_manager.server.proto.message_template.message_templates_pb2 as message_templates_pb2
import datalake_manager.server.proto.message_template.message_templates_pb2_grpc as message_templates_pb2_grpc
import datalake_manager.server.proto.msgs.msgs_pb2 as msgs_pb2
import datalake_manager.server.proto.msgs.msgs_pb2_grpc as msgs_pb2_grpc
import datalake_manager.server.proto.traces.traces_pb2 as traces_pb2
import datalake_manager.server.proto.traces.traces_pb2_grpc as traces_pb2_grpc
from datalake_manager.redshift_manager import RedshiftManager
from datalake_manager.server.interceptors import RateLimiterInterceptor
from datalake_manager.server.proto.events import events_pb2, events_pb2_grpc

redshift = RedshiftManager()


class DatalakeManagerService(
    msgs_pb2_grpc.DatalakeManagerServiceServicer,
    traces_pb2_grpc.DatalakeManagerServiceServicer,
    message_templates_pb2_grpc.DatalakeManagerServiceServicer,
    commerce_webhook_pb2_grpc.CommerceWebhookServiceServicer,
):
    def __init__(self, redshift=None):
        self.redshift = redshift or RedshiftManager()

    def InsertData(self, request, context):
        data_dict = MessageToDict(request.data)

        print(f"Received: path={request.path}, data={data_dict}")

        try:
            response = self.redshift.insert(request.path, data_dict)
            print("Everything right!", response)

            return msgs_pb2.InsertResponse(status="success")
        except Exception as e:
            print("Bad things happens with good people:", str(e))
            return msgs_pb2.InsertResponse(status="error")

    def InsertTraceData(self, request, context):
        data_dict = MessageToDict(request.data)
        print(f"Received Trace Data: path={request.path}, data={data_dict}")
        try:
            response = self.redshift.insert_trace(request.path, data_dict)
            print("Trace inserted successfully!", response)
            return traces_pb2.InsertTraceResponse(status="success")
        except Exception as e:
            print("Error inserting trace data:", str(e))
            return traces_pb2.InsertTraceResponse(status="error")

    def InsertMessageTemplateData(self, request, context):
        data_dict = MessageToDict(request.data)
        print(f"Received Message Template Data: data={data_dict}")
        try:
            response = self.redshift.insert_message_template(data_dict)
            print("Message Template inserted successfully!", response)
            return message_templates_pb2.InsertMessageTemplateResponse(status="success")
        except Exception as e:
            print("Error inserting message template data:", str(e))
            return message_templates_pb2.InsertMessageTemplateResponse(status="error")

    def InsertMessageTemplateStatusData(self, request, context):
        data_dict = MessageToDict(request.data)
        print(f"Received Message Template Status Data: data={data_dict}")
        try:
            response = self.redshift.insert_message_template_status(data_dict)
            print("Message Template Status inserted successfully!", response)
            return message_templates_pb2.InsertMessageTemplateStatusResponse(
                status="success"
            )
        except Exception as e:
            print("Error inserting message template status data:", str(e))
            return message_templates_pb2.InsertMessageTemplateStatusResponse(
                status="error"
            )

    def InsertEventData(self, request, context):
        # Extract data from individual fields of the request
        data_dict = {
            "event_name": request.event_name,
            "key": request.key,
            "date": (
                request.date.ToDatetime().isoformat() + "Z" if request.date else None
            ),
            "project": request.project,
            "contact_urn": request.contact_urn,
            "value_type": self._get_value_type_string(request.value_type),
            "value": self._extract_value_from_value_data(request.value),
            "metadata": MessageToDict(request.metadata) if request.metadata else {},
        }

        print(f"Received Event Data: data={data_dict}")
        try:
            response = self.redshift.insert_event(data_dict)
            print("Event inserted successfully!", response)
            return events_pb2.InsertEventResponse(status="success")
        except Exception as e:
            print("Error inserting event data:", str(e))
            return events_pb2.InsertEventResponse(status="error")

    def _get_value_type_string(self, value_type_enum):
        """Convert enum ValueType to string"""
        if value_type_enum == events_pb2.VALUE_TYPE_INT:
            return "int"
        elif value_type_enum == events_pb2.VALUE_TYPE_STRING:
            return "string"
        elif value_type_enum == events_pb2.VALUE_TYPE_BOOL:
            return "bool"
        elif value_type_enum == events_pb2.VALUE_TYPE_LIST:
            return "list"
        else:
            return "string"  # default

    def _extract_value_from_value_data(self, value_data):
        """Extract the value from the ValueData based on the type"""
        if value_data.HasField("int_value"):
            return value_data.int_value
        elif value_data.HasField("string_value"):
            return value_data.string_value
        elif value_data.HasField("bool_value"):
            return value_data.bool_value
        elif value_data.HasField("list_value"):
            return list(value_data.list_value.values)
        else:
            return ""

    def InsertCommerceWebhookData(self, request, context):
        try:
            data_dict = MessageToDict(request, preserving_proto_field_name=True)
            response = self.redshift.insert_commerce_webhook(data_dict)
            print("Commerce Webhook inserted successfully!", response)
            return commerce_webhook_pb2.InsertCommerceWebhookResponse(status="success")
        except Exception as e:
            print("Error inserting commerce webhook data:", str(e))
            return commerce_webhook_pb2.InsertCommerceWebhookResponse(status="error")


def serve():  # pragma: no cover
    # Define rate limits for each service.
    service_limits = {
        "events.DatalakeManagerService": "300/minute",
        "traces.DatalakeManagerService": "300/minute",
        "msgs.DatalakeManagerService": "300/minute",
        "message_template.DatalakeManagerService": "700/minute",
    }

    # A default limit for any service not specified above.
    default_limit = os.environ.get("GRPC_DEFAULT_RATE_LIMIT", "1000/minute")

    rate_limiter = RateLimiterInterceptor(
        default_rate_limit=default_limit,
        service_rate_limits=service_limits,
    )

    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=10), interceptors=[rate_limiter]
    )
    msgs_pb2_grpc.add_DatalakeManagerServiceServicer_to_server(
        DatalakeManagerService(), server
    )
    traces_pb2_grpc.add_DatalakeManagerServiceServicer_to_server(
        DatalakeManagerService(), server
    )
    message_templates_pb2_grpc.add_DatalakeManagerServiceServicer_to_server(
        DatalakeManagerService(), server
    )
    events_pb2_grpc.add_DatalakeManagerServiceServicer_to_server(
        DatalakeManagerService(), server
    )
    commerce_webhook_pb2_grpc.add_CommerceWebhookServiceServicer_to_server(
        DatalakeManagerService(), server
    )
    server.add_insecure_port("[::]:50051")
    print(f"Server starting at [::]:50051 with default rate limit: {default_limit}")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":  # pragma: no cover
    serve()
