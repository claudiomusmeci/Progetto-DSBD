import grpc
import sys
import time
sys.path.append('./grpc')
import messaggi_pb2 as pb2
import messaggi_pb2_grpc as pb2_grpc

def send_constraint_to_server(prezzo, variazione_percentuale, prezzo_min_24h, prezzo_max_24h, topic, user):
    channel = grpc.insecure_channel('microservizio1:50051')
    stub = pb2_grpc.ClientManagementStub(channel)

    #Costruisco la richiesta con un insieme di constraint, un topic e un utente
    request = pb2.RequestData(
        constraints=pb2.Constraint(field1=prezzo, field2=variazione_percentuale, field3=prezzo_min_24h, field4=prezzo_max_24h),
        topic=pb2.Topic(field1=topic),  # Sostituisci con i dati del tuo topic
        user=pb2.User(field1=user)   # Sostituisci con i dati del tuo utente
    )
    #Chiamata al metodo del servizio
    response = stub.SendData(request)
    print("Response received:", response)

def send_subscriber_to_server(utente_fornito, topic_fornito):
    channel = grpc.insecure_channel('microservizio1:50051')
    stub = pb2_grpc.ClientManagementStub(channel)

    #Costruisco la richiesta con un utente e un insieme di topic
    request = pb2.Subscriber(
        user=pb2.User(nome_utente=utente_fornito),
        topic=pb2.Topic(topic=topic_fornito)
    )
    # Chiamata al metodo del servizio
    response = stub.SendNewSubscriber(request)
    print("Response received:", response)

def main():
    
    while True:
        time.sleep(150)
        print('Scelta')
        print('1) Aggiungi utente ad un topic')
        print('2) Aggiungi dei vincoli')
        scelta = input()
        match int(scelta):
            case 1:
                print("Inserisci il nome dell'utente")
                utente = input()
                print("Inserisci un topic: [Bitcoin, Ethereum, Tether]")
                topic = input()
                send_subscriber_to_server(utente, topic)
                
            case 2:
                print("Inserisci il nome dell'utente")
                utente = input()
                print("Inserisci un topic: [Bitcoin, Ethereum, Tether]")
                topic = input()
                print("Inserisci i vincoli")
                str_vincoli = input()
                vincoli = str_vincoli.split(',')
                if len(vincoli) == 4:
                    send_constraint_to_server(vincoli[0], vincoli[1], vincoli[2], vincoli[3], topic, utente)

            case _:
                print('Scelta non valida')
        
        

#Funzione main
if __name__ == '__main__':
    main()
    