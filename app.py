import asyncio
from typing import Union
from cassandra.cluster import Cluster
from cassandra.cqlengine.management import sync_table
from cassandra.cqlengine import connection
from models import Cinema
from fastapi import FastAPI, Depends
import schemas

from database import Database


# def run_migration(db: Database, filename: str):
#     with open(filename, "r") as file:
#         schema_commands = file.read()

#         for command in schema_commands.split(";"):
#             command = command.strip()
#             if command:
#                 try:
#                     db.cluster.connect().execute(command)
#                     print(f"Add table: {command}")
#                 except Exception as e:
#                     print(f"Error: {command}\n{e}")


app = FastAPI()
db = Database(Cluster())

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


@app.get("/ping")
def read_root():
    return {"status": "ok"}


@app.get("/cinemas")
def get_cinemas():
    rows = db.movie.execute("SELECT * FROM cinemas;")
    result = []
    for row in rows:
        result.append(
            {
                "id": row.cinema_id,
                "name": row.name,
                "address": convert_address(row.address),
                "halls": row.halls,
            }
        )
    return result


@app.get("/tickets")
def get_tickets():
    rows = db.movie.execute("SELECT * FROM tickets;")
    result = []
    for row in rows:
        result.append(
            {
                "id": row.cinema_id,
                "name": row.name,
                "address": convert_address(row.address),
                "halls": row.halls,
            }
        )
    return result


@app.get("/movies")
def get_movies():
    pass


@app.get("/sessions")
def get_sessions():
    pass


@app.get("/users")
def get_users():
    pass


# INSERT INTO cinemas (cinema_id, halls, name, address) VALUES (1, 3, 'test', {city: 'Moscow', street: 'Stromunka'});


@app.post("/cinemas")
def create_cinema(cinema: schemas.Cinema):
    print(unconvert_address(cinema.address))
    query = (
        "INSERT INTO cinemas (cinema_id, halls, name, address) "
        f"VALUES ({cinema.cinema_id}, {cinema.halls}, '{cinema.name}', {unconvert_address(cinema.address)})"
    )
    print(query)
    res = db.movie.execute(query)
    return cinema
