# Progetto DSBD

## Configurazione
Una volta clonata la repository è necessario eseguire il seguente comando da terminale:

```bash
docker-compose up -d && docker-compose exec -it management python main.py
```

Affinchè il sistema entri in funzione correttamente, è necessario attendere qualche minuto (circa 2-3), fino a quando all'interno del terminale verrà caricato il menù testuale relativo al microservizio management.

In caso di eventuali errori, è necessario eseguire:

```bash
docker compose down -v
```
ed eseguire nuovamente il comando inziale di avvio.

### Info
Il sistema presenta anche un db manager phpMyAdmin per monitorare il database, è possibile accedervi attraverso 'localhost:8080' <a href="http://localhost:8080" target="_blank">Apri</a>
