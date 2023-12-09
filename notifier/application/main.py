from kafka import KafkaConsumer
import os
import json
import threading

print('Consumatore')

subscriptions = {}

def gestisci_messaggio(user, message):
    # Elabora il messaggio
    data = json.loads(message.value)
    print('{} Nuovi dati dal topic {} Kafka: {}'.format(user, message.topic, data))

def sottoscrivi_utenti(user, topics):
    group_id = f"CONSUMER_{user}"
    consumer = KafkaConsumer(
        group_id=group_id,
        bootstrap_servers=[os.environ['KAFKA_BROKER']],
        value_deserializer=lambda x: json.loads(x.decode('ascii'))
    )
    consumer.subscribe(topics)
    subscriptions[user] = consumer

def consume_message(user):
    consumer = subscriptions[user]
    for message in consumer:
        gestisci_messaggio(user, message)

# Sottoscrizioni degli utenti
sottoscrivi_utenti('Utente1', ['Bitcoin', 'Ethereum'])
sottoscrivi_utenti('Utente2', ['Ethereum', 'Bitcoin'])
sottoscrivi_utenti('Utente3', ['Bitcoin'])

# Avvio dei thread per ciascun utente
threads = []
for user_id, user_topics in subscriptions.items():
    thread = threading.Thread(target=consume_message, args=(user_id,))
    threads.append(thread)
    thread.start()

# Attendi che tutti i thread terminino (puoi gestire questo in modo più avanzato)
for thread in threads:
    thread.join()

print("Tutti i thread sono terminati")
