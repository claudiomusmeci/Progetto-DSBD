# Progetto DSBD

## Configurazione
Una volta clonata la repository è necessario eseguire il seguente comando da terminale:

```bash
docker-compose up -d
```

Affinchè il sistema entri in funzione correttamente, è necessario attendere qualche minuto (circa 2-3).

Per interagire con il sistema (microservizio management) è necessario accedervi attraverso <a href="http://localhost:10001" target="_blank">'localhost:10001'</a>

In caso di eventuali errori, è necessario eseguire:

```bash
docker compose down -v
```
ed eseguire nuovamente il comando inziale di avvio.

### Info
Il sistema presenta anche un db manager phpMyAdmin per monitorare il database, è possibile accedervi attraverso <a href="http://localhost:8080" target="_blank">'localhost:8080'</a>
