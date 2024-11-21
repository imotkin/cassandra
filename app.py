from datetime import datetime
from typing import Annotated

from fastapi import FastAPI, Path
import schemas

from database import Database


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


app = FastAPI()
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


@app.get("/cinemas", summary="Получение списка всех кинотеатров")
def get_cinemas():
    rows = db.movie.execute("SELECT * FROM cinemas")
    return [dict(row) for row in rows]


@app.get("/cinemas/{cinema_id}", summary="Получение информации о кинотеатре")
def get_cinema_by_id(cinema_id: int):
    select_query = "SELECT * FROM cinemas WHERE cinema_id = %i"
    rows = db.movie.execute(select_query, cinema_id)
    return [dict(row) for row in rows]


@app.get("/movies", summary="Получение списка всех фильмов")
def get_movies():
    rows = db.movie.execute("SELECT * FROM movies")
    return [dict(row) for row in rows]


@app.get("/movies/{movie_id}", summary="Получение информации о фильме")
def get_movie_by_id(movie_id: int):
    select_query = "SELECT * FROM movies WHERE movie_id = %i"
    rows = db.movie.execute(select_query, movie_id)
    return [dict(row) for row in rows]


@app.get("/movies/{cinema_id}/", summary="Получение списка фильмов для определенного кинотеатра")
def get_movies_by_cinema(cinema_id: int):
    select_query = "SELECT * FROM movies_by_cinema WHERE cinema_id = %i"
    rows = db.movie.execute(select_query, cinema_id)
    return [dict(row) for row in rows]


@app.get("/movies/{date}/", summary="Получение списка фильмов для определенной даты")
def get_movies_by_cinema(date: datetime):
    select_query = (
        "SELECT * FROM movies_by_date"
        f"WHERE date = {date}"
    )
    rows = db.movie.execute(select_query)
    return [dict(row) for row in rows]


@app.get("/movies/{genre}/", summary="Получение списка фильмов для определенного жанра")
def get_movies_by_cinema(genre: str):
    select_query = (
        "SELECT * FROM movies_by_genre"
        f"WHERE genre = {genre}"
    )
    rows = db.movie.execute(select_query)
    return [dict(row) for row in rows]


@app.get("/sessions", summary="Получение списка всех сеансов")
def get_sessions():
    rows = db.movie.execute("SELECT * FROM sessions")
    return [dict(row) for row in rows]


@app.get("/sessions/{session_id}", summary="Получение информации о сеансе")
def get_session_by_id(session_id: int):
    select_query = "SELECT * FROM sessions WHERE session_id = %i"
    rows = db.movie.execute(select_query, session_id)
    return [dict(row) for row in rows]


@app.get("/sessions/{movie_id}", summary="Получение сеансов по фильму")
def get_session_by_movie(movie_id: int):
    select_query = "SELECT * FROM sessions_by_movie WHERE movie_id = %i"
    rows = db.movie.execute(select_query, movie_id)
    return [dict(row) for row in rows]


@app.get("/users", summary="Получение списка всех пользователей")
def get_users():
    rows = db.ticket.execute("SELECT * FROM users")
    return [dict(row) for row in rows]


@app.get("/users/{user_id}", summary="Получение информации о пользователе")
def get_user_by_id(user_id: int):
    select_query = "SELECT * FROM users WHERE user_id = %i"
    rows = db.ticket.execute(select_query, user_id)
    return [dict(row) for row in rows]


@app.get("/tickets", summary="Получение списка всех билетов")
def get_tickets():
    rows = db.ticket.execute("SELECT * FROM tickets")
    return [dict(row) for row in rows]


@app.get("/tickets/{ticket_id}", summary="Получение информации о билете")
def get_ticket_by_id(ticket_id: int):
    select_query = "SELECT * FROM tickets WHERE ticket_id = %i"
    rows = db.ticket.execute(select_query, ticket_id)
    return [dict(row) for row in rows]


@app.get("/tickets/{order_id}", summary="Получение билетов для определенного заказа")
def get_ticket_by_order(order_id: int):
    select_query = "SELECT * FROM tickets_by_order WHERE order_id = %i"
    rows = db.ticket.execute(select_query, order_id)
    return [dict(row) for row in rows]


@app.get("/tickets/{user_id}", summary="Получение билетов для определенного пользователя")
def get_ticket_by_order(user_id: int):
    select_query = "SELECT * FROM tickets_by_user WHERE user_id = %i"
    rows = db.ticket.execute(select_query, user_id)
    return [dict(row) for row in rows]


@app.get("/orders", summary="Получение списка всех заказов")
def get_orders():
    rows = db.ticket.execute("SELECT * FROM orders")
    return [dict(row) for row in rows]


@app.get("/orders/{order_id}", summary="Получение информации о заказе")
def get_order_by_id(order_id: int):
    select_query = "SELECT * FROM orders WHERE order_id = %i"
    rows = db.ticket.execute(select_query, order_id)
    return [dict(row) for row in rows]


@app.get("/orders/{session_id}", summary="Получение заказов для определенного сеанса")
def get_orders_by_session(session_id: int):
    select_query = "SELECT * FROM orders_by_session WHERE session_id = %i"
    rows = db.movie.execute(select_query, session_id)
    return [dict(row) for row in rows]


@app.post("/cinemas", summary="Добавление нового кинотеатра")
def create_cinema(cinema: schemas.Cinema):
    print(unconvert_address(cinema.address))
    query = (
        "INSERT INTO cinemas (cinema_id, halls, name, address) "
        f"VALUES ({cinema.cinema_id}, {cinema.halls}, '{cinema.name}', {unconvert_address(cinema.address)})"
    )
    print(query)
    db.movie.execute(query)
    return cinema
