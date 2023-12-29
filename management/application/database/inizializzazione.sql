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
