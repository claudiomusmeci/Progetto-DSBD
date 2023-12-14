import mysql.connector
from mysql.connector import Error
from time import sleep
import os
import ast

class DatabaseManager():
    #Mi connetto al database
    def connect(self):
        while True:
            try:
                sleep(5)
                print('Trying to connect to MySQL Host...')
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
                print('Error during connection : MySQL Host not available')
                print('Retry sooner...')
        return database

    #Interazioni con database
    def inserisci_subscriber(self, email_utente, topic) :
        db = self.connect()
        if db is None:
            return False
        cursor = db.cursor()
        try :
            # Verifica che il topic esista
            cursor.execute("SELECT * FROM Topic WHERE nome = %s", (topic,))
            topic_exists = cursor.fetchone()
            if topic_exists:
                # Verifica se la sottoscrizione esiste già
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
                        new_user = input("Inserisci i valori separati da una virgola: nome,cognome,email,telefono")
                        dati_user = new_user.split(',')
                        cursor.execute("INSERT INTO Utente (nome, cognome, email, telefono) VALUES (%s,%s,%s,%s)", (dati_user[0],dati_user[1],dati_user[2],dati_user[3]))
            
                    #Inserisco l'entry nella tabella Sottoscrizione
                    cursor.execute("INSERT INTO Sottoscrizione (email_utente, topic_utente) VALUES (%s, %s)", (email_utente, topic))
                    db.commit()
                    print(f"Sottoscrizione aggiunta per {email_utente} al topic {topic}")
                    return True
            else:
                print(f"Il topic '{topic}' non esiste.")

        except Error as e :
            print("Errore nell'aggiunta della sottoscrizione")
            return False
        finally:
            cursor.close()
            db.close()