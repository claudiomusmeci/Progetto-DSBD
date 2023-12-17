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

def avvisa_utente(user, topic, valori_ricevuti, vincoli_utente):
    vincoli=json.loads(vincoli_utente)
    if(valori_ricevuti['variazione_percentuale'] >= vincoli['variazione_percentuale']):
        print("Notifico l'utente {}, violazione dei vincoli per il topic {}".format(user, topic))



def gestisci_messaggio(user, message):
    # Elabora il messaggio
    data = json.loads(message.value)
    print("Utente {}".format(user))
    print("Topic {}".format(message.topic))
    print("{}".format(data))

    #Implementare la logica per avvisare l'utente
    user_info = subscriptions.get(user)
    if user_info and user_info['topics'].get(message.topic):
        vincoli_topic = user_info['topics'][message.topic]['vincoli']
        if vincoli_topic:
            avvisa_utente(user, message.topic, data, vincoli_topic)
        #avvisa_utente(user, data, vincoli_topic)

def sottoscrivi_utenti(user, topics, lista_thread):
    nome_utente=user.split('@')
    group_id = f"CONSUMER_{nome_utente[0]}"
    consumer = KafkaConsumer(
        group_id=group_id,
        bootstrap_servers=[os.environ['KAFKA_BROKER']],
        value_deserializer=lambda x: json.loads(x.decode('ascii'))
    )
    consumer.subscribe(topics)

    subscriptions[user] = {'consumer': consumer, 'topics': {}}
    for topic in topics:
        subscriptions[user]['topics'][topic] = {'vincoli': None}

    thread = threading.Thread(target=consume_message, args=(user,))
    lista_thread.append(thread)
    thread.start()

def consume_message(user):
    consumer = subscriptions[user]['consumer']
    for message in consumer:
        gestisci_messaggio(user, message)

def main():
    # Sottoscrizioni di utenti di prova
    sottoscrivi_utenti('utente1@example.com', ['Tether', 'Ethereum'], lista_thread)
    sottoscrivi_utenti('utente2@example.com', ['Ethereum', 'Bitcoin'], lista_thread)
    sottoscrivi_utenti('utente3@example.com', ['Bitcoin'], lista_thread)

    print('Ascolto il client gRPC')
    ClientManagementService.serve()

#Gestione server gRPC
class ClientManagementService(pb2_grpc.ClientManagementServicer):
    def SendData(self, request, context):
        #Implemento la logica per il metodo SendData
        print("Received data from client:")
        print("Constraints:", request.constraints)
        print("Topic:", request.topic)
        print("User:", request.user)

        # Converti l'oggetto Constraint in un dizionario Python
        constraints_dict = {
            "prezzo": request.constraints.prezzo,
            "variazione_percentuale": request.constraints.variazione_percentuale,
            "prezzo_min_24h": request.constraints.prezzo_min_24h,
            "prezzo_max_24h": request.constraints.prezzo_max_24h,
        }

        # Converti il dizionario in una rappresentazione JSON
        constraints_json = json.dumps(constraints_dict)

        user_info = subscriptions.get(request.user)
        if user_info and user_info['topics'].get(request.topic):
            user_info['topics'][request.topic]['vincoli'] = constraints_json
            response_message = f"Vincoli received successfully for user {request.user}, in topic {request.topic}"
        else:
            response_message = f"User {request.user} not found in subscriptions."

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
    i=0
    main()
    #Attendo che tutti i thread terminino (anche se non è previsto che essi terminino)
    for thread in lista_thread:
        thread.join()
        print("Tutti i thread sono terminati")