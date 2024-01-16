from Database import DatabaseManager
from Client import *
from flask import Flask, render_template, request

app = Flask(__name__)
database = DatabaseManager()

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
        send_subscriber_to_server(mail, topic)
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
        send_constraint_to_server(prezzo, variazione_percentuale, max_24h, min_24h, topic, utente)
        return f"Vincoli aggiunti per l'utente {utente} nel topic {topic}"
    else:
        return f"L'utente {utente} non è sottoscritto o il topic {topic} non esiste"   

#Funzione main
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=10001)
    