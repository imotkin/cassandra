DROP KEYSPACE IF EXISTS "movie";
CREATE KEYSPACE movie WITH replication = {'class': 'SimpleStrategy', 'replication_factor': '1'}  AND durable_writes = true;

CREATE TYPE movie.address (
    city text,
    street text,
    postal_code int,
    house text,
    building int
);

CREATE TABLE movie.cinemas (
    cinema_id uuid PRIMARY KEY,
    address address,
    halls smallint,
    name text
) WITH additional_write_policy = '99p'
    AND bloom_filter_fp_chance = 0.01
    AND caching = {'keys': 'ALL', 'rows_per_partition': 'NONE'}
    AND comment = ''
    AND compaction = {'class': 'org.apache.cassandra.db.compaction.SizeTieredCompactionStrategy', 'max_threshold': '32', 'min_threshold': '4'}
    AND compression = {'chunk_length_in_kb': '16', 'class': 'org.apache.cassandra.io.compress.LZ4Compressor'}
    AND crc_check_chance = 1.0
    AND default_time_to_live = 0
    AND gc_grace_seconds = 864000
    AND max_index_interval = 2048
    AND memtable_flush_period_in_ms = 0
    AND min_index_interval = 128
    AND read_repair = 'BLOCKING'
    AND speculative_retry = '99p';

CREATE TABLE movie.cinemas_by_movie (
    movie_id uuid,
    name text,
    address address,
    cinema_id uuid,
    PRIMARY KEY (movie_id, name)
) WITH CLUSTERING ORDER BY (name ASC)
    AND additional_write_policy = '99p'
    AND bloom_filter_fp_chance = 0.01
    AND caching = {'keys': 'ALL', 'rows_per_partition': 'NONE'}
    AND comment = ''
    AND compaction = {'class': 'org.apache.cassandra.db.compaction.SizeTieredCompactionStrategy', 'max_threshold': '32', 'min_threshold': '4'}
    AND compression = {'chunk_length_in_kb': '16', 'class': 'org.apache.cassandra.io.compress.LZ4Compressor'}
    AND crc_check_chance = 1.0
    AND default_time_to_live = 0
    AND gc_grace_seconds = 864000
    AND max_index_interval = 2048
    AND memtable_flush_period_in_ms = 0
    AND min_index_interval = 128
    AND read_repair = 'BLOCKING'
    AND speculative_retry = '99p';

CREATE TABLE movie.movies (
    movie_id uuid PRIMARY KEY,
    duration duration,
    genre text,
    release_date date,
    score float,
    title text
) WITH additional_write_policy = '99p'
    AND bloom_filter_fp_chance = 0.01
    AND caching = {'keys': 'ALL', 'rows_per_partition': 'NONE'}
    AND comment = ''
    AND compaction = {'class': 'org.apache.cassandra.db.compaction.SizeTieredCompactionStrategy', 'max_threshold': '32', 'min_threshold': '4'}
    AND compression = {'chunk_length_in_kb': '16', 'class': 'org.apache.cassandra.io.compress.LZ4Compressor'}
    AND crc_check_chance = 1.0
    AND default_time_to_live = 0
    AND gc_grace_seconds = 864000
    AND max_index_interval = 2048
    AND memtable_flush_period_in_ms = 0
    AND min_index_interval = 128
    AND read_repair = 'BLOCKING'
    AND speculative_retry = '99p';

CREATE TABLE movie.movies_by_cinema (
    cinema_id uuid,
    title text,
    date date,
    duration duration,
    genre text,
    movie_id uuid,
    PRIMARY KEY (cinema_id, title, date)
) WITH CLUSTERING ORDER BY (title ASC, date DESC)
    AND additional_write_policy = '99p'
    AND bloom_filter_fp_chance = 0.01
    AND caching = {'keys': 'ALL', 'rows_per_partition': 'NONE'}
    AND comment = ''
    AND compaction = {'class': 'org.apache.cassandra.db.compaction.SizeTieredCompactionStrategy', 'max_threshold': '32', 'min_threshold': '4'}
    AND compression = {'chunk_length_in_kb': '16', 'class': 'org.apache.cassandra.io.compress.LZ4Compressor'}
    AND crc_check_chance = 1.0
    AND default_time_to_live = 0
    AND gc_grace_seconds = 864000
    AND max_index_interval = 2048
    AND memtable_flush_period_in_ms = 0
    AND min_index_interval = 128
    AND read_repair = 'BLOCKING'
    AND speculative_retry = '99p';

