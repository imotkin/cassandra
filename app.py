from datetime import datetime
from fastapi import FastAPI
from database import Database

import schemas
import uuid

tags_metadata = [
    {
        "name": "movies",
        "description": ""
    },
    {
        "name": "cinemas",
        "description": ""
    },
    {
        "name": "sessions",
        "description": ""
    },
    {
        "name": "orders",
        "description": ""
    },
    {
        "name": "tickets",
        "description": ""
    },
    {
        "name": "users",
        "description": ""
    }
]


def run_migration(db: Database, filename: str):
    with open(filename, "r") as file:
        commands = file.read().split(";")

        for cmd in commands:
            cmd = cmd.strip()
            if cmd:
                try:
                    db.cluster.connect().execute(cmd)
                    print(f"Add table: {cmd}")
                except Exception as e:
                    print(f"Error: {cmd}\n{e}")


app = FastAPI(openapi_tags=tags_metadata)
db = Database(test=False)

# run_migration(db, "init.cql")

'''

UUIDs:
    users: ebf08275-68b4-4572-9239-d662eba9c645
    cinemas: 221402f3-0f08-4b91-b36d-7d4cf99e70e3
    movies: 75e1da89-a6ab-488a-b8a0-8f5be093be2f, ca15c3ec-a7ec-421a-9f36-ddde25de358b
    orders: 76b9a1f3-b44e-4ee0-8bba-bc0bb807f663
    sessions: f44a57ee-f30c-4cc2-a808-5bbd4fdffb86, b3687303-1a9a-4acd-8c6e-573340b28354
    tickets: c4ad1b51-78e9-4c4d-ac7d-6007fcc6294e, cfcd0aeb-69c4-48e3-82e9-91a822a6cb3c

TEST:
    http://127.0.0.1:8000/orders?session_id=b3687303-1a9a-4acd-8c6e-573340b28354&user_id=ebf08275-68b4-4572-9239-d662eba9c645&cinema_id=221402f3-0f08-4b91-b36d-7d4cf99e70e3

'''


def convert_address(obj):
    if obj is None:
        return obj

    return {
        "city": obj.city,
        "street": obj.street,
        "postal_code": obj.postal_code,
        "house": obj.house,
        "building": obj.building,
    }


def unconvert_address(obj):
    obj_dict = dict(obj)
    result = []

    for key, value in obj_dict.items():
        if type(value) is int:
            result.append(f"{key}: {value}")
        else:
            result.append(f"{key}: '{value}'")

    return "{" + ", ".join(result) + "}"


@app.get("/hosts")
def get_hosts():
    return db.hosts


@app.get("/cinemas/{cinema_id}", summary="Получение информации о кинотеатре", tags=["cinemas"])
def get_cinema_by_id(cinema_id: uuid.UUID):
    select_query = "SELECT * FROM cinemas WHERE cinema_id = %s"
    rows = db.movie.execute(select_query, [cinema_id])
    return [dict(row) for row in rows]


@app.get("/cinemas/movies/{movie_id}", summary="Получение кинотеатров для фильма", tags=["cinemas"])
def get_cinemas_by_movie(movie_id: uuid.UUID):
    select_query = "SELECT * FROM cinemas_by_movie WHERE movie_id = %s"
    rows = db.movie.execute(select_query, [movie_id])
    return [dict(row) for row in rows]


@app.get("/movies/{movie_id}", summary="Получение информации о фильме", tags=["movies"])
def get_movie_by_id(movie_id: uuid.UUID):
    select_query = "SELECT * FROM movies WHERE movie_id = %s"
    rows = db.movie.execute(select_query, [movie_id])
    return [dict(row) for row in rows]


@app.get(
    "/movies/cinemas/{cinema_id}/",
    summary="Получение списка фильмов для определенного кинотеатра",
    tags=["movies"]
)
def get_movies_by_cinema(cinema_id: uuid.UUID):
    select_query = "SELECT * FROM movies_by_cinema WHERE cinema_id = %s"
    rows = db.movie.execute(select_query, [cinema_id])
    return [dict(row) for row in rows]


@app.get("/movies/dates/{date}/", summary="Получение списка фильмов для определенной даты", tags=["movies"])
def get_movies_by_date(date: str):
    select_query = "SELECT * FROM movies_by_date WHERE date = %s"
    rows = db.movie.execute(select_query, [date])
    return [dict(row) for row in rows]


