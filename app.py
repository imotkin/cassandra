from datetime import datetime
from fastapi import FastAPI
import schemas

from database import Database

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
db = Database(test=True)

# run_migration(db, "init.cql")


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
def get_cinema_by_id(cinema_id: int):
    select_query = "SELECT * FROM cinemas WHERE cinema_id = %i"
    rows = db.movie.execute(select_query, cinema_id)
    return [dict(row) for row in rows]


@app.get("/cinemas/{movie_id}", summary="Получение кинотеатров для фильма", tags=["cinemas"])
def get_cinemas_by_movie(movie_id: int):
    select_query = "SELECT * FROM cinemas_by_movie WHERE cinema_id = %i"
    rows = db.movie.execute(select_query, movie_id)
    return [dict(row) for row in rows]


@app.get("/movies/{movie_id}", summary="Получение информации о фильме", tags=["movies"])
def get_movie_by_id(movie_id: int):
    select_query = "SELECT * FROM movies WHERE movie_id = %i"
    rows = db.movie.execute(select_query, movie_id)
    return [dict(row) for row in rows]


@app.get(
    "/movies/{cinema_id}/",
    summary="Получение списка фильмов для определенного кинотеатра",
    tags=["movies"]
)
def get_movies_by_cinema(cinema_id: int):
    select_query = "SELECT * FROM movies_by_cinema WHERE cinema_id = %i"
    rows = db.movie.execute(select_query, cinema_id)
    return [dict(row) for row in rows]


@app.get("/movies/{date}/", summary="Получение списка фильмов для определенной даты", tags=["movies"])
def get_movies_by_date(date: datetime):
    select_query = "SELECT * FROM movies_by_date" f"WHERE date = {date}"
    rows = db.movie.execute(select_query)
    return [dict(row) for row in rows]


@app.get("/movies/{genre}/", summary="Получение списка фильмов для определенного жанра", tags=["movies"])
def get_movies_by_genre(genre: str):
    select_query = "SELECT * FROM movies_by_genre" f"WHERE genre = {genre}"
    rows = db.movie.execute(select_query)
    return [dict(row) for row in rows]


@app.get("/sessions/{session_id}", summary="Получение информации о сеансе", tags=["sessions"])
def get_session_by_id(session_id: int):
    select_query = "SELECT * FROM sessions WHERE session_id = %i"
    rows = db.movie.execute(select_query, session_id)
    return [dict(row) for row in rows]


@app.get("/sessions/{movie_id}", summary="Получение сеансов по фильму", tags=["sessions"])
def get_session_by_movie(movie_id: int):
    select_query = "SELECT * FROM sessions_by_movie WHERE movie_id = %i"
    rows = db.movie.execute(select_query, movie_id)
    return [dict(row) for row in rows]


@app.get("/users/{user_id}", summary="Получение информации о пользователе", tags=["users"])
def get_user_by_id(user_id: int):
    select_query = "SELECT * FROM users WHERE user_id = %i"
    rows = db.ticket.execute(select_query, user_id)
    return [dict(row) for row in rows]


@app.get("/tickets/{ticket_id}", summary="Получение информации о билете", tags=["tickets"])
def get_ticket_by_id(ticket_id: int):
    select_query = "SELECT * FROM tickets WHERE ticket_id = %i"
    rows = db.ticket.execute(select_query, ticket_id)
    return [dict(row) for row in rows]


@app.get("/tickets/{order_id}", summary="Получение билетов для определенного заказа", tags=["tickets"])
def get_ticket_by_order(order_id: int):
    select_query = "SELECT * FROM tickets_by_order WHERE order_id = %i"
    rows = db.ticket.execute(select_query, order_id)
    return [dict(row) for row in rows]


@app.get(
    "/tickets/{user_id}", summary="Получение билетов для определенного пользователя",
    tags=["tickets"]
)
def get_ticket_by_user(user_id: int):
    select_query = "SELECT * FROM tickets_by_user WHERE user_id = %i"
    rows = db.ticket.execute(select_query, user_id)
    return [dict(row) for row in rows]


@app.get("/orders/{order_id}", summary="Получение информации о заказе", tags=["orders"])
def get_order_by_id(order_id: int):
    select_query = "SELECT * FROM orders WHERE order_id = %i"
    rows = db.ticket.execute(select_query, order_id)
    return [dict(row) for row in rows]


@app.get("/orders/{session_id}", summary="Получение заказов для определенного сеанса", tags=["orders"])
def get_orders_by_session(session_id: int):
    select_query = "SELECT * FROM orders_by_session WHERE session_id = %i"
    rows = db.movie.execute(select_query, session_id)
    return [dict(row) for row in rows]


@app.post("/cinemas", summary="Добавление нового кинотеатра", tags=["cinemas"])
def create_cinema(cinema: schemas.Cinema):
    print(unconvert_address(cinema.address))
    query = (
        "INSERT INTO cinemas (cinema_id, halls, name, address) "
        f"VALUES ({cinema.cinema_id}, {cinema.halls}, '{cinema.name}', {unconvert_address(cinema.address)})"
    )
    print(query)
    db.movie.execute(query)
    return cinema
