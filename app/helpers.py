from typing import List
from datetime import datetime
from data_models import Connection, ConnectionFlight  
import logging


def make_location(city="", airport=""):
    return {"city": city, "airport": airport}

def check_lower_price(flights : List[dict]) -> float:
    lower_price = float("inf")

    for f in flights:
        for d in f["data"]:
            price = float(d["price"]["total"])
            lower_price = min(lower_price, price)

    return lower_price

def calc_waiting_time(flights: List[ConnectionFlight]) -> List[Connection]:
    conexions = []

    for i in range(len(flights) - 1):
        f1 = flights[i]
        f2 = flights[i + 1]

        # checa se o destino do primeiro é a origem do segundo
        if f1.destination["city"] == f2.origin["city"]:
            change_airport = False
            location = [f1.destination]
            if f1.destination["airport"] != f2.origin["airport"]:
                change_airport = True
                location = [f1.destination, f2.origin]
            date_f1= datetime.strptime(f1.arrival, "%Y-%m-%dT%H:%M:%S")
            date_f2 = datetime.strptime(f2.departure, "%Y-%m-%dT%H:%M:%S")
            waiting_time = date_f2 - date_f1
            conexions.append(Connection(location, waiting_time, change_airport))
    logging.debug("Calculating waiting time in conexions")

    return conexions
