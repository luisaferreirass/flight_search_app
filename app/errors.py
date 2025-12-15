
class InvalidIATACodeError(Exception):
    """Código IATA inválido"""
    def __init__(self, *args):
        self.message = f"Iata code invalid: {args}."
        super().__init__(*args)


class InvalidDateRangeError(Exception):
    """"""
    def __init__(self, *args):
        self.message = f"Invalid date range: {args[0]} -> {args[1]}"
        super().__init__(*args)
