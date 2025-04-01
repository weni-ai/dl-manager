from concurrent import futures

import grpc
from google.protobuf.json_format import MessageToDict

import datalake_manager.server.proto.msgs_pb2 as msgs_pb2
import datalake_manager.server.proto.msgs_pb2_grpc as msgs_pb2_grpc
from datalake_manager.redshift_manager import RedshiftManager

redshift = RedshiftManager()


class DatalakeManagerService(msgs_pb2_grpc.DatalakeManagerServiceServicer):
    def InsertData(self, request, context):
        data_dict = MessageToDict(request.data)

        print(f"Received: path={request.path}, data={data_dict}")

        try:
            response = redshift.insert(request.path, data_dict)
            print("Everything right!", response)

            return msgs_pb2.InsertResponse(status="success")
        except Exception as e:
            print("Bad things happens with good people:", str(e))
            return msgs_pb2.InsertResponse(status="error")


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    msgs_pb2_grpc.add_DatalakeManagerServiceServicer_to_server(
        DatalakeManagerService(), server
    )
    server.add_insecure_port("[::]:50051")
    server.start()
    print("Server running in 50051...")
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
