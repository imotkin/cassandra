import uuid
from datetime import datetime, date
from pydantic import BaseModel


class Model(BaseModel):
    def toJSON(self, fields: dict = None):
        model_dict = self.__dict__
        if fields is not None:
            model_dict.update(fields)
        return model_dict


class Address(Model):
    city: str
    street: str
    postal_code: int
    house: str
    building: int


class Movie(Model):
    # id: uuid.UUID
    title: str
    duration: str
    release_date: date
    genre: str
    score: float


class Session(Model):
    # id: uuid.UUID
    available_seats: int
    time: datetime
    price: float
    hall: int
    format: str


class Cinema(Model):
    # id: uuid.UUID
    name: str
    address: Address
    halls: int


class User(Model):
    # id: uuid.UUID
    name: str
    password: str
    email: str
    phone: str


class Ticket(Model):
    # id: uuid.UUID
    price: float
    hall: int
    seat: int
    date: datetime


class Order(Model):
    # id: uuid.UUID
    # user_id: uuid.UUID
    # date: datetime
    status: str
    price: float
