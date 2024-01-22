CREATE DATABASE IF NOT EXISTS sottoscrizioni;
CREATE DATABASE IF NOT EXISTS metriche;

USE sottoscrizioni;
/* Creazione della tabella Utente */
CREATE TABLE IF NOT EXISTS Utente (
    nome VARCHAR(255),
    cognome VARCHAR(255),
    email VARCHAR(255) 	PRIMARY KEY,
    telefono VARCHAR(255)
);
/* Creazione della tabella Topic */
CREATE TABLE IF NOT EXISTS Topic (
    nome VARCHAR(255) PRIMARY KEY
);
/* Creazione della tabella Sottoscrizione */
CREATE TABLE IF NOT EXISTS Sottoscrizione (
    email_utente VARCHAR(255),
    topic_utente VARCHAR(255),
    PRIMARY KEY (email_utente, topic_utente),
    FOREIGN KEY (email_utente) REFERENCES Utente(email),
    FOREIGN KEY (topic_utente) REFERENCES Topic(nome)
);
/* Creazione della tabella Vincoli */
CREATE TABLE IF NOT EXISTS Vincoli (
    email_utente VARCHAR(255),
    topic_utente VARCHAR(255),
    prezzo float,
    prezzo_max float,
    prezzo_min float,
    variazione_percentuale float,
    PRIMARY KEY (email_utente, topic_utente),
    FOREIGN KEY (email_utente) REFERENCES Utente(email),
    FOREIGN KEY (topic_utente) REFERENCES Topic(nome)
);
/*Mock data*/
-- Inserimento degli Utenti
INSERT INTO Utente (nome, cognome, email, telefono) VALUES ('Utente1', 'Cognome1', 'utente1@example.com', '1234567890');
INSERT INTO Utente (nome, cognome, email, telefono) VALUES ('Utente2', 'Cognome2', 'utente2@example.com', '9876543210');
INSERT INTO Utente (nome, cognome, email, telefono) VALUES ('Utente3', 'Cognome3', 'utente3@example.com', '5555555555');

-- Inserimento dei Topic
INSERT INTO Topic (nome) VALUES ('Bitcoin');
INSERT INTO Topic (nome) VALUES ('Ethereum');
INSERT INTO Topic (nome) VALUES ('Tether');

-- Inserimento delle Sottoscrizioni
INSERT INTO Sottoscrizione (email_utente, topic_utente) VALUES ('utente1@example.com', 'Bitcoin');
INSERT INTO Sottoscrizione (email_utente, topic_utente) VALUES ('utente1@example.com', 'Ethereum');
INSERT INTO Sottoscrizione (email_utente, topic_utente) VALUES ('utente2@example.com', 'Ethereum');
INSERT INTO Sottoscrizione (email_utente, topic_utente) VALUES ('utente2@example.com', 'Bitcoin');
INSERT INTO Sottoscrizione (email_utente, topic_utente) VALUES ('utente3@example.com', 'Bitcoin');

-- Inserimento dei Vincoli
INSERT INTO Vincoli (email_utente, topic_utente, prezzo, prezzo_max, prezzo_min, variazione_percentuale)
VALUES ('utente1@example.com', 'Bitcoin', 50000, 55000, 48000, 5.0);

INSERT INTO Vincoli (email_utente, topic_utente, prezzo, prezzo_max, prezzo_min, variazione_percentuale)
VALUES ('utente1@example.com', 'Ethereum', 3000, 3300, 2800, 4.5);

INSERT INTO Vincoli (email_utente, topic_utente, prezzo, prezzo_max, prezzo_min, variazione_percentuale)
VALUES ('utente2@example.com', 'Ethereum', 3100, 3400, 2900, 3.0);

INSERT INTO Vincoli (email_utente, topic_utente, prezzo, prezzo_max, prezzo_min, variazione_percentuale)
VALUES ('utente2@example.com', 'Bitcoin', 48000, 52000, 45000, 6.0);

INSERT INTO Vincoli (email_utente, topic_utente, prezzo, prezzo_max, prezzo_min, variazione_percentuale)
VALUES ('utente3@example.com', 'Bitcoin', 49000, 53000, 46000, 5.5);

USE metriche;

/* Creazione della tabella per memorizzare le metriche SLA */
CREATE TABLE IF NOT EXISTS Metrica (
    metric_name VARCHAR(50) PRIMARY KEY
);

/* Creazione della tabella per memorizzare le metriche SLA */
CREATE TABLE IF NOT EXISTS sla_metrics (
    metric_name VARCHAR(50) PRIMARY KEY,
    desired_value FLOAT,
    range_low FLOAT,
    range_high FLOAT,
    FOREIGN KEY (metric_name) REFERENCES Metrica(metric_name)
);
 
/*Creazione della tabella per memorizzare le informazioni sulle violazioni*/
CREATE TABLE IF NOT EXISTS sla_violations (
    metric_name VARCHAR(50),
    violation_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (metric_name, violation_timestamp),
    FOREIGN KEY (metric_name) REFERENCES sla_metrics(metric_name)
    
);

INSERT INTO Metrica (metric_name) VALUES ('container_cpu_load_average_10s');
INSERT INTO Metrica (metric_name) VALUES ('container_fs_io_time_seconds_total');
INSERT INTO Metrica (metric_name) VALUES ('container_memory_usage_bytes');
INSERT INTO Metrica (metric_name) VALUES ('container_memory_failcnt');
INSERT INTO Metrica (metric_name) VALUES ('container_network_receive_errors_total');
INSERT INTO Metrica (metric_name) VALUES ('container_network_transmit_errors_total');
INSERT INTO Metrica (metric_name) VALUES ('container_start_time_seconds');

INSERT INTO sla_metrics (metric_name, desired_value, range_low, range_high) VALUES ('container_cpu_load_average_10s', 15, 0.0, 35.0);
INSERT INTO sla_metrics (metric_name, desired_value, range_low, range_high) VALUES ('container_fs_io_time_seconds_total', 15, 0.0, 100.0);
INSERT INTO sla_metrics (metric_name, desired_value, range_low, range_high) VALUES ('container_memory_usage_bytes', 15, 0.0, 520000000);
INSERT INTO sla_metrics (metric_name, desired_value, range_low, range_high) VALUES ('container_network_receive_errors_total', 2, 0.0, 10);
INSERT INTO sla_metrics (metric_name, desired_value, range_low, range_high) VALUES ('container_network_transmit_errors_total', 2, 0.0, 10);
