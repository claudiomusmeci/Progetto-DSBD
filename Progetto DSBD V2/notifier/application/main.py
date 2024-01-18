import os
import sys
import grpc
from concurrent import futures
sys.path.append('./grpc')
import messaggi_pb2 as pb2
import messaggi_pb2_grpc as pb2_grpc
import smtplib

mittente = os.environ['MITTENTE']
password = os.environ['PASSWORD']

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

#Gestione server gRPC
class ClientManagementService(pb2_grpc.ClientManagementServicer):

    def SendNewSubscriber(self, request, context):
        #Implemento la logica per il metodo SendNewSubscriber
        print(f"Received new subscriber data from client\nUser: {request.user}, topic: {request.topic}")
        contenuto = (f"Utente {request.user}, violazione dei vincoli per il topic {request.topic}")
        #invia_mail(request.user, contenuto)
        response_message = f"Ho avvisato {request.user}"
        return pb2.ResponseData(message=response_message)

    def serve(self):
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        pb2_grpc.add_ClientManagementServicer_to_server(self, server)
        server.add_insecure_port('[::]:50051')
        print('Avvio il server, in ascolto nella porta 50051')
        server.start()
        server.wait_for_termination()

def main():
    print('Ascolto il client gRPC')
    grpc_server = ClientManagementService()
    grpc_server.serve()

#Avvio del main
if __name__ == '__main__':
    main()