CREATE TABLE movie.movies_by_date (
    date date,
    title text,
    duration duration,
    genre text,
    movie_id uuid,
    PRIMARY KEY (date, title)
) WITH CLUSTERING ORDER BY (title ASC)
    AND additional_write_policy = '99p'
    AND bloom_filter_fp_chance = 0.01
    AND caching = {'keys': 'ALL', 'rows_per_partition': 'NONE'}
    AND comment = ''
    AND compaction = {'class': 'org.apache.cassandra.db.compaction.SizeTieredCompactionStrategy', 'max_threshold': '32', 'min_threshold': '4'}
    AND compression = {'chunk_length_in_kb': '16', 'class': 'org.apache.cassandra.io.compress.LZ4Compressor'}
    AND crc_check_chance = 1.0
    AND default_time_to_live = 0
    AND gc_grace_seconds = 864000
    AND max_index_interval = 2048
    AND memtable_flush_period_in_ms = 0
    AND min_index_interval = 128
    AND read_repair = 'BLOCKING'
    AND speculative_retry = '99p';

CREATE TABLE movie.movies_by_genre (
    genre text,
    title text,
    duration duration,
    movie_id uuid,
    PRIMARY KEY (genre, title)
) WITH CLUSTERING ORDER BY (title ASC)
    AND additional_write_policy = '99p'
    AND bloom_filter_fp_chance = 0.01
    AND caching = {'keys': 'ALL', 'rows_per_partition': 'NONE'}
    AND comment = ''
    AND compaction = {'class': 'org.apache.cassandra.db.compaction.SizeTieredCompactionStrategy', 'max_threshold': '32', 'min_threshold': '4'}
    AND compression = {'chunk_length_in_kb': '16', 'class': 'org.apache.cassandra.io.compress.LZ4Compressor'}
    AND crc_check_chance = 1.0
    AND default_time_to_live = 0
    AND gc_grace_seconds = 864000
    AND max_index_interval = 2048
    AND memtable_flush_period_in_ms = 0
    AND min_index_interval = 128
    AND read_repair = 'BLOCKING'
    AND speculative_retry = '99p';

CREATE TABLE movie.orders_by_session (
    session_id uuid,
    order_id uuid,
    date timestamp,
    price float,
    status text,
    PRIMARY KEY (session_id, order_id, date)
) WITH CLUSTERING ORDER BY (order_id ASC, date DESC)
    AND additional_write_policy = '99p'
    AND bloom_filter_fp_chance = 0.01
    AND caching = {'keys': 'ALL', 'rows_per_partition': 'NONE'}
    AND comment = ''
    AND compaction = {'class': 'org.apache.cassandra.db.compaction.SizeTieredCompactionStrategy', 'max_threshold': '32', 'min_threshold': '4'}
    AND compression = {'chunk_length_in_kb': '16', 'class': 'org.apache.cassandra.io.compress.LZ4Compressor'}
    AND crc_check_chance = 1.0
    AND default_time_to_live = 0
    AND gc_grace_seconds = 864000
    AND max_index_interval = 2048
    AND memtable_flush_period_in_ms = 0
    AND min_index_interval = 128
    AND read_repair = 'BLOCKING'
    AND speculative_retry = '99p';

CREATE TABLE movie.sessions (
    session_id uuid PRIMARY KEY,
    available_seats smallint,
    format text,
    hall smallint,
    price float,
    time time
) WITH additional_write_policy = '99p'
    AND bloom_filter_fp_chance = 0.01
    AND caching = {'keys': 'ALL', 'rows_per_partition': 'NONE'}
    AND comment = ''
    AND compaction = {'class': 'org.apache.cassandra.db.compaction.SizeTieredCompactionStrategy', 'max_threshold': '32', 'min_threshold': '4'}
    AND compression = {'chunk_length_in_kb': '16', 'class': 'org.apache.cassandra.io.compress.LZ4Compressor'}
    AND crc_check_chance = 1.0
    AND default_time_to_live = 0
    AND gc_grace_seconds = 864000
    AND max_index_interval = 2048
    AND memtable_flush_period_in_ms = 0
    AND min_index_interval = 128
    AND read_repair = 'BLOCKING'
    AND speculative_retry = '99p';

