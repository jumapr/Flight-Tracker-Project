class FlightData:
    """
    Stores flight data
    """
    def __init__(self, price: int, departure_city: str, departure_iata: str, arrival_city: str, arrival_iata: str,
                 outbound_date: str, inbound_date: str, stop_overs: int = 0, via_city: str = ""):
        """
        Creates FlightData object
        :param price: flight price
        :param departure_city: departure city
        :param departure_iata: IATA code for departure city
        :param arrival_city: arrival city
        :param arrival_iata: IATA code for arrival city
        :param outbound_date: departure date
        :param inbound_date: return data
        :param stop_overs: number of layovers
        :param via_city: layover city
        """
        self.price = price
        self.departure_city = departure_city
        self.departure_iata = departure_iata
        self.arrival_city = arrival_city
        self.arrival_iata = arrival_iata
        self.outbound_date = outbound_date
        self.inbound_date = inbound_date
        self.stop_overs = stop_overs
        self.via_city = via_city
