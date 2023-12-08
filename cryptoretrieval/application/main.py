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

#API da cui estrarre i dati
api_url = 'http://www.randomnumberapi.com/api/v1.0/random?min=100&max=1000&count=3'

#Topic Kafka
topic = os.environ['KAFKA_TOPIC']

try:
    while True:
        #Richiesta all'API per ottenere i dati
        response = requests.get(api_url)
        data = response.json()

        #Invia i dati al topic Kafka
        producer.send(topic, data)

        print('Dati inviati al topic {} Kafka: {}'.format(topic, data))
        sleep_time = int(os.environ['INTERVAL_TIME_SECONDS'])
        #Attendo 120 secondi
        time.sleep(sleep_time)

except KeyboardInterrupt:
    pass

finally:
    #Chiudo il producer
    producer.close()