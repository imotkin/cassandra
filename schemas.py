import uuid
from datetime import datetime, date
from pydantic import BaseModel
from typing import Optional, Union
from fastapi import Body


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
    
    
class MovieUpdate(Model):
    title: Optional[str] = Body(default=None)
    duration: Optional[str] = Body(default=None)
    release_date: Optional[date] = Body(default=None)
    genre: Optional[str] = Body(default=None)
    score:  Optional[float] = Body(default=None)


class CinemaUpdate(Model):
    name: Optional[str]
    address: Optional[Address] = Body(default=None)


class TicketUpdate(Model):
    price: Optional[float] = Body(default=None)
    seat: Optional[int] = Body(default=None)
    hall: Optional[int] = Body(default=None)
    date: Optional[datetime] = Body(default=None)