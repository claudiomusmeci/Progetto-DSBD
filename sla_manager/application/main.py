from datetime import datetime, timedelta
from prometheus_api_client import PrometheusConnect
from flask import Flask, request, jsonify
from Database import DatabaseManager
from traceback import format_exc
from scipy.stats import norm
import pandas as pd
from pmdarima import auto_arima


app = Flask(__name__)
database = DatabaseManager()
prometheus_url = 'http://prometheus:9090'
metric_list=['container_cpu_load_average_10s',
                  'container_fs_io_time_seconds_total', 'container_memory_usage_bytes',
                  'container_memory_failcnt', 'container_network_receive_errors_total',
                  'container_network_transmit_errors_total', 'container_start_time_seconds']


@app.route('/')
def index():
    return jsonify('')

@app.route('/metriche_attuali_sla', methods=['GET'])
def metriche_attuali_prometheus():
    lista_metriche = database.getMetriche()
    response = {}
    if lista_metriche:
        prometheus = PrometheusConnect(url=prometheus_url, disable_ssl=True)
        for metrica in lista_metriche:
            nome_metrica=str(metrica[0])
            response_metrica=[]
            try:
                result = prometheus.custom_query(nome_metrica)
                for elemento in result:
                    if(elemento['metric'].get('container_label_com_docker_compose_service')):
                        response_metrica.append({'nome_servizio': elemento['metric'].get('container_label_com_docker_compose_service'), 'valore attuale':elemento['value'][1]})
            except Exception as e:
                print(f"Errore nella metrica '{nome_metrica}': {format_exc()}")
                continue
            response[nome_metrica] = response_metrica
    return jsonify(response)

@app.route('/valori_desiderati_sla', methods=['GET'])
def valori_desiderati_sla():
    lista_metriche = database.getMetriche()
    response = []
    if lista_metriche:
        for metrica in lista_metriche:
            response.append({metrica[0]:metrica[1]})
    return jsonify(response)

@app.route('/aggiorna_metrica_sla', methods=['POST'])
def aggiorna_metrica_sla():
    data = request.get_json()
    
    nome_metrica = data.get('metrica')
    valore_desiderato = data.get('valore_desiderato')
    valore_minimo = data.get('valore_minimo')
    valore_massimo = data.get('valore_massimo')

    esito = database.aggiorna_sla(nome_metrica, valore_desiderato, valore_minimo, valore_massimo)
    if esito:
        response = 'Metrica aggiunta o aggiornata in SLA'
    else:
        response = 'Errore nella aggiunta della metrica in SLA'
    
    return response

@app.route('/elimina_metrica_sla', methods=['POST'])
def elimina_metrica_sla():
    data = request.get_json()
    nome_metrica = data.get('metrica')
    esito = database.elimina_sla(nome_metrica)
    if esito:
        response = 'Metrica eliminata da SLA'
    else:
        response = 'Errore nella rimozione della metrica in SLA'
    
    return response

@app.route('/violazioni_metriche_sla', methods=['GET'])
def violazioni_metriche_sla():
    lista_metriche = database.getMetriche()
    response = {}
    if lista_metriche:
        prometheus = PrometheusConnect(url=prometheus_url, disable_ssl=True)
        for metrica in lista_metriche:
            nome_metrica=str(metrica[0])
            valore_minimo_metrica = float(metrica[2])
            valore_massimo_metrica = float(metrica[3])
            response_metrica=[]
            try:
                result = prometheus.custom_query(nome_metrica)
                for elemento in result:
                    if(elemento['metric'].get('container_label_com_docker_compose_service')):
                        valore = float(elemento['value'][1])
                        if(valore>=valore_massimo_metrica):
                            response_metrica.append({nome_metrica:'SLA violato', 'nome_servizio': elemento['metric'].get('container_label_com_docker_compose_service')})
                        else:
                            response_metrica.append({nome_metrica:'SLA non violato', 'nome_servizio': elemento['metric'].get('container_label_com_docker_compose_service')})
            except Exception as e:
                print(f"Errore nella metrica '{nome_metrica}': {format_exc()}")
                continue
            response[nome_metrica] = response_metrica
    return jsonify(response)

@app.route('/violazioni_tempo_sla', methods=['GET'])
def violazioni_tempo_sla():
    #data = request.json
    lista_metriche = database.getMetriche()
    response = {}
    data=5
    if lista_metriche:
        prometheus = PrometheusConnect(url=prometheus_url, disable_ssl=True)
        for metrica in lista_metriche:
            nome_metrica=str(metrica[0])
            valore_minimo_metrica = float(metrica[2])
            valore_massimo_metrica = (metrica[3])
            end=datetime.utcnow()
            start=end-timedelta(hours=data)
            response_metrica=[]
            try:
                query = f'count_over_time({metrica[0]} > {metrica[3]})'
                result = prometheus.custom_query_range(query, start_time=start, end_time=end, step='1h')
                response_metrica.append({'metrica': nome_metrica, 'violazioni' : result})
                
            except Exception as e:
                print(f"Errore nella metrica '{nome_metrica}': {format_exc()}")
                continue
            response[nome_metrica] = response_metrica
    return jsonify(response)

