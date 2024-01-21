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

    def aggiorna_sla(self, nome_metrica, valore_desiderato, valore_minimo, valore_massimo) :
        db = self.connect()
        if db is None:
            return False
        cursor = db.cursor()
        try :
            #Verifico l'esistenza della metrica scelta
            cursor.execute("SELECT * FROM sla_metrics WHERE metric_name = %s", (nome_metrica,))
            metrica_exists = cursor.fetchone()
            if metrica_exists:
                    print(f'Aggiorno la metrica {nome_metrica}')
                    cursor.execute("UPDATE sla_metrics SET desired_value = %s, range_low = %s, range_high = %s WHERE metric_name = %s;", (valore_desiderato, valore_minimo, valore_massimo, nome_metrica))
            else:
                print(f'Aggiungo la metrica {nome_metrica}')
                cursor.execute("INSERT INTO sla_metrics (metric_name, desired_value, range_low, range_high) VALUES (%s, %s, %s, %s);",
                                       (nome_metrica, valore_desiderato, valore_minimo, valore_massimo))
            db.commit()
            return True
        except Error as e :
            print("Errore nell'aggiunta della metrica per SLA ", e)
            return False
        finally:
            cursor.close()
            db.close()

    def elimina_sla(self, nome_metrica) :
        db = self.connect()
        if db is None:
            return False
        cursor = db.cursor()
        try :
            #Verifico l'esistenza della metrica scelta
            cursor.execute("SELECT * FROM sla_metrics WHERE metric_name = %s", (nome_metrica,))
            metrica_exists = cursor.fetchone()
            if metrica_exists:
                    print(f'rimuovo la metrica {nome_metrica}')
                    cursor.execute("DELETE FROM sla_metrics WHERE metric_name = %s;", (nome_metrica))
                    db.commit()
            return True
        except Error as e :
            print("Errore nella rimozione della metrica per SLA ", e)
            return False
        finally:
            cursor.close()
            db.close()
    
    