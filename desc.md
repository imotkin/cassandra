~~INSERT:~~
    ~~movies -> movies_by_genre (Михаил)~~
    ~~orders -> orders_by_session (Михаил)~~
    ~~tickets -> tickets_by_order, ticket_by_user (Илья)~~
    ~~sessions (Илья)~~
UPDATE:
    ~~movies (title, duration, genre) -> movies_by_date, ..._by_genre, ..._by_cinema  (Михаил)~~
    ~~cinema (name, address) -> cinemas_by_movie (Илья)~~
    ~~tickets (price, seat, hall, date) -> tickets_by_user, tickets_by_order (Михаил)~~
~~DELETE~~:
    ~~tickets (ticket_id) -> tickets_by_order (ticket_id, order_id), tickets_by_user (ticket_id, user_id) (Илья)~~