@app.get("/movies/genres/{genre}/", summary="Получение списка фильмов для определенного жанра", tags=["movies"])
def get_movies_by_genre(genre: str):
    select_query = "SELECT * FROM movies_by_genre WHERE genre = %s"
    rows = db.movie.execute(select_query, [genre])
    return [dict(row) for row in rows]


@app.get("/sessions/{session_id}", summary="Получение информации о сеансе", tags=["sessions"])
def get_session_by_id(session_id: uuid.UUID):
    select_query = "SELECT * FROM sessions WHERE session_id = %s"
    rows = db.movie.execute(select_query, session_id)
    return [dict(row) for row in rows]


@app.get("/sessions/movies/{movie_id}", summary="Получение сеансов по фильму", tags=["sessions"])
def get_session_by_movie(movie_id: uuid.UUID):
    select_query = "SELECT * FROM sessions_by_movie WHERE movie_id = %s"
    rows = db.movie.execute(select_query, [movie_id])
    return [dict(row) for row in rows]


@app.get("/users/{user_id}", summary="Получение информации о пользователе", tags=["users"])
def get_user_by_id(user_id: uuid.UUID):
    select_query = "SELECT * FROM users WHERE user_id = %s"
    rows = db.ticket.execute(select_query, [user_id])
    return [dict(row) for row in rows]


@app.get("/tickets/{ticket_id}", summary="Получение информации о билете", tags=["tickets"])
def get_ticket_by_id(ticket_id: uuid.UUID):
    select_query = "SELECT * FROM tickets WHERE ticket_id = %s"
    rows = db.ticket.execute(select_query, [ticket_id])
    return [dict(row) for row in rows]


@app.get("/tickets/orders/{order_id}", summary="Получение билетов для определенного заказа", tags=["tickets"])
def get_ticket_by_order(order_id: uuid.UUID):
    select_query = "SELECT * FROM tickets_by_order WHERE order_id = %s;"
    rows = db.ticket.execute(select_query, [order_id])
    return [dict(row) for row in rows]


@app.get(
    "/tickets/users/{user_id}", summary="Получение билетов для определенного пользователя",
    tags=["tickets"]
)
def get_ticket_by_user(user_id: uuid.UUID):
    select_query = "SELECT * FROM tickets_by_user WHERE user_id = %s"
    rows = db.ticket.execute(select_query, [user_id])
    return [dict(row) for row in rows]


@app.get("/orders/{order_id}", summary="Получение информации о заказе", tags=["orders"])
def get_order_by_id(order_id: uuid.UUID):
    select_query = "SELECT * FROM orders WHERE order_id = %s"
    rows = db.ticket.execute(select_query, [order_id])
    return [dict(row) for row in rows]


@app.get("/orders/{session_id}", summary="Получение заказов для определенного сеанса", tags=["orders"])
def get_orders_by_session(session_id: uuid.UUID):
    select_query = "SELECT * FROM orders_by_session WHERE session_id = %s"
    rows = db.movie.execute(select_query, [session_id])
    return [dict(row) for row in rows]


@app.post("/cinemas", summary="Добавление нового кинотеатра", tags=["cinemas"])
def create_cinema(cinema: schemas.Cinema):
    cinema_id = uuid.uuid4()
    query = (
        "INSERT INTO cinemas (cinema_id, halls, name, address) "
        f"VALUES (%s, %s, %s, {unconvert_address(cinema.address)})"
    )
    db.movie.execute(query, [cinema_id, cinema.halls, cinema.name])
    return cinema.toJSON({"id": cinema_id})


@app.post("/sessions", summary="Добавлеие нового сеанса", tags=["sessions"])
def create_session(session: schemas.Session):
    session_id = uuid.uuid4()
    query = (
        "INSERT INTO sessions (session_id, available_seats, time, price, hall, format)"
        "VALUES (%s, %s, %s, %s, %s, %s)"
    )
    db.movie.execute(query, [session_id, session.available_seats, session.time, session.price, session.hall, session.format])

    return session.toJSON({"id": session_id})


