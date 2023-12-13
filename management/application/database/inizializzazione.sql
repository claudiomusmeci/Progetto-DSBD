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
    prezz_max float,
    prezzo_min float,
    variazione_percentuale float,
    PRIMARY KEY (email_utente, topic_utente),
    FOREIGN KEY (email_utente) REFERENCES Utente(email),
    FOREIGN KEY (topic_utente) REFERENCES Topic(nome)
);