import mysql.connector
from mysql.connector import Error
from time import sleep
import os

class DatabaseManager():
    #Connessione al database
    def connect(self):
        while True:
            try:
                sleep(5)
                print('Provo a connettermi a MySQL')
                database = mysql.connector.connect(
                    host=os.environ['MYSQL_HOST'],
                    user="root",
                    password="password",
                    database="database"
                )
                if database.is_connected():
                    print('Connection established')
                    break
            except:
                print('Errore durante la connessione: host MySQL non disponibile')
                print('Ritento la connessione')
        return database

    #Interazioni con database
    def inserisci_subscriber(self, email_utente, topic) :
        db = self.connect()
        if db is None:
            return False
        cursor = db.cursor()
        try :
            #Verifico che il topic esista
            cursor.execute("SELECT * FROM Topic WHERE nome = %s", (topic,))
            topic_exists = cursor.fetchone()
            if topic_exists:
                #Verifico se la sottoscrizione esiste già
                cursor.execute("SELECT * FROM Sottoscrizione WHERE email_utente = %s AND topic_utente = %s", (email_utente, topic))
                subscription_exists = cursor.fetchone()
                if subscription_exists:
                    print("L'utente è già sottoscritto al topic")
                    return False
                else:
                    #Verifico l'esistenza dell'utente
                    cursor.execute("SELECT * FROM Utente WHERE email = %s", (email_utente,))
                    user_exists = cursor.fetchone()
                    if user_exists is None:
                        new_user = input("Inserisci i valori separati da una virgola: nome,cognome,telefono ")
                        dati_user = new_user.split(',')
                        cursor.execute("INSERT INTO Utente (nome, cognome, email, telefono) VALUES (%s,%s,%s,%s)", (dati_user[0],dati_user[1],email_utente,dati_user[2]))
                    #Inserisco l'entry nella tabella Sottoscrizione
                    cursor.execute("INSERT INTO Sottoscrizione (email_utente, topic_utente) VALUES (%s, %s)", (email_utente, topic))
                    db.commit()
                    print(f"Sottoscrizione aggiunta per {email_utente} al topic {topic}")
                    return True
            else:
                print(f"Il topic '{topic}' non esiste.")
        except Error as e :
            print("Errore nell'aggiunta della sottoscrizione ", e)
            return False
        finally:
            cursor.close()
            db.close()

    
    def inserisci_vincoli(self, prezzo, variazione_percentuale, max_24h, min_24h ,email_utente, topic) :
        db = self.connect()
        if db is None:
            return False
        cursor = db.cursor()
        try :
            #Verifico l'esistenza del topic
            cursor.execute("SELECT * FROM Topic WHERE nome = %s", (topic,))
            topic_exists = cursor.fetchone()
            if topic_exists:
                #Verifico la sottoscrizione di un utente ad un topic
                cursor.execute("SELECT * FROM Sottoscrizione WHERE email_utente = %s AND topic_utente = %s", (email_utente, topic))
                subscription_exists = cursor.fetchone()
                if subscription_exists is None:
                    print(f"L'utente {email_utente} non è sottoscritto al topic {topic}")
                    return False
                else:
                    #Verifico la presenza di vincoli già forniti in precedenza per quell'utente
                    cursor.execute("SELECT * FROM Vincoli WHERE email_utente = %s AND topic_utente = %s", (email_utente, topic))
                    constraint_exists = cursor.fetchone()
                    if constraint_exists is None:
                        cursor.execute("INSERT INTO Vincoli (email_utente, topic_utente, prezzo, prezzo_max, prezzo_min, variazione_percentuale) VALUES (%s, %s, %s, %s, %s, %s);",
                                       (email_utente, topic, prezzo, max_24h, min_24h, variazione_percentuale))
                    else:
                        cursor.execute("UPDATE Vincoli SET prezzo = %s, prezzo_max = %s, prezzo_min = %s, variazione_percentuale = %s WHERE email_utente = %s AND topic_utente = %s;", (prezzo, max_24h, min_24h, variazione_percentuale, email_utente, topic))
                    db.commit()
                    return True
            else:
                print(f"Il topic '{topic}' non esiste.")
        except Error as e :
            print("Errore nell'aggiunta dei vincoli ", e)
            return False
        finally:
            cursor.close()
            db.close()