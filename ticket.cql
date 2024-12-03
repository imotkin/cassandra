DROP KEYSPACE IF EXISTS "ticket";
CREATE KEYSPACE ticket WITH replication = {'class': 'SimpleStrategy', 'replication_factor': '1'}  AND durable_writes = true;

CREATE TABLE ticket.orders (
    order_id uuid PRIMARY KEY,
    cinema_id uuid,
    date timestamp,
    price float,
    status text,
    user_id uuid
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

CREATE TABLE ticket.tickets (
    ticket_id uuid PRIMARY KEY,
    date timestamp,
    hall smallint,
    price float,
    seat smallint
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

CREATE TABLE ticket.tickets_by_order (
    order_id uuid,
    date timestamp,
    ticket_id uuid,
    hall smallint,
    price float,
    seat smallint,
    PRIMARY KEY (order_id, date, ticket_id)
) WITH CLUSTERING ORDER BY (date DESC, ticket_id ASC)
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

CREATE TABLE ticket.tickets_by_user (
    user_id uuid,
    date timestamp,
    ticket_id uuid,
    hall smallint,
    price float,
    seat smallint,
    PRIMARY KEY (user_id, date, ticket_id)
) WITH CLUSTERING ORDER BY (date DESC, ticket_id ASC)
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

CREATE TABLE ticket.users (
    user_id uuid PRIMARY KEY,
    email text,
    name text,
    password text,
    phone text
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
INSERT INTO "ticket"."orders" ("order_id", "cinema_id", "date", "price", "status", "user_id") VALUES (76b9a1f3-b44e-4ee0-8bba-bc0bb807f663, 221402f3-0f08-4b91-b36d-7d4cf99e70e3, 1732830544992, 12345.0, 'READY', ebf08275-68b4-4572-9239-d662eba9c645);
INSERT INTO "ticket"."users" ("user_id", "email", "name", "password", "phone") VALUES (ebf08275-68b4-4572-9239-d662eba9c645, 'johndoe@mail.com', 'John Doe', 'secret', '+123456789');
INSERT INTO tickets_by_user (user_id, ticket_id, date, hall, price, seat) VALUES (ebf08275-68b4-4572-9239-d662eba9c645, c4ad1b51-78e9-4c4d-ac7d-6007fcc6294e, '2024-12-03T19:31:21.685Z', 15, 1250, 13);
INSERT INTO tickets_by_order (order_id, ticket_id, date, hall, price, seat) VALUES (76b9a1f3-b44e-4ee0-8bba-bc0bb807f663, c4ad1b51-78e9-4c4d-ac7d-6007fcc6294e, '2024-12-03T19:31:21.685Z', 15, 1250, 13);