@app.route('/probabilita_variazione_metriche', methods=['POST']) #Sostituire il numero di minuti con metodo POST
def probabilita_variazione_metriche():
    lista_metriche = database.getMetriche()
    data = request.get_json()
    minuti = int(data['minuti'])
    response = {}
    if lista_metriche:
        prometheus = PrometheusConnect(url=prometheus_url, disable_ssl=True)
        for metrica in lista_metriche:
            nome_metrica = str(metrica[0])
            valore_massimo_metrica = float(metrica[3])
            response_metrica = []
            try:
                #Recupero da prometheus i dati relativi a valore medio e deviazione standard
                result = prometheus.custom_query('avg'+'('+nome_metrica+')')
                mean_value = float(result[0]["value"][1])
                result = prometheus.custom_query('stddev'+'('+nome_metrica+')')
                std_dev = float(result[0]["value"][1])
                
                # Calcola la probabilità di variazione nei prossimi x minuti
                if(std_dev != 0):
                    z_score = (valore_massimo_metrica - mean_value) / std_dev
                else:
                    z_score = 0
                probability = 1 - norm.cdf(z_score)
                probability_next_interval = 1 - (1 - probability) ** minuti
                
                response_metrica.append({
                    'nome_metrica': nome_metrica,
                    'probabilita_variazione': probability_next_interval
                })
                
            except Exception as e:
                print(f"Errore nella metrica '{nome_metrica}': {format_exc()}")
                continue
            
            response[nome_metrica] = response_metrica
            
    return jsonify(response)


@app.route('/probabilita_violazione_arima', methods=['POST'])
def probabilita_violazione_arima():
    lista_metriche = database.getMetriche()
    response = {}
    data = request.get_json()
    minuti = int(data['minuti'])
    periodi_totali = (minuti * 4) #Il 4 deriva da 60 secondi/15 scrapying time di prometheus
    if lista_metriche:
        prometheus = PrometheusConnect(url=prometheus_url, disable_ssl=True)
        for metrica in lista_metriche:
            nome_metrica = str(metrica[0])
            valore_massimo_metrica = float(metrica[3])
            response_metrica = []
            try:
                #Recupero da prometheus i dati relativi a valore medio e deviazione standard
                result = prometheus.custom_query(nome_metrica+'[30m]')
                for elemento in result:
                    #return jsonify(elemento['values'])
                    if(elemento['metric'].get('container_label_com_docker_compose_service')):
                        timestamps = [item[0] for item in elemento['values']]
                        values = [item[1] for item in elemento['values']]
                    
                        datetime_objects = pd.to_datetime(timestamps, unit = 's')
                        numeric_values = pd.to_numeric(values)

                
                        df = pd.DataFrame({'timestamp': datetime_objects, 'value': numeric_values})
                        df.set_index('timestamp', inplace=True)

                        #Addestramento del modello ARIMA automatico
                        model = auto_arima(df['value'], seasonal=False, suppress_warnings=True)

                        #Previsioni per i prossimi n periodi
                        forecast, conf_int = model.predict(n_periods=periodi_totali, return_conf_int=True)
                    
                        #Calcolo la deviazione standard delle previsioni
                        std_dev_forecast = forecast.std()
                        mean_value_forecast = forecast.mean()
                        '''
                        #Calcolo lo z-score
                        z_value = (valore_massimo_metrica - mean_value_forecast) / std_dev_forecast if std_dev_forecast else 0.0
                        #Calcolo la probabilità di violazione
                        probability = 1 - norm.cdf(z_value)
                        #Calcolo la probabilità di violazione nei prossimi n periodi
                        probability_next_interval = 1 - (1 - probability) ** periodi_totali
                        response_metrica.append({
                        'nome_servizio': elemento['metric'].get('container_label_com_docker_compose_service'),
                        'probabilita_violazione': probability_next_interval * 100,
                        'valore_medio':mean_value_forecast,
                        'deviazione_standard':std_dev_forecast,
                        'valore_soglia_metrica':valore_massimo_metrica,
                        'z_score':z_value
                        }) 
                        '''
                        #Metodo alternativo calcolo probabilità di errore
                        violations = sum(forecast > valore_massimo_metrica)
                        print("Valori previsti: ", forecast.values)
                        print("Violazioni : ",  violations)
                        probability_next_interval = violations / len(forecast)
                        response_metrica.append({
                        'nome_servizio': elemento['metric'].get('container_label_com_docker_compose_service'),
                        'probabilita_violazione': probability_next_interval * 100,
                        'valore_soglia_metrica':valore_massimo_metrica,
                        'nome_metrica:': nome_metrica
                        }) 
                return jsonify(response_metrica) #Calcolato solo per una metrica per non appesantire l'esecuzione
                
            except Exception as e:
                print(f"Errore nella metrica '{nome_metrica}': {format_exc()}")
                continue
            
            response[nome_metrica] = response_metrica
            
    return jsonify(response)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3000)