from Database import DatabaseManager
from Client import *

def main():
    database = DatabaseManager()
    while True:
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
                    print(f"L'utente {mail} è già sottoscritto o il topic {topic} non esiste")
                
            case 2:
                utente = input("Inserisci la email dell'utente ")
                topic = input("Inserisci un topic: [Bitcoin, Ethereum, Tether] ")
                str_vincoli = input("Inserisci i vincoli separati da una virgola: prezzo, variazione percentuale, max_24h, min_24h ")
                vincoli = str_vincoli.split(',')
                if len(vincoli) == 4:
                    esito = database.inserisci_vincoli(vincoli[0], vincoli[1], vincoli[2], vincoli[3], utente, topic)
                    if esito == True:
                        send_constraint_to_server(vincoli[0], vincoli[1], vincoli[2], vincoli[3], topic, utente)
                    else:
                        print(f"L'utente {utente} non è sottoscritto o il topic {topic} non esiste")

            case _:
                print('Scelta non valida')
        

#Funzione main
if __name__ == '__main__':
    main()
    