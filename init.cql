CREATE KEYSPACE IF NOT EXISTS movie WITH REPLICATION = {'class': 'SimpleStrategy', 'replication_factor': 1};

USE movie;

CREATE TABLE IF NOT EXISTS movies (
    movie_id     UUID PRIMARY KEY,
    title        TEXT,
    duration     DURATION,
    release_date DATE,
    genre        TEXT,
    score        FLOAT
);

CREATE TABLE IF NOT EXISTS movies_by_cinema (
    cinema_id UUID,
    movie_id  UUID,
    title     TEXT,
    date      DATE,
    genre     TEXT,
    duration  DURATION,
    PRIMARY KEY (cinema_id, movie_id)
) WITH CLUSTERING ORDER BY (movie_id);

CREATE TABLE IF NOT EXISTS movies_by_date (
    date     DATE,
    movie_id UUID,
    title    TEXT,
    genre    TEXT,
    duration DURATION,
    PRIMARY KEY (date, movie_id)
) WITH CLUSTERING ORDER BY (movie_id);

CREATE TABLE IF NOT EXISTS movies_by_genre (
    genre    TEXT,
    movie_id UUID,
    title    TEXT,
    duration DURATION,
    PRIMARY KEY (genre, movie_id)
) WITH CLUSTERING ORDER BY (movie_id);

CREATE TYPE IF NOT EXISTS address (
    city        TEXT,
    street      TEXT,
    postal_code INT,
    house       TEXT,
    building    INT
);

CREATE TABLE IF NOT EXISTS cinemas_by_movie (
    movie_id  UUID,
    cinema_id UUID,
    name      TEXT,
    address   ADDRESS,
    PRIMARY KEY (movie_id, cinema_id)
) WITH CLUSTERING ORDER BY (cinema_id);

CREATE TABLE IF NOT EXISTS cinemas (
    cinema_id UUID PRIMARY KEY,
    name      TEXT,
    address   ADDRESS,
    halls     SMALLINT
);

CREATE TABLE IF NOT EXISTS sessions_by_movie (
    movie_id   UUID,
    session_id UUID,
    time       TIME,
    hall       SMALLINT,
    price      FLOAT,
    PRIMARY KEY (movie_id, session_id)
) WITH CLUSTERING ORDER BY (session_id);

CREATE TABLE IF NOT EXISTS sessions (
    session_id      UUID PRIMARY KEY,
    available_seats SMALLINT,
    time            TIME,
    price           FLOAT,
    hall            SMALLINT,
    format          TEXT
);

CREATE TABLE IF NOT EXISTS orders_by_session (
    session_id UUID,
    order_id   UUID,
    date       TIMESTAMP,
    status     TEXT,
    price      FLOAT,
    PRIMARY KEY (session_id, order_id, date)
) WITH CLUSTERING ORDER BY (order_id ASC, date DESC);

CREATE KEYSPACE IF NOT EXISTS ticket WITH REPLICATION = {'class': 'SimpleStrategy', 'replication_factor': 1};

USE ticket;

CREATE TABLE IF NOT EXISTS tickets (
    ticket_id UUID PRIMARY KEY,
    price     FLOAT,
    hall      SMALLINT,
    seat      SMALLINT,
    date      TIMESTAMP
);

CREATE TABLE IF NOT EXISTS orders (
    order_id  UUID PRIMARY KEY,
    user_id   UUID,
    cinema_id UUID,
    date      TIMESTAMP,
    status    TEXT,
    price     FLOAT
);

CREATE TABLE IF NOT EXISTS tickets_by_order (
    order_id  UUID,
    date      TIMESTAMP,
    ticket_id UUID,
    price     FLOAT,
    hall      SMALLINT,
    seat      SMALLINT,
    PRIMARY KEY (order_id, date, ticket_id)
) WITH CLUSTERING ORDER BY (date DESC, ticket_id ASC);

CREATE TABLE IF NOT EXISTS users (
    user_id  UUID PRIMARY KEY,
    name     TEXT,
    password TEXT,
    email    TEXT,
    phone    TEXT
);

CREATE TABLE IF NOT EXISTS tickets_by_user (
    user_id   UUID,
    date      TIMESTAMP,
    ticket_id UUID,
    price     FLOAT,
    hall      SMALLINT,
    seat      SMALLINT,
    PRIMARY KEY (user_id, date, ticket_id)
) WITH CLUSTERING ORDER BY (date DESC, ticket_id ASC);


INSERT INTO ticket.users (user_id, name, password, email, phone)
VALUES (UUID(), 'John Doe', 'secret', 'johndoe@mail.com', '+123456789');

INSERT INTO movie.sessions (session_id, available_seats, time, price, hall, format)
VALUES (UUID(), 120, '14:30:00', 350, 1, 'IMAX');

INSERT INTO movie.cinemas (cinema_id, halls, name, address) 
VALUES (UUID(), 3, 'Киномакс', {city: 'Москва', street: 'пр-т Вернадского', building: 73});

INSERT INTO movie.movies (movie_id, title, duration, release_date, genre, score) 
VALUES (UUID(), 'Стражи Галактики', null, null, 'Action', 7.5);

INSERT INTO movie.movies (movie_id, title, duration, release_date, genre, score) 
VALUES (UUID(), 'Убить Билла', null, null, 'Thriller', 8);

INSERT INTO movie.movies_by_cinema (cinema_id, movie_id, title, duration, date, genre) 
VALUES (UUID(), 2, 'Убить Билла', null, '2008-01-01', 'Thriller');

INSERT INTO movie.movies_by_cinema (cinema_id, movie_id, title, duration, date, genre) 
VALUES (UUID(), 1, 'Стражи Галактики', null, '2014-01-01', 'Action');