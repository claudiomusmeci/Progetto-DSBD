import grpc
import sys
import time
from Database import DatabaseManager
sys.path.append('./grpc')
import messaggi_pb2 as pb2
import messaggi_pb2_grpc as pb2_grpc
import _mysql_connector


def send_constraint_to_server(prezzo, variazione_percentuale, prezzo_min_24h, prezzo_max_24h, topic_fornito, user_fornito):
    channel = grpc.insecure_channel('microservizio1:50051')
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
    channel = grpc.insecure_channel('microservizio1:50051')
    stub = pb2_grpc.ClientManagementStub(channel)

    #Costruisco la richiesta con un utente e un insieme di topic
    request = pb2.Subscriber(
        user=utente_fornito,
        topic=topic_fornito
    )
    # Chiamata al metodo del servizio
    response = stub.SendNewSubscriber(request)
    print("Response received:", response)

def main():
    database = DatabaseManager()
    while True:
        print('Scelta')
        print('1) Aggiungi utente ad un topic')
        print('2) Aggiungi dei vincoli')
        scelta = input()
        match int(scelta):
            case 1:
                mail = input("Inserisci la email dell'utente: ")
                topic = input("Inserisci un topic [Bitcoin, Ethereum, Tether]: ")
                
                esito = database.inserisci_subscriber(mail, topic)
                if esito == True:
                    send_subscriber_to_server(mail, topic)
                else:
                    print("L'utente è già sottoscritto o il topic non esiste")
                
            case 2:
                utente = input("Inserisci il nome dell'utente ")
                topic = input("Inserisci un topic: [Bitcoin, Ethereum, Tether] ")
                str_vincoli = input("Inserisci i vincoli separati da una virgola: prezzo, variazione percentuale, max_24h, min_24h ")
                vincoli = str_vincoli.split(',')
                if len(vincoli) == 4:
                    send_constraint_to_server(vincoli[0], vincoli[1], vincoli[2], vincoli[3], topic, utente)
                    #Inserisco nel database

            case _:
                print('Scelta non valida')
        
        

#Funzione main
if __name__ == '__main__':
    main()
    