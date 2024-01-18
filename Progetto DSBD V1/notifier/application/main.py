from Server import *

def main():
    #Sottoscrizioni di utenti di prova
    sottoscrivi_utenti('utente1@example.com', ['Bitcoin', 'Ethereum'], lista_thread)
    sottoscrivi_utenti('utente2@example.com', ['Ethereum', 'Bitcoin'], lista_thread)
    sottoscrivi_utenti('utente3@example.com', ['Bitcoin'], lista_thread)

    print('Ascolto il client gRPC')
    ClientManagementService.serve()

#Avvio del main
if __name__ == '__main__':
    subscriptions = {}
    lista_thread = []
    main()
    #Attendo che tutti i thread terminino (anche se non è previsto che essi terminino)
    for thread in lista_thread:
        thread.join()
        print("Tutti i thread sono terminati")