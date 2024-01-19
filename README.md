# Progetto DSBD

## Configurazione
Una volta clonata la repository è necessario eseguire il seguente comando da terminale:

'''bash
docker-compose up -d
'''

Affinchè il sistema entri in funzione correttamente, è necessario attendere qualche minuto (circa 2-3).

Per interagire con il sistema è necessario inviare delle richieste HTTP all'endpoint <a href="http://localhost:10001/" target="_blank">'localhost:10001/'</a> del microservizio 'management'

In caso di eventuali errori, è necessario eseguire:

'''bash
docker compose down -v
'''
ed eseguire nuovamente il comando inziale di avvio.

### Info
Il sistema presenta anche un db manager PhpMyadmin per monitorare il database, è possibile accedervi attraverso <a href="http://localhost:8081" target="_blank">'localhost:8081'</a>
