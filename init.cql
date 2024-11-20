CREATE KEYSPACE movie WITH REPLICATION = {'class': 'SimpleStrategy', 'replication_factor': 1};

USE movie;

CREATE TABLE IF NOT EXISTS movies (
    movies       BIGINT PRIMARY KEY,
    title        TEXT,
    duration     DURATION,
    release_date DATE,
    genre        TEXT,
    score        FLOAT
);

CREATE TABLE IF NOT EXISTS movies_by_cinema (
    cinema_id INT,
    title     TEXT,
    date      DATE,
    movie_id  BIGINT,
    genre     TEXT,
    duration  DURATION,
    PRIMARY KEY (cinema_id, title, date)
) WITH CLUSTERING ORDER BY (title ASC, date DESC);

CREATE TABLE IF NOT EXISTS movies_by_date (
    date     DATE,
    title    TEXT,
    movie_id BIGINT,
    genre    TEXT,
    duration DURATION,
    PRIMARY KEY (date, title)
) WITH CLUSTERING ORDER BY (title ASC);

CREATE TABLE IF NOT EXISTS movies_by_genre (
    genre    TEXT,
    title    TEXT,
    movie_id BIGINT,
    duration DURATION,
    PRIMARY KEY (genre, title)
) WITH CLUSTERING ORDER BY (title ASC);

CREATE TYPE IF NOT EXISTS address (
    city        TEXT,
    street      TEXT,
    postal_code INT,
    house       TEXT,
    building    INT
);

CREATE TABLE IF NOT EXISTS cinemas_by_movie (
    movie_id  BIGINT,
    name      TEXT,
    cinema_id INT,
    address   ADDRESS,
    PRIMARY KEY (movie_id, name)
) WITH CLUSTERING ORDER BY (name ASC);

CREATE TABLE IF NOT EXISTS cinemas (
    cinema_id INT PRIMARY KEY,
    name      TEXT,
    address   ADDRESS,
    halls     SMALLINT
);

CREATE TABLE IF NOT EXISTS sessions_by_movie (
    movie_id   BIGINT,
    time       TIME,
    session_id INT,
    hall       SMALLINT,
    price      FLOAT,
    PRIMARY KEY (movie_id, time)
) WITH CLUSTERING ORDER BY (time ASC);

CREATE TABLE IF NOT EXISTS sessions (
    session_id      INT PRIMARY KEY,
    available_seats SMALLINT,
    time            TIME,
    price           FLOAT,
    hall            SMALLINT,
    format          TEXT
);

CREATE TABLE IF NOT EXISTS orders_by_session (
    session_id INT,
    order_id   INT,
    date       TIMESTAMP,
    status     TEXT,
    price      FLOAT,
    PRIMARY KEY (session_id, order_id, date)
) WITH CLUSTERING ORDER BY (order_id ASC, date DESC);

CREATE KEYSPACE IF NOT EXISTS ticket WITH REPLICATION = {'class': 'SimpleStrategy', 'replication_factor': 1};

USE ticket;

CREATE TABLE IF NOT EXISTS tickets (
    ticket_id BIGINT PRIMARY KEY,
    price     FLOAT,
    hall      SMALLINT,
    seat      SMALLINT,
    date      TIMESTAMP
);

CREATE TABLE IF NOT EXISTS orders (
    order_id INT PRIMARY KEY,
    user_id  INT,
    date     TIMESTAMP,
    status   TEXT,
    price    FLOAT
);

CREATE TABLE IF NOT EXISTS tickets_by_order (
    order_id  INT,
    date      TIMESTAMP,
    ticket_id BIGINT,
    price     FLOAT,
    hall      SMALLINT,
    seat      SMALLINT,
    PRIMARY KEY (order_id, date, ticket_id)
) WITH CLUSTERING ORDER BY (date DESC, ticket_id ASC);

CREATE TABLE IF NOT EXISTS users (
    user_id  INT PRIMARY KEY,
    name     TEXT,
    password TEXT,
    email    TEXT,
    phone    TEXT
);

CREATE TABLE IF NOT EXISTS tickets_by_user (
    user_id   INT,
    date      TIMESTAMP,
    ticket_id BIGINT,
    price     FLOAT,
    hall      SMALLINT,
    seat      SMALLINT,
    PRIMARY KEY (user_id, date, ticket_id)
) WITH CLUSTERING ORDER BY (date DESC, ticket_id ASC);


INSERT INTO ticket.users (user_id, name, password, email, phone)
VALUES (1, 'john doe', 'secret', 'johndoe@mail.com', '+123456789');

INSERT INTO movie.sessions (session_id, available_seats, time, price, hall, format)
VALUES (1, 120, '14:30:00', 350, 1, 'IMAX');

INSERT INTO movie.cinemas (cinema_id, halls, name, address) 
VALUES (1, 3, 'test', {city: 'Москва', street: 'пр-т Вернадского', building: 73});