CREATE TABLE movie.sessions_by_movie (
    movie_id uuid,
    time time,
    hall smallint,
    price float,
    session_id uuid,
    PRIMARY KEY (movie_id, time)
) WITH CLUSTERING ORDER BY (time ASC)
    AND additional_write_policy = '99p'
    AND bloom_filter_fp_chance = 0.01
    AND caching = {'keys': 'ALL', 'rows_per_partition': 'NONE'}
    AND comment = ''
    AND compaction = {'class': 'org.apache.cassandra.db.compaction.SizeTieredCompactionStrategy', 'max_threshold': '32', 'min_threshold': '4'}
    AND compression = {'chunk_length_in_kb': '16', 'class': 'org.apache.cassandra.io.compress.LZ4Compressor'}
    AND crc_check_chance = 1.0
    AND default_time_to_live = 0
    AND gc_grace_seconds = 864000
    AND max_index_interval = 2048
    AND memtable_flush_period_in_ms = 0
    AND min_index_interval = 128
    AND read_repair = 'BLOCKING'
    AND speculative_retry = '99p';
INSERT INTO "movie"."cinemas" ("cinema_id", "address", "halls", "name") VALUES (221402f3-0f08-4b91-b36d-7d4cf99e70e3, {city: 'Москва', street: 'Пр-кт Вернадского', postal_code: 0, house: 'string', building: 0}, 12, 'KARO 2');
INSERT INTO "movie"."cinemas_by_movie" ("movie_id", "name", "address", "cinema_id") VALUES (ca15c3ec-a7ec-421a-9f36-ddde25de358b, 'КАРО 1', {city: 'Пермь', street: 'Пр-кт Ленина', postal_code: 123123, house: '123', building: 12}, 221402f3-0f08-4b91-b36d-7d4cf99e70e3);
INSERT INTO "movie"."movies" ("movie_id", "duration", "genre", "release_date", "score", "title") VALUES (ca15c3ec-a7ec-421a-9f36-ddde25de358b, 0mo0d8040000000000ns, 'sport', 2147499461, 8.0, 'Легенда №17');
INSERT INTO "movie"."movies" ("movie_id", "duration", "genre", "release_date", "score", "title") VALUES (75e1da89-a6ab-488a-b8a0-8f5be093be2f, 0mo0d11520000000000ns, 'criminal', 2147492554, 10.0, 'Криминальное чтиво');
INSERT INTO "movie"."movies_by_genre" ("genre", "title", "duration", "movie_id") VALUES ('criminal', 'Криминальное чтиво', 0mo0d11520000000000ns, 75e1da89-a6ab-488a-b8a0-8f5be093be2f);
INSERT INTO "movie"."movies_by_genre" ("genre", "title", "duration", "movie_id") VALUES ('sport', 'Легенда №17', 0mo0d8040000000000ns, ca15c3ec-a7ec-421a-9f36-ddde25de358b);
INSERT INTO "movie"."orders_by_session" ("session_id", "order_id", "date", "price", "status") VALUES (b3687303-1a9a-4acd-8c6e-573340b28354, 76b9a1f3-b44e-4ee0-8bba-bc0bb807f663, 1732830544992, 12345.0, 'READY');
INSERT INTO "movie"."sessions" ("session_id", "available_seats", "format", "hall", "price", "time") VALUES (f44a57ee-f30c-4cc2-a808-5bbd4fdffb86, 123, '2D', 2, 1234.0, '00:28:21.196591549');
INSERT INTO "movie"."sessions" ("session_id", "available_seats", "format", "hall", "price", "time") VALUES (b3687303-1a9a-4acd-8c6e-573340b28354, 123, '2D', 2, 1234.0, '00:28:52.818991549');
INSERT INTO cinemas_by_movie (movie_id, cinema_id, name, address) VALUES (75e1da89-a6ab-488a-b8a0-8f5be093be2f, 221402f3-0f08-4b91-b36d-7d4cf99e70e3, 'Киномакс', {city: 'Москва', street: 'Пр-кт Вернадского', postal_code: 0, house: 'string', building: 0});
INSERT INTO cinemas_by_movie (movie_id, cinema_id, name, address) VALUES (ca15c3ec-a7ec-421a-9f36-ddde25de358b, 221402f3-0f08-4b91-b36d-7d4cf99e70e3, 'Киномакс', {city: 'Москва', street: 'Пр-кт Вернадского', postal_code: 0, house: 'string', building: 0});
INSERT INTO movies_by_cinema (cinema_id, movie_id, title, date, genre, duration) VALUES (221402f3-0f08-4b91-b36d-7d4cf99e70e3, ca15c3ec-a7ec-421a-9f36-ddde25de358b, 'Легенда №17', 2147499461, 'sport', 0mo0d8040000000000ns);
INSERT INTO movies_by_cinema (cinema_id, movie_id, title, date, genre, duration) VALUES (221402f3-0f08-4b91-b36d-7d4cf99e70e3, 75e1da89-a6ab-488a-b8a0-8f5be093be2f, 'Криминальное чтиво', 2147492554, 'criminal', 0mo0d11520000000000ns);