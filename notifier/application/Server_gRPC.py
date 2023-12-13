import grpc
from concurrent import futures
import sys
sys.path.append('./grpc') 
import messaggi_pb2 as pb2
import messaggi_pb2_grpc as pb2_grpc

class ClientManagementService(pb2_grpc.ClientManagementServicer):
    def SendData(self, request, context):
        # Implementa la logica per il metodo SendData
        print("Received data from client:")
        print("Constraints:", request.constraints)
        print("Topic:", request.topic)
        print("User:", request.user)
        response_message = f"Data received successfully for user {request.user.nome_utente}"
        
        return pb2.ResponseData(message=response_message)

    def SendNewSubscriber(self, request, context):
        # Implementa la logica per il metodo SendNewSubscriber
        print("Received new subscriber data from client:")
        print("User:", request.user)
        print("Topic:", request.topic)
        response_message = f"New subscriber added successfully: {request.user.nome_utente}"
        return pb2.ResponseData(message=response_message)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pb2_grpc.add_ClientManagementServicer_to_server(ClientManagementService(), server)
    server.add_insecure_port('[::]:50051')
    print('Avvio il server, in ascolto nella porta 50051')
    server.start()
    server.wait_for_termination()