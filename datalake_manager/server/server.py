from concurrent import futures
import grpc
import msgs_pb2
import msgs_pb2_grpc
from google.protobuf.json_format import MessageToDict

class DatalakeManagerService(msgs_pb2_grpc.DatalakeManagerServiceServicer):
    def InsertData(self, request, context):
        data_dict = MessageToDict(request.data)

        print(f"Received: path={request.path}, data={data_dict}")
        

        return msgs_pb2.InsertResponse(status="success")

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    msgs_pb2_grpc.add_DatalakeManagerServiceServicer_to_server(DatalakeManagerService(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    print("Server running in 50051...")
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
