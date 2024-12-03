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
); -- WITH CLUSTERING ORDER BY (movie_id);

CREATE TABLE IF NOT EXISTS movies_by_date (
    date     DATE,
    movie_id UUID,
    title    TEXT,
    genre    TEXT,
    duration DURATION,
    PRIMARY KEY (date, movie_id)
); -- WITH CLUSTERING ORDER BY (movie_id);

CREATE TABLE IF NOT EXISTS movies_by_genre (
    genre    TEXT,
    movie_id UUID,
    title    TEXT,
    duration DURATION,
    PRIMARY KEY (genre, movie_id)
); -- WITH CLUSTERING ORDER BY (movie_id);

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
); -- WITH CLUSTERING ORDER BY (cinema_id);

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
); -- WITH CLUSTERING ORDER BY (session_id);

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


INSERT INTO "movie"."cinemas" ("cinema_id", "address", "halls", "name") VALUES (221402f3-0f08-4b91-b36d-7d4cf99e70e3, {city: 'Москва', street: 'Пр-кт Вернадского', postal_code: 0, house: 'string', building: 0}, 12, 'KARO 2');
INSERT INTO "movie"."cinemas_by_movie" ("movie_id", "name", "address", "cinema_id") VALUES (ca15c3ec-a7ec-421a-9f36-ddde25de358b, 'КАРО 1', {city: 'Пермь', street: 'Пр-кт Ленина', postal_code: 123123, house: '123', building: 12}, 221402f3-0f08-4b91-b36d-7d4cf99e70e3);
INSERT INTO "movie"."movies" ("movie_id", "duration", "genre", "release_date", "score", "title") VALUES (ca15c3ec-a7ec-421a-9f36-ddde25de358b, 0mo0d8040000000000ns, 'sport', 2147499461, 8.0, 'Легенда №17');
INSERT INTO "movie"."movies" ("movie_id", "duration", "genre", "release_date", "score", "title") VALUES (75e1da89-a6ab-488a-b8a0-8f5be093be2f, 0mo0d11520000000000ns, 'criminal', 2147492554, 10.0, 'Криминальное чтиво');
INSERT INTO "movie"."movies_by_genre" ("genre", "title", "duration", "movie_id") VALUES ('criminal', 'Криминальное чтиво', 0mo0d11520000000000ns, 75e1da89-a6ab-488a-b8a0-8f5be093be2f);
INSERT INTO "movie"."movies_by_genre" ("genre", "title", "duration", "movie_id") VALUES ('sport', 'Легенда №17', 0mo0d8040000000000ns, ca15c3ec-a7ec-421a-9f36-ddde25de358b);
INSERT INTO "movie"."orders_by_session" ("session_id", "order_id", "date", "price", "status") VALUES (b3687303-1a9a-4acd-8c6e-573340b28354, 76b9a1f3-b44e-4ee0-8bba-bc0bb807f663, 1732830544992, 12345.0, 'READY');
INSERT INTO "movie"."sessions" ("session_id", "available_seats", "format", "hall", "price", "time") VALUES (f44a57ee-f30c-4cc2-a808-5bbd4fdffb86, 123, '2D', 2, 1234.0, '00:28:21.196591549');
INSERT INTO "movie"."sessions" ("session_id", "available_seats", "format", "hall", "price", "time") VALUES (b3687303-1a9a-4acd-8c6e-573340b28354, 123, '2D', 2, 1234.0, '00:28:52.818991549');
INSERT INTO "movie"."cinemas_by_movie" (movie_id, cinema_id, name, address) VALUES (75e1da89-a6ab-488a-b8a0-8f5be093be2f, 221402f3-0f08-4b91-b36d-7d4cf99e70e3, 'Киномакс', {city: 'Москва', street: 'Пр-кт Вернадского', postal_code: 0, house: 'string', building: 0});
INSERT INTO "movie"."cinemas_by_movie" (movie_id, cinema_id, name, address) VALUES (ca15c3ec-a7ec-421a-9f36-ddde25de358b, 221402f3-0f08-4b91-b36d-7d4cf99e70e3, 'Киномакс', {city: 'Москва', street: 'Пр-кт Вернадского', postal_code: 0, house: 'string', building: 0});
INSERT INTO "movie"."movies_by_cinema" (cinema_id, movie_id, title, date, genre, duration) VALUES (221402f3-0f08-4b91-b36d-7d4cf99e70e3, ca15c3ec-a7ec-421a-9f36-ddde25de358b, 'Легенда №17', 2147499461, 'sport', 0mo0d8040000000000ns);
INSERT INTO "movie"."movies_by_cinema" (cinema_id, movie_id, title, date, genre, duration) VALUES (221402f3-0f08-4b91-b36d-7d4cf99e70e3, 75e1da89-a6ab-488a-b8a0-8f5be093be2f, 'Криминальное чтиво', 2147492554, 'criminal', 0mo0d11520000000000ns);

INSERT INTO "ticket"."orders" ("order_id", "cinema_id", "date", "price", "status", "user_id") VALUES (76b9a1f3-b44e-4ee0-8bba-bc0bb807f663, 221402f3-0f08-4b91-b36d-7d4cf99e70e3, 1732830544992, 12345.0, 'READY', ebf08275-68b4-4572-9239-d662eba9c645);
INSERT INTO "ticket"."users" ("user_id", "email", "name", "password", "phone") VALUES (ebf08275-68b4-4572-9239-d662eba9c645, 'johndoe@mail.com', 'John Doe', 'secret', '+123456789');
INSERT INTO "ticket"."tickets_by_user" (user_id, ticket_id, date, hall, price, seat) VALUES (ebf08275-68b4-4572-9239-d662eba9c645, c4ad1b51-78e9-4c4d-ac7d-6007fcc6294e, '2024-12-03T19:31:21.685Z', 15, 1250, 13);
INSERT INTO "ticket"."tickets_by_order" (order_id, ticket_id, date, hall, price, seat) VALUES (76b9a1f3-b44e-4ee0-8bba-bc0bb807f663, c4ad1b51-78e9-4c4d-ac7d-6007fcc6294e, '2024-12-03T19:31:21.685Z', 15, 1250, 13);


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