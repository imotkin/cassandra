from datetime import datetime, date


class Address:
    def __init__(self, city, street, postal_code, house, building):
        self.city = city
        self.street = street
        self.postal_code = postal_code
        self.house = house
        self.building = building

    city: str
    street: str
    postal_code: int
    house: str
    building: int


class Movie:
    def __init__(self, id, title, duration, release_date, genre, score):
        self.id = id
        self.title = title
        self.duration = duration
        self.release_date = release_date
        self.genre = genre
        self.score = score

    movie_id: int
    title: str
    duration: str
    release_date: date
    genre: str
    score: float


class Session:
    def __init__(self, id, available_seats, time, price, hall, format):
        self.id = id
        self.available_seats = available_seats
        self.time = time
        self.price = price
        self.hall = hall
        self.format = format

    session_id: int
    available_seats: int
    time: datetime
    price: float
    hall: int
    format: str


class Cinema:
    def __init__(self, cinema_id, name, address, halls):
        self.cinema_id = cinema_id
        self.name = name
        self.halls = halls
        self.address = address

    cinema_id: int
    name: str
    halls: int
    address: Address


class User:
    def __init__(self, user_id, email, name, password, phone):
        self.user_id = user_id
        self.name = name
        self.password = password
        self.email = email
        self.phone = phone

    user_id: int
    name: str
    password: str
    email: str
    phone: str


class Ticket:
    def __init__(self, id, price, hall, seat, date):
        self.id = id
        self.price = price
        self.hall = hall
        self.seat = seat
        self.date = date

    id: int
    price: float
    hall: int
    seat: int
    date: datetime


class Order:
    def __init__(self, order_id, user_id, date, status, price):
        self.order_id = order_id
        self.user_id = user_id
        self.date = date
        self.status = status
        self.price = price

    order_id: int
    user_id: int
    date: datetime
    status: str
    price: float