@app.post("/movies", summary="Добавление нового фильма", tags=["movies"])
def create_movie(movie: schemas.Movie):
    movie_id = uuid.uuid4()
    movie_query = (
        "INSERT INTO movies (movie_id, title, duration, release_date, genre, score) "
        f"VALUES (%s, %s, {movie.duration}, %s, %s, %s);"
    )

    genre_movie_query = (
        "INSERT INTO movies_by_genre (genre, title, movie_id, duration) "
        f"VALUES (%s, %s, %s, {movie.duration});"
    )

    db.movie.execute(movie_query, [movie_id, movie.title,
                     movie.release_date, movie.genre, movie.score])
    db.movie.execute(genre_movie_query, [movie.genre, movie.title, movie_id])

    return movie.toJSON({"id": movie_id})


@app.post("/orders", summary="Добавление нового заказа", tags=["orders"])
def create_order(order: schemas.Order, session_id: uuid.UUID, user_id: uuid.UUID, cinema_id: uuid.UUID):
    order_id = uuid.uuid4()
    order_date = datetime.now()
    
    orders_query = (
        "INSERT INTO orders (order_id, user_id, cinema_id, date, status, price)"
        "VALUES (%s, %s, %s, %s, %s, %s)"
    )

    orders_by_session_query = (
        "INSERT INTO orders_by_session (session_id, order_id, date, status, price)"
        "VALUES (%s, %s, %s, %s, %s)"
    )
    
    db.ticket.execute(orders_query, [order_id, user_id, cinema_id, order_date, order.status, order.price])
    db.movie.execute(orders_by_session_query, [session_id, order_id, order_date, order.status, order.price])

    return order.toJSON({"date": order_date, "id": order_id})


@app.post("/tickets", summary="Добавление нового билета", tags=["tickets"])
def create_ticket(ticket: schemas.Ticket, order_id: uuid.UUID, user_id: uuid.UUID):
    ticket_id = uuid.uuid4()
    
    tickets_query = (
        "INSERT INTO tickets (ticket_id, price, hall, seat, date)"
        "VALUES (%s, %s, %s, %s, %s)"
    )
    
    tickets_order_query = (
        "INSERT INTO tickets_by_order (order_id, date, ticket_id, price, hall, seat)"
        "VALUES (%s, %s, %s, %s, %s, %s)"
    )

    tickets_user_query = (
        "INSERT INTO tickets_by_user (user_id, date, ticket_id, price, hall, seat)"
        "VALUES (%s, %s, %s, %s, %s, %s)"
    )
    
    db.ticket.execute(tickets_query, [ticket_id, ticket.price, ticket.hall, ticket.seat, ticket.date])
    db.ticket.execute(tickets_order_query, [order_id, ticket.date, ticket_id, ticket.price, ticket.hall, ticket.seat])
    db.ticket.execute(tickets_user_query, [user_id, ticket.date, ticket_id, ticket.price, ticket.hall, ticket.seat])
    
    return ticket.toJSON({"id": ticket_id})


@app.delete("/tickets/{ticket_id}", summary="Удаление записи о билете", tags=["tickets"])
def delete_ticket(ticket_id: uuid.UUID, order_id: uuid.UUID, user_id: uuid.UUID, ticket_date: datetime):
    tickets_query = ("DELETE FROM tickets WHERE ticket_id = %s")
    tickets_order_query= ("DELETE FROM tickets_by_order WHERE ticket_id = %s AND order_id = %s AND date = %s")
    tickets_user_query = ("DELETE FROM tickets_by_user WHERE ticket_id = %s AND user_id = %s AND date = %s")

    db.ticket.execute(tickets_query, [ticket_id])
    db.ticket.execute(tickets_order_query, [ticket_id, order_id, ticket_date])
    db.ticket.execute(tickets_user_query, [ticket_id, user_id, ticket_date])

    return {"status": "success"}


