from Database import DatabaseManager
from Client import *
from flask import Flask, render_template, request
from kafka import KafkaConsumer
from threading import Thread
import json
import time

app = Flask(__name__)
database = DatabaseManager()
topics=["Bitcoin", "Ethereum", "Tether"]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/aggiungi_utente', methods=['POST'])
def aggiungi_utente():
    mail = request.form['mail']
    topic = request.form['topic']
    nome = request.form['nome']
    cognome = request.form['cognome']
    telefono = request.form['telefono']

    esito = database.inserisci_subscriber(mail, topic, nome, cognome, telefono)
    if esito == True:
        return f"L'utente {mail} è stato aggiunto al topic {topic}"
    else:
        return f"L'utente {mail} è già sottoscritto o il topic {topic} non esiste"

@app.route('/aggiungi_vincoli', methods=['POST'])
def aggiungi_vincoli():
    utente = request.form['utente']
    topic = request.form['topic']
    prezzo = request.form['prezzo']
    variazione_percentuale = request.form['variazione_percentuale']
    max_24h = request.form['max_24h']
    min_24h = request.form['min_24h']   
    
    esito = database.inserisci_vincoli(prezzo, variazione_percentuale, max_24h, min_24h, utente, topic)
    if esito:
        return f"Vincoli aggiunti per l'utente {utente} nel topic {topic}"
    else:
        return f"L'utente {utente} non è sottoscritto o il topic {topic} non esiste"   


def kafka_consumer_thread():
    consumer = KafkaConsumer(
            group_id="gruppo",
            bootstrap_servers=[os.environ['KAFKA_BROKER']],
            value_deserializer=lambda x: json.loads(x.decode('ascii'))
        )
    consumer.subscribe(topics)
    try:
        for message in consumer:
            #Stampo a schermo il messaggio generato
            data = json.loads(message.value)
            print("Topic {}\n{}".format(message.topic, data))
            #Valuto i vincoli (per semplicità viene valutata solo la variazione percentuale, se quella ottenuta è minore allora avviso l'utente)
            topic_nome= message.topic
            variazione_percentuale = float(data['variazione_percentuale'])
            #Eseguo la query per ottenere l'email degli utenti associati al topic dalla tabella Vincoli
            utenti_email = database.check_vincoli(topic_nome, variazione_percentuale)
    
            for singolo_utente_email in utenti_email:
                utente_email = singolo_utente_email[0]
                print(f"Violazione del vincolo per l'utente {utente_email} nel topic {topic_nome}!")
                #Avviso il notifier tramite gRPC
                send_subscriber_to_server(utente_email, topic_nome)
            
        sleep_time = int(os.environ['INTERVAL_TIME_SECONDS'])
        time.sleep(sleep_time)
    except KeyboardInterrupt:
        pass

    finally:
        #Chiudi il consumatore
        consumer.close()
#Funzione main
if __name__ == '__main__':
    kafka_consumer1 = Thread(target=kafka_consumer_thread)
    kafka_consumer2 = Thread(target=kafka_consumer_thread)
    kafka_consumer1.start()
    kafka_consumer2.start()
    app.run(debug=True, host='0.0.0.0', port=10001)