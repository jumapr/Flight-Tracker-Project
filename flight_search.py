import requests
import os
from datetime import datetime, timedelta
from flight_data import FlightData

API_KEY = os.environ.get('TEQUILA_API_KEY')
LOCATIONS_ENDPOINT = "https://tequila-api.kiwi.com/locations/query"
SEARCH_ENDPOINT = "https://tequila-api.kiwi.com/v2/search"
TOMORROW = datetime.today() + timedelta(days=1)


class FlightSearch:
    """This class is responsible for interfacing with the Tequila Flight Search API."""
    @staticmethod
    def get_iata_code(city: str) -> str:
        """
        Gets airport IATA code, given city name
        :param city: city to get IATA code for
        :return: IATA code
        """
        parameters = {'apikey': API_KEY,
                      'term': city}
        response = requests.get(url=LOCATIONS_ENDPOINT, params=parameters)
        city_code = response.json()['locations'][0]['code']
        return city_code

    @staticmethod
    def search_flights(fly_to: str, fly_from: str = 'DTW', day_range: int = 180, min_trip_length: int = 7,
                       max_trip_length: int = 28, flight_type: str = 'round', currency: str = 'USD',
                       stop_overs: int = 0):
        """
        Searches for flights with constraints specified, using Tequila API
        :param fly_to: city or airport code for destination
        :param fly_from: Airport or city code for departure
        :param day_range: The maximum number of days from tomorrow for which to include departure flights. For example,
        180 will search for flights leaving within the next 6 months.
        :param min_trip_length: minimum nights to stay at destination
        :param max_trip_length: maximum nights to stay at destination
        :param flight_type: "round" or "oneway"
        :param currency: currency code for the response, for example. 'USD' or 'GBP'
        :param stop_overs: maximum number of layovers. Program is not set up for more flight with more than 1.
        :return flight_data: FlightData object containing the flight information
        """
        parameters = {"apikey": API_KEY,
                      "fly_from": fly_from,
                      "fly_to": fly_to,
                      "date_from": TOMORROW.strftime('%d/%m/%Y'),
                      "date_to": (TOMORROW + timedelta(days=day_range)).strftime('%d/%m/%Y'),
                      "nights_in_dst_from": min_trip_length,
                      "nights_in_dst_to": max_trip_length,
                      "flight_type": flight_type,
                      "curr": currency,
                      "max_stopovers": stop_overs}
        response = requests.get(url=SEARCH_ENDPOINT, params=parameters)
        response.raise_for_status()
        try:
            data = response.json()['data'][0]
        except IndexError:
            return None
        # check if the flight has a layover
        if len(data['route']) > 2:
            flight_info = FlightData(data['price'], data['cityFrom'], data['flyFrom'], data['cityTo'], data['flyTo'],
                                     data['local_departure'][:10], data['route'][1]['local_departure'][:10], 1,
                                     data['route'][0]['cityTo'])
        else:
            flight_info = FlightData(data['price'], data['cityFrom'], data['flyFrom'], data['cityTo'], data['flyTo'],
                                     data['local_departure'][:10], data['route'][1]['local_departure'][:10])
        return flight_info
