from datetime import datetime, date


class Address:
    
    def __init__(self, city, street, postal_code, house, building):
        self.city = city
        self.street = street
        self.postal_code = postal_code
        self.house = house
        self.building = building


class Movie:

    def __init__(self, id, title, duration, release_date, genre, score):
        self.id = id
        self.title = title
        self.duration = duration
        self.release_date = release_date
        self.genre = genre
        self.score = score


class Session:

    def __init__(self, id, available_seats, time, price, hall, format):
        self.id = id
        self.available_seats = available_seats
        self.time = time
        self.price = price
        self.hall = hall
        self.format = format


class Cinema:

    def __init__(self, cinema_id, name, address, halls):
        self.cinema_id = cinema_id
        self.name = name
        self.halls = halls
        self.address = address


class User:

    def __init__(self, user_id, email, name, password, phone):
        self.user_id = user_id
        self.name = name
        self.password = password
        self.email = email
        self.phone = phone


class Ticket:

    def __init__(self, id, price, hall, seat, date):
        self.id = id
        self.price = price
        self.hall = hall
        self.seat = seat
        self.date = date


class Order:

    def __init__(self, order_id, user_id, date, status, price):
        self.order_id = order_id
        self.user_id = user_id
        self.date = date
        self.status = status
        self.price = price
