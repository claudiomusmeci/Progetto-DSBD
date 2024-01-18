import json
from kafka import KafkaProducer
import requests
import time
import os

#Parametri del producer
producer = KafkaProducer(
    bootstrap_servers=[os.environ['KAFKA_BROKER']],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

#https://www.coingecko.com/api/documentation
#API da cui estrarre i dati
api_url = 'https://api.coingecko.com/api/v3/coins/markets?vs_currency=eur&order=market_cap_desc&per_page=3&page=1&sparkline=false&locale=en'
prezzo_precedente = {"Bitcoin": 0.0, "Ethereum": 0.0, "Tether": 0.0}
variazione_percentuale = 0.0
try:
    while True:
        #Attendo N secondi
        sleep_time = int(os.environ['INTERVAL_TIME_SECONDS'])
        time.sleep(sleep_time)
        #Richiesta all'API per ottenere i dati
        response = requests.get(api_url)
        data = response.json()
        #Processo i dati (Scraping)
        for elemento in data:
            prezzo = elemento["current_price"]
            topic = elemento["name"]
            if prezzo_precedente[topic] > 0:
                variazione_percentuale = (prezzo - prezzo_precedente[topic])/prezzo_precedente[topic] * 100
            nuovo_json_string = json.dumps({"nome": elemento["name"], "prezzo": elemento["current_price"], "max_24h": elemento["high_24h"], "min_24h": elemento["low_24h"], "variazione_percentuale": variazione_percentuale}, indent=2)
            #Pubblica i dati nel relativo topic Kafka
            producer.send(topic, nuovo_json_string)
            print('Dati inviati al topic {} Kafka: {}'.format(topic, nuovo_json_string))
            prezzo_precedente[topic] = prezzo
except KeyboardInterrupt:
    pass

finally:
    #Chiudo il producer
    producer.close()