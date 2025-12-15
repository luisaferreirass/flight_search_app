from typing import List, TypedDict
from datetime import datetime
from dataclasses import dataclass, field



@dataclass
class Connection:
    locations : List[dict]
    waiting_time : str
    change_airport : bool

@dataclass
class ConnectionFlight:
    origin: dict
    destination: dict
    departure: datetime
    arrival: datetime
    flight_number : str

@dataclass
class Flight:
    origin: dict
    destination: dict
    date: datetime
    duration: str  # ou timedelta
    included_baggage: bool = False
    flight_number: str = ""
    segments: List[ConnectionFlight] = field(default_factory=list)
    connections: List[Connection] = field(default_factory=list)


@dataclass
class Itinerarie:
    price : float
    flight_departure : Flight
    flight_return : Flight