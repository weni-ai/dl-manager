from concurrent import futures

import grpc
from google.protobuf.json_format import MessageToDict

import datalake_manager.server.proto.message_template.message_templates_pb2 as message_templates_pb2
import datalake_manager.server.proto.message_template.message_templates_pb2_grpc as message_templates_pb2_grpc
import datalake_manager.server.proto.msgs.msgs_pb2 as msgs_pb2
import datalake_manager.server.proto.msgs.msgs_pb2_grpc as msgs_pb2_grpc
import datalake_manager.server.proto.traces.traces_pb2 as traces_pb2
import datalake_manager.server.proto.traces.traces_pb2_grpc as traces_pb2_grpc
from datalake_manager.redshift_manager import RedshiftManager

redshift = RedshiftManager()


class DatalakeManagerService(
    msgs_pb2_grpc.DatalakeManagerServiceServicer,
    traces_pb2_grpc.DatalakeManagerServiceServicer,
    message_templates_pb2_grpc.DatalakeManagerServiceServicer,
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


def serve():  # pragma: no cover
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    msgs_pb2_grpc.add_DatalakeManagerServiceServicer_to_server(
        DatalakeManagerService(), server
    )
    traces_pb2_grpc.add_DatalakeManagerServiceServicer_to_server(
        DatalakeManagerService(), server
    )
    message_templates_pb2_grpc.add_DatalakeManagerServiceServicer_to_server(
        DatalakeManagerService(), server
    )
    server.add_insecure_port("[::]:50051")
    server.start()
    print("Server running in 50051...")
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
