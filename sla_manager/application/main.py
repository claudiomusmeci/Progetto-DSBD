from prometheus_api_client import PrometheusConnect
from flask import Flask, request, jsonify
from Database import DatabaseManager
import time
from traceback import format_exc

app = Flask(__name__)
database = DatabaseManager()
prometheus_url = 'http://prometheus:9090'
metric_list=['container_cpu_load_average_10s',
                  'container_fs_io_time_seconds_total', 'container_memory_usage_bytes',
                  'container_memory_failcnt', 'container_network_receive_errors_total',
                  'container_network_transmit_errors_total', 'container_start_time_seconds']

def istruzioni_API():
    endpoints = {
        "_metric_list" : metric_list,

        "aggiungi_metrica": {
            "url": "/aggiungi_metrica",
            "method": "POST",
            "description": "Aggiungi una metrica a SLA."
        },
        "rimuovi_metrica":  {
            "url": "/rimuovi_metrica",
            "method": "POST",
            "description": "Rimuovi una metrica a SLA."
        },
        "get_sla_status": {
            "url": "/get_sla_status",
            "method": "GET",
            "description": "Prende lo stato delle metriche SLA: valore corrente, valore desiderato, stato di violazione, numero di violazioni, e probabilità di violazione."
        },
        "get_metrica_attuale": {
            "url": "/{'nome_metrica'}",
            "method": "GET",
            "description": "Ritorna il valore della metrica scelta"
        }
    }
    return endpoints

@app.route('/')
def index():
    endpoints = istruzioni_API()
    return jsonify(endpoints)

@app.route('/<metrica>', methods=['GET'])
def metriche_prometheus(metrica):
    #Esempio di query (container_network_receive_errors_total{container_label_com_docker_compose_service='retrieval'})
    prometheus = PrometheusConnect(url=prometheus_url, disable_ssl=True)
    metrica = str(metrica)
    result=prometheus.custom_query(metrica)
    return jsonify(result)

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

"""
@app.route('/sla', methods=['POST'])
def create_or_update_sla():
    data = request.get_json()
    metric_name = data['nome_metrica']
    soglia_min = data['soglia_min']
    soglia_max = data['soglia_max']

    sla_metric = SLAMetric.query.filter_by(metric_name=metric_name).first()
    if sla_metric:
        sla_metric.threshold_min = threshold_min
        sla_metric.threshold_max = threshold_max
    else:
        new_sla_metric = SLAMetric(metric_name=metric_name, threshold_min=threshold_min, threshold_max=threshold_max)
        db.session.add(new_sla_metric)

    db.session.commit()
    return jsonify({'message': 'SLA updated successfully'}), 201




@app.route('/aggiungi_metrica', methods=['POST'])
def add_metric():
    data = request.get_json()
    metric_name = data.get('metric_name')

    # Aggiungi la metrica all'SLA
    sla_metrics[metric_name] = {
        'desired_value': data.get('desired_value'),
        'range_low': data.get('range_low'),
        'range_high': data.get('range_high')
    }

    return jsonify({"message": f"Metric {metric_name} aggiunta a SLA"}), 201

@app.route('/rimuovi_metrica', methods=['POST'])
def remove_metric():
    data = request.get_json()
    metric_name = data.get('metric_name')

    # Rimuovi la metrica dall'SLA
    if metric_name in sla_metrics:
        del sla_metrics[metric_name]
        return jsonify({"message": f"Metrica {metric_name} rimossa da SLA"}), 200
    else:
        return jsonify({"error": f"Metrica {metric_name} non trovata in SLA"}), 404

@app.route('/get_sla_status', methods=['GET'])
def get_sla_status():
    metric_name = request.args.get('metric_name')

    if metric_name not in sla_metrics:
        return jsonify({"error": "Metric not found in SLA"}), 404

    #logica per ottenere le informazioni richieste sull'SLA
    
    prom = PrometheusConnect(url=prometheus_url, disable_ssl=True)
    
    # Otteniamo il valore corrente della metrica di Prometheus
    query_result = prom.custom_query(query=f'{metric_name}', timestamp=int(time.time()))
    current_value = float(query_result['value'][1]) if query_result else None
    # Implementa la logica per ottenere il valore attuale della metrica "up"
    # Esempio di implementazione:
    #up_metric_query = prom.custom_query(query='up', timestamp=int(time.time()))
    #up_metric_value = float(up_metric_query['value'][1]) if up_metric_query else None

    # Otteniamo il valore desiderato e i range dalla definizione SLA
    sla_info = sla_metrics[metric_name]
    desired_value = sla_info['desired_value']
    range_low = sla_info['range_low']
    range_high = sla_info['range_high']

    # Calcolo dello stato di violazione
    violation = current_value < range_low or current_value > range_high

    # Implementiamo la logica per ottenere il numero di violazioni (ad esempio, controlla uno storico)
    # Nota: Qui il numero di violazioni è fisso, dovrai adattarlo alla tua logica effettiva
    violation_count = database.get_violation_count(metric_name)

    # Implementa la logica per calcolare la probabilità di violazione
    # Nota: Qui la probabilità di violazione è fissa, dovrai adattarla alla tua logica effettiva
    probability_of_violation = calculate_probability(violation_count)

    sla_info = {
        "metric_name": metric_name,
        "current_value": current_value,
        "desired_value": desired_value,
        "violation": violation,
        "violation_count": violation_count,
        "probability_of_violation": probability_of_violation
    }
    return jsonify(sla_info)

def calculate_probability(violation_count):
    # Implementa la tua logica per calcolare la probabilità di violazione
    # Questo è solo un esempio di implementazione
    if violation_count > 0:
        return 0.8
    else:
        return 0.2

        

"""
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3000)