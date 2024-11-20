from datetime import datetime, date
from pydantic import BaseModel


class Address(BaseModel):
    city: str
    street: str
    postal_code: int
    house: str
    building: int


class Movie(BaseModel):
    id: int
    title: str
    duration: str
    release_date: date
    genre: str
    score: float


class Session(BaseModel):
    id: int
    available_seats: int
    time: datetime
    price: float
    hall: int
    format: str


class Cinema(BaseModel):
    cinema_id: int
    name: str
    address: Address
    halls: int


class User(BaseModel):
    id: int
    name: str
    password: str
    email: str
    phone: str


class Ticket(BaseModel):
    id: int
    price: float
    hall: int
    seat: int
    date: datetime
