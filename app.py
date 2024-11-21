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


@app.get("/cinemas")
def get_cinemas():
    rows = db.movie.execute("SELECT * FROM cinemas")
    return [dict(row) for row in rows]


@app.get("/movies")
def get_movies():
    rows = db.movie.execute("SELECT * FROM movies")
    return [dict(row) for row in rows]


@app.get("/movies/{cinema_id}/", summary="Получение списка фильмов для определенного кинотеатра")
def get_movies_by_cinema(cinema_id: int):
    select_query = (
        "SELECT * FROM movies_by_cinema"
        f"WHERE cinema_id = {cinema_id}"
    )
    rows = db.movie.execute(select_query)
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


@app.get("/sessions")
def get_sessions():
    rows = db.movie.execute("SELECT * FROM sessions")
    return [dict(row) for row in rows]


@app.get("/users")
def get_users():
    rows = db.ticket.execute("SELECT * FROM users")
    return [dict(row) for row in rows]


@app.get("/tickets")
def get_tickets():
    rows = db.ticket.execute("SELECT * FROM tickets")
    return [dict(row) for row in rows]


@app.get("/orders")
def get_orders():
    rows = db.ticket.execute("SELECT * FROM orders")
    return [dict(row) for row in rows]


@app.post("/cinemas")
def create_cinema(cinema: schemas.Cinema):
    print(unconvert_address(cinema.address))
    query = (
        "INSERT INTO cinemas (cinema_id, halls, name, address) "
        f"VALUES ({cinema.cinema_id}, {cinema.halls}, '{cinema.name}', {unconvert_address(cinema.address)})"
    )
    print(query)
    db.movie.execute(query)
    return cinema
