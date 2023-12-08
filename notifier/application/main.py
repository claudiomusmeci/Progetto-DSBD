from kafka import KafkaConsumer
import os
import json

print('Consumatore')
# Configura i parametri del consumatore
consumer = KafkaConsumer(
    group_id="CONSUMER PROVA",
    bootstrap_servers=[os.environ['KAFKA_BROKER']],
    value_deserializer=lambda x: json.loads(x.decode('ascii'))
)
topic = os.environ['KAFKA_TOPIC']
consumer.subscribe(topic)
print('Sottoscritto')
try:
    for message in consumer:
        # Elabora il messaggio
        data = message.value
        print('Nuovi dati dal topic {} Kafka: {}'.format(topic ,data))

except KeyboardInterrupt:
    pass

finally:
    # Chiudi il consumatore
    consumer.close()