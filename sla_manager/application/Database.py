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
                
            except:
                print('Errore durante la connessione: host MySQL non disponibile')
                print('Ritento la connessione')
                sleep(5)
        return database

    #Interazioni con database
    def getMetriche(self) :
        db = self.connect()
        if db is None:
            return False
        cursor = db.cursor()
        try :
            cursor.execute("SELECT  * FROM sla_metrics")
            metriche=cursor.fetchall()
            return metriche
        except Error as e :
            print("Errore nel recupero delle metriche ", e)
            return False
        finally:
            cursor.close()
            db.close()

    
    