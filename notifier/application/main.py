from kafka import KafkaConsumer
import os
import json
import threading
import sys
import grpc
from concurrent import futures
sys.path.append('./grpc')
import messaggi_pb2 as pb2
import messaggi_pb2_grpc as pb2_grpc
#from Server_gRPC import serve

def gestisci_messaggio(user, message):
    # Elabora il messaggio
    data = json.loads(message.value)
    print('{} Nuovi dati dal topic {} Kafka: {}'.format(user, message.topic, data))
    #Implementare la logica per avvisare l'utente

def sottoscrivi_utenti(user, topics, lista_thread):
    group_id = f"CONSUMER_{user}"
    consumer = KafkaConsumer(
        group_id=group_id,
        bootstrap_servers=[os.environ['KAFKA_BROKER']],
        value_deserializer=lambda x: json.loads(x.decode('ascii'))
    )
    consumer.subscribe(topics)
    subscriptions[user] = consumer
    thread = threading.Thread(target=consume_message, args=(user,))
    lista_thread.append(thread)
    thread.start()
    

def consume_message(user):
    consumer = subscriptions[user]
    for message in consumer:
        gestisci_messaggio(user, message)

def main():
    # Sottoscrizioni di utenti di prova
    sottoscrivi_utenti('Utente1', ['Bitcoin', 'Ethereum'], lista_thread)
    sottoscrivi_utenti('Utente2', ['Ethereum', 'Bitcoin'], lista_thread)
    sottoscrivi_utenti('Utente3', ['Bitcoin'], lista_thread)

    print('Ascolto il client gRPC')
    ClientManagementService.serve()
    
    
    #Attendo che tutti i thread terminino (anche se non è previsto che essi terminino)
    for thread in lista_thread:
        thread.join()
        print("Tutti i thread sono terminati")

#Gestione server gRPC
class ClientManagementService(pb2_grpc.ClientManagementServicer):
    def SendData(self, request, context):
        # Implementa la logica per il metodo SendData
        print("Received data from client:")
        print("Constraints:", request.constraints)
        print("Topic:", request.topic)
        print("User:", request.user)
        response_message = f"Data received successfully for user {request.user}"
        
        return pb2.ResponseData(message=response_message)

    def SendNewSubscriber(self, request, context):
        # Implementa la logica per il metodo SendNewSubscriber
        print("Received new subscriber data from client:")
        print("User:", request.user)
        print("Topic:", request.topic)
        sottoscrivi_utenti(request.user, [request.topic], lista_thread)
        response_message = f"New subscriber added successfully: {request.user}"
        return pb2.ResponseData(message=response_message)

    @classmethod
    def serve(cls):
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        pb2_grpc.add_ClientManagementServicer_to_server(cls(), server)
        server.add_insecure_port('[::]:50051')
        print('Avvio il server, in ascolto nella porta 50051')
        server.start()
        server.wait_for_termination()


#Avvio del main
if __name__ == '__main__':
    subscriptions = {}
    lista_thread = []
    main()