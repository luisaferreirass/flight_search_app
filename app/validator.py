import airportsdata
from errors import InvalidIATACodeError, InvalidDateRangeError, APITokenExpiredError
from datetime import datetime

class Validator:
    def __init__(self):
        self.airports = airportsdata.load('IATA')

    def validate_date(self, date_s : datetime, date_e : datetime):
        if date_s < datetime.now() or date_e < datetime.now():
            raise ValueError("Data inválida: Coloque uma data depois do dia de hoje")

        if date_e < date_s:
            raise InvalidDateRangeError(date_s, date_e)

    def validate_qt_days(self, qt_days : int):
        if qt_days <= 0:
            raise ValueError("A quantidade de dias de estadia deve ser maior do que 0")

    def validade_iata_code(self, iata_code : str):
        if iata_code not in self.airports:
            raise InvalidIATACodeError(iata_code)

    def validate_locations(self, origin : dict, destination : dict):
        if origin["city"] == destination["city"]:
            raise ValueError("Não é possível pesquisar voos para a mesma cidade")