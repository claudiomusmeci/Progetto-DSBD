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
import smtplib

mittente = os.environ['MITTENTE']
password = os.environ['PASSWORD']

subscriptions = {}
lista_thread = []

def invia_mail(destinatario, contenuto):
    try:
        email = smtplib.SMTP("smtp.gmail.com", 587)
        email.ehlo()
        email.starttls()
        email.login(mittente, password)
        email.sendmail(mittente, destinatario, contenuto)
        email.quit()
    except Exception as e:
        print(f"Errore durante l'invio dell'email a {destinatario}: {e}")

def avvisa_utente(user, topic, valori_ricevuti, vincoli_utente):
    vincoli=json.loads(vincoli_utente)
    if(valori_ricevuti['variazione_percentuale'] >= vincoli['variazione_percentuale']):
        contenuto = (f"Utente {user}, violazione dei vincoli per il topic {topic}")
        print(contenuto)
        #invia_mail(user, contenuto)


def gestisci_messaggio(user, message):
    #Elaboro il messaggio
    data = json.loads(message.value)
    print("\nUtente {}\nTopic {}\n{}".format(user, message.topic, data))

    #Implemento la logica per avvisare l'utente
    user_info = subscriptions.get(user)
    if user_info and user_info['topics'].get(message.topic):
        vincoli_topic = user_info['topics'][message.topic]['vincoli']
        if vincoli_topic:
            avvisa_utente(user, message.topic, data, vincoli_topic)

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

#Gestione server gRPC
class ClientManagementService(pb2_grpc.ClientManagementServicer):
    def SendData(self, request, context):
        #Converto l'oggetto Constraint ricevuto in un dizionario
        constraints_dict = {
            "prezzo": request.constraints.prezzo,
            "variazione_percentuale": request.constraints.variazione_percentuale,
            "prezzo_min_24h": request.constraints.prezzo_min_24h,
            "prezzo_max_24h": request.constraints.prezzo_max_24h,
        }
        print(f"Ricevuti dati dal client\nConstraints: {constraints_dict}\nTopic: {request.topic}\nUser: {request.user}")
        #Converto il dizionario in un JSON
        constraints_json = json.dumps(constraints_dict)

        user_info = subscriptions.get(request.user)
        if user_info and user_info['topics'].get(request.topic):
            user_info['topics'][request.topic]['vincoli'] = constraints_json
            response_message = f"Vincoli received successfully for user {request.user}, in topic {request.topic}"
        else:
            response_message = f"User {request.user} not found in subscriptions."

        return pb2.ResponseData(message=response_message)

    def SendNewSubscriber(self, request, context):
        #Implemento la logica per il metodo SendNewSubscriber
        print(f"Received new subscriber data from client\nUser: {request.user}, topic: {request.topic}")
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





        ''' Struttura del dizionario subscriptions
        subscriptions = {
                'utente1@example.com': {
                    'consumer': <oggetto_consumer_utente1>,
                    'topics': {
                        'topic1': {'vincoli': <vincoli_topic1>},
                        'topic2': {'vincoli': <vincoli_topic2>},
                        # ... altri topic
                    }
                },
                'utente2@example.com': {
                    'consumer': <oggetto_consumer_utente2>,
                    'topics': {
                        'topic1': {'vincoli': <vincoli_topic1>},
                        'topic3': {'vincoli': <vincoli_topic3>},
                        # ... altri topic
                    }
                },
                # ... altri utenti
            }
        '''