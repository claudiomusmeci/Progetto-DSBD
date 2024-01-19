from Database import DatabaseManager
from Client import *
from flask import Flask, request, jsonify
from kafka import KafkaConsumer
from threading import Thread
import json
import time
import os

app = Flask(__name__)
database = DatabaseManager()
topic_kafka = [os.environ['KAFKA_TOPIC']]

def istruzioni_API():
    endpoints = {
        "aggiungi_utente": {
            "url": "/aggiungi_utente",
            "method": "POST",
            "description": "Aggiunge un utente al database."
        },
        "aggiungi_vincoli": {
            "url": "/aggiungi_vincoli",
            "method": "POST",
            "description": "Aggiunge vincoli per un utente e un topic specifico."
        }
    }
    return endpoints


@app.route('/')
def index():
    endpoints = istruzioni_API()
    return jsonify(endpoints)

@app.route('/aggiungi_utente', methods=['POST'])
def aggiungi_utente():
    data = request.get_json()
    
    mail = data.get('mail')
    topic = data.get('topic')
    nome = data.get('nome')
    cognome = data.get('cognome')
    telefono = data.get('telefono')

    esito = database.inserisci_subscriber(mail, topic, nome, cognome, telefono)
    if esito == True:
        return jsonify({"message": f"L'utente {mail} è stato aggiunto al topic {topic}"})
    else:
        return jsonify({"message": f"L'utente {mail} è già sottoscritto o il topic {topic} non esiste"})

@app.route('/aggiungi_vincoli', methods=['POST'])
def aggiungi_vincoli():
    data = request.get_json()

    utente = data.get('utente')
    topic = data.get('topic')
    prezzo = data.get('prezzo')
    variazione_percentuale = data.get('variazione_percentuale')
    max_24h = data.get('max_24h')
    min_24h = data.get('min_24h')

    esito = database.inserisci_vincoli(prezzo, variazione_percentuale, max_24h, min_24h, utente, topic)
    if esito:
        return jsonify({"message": f"Vincoli aggiunti per l'utente {utente} nel topic {topic}"})
    else:
        return jsonify({"message": f"L'utente {utente} non è sottoscritto o il topic {topic} non esiste"})


def kafka_consumer_thread():
    consumer = KafkaConsumer(
            group_id="gruppo",
            bootstrap_servers=[os.environ['KAFKA_BROKER']],
            value_deserializer=lambda x: json.loads(x.decode('ascii'))
        )
    consumer.subscribe(topic_kafka)
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
            if utenti_email:
                for singolo_utente_email in utenti_email:
                    utente_email = singolo_utente_email[0]
                    print(f"Violazione del vincolo per l'utente {utente_email} nel topic {topic_nome}!")
                    #Avviso il notifier tramite gRPC
                    send_subscriber_to_server(utente_email, topic_nome)
           
        #sleep_time = int(os.environ['INTERVAL_TIME_SECONDS'])
        #time.sleep(sleep_time)
        
    except KeyboardInterrupt:
        pass

    finally:
        #Chiudi il consumatore
        consumer.close()

def flask_app_thread():
    app.run(debug=True, host='0.0.0.0', port=10001, use_reloader=False)

#Funzione main
if __name__ == '__main__':
    kafka_consumer = Thread(target=kafka_consumer_thread)
    flask_thread = Thread (target=flask_app_thread)
    kafka_consumer.start()
    flask_thread.start()

    kafka_consumer.join()
    flask_thread.join()
    