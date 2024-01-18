import sys
import grpc
sys.path.append('./grpc')
import messaggi_pb2 as pb2
import messaggi_pb2_grpc as pb2_grpc
import os


def send_constraint_to_server(prezzo, variazione_percentuale, prezzo_min_24h, prezzo_max_24h, topic_fornito, user_fornito):
    channel = grpc.insecure_channel(os.environ['SERVER_GRPC'])
    #channel = grpc.insecure_channel('microservizio1:50051')
    stub = pb2_grpc.ClientManagementStub(channel)

    #Costruisco la richiesta con un insieme di constraint, un topic e un utente
    request = pb2.RequestData(
        constraints=pb2.Constraint(prezzo=float(prezzo), variazione_percentuale=float(variazione_percentuale), prezzo_min_24h=float(prezzo_min_24h), prezzo_max_24h=float(prezzo_max_24h)),
        topic=topic_fornito,
        user=user_fornito
    )
    #Chiamata al metodo del servizio
    response = stub.SendData(request)
    print("Response received:", response)

def send_subscriber_to_server(utente_fornito, topic_fornito):
    channel = grpc.insecure_channel(os.environ['SERVER_GRPC'])
    #channel = grpc.insecure_channel('microservizio1:50051')
    stub = pb2_grpc.ClientManagementStub(channel)

    #Costruisco la richiesta con un utente e un insieme di topic
    request = pb2.Subscriber(
        user=utente_fornito,
        topic=topic_fornito
    )
    #Chiamata al metodo del servizio
    response = stub.SendNewSubscriber(request)
    print("Response received:", response)