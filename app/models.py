import logging
import airportsdata
from typing import List
from datetime import datetime, timedelta
from data_models import ConnectionFlight, Flight, Itinerarie
from helpers import make_location, check_lower_price, calc_waiting_time
from api_client import search_flights
from validator import Validator
from errors import InvalidIATACodeError, InvalidDateRangeError


class FlightSearcher:
    def __init__(self, token):
        self.logger = logging.getLogger(__name__)
        self.token = token
        self.airports = airportsdata.load('IATA')
        self.validator = Validator()

    def __iata_to_location(self, iata : str) -> dict:
        self.validator.validade_iata_code(iata)
        location = make_location(self.airports[iata]["city"], self.airports[iata]["name"])
        return location

    
    def __get_segments(self, segments) -> List[ConnectionFlight]:
        flights = []
        for f in segments:
            departure_time = f["departure"]["at"]
            arrival_time = f["arrival"]["at"]
            flight_number = f"{f["carrierCode"]} {f["number"]}"
            origin = self.__iata_to_location(f["departure"]["iataCode"])
            destination = self.__iata_to_location(f["arrival"]["iataCode"])
            flight = ConnectionFlight(origin=origin, destination=destination, departure=departure_time, arrival=arrival_time, flight_number=flight_number)
            flights.append(flight)
        self.logger.debug("Getting conexion flights")
        return flights
    
    def __create_flight(self, json : dict, origin : dict, destination : dict) -> Flight:
        segments_json = json["segments"]
        duration = json["duration"]

        if len(segments_json) > 1: # significa q tem paradas
            segments = self.__get_segments(segments_json)
            conexions = calc_waiting_time(segments)
            return Flight(origin=origin, destination=destination, date=segments[0].departure, duration=duration, included_baggage=False, segments=segments, connections=conexions)

        departure_time = segments_json[0]["departure"]["at"]
        flight_number = f"{segments_json[0]["carrierCode"]} {segments_json[0]["number"]}"
        return Flight(origin=origin, destination=destination, date=departure_time, duration=duration, included_baggage=False, flight_number=flight_number)


    def search(self, date_start: str, date_end: str, city_from: str, city_to: str, qtd_days : int) -> List[Itinerarie]:
        try:
            self.validator.validate_qt_days(qtd_days)

            date_s= datetime.strptime(date_start, "%d-%m-%Y")
            date_e = datetime.strptime(date_end, "%d-%m-%Y")
            date = date_s

            self.validator.validate_date(date_s, date_e)

            datas = []

            while date <= date_e:
                date_r = date + timedelta(days=qtd_days)
                datas.append((date, date_r))
                date = date + timedelta(days=3)


            flights_d = []
            result_flights = []

            origin = self.__iata_to_location(city_from)
            destination = self.__iata_to_location(city_to)

            self.validator.validate_locations(origin, destination)

            for t in datas:
                flight = search_flights(t[0].day, t[0].month, t[0].year, city_from, city_to, self.token, t[1].day, t[1].month, t[1].year)
                flights_d.append(flight.json())
                self.logger.debug("Searching flights: %s -> %s", t[0].date(), t[1].date())
            self.logger.info("Search concluded. %d results collected.", len(flights_d))


            lower_price = check_lower_price(flights_d)
            self.logger.info("Lowest price: %d", lower_price)

            for f in flights_d:
                for d in f["data"]:
                    price = float(d["price"]["total"])
                    if price == lower_price:
                        flight_departure = self.__create_flight(d["itineraries"][0], origin, destination)
                        flight_back = self.__create_flight(d["itineraries"][1], destination, origin)

                        new_itinerarie = Itinerarie(price, flight_departure, flight_back)

                        result_flights.append(new_itinerarie)
            
            if not result_flights:
                raise ValueError("Nenhum voo encontrado com esse critério.")


            return result_flights

        except (ValueError, InvalidDateRangeError, InvalidIATACodeError) as e:
            self.logger.error("Validation error: %s", str(e))
            raise