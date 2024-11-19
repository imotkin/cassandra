from typing import Union
from cassandra.cluster import Cluster
from fastapi import FastAPI

from database import Database

app = FastAPI()
db = Database(Cluster())


@app.get("/ping")
def read_root():
    return {"status": "ok"}


@app.get("/cinemas")
def get_cinemas():
    db.ticket.execute()


@app.get("/tickets")
def get_tickets():
    pass


@app.get("/movies")
def get_movies():
    pass


@app.get("/sessions")
def get_sessions():
    pass


@app.get("/users")
def get_users():
    pass