@app.put("/movies/{movie_id}", summary="Обновление информации о фильме", tags=["movies"])
def update_movie(movie_id: uuid.UUID, movie: schemas.MovieUpdate):

    def get_params(param_list: list, movie, old_row=None):
        params = []
        args = []
        movie_dict = movie.toJSON()

        for param in param_list:
            if param in movie_dict.keys() and movie_dict[param] is not None:
                params.append(f"{param} = %s")
                args.append(movie_dict[param])
            elif old_row is not None:
                params.append(f"{param} = %s")
                args.append(old_row[param])

        return params, args

    params = []
    args = []
    movie_date = None
    movie_genre = None

    if movie.genre is not None:
        movie_genre = True
    if movie.release_date is not None:
        movie_date = True

    old_row = get_movie_by_id(movie_id)[0]

    params, args = get_params(list(movie.toJSON().keys()), movie)
    params = ", ".join(params)
    print(params, "\n", args)
    
    movies_query = f"UPDATE movies SET {params} WHERE movie_id = %s"
    db.movie.execute(movies_query, (*args, movie_id))

    cinemas = get_cinemas_by_movie(movie_id)
    params = params.replace("release_date", "date", 1)
    print(params)
    movies_by_cinema_query = f"UPDATE movies_by_cinema SET {params} WHERE cinema_id = %s AND movie_id = %s"

    for cinema in cinemas:
        db.movie.execute(movies_by_cinema_query, (*args, cinema.get("cinema_id"), movie_id))

    if movie_date is not None:
        delete_query = "DELETE FROM movies_by_date WHERE date = %s AND movie_id = %s"
        db.movie.execute(delete_query, (old_row["release_date"], movie_id))

        params, args = get_params(["title", "genre", "duration"], movie, old_row)

        insert_args = [movie.release_date, movie_id]
        insert_args.extend(args)

        insert_query = "INSERT INTO movies_by_date (date, movie_id, title, genre, duration) VALUES (%s, %s, %s, %s, %s)"
        print(insert_query, insert_args)
        db.movie.execute(insert_query, insert_args)
        
        # movies_by_date_query = "UPDATE movies_by_date SET = {params} WHERE date = %s AND movie_id = %s"

    if movie_genre is not None:
        # print(movie)
        # print(old_row)

        delete_query = "DELETE FROM movies_by_genre WHERE genre = %s AND movie_id = %s"
        db.movie.execute(delete_query, (old_row["genre"], movie_id))

        params, args = get_params(["title", "duration"], movie, old_row)

        insert_args = [movie.genre, movie_id]
        insert_args.extend(args)

        insert_query = "INSERT INTO movies_by_genre (genre, movie_id, title, duration) VALUES (%s, %s, %s, %s)"
        print(insert_query, insert_args)
        db.movie.execute(insert_query, insert_args)

        # movies_by_genre_query = "UPDATE movies_by_genre SET = {params} WHERE genre = %s AND movie_id = %s"
    
    # print(movie)


@app.put("/cinema/{cinema_id}", summary="Обновление информации о кинотеатре", tags=["cinemas"])
def update_cinema(cinema_id: uuid.UUID, update: schemas.CinemaUpdate):
    params = []
    args = []

    if update.name:
        params.append("name = %s")
        args.append(update.name)
    if update.address:
        params.append(f"address = {unconvert_address(update.address)}")

    args.append(cinema_id)

    params = ", ".join(params)

    query = f"UPDATE cinemas SET {params} WHERE cinema_id = %s"
    db.movie.execute(query, args)

    movies = get_movies_by_cinema(cinema_id)
    query = f"UPDATE cinemas_by_movie SET {params} WHERE cinema_id = %s AND movie_id = %s"

    for movie in movies:
        db.movie.execute(query, (*args, movie.get("movie_id")))

    return


@app.put("/tickets/{ticket_id}", summary="Обновление информации о билете", tags=["tickets"])
def update_ticket(ticket_id: uuid.UUID, order_id: uuid.UUID, user_id: uuid.UUID, update: schemas.TicketUpdate):
    # order_id, ticket_id
    params = []
    args = []
    ticket_date = None
    
    if update.price:
        params.append("price = %s")
        args.append(update.price)
    if update.hall:
        params.append("hall = %s")
        args.append(update.hall)
    if update.seat:
        params.append("seat = %s")
        args.append(update.seat)
    if update.date:
        params.append("date = %s")
        args.append(update.date)
        ticket_date = update.date
    else:
        old_row = get_ticket_by_id(ticket_id)[0]
        ticket_date = old_row['date']
    
    params = ", ".join(params)

    query = f'UPDATE tickets SET {params} WHERE ticket_id = %s'
    db.ticket.execute(query, (*args, ticket_id))
    
    query = f"UPDATE tickets_by_order SET {params} WHERE order_id = %s AND date = %s AND ticket_id = %s"
    db.ticket.execute(query, (*args, order_id, ticket_date, ticket_id))

    query = f"UPDATE tickets_by_user SET {params} WHERE user_id = %s AND date = %s AND ticket_id = %s"
    db.ticket.execute(query, (*args, user_id, ticket_date, ticket_id))
