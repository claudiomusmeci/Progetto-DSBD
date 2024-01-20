import mysql.connector
from mysql.connector import Error
from time import sleep
import os

class DatabaseManager():
    #Connessione al database
    def connect(self):
        while True:
            try:
                print('Provo a connettermi a MySQL')
                database = mysql.connector.connect(
                    host=os.environ['MYSQL_HOST'],
                    user="root",
                    password="password",
                    database="metriche"
                )
                if database.is_connected():
                    print('Connection established')
                    break
                sleep(5)
            except:
                print('Errore durante la connessione: host MySQL non disponibile')
                print('Ritento la connessione')
        return database

    #Interazioni con database
    def inserisci_subscriber(self, email_utente, topic, nome, cognome, telefono) :
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
                    # Verifica l'esistenza dell'utente
                    cursor.execute("SELECT * FROM Utente WHERE email = %s", (email_utente,))
                    user_exists = cursor.fetchone()
                    if user_exists is None:
                        cursor.execute("INSERT INTO Utente (nome, cognome, email, telefono) VALUES (%s,%s,%s,%s)", (nome, cognome, email_utente, telefono))
                    # Inserisci l'entry nella tabella Sottoscrizione
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

    
    