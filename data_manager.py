import requests


SHEETY_PRICE_ENDPOINT = "https://api.sheety.co/281b7b354b6373ee95bc3bc916c24399/flightDeals/prices"
SHEETY_USER_ENDPOINT = "https://api.sheety.co/281b7b354b6373ee95bc3bc916c24399/flightDeals/users"


class DataManager:
    """This class is responsible for talking to the Google Sheet."""
    def __init__(self):
        self.header_info = {"Content-Type": "application/json"}
        self.destinations = requests.get(url=SHEETY_PRICE_ENDPOINT).json()["prices"]
        self.users = requests.get(url=SHEETY_USER_ENDPOINT).json()["users"]

    def add_destination(self, city: str, price_threshold: int, IATA_code: str = ""):
        """
        Adds a new destination city to the Google Spreadsheet
        :param city: Destination city name
        :param price_threshold: Highest flight price for which the user would like to be notified
        :param IATA_code: Destination IATA code if known. Defaults to empty string.
        """
        # len(self.destinations) + 2 corresponds to the spreadsheet row where the new location will be added, which
        # will become its object id for Sheety. +1 is needed to account for header row
        new_dest = {'city': city, 'iataCode': IATA_code, 'lowestPrice': price_threshold, 'id': len(self.destinations)+2}
        self.destinations.append(new_dest)
        sheet_inputs = {"price": new_dest}
        sheet_response = requests.post(SHEETY_PRICE_ENDPOINT, json=sheet_inputs, headers=self.header_info)
        sheet_response.raise_for_status()

    def change_price(self, city_to_edit: str, new_price: int):
        """
        Changes a price threshold for `city_to_edit` in the Google sheet
        :param city_to_edit: Destination city for which to send the price threshold
        :param new_price: New price threshold
        """
        for destination in self.destinations:
            if destination["city"] == city_to_edit:
                destination["lowestPrice"] = new_price
                sheet_inputs = {"price": destination}
                response = requests.put(f"{SHEETY_PRICE_ENDPOINT}/{destination['id']}", json=sheet_inputs, headers=self.header_info)
                response.raise_for_status()

    def change_iata(self, city_to_edit, new_iata):
        """
        Changes or adds an IATA code for `city_to_edit` in the Google sheet
        :param city_to_edit: Destination city to change or add IATA code for
        :param new_iata: New IATA code
        """
        for destination in self.destinations:
            if destination["city"] == city_to_edit:
                destination["iataCode"] = new_iata
                sheet_inputs = {"price": destination}
                response = requests.put(f"{SHEETY_PRICE_ENDPOINT}/{destination['id']}", json=sheet_inputs, headers=self.header_info)
                response.raise_for_status()

    def add_user(self, first, last, email, home_airport, min_length, max_length):
        """
        Adds new user to Sheety
        :param first: user's first name
        :param last: user's last name
        :param email: user's email
        :param home_airport: user's home airport
        :param min_length: minimum desired length of trip
        :param max_length: maximum desired length of trip
        """
        sheet_inputs = {"user": {"firstName": first, "lastName": last, "email": email, "homeAirport": home_airport,
                                 "minLength": min_length, "maxLength": max_length}}
        response = requests.post(SHEETY_USER_ENDPOINT, json=sheet_inputs, headers=self.header_info)
        response.raise_for_status()

