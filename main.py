""" This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes to achieve
the program requirements"""
from data_manager import DataManager
from flight_search import FlightSearch
from notification_manager import NotificationManager

FIRST_PROMPT = """Welcome to Julia's Flight Club. 
We find the best flight deals and email you.
What is your first name?"""


def fill_in_iata(data_manager: DataManager):
    """
    Checks if any cities in the Google Flights sheet are missing IATA codes. If any are, it calls
    `FlightSearch.get_iata_code` to get the code and then calls `data_manager.change_iata` to fill them in
    :param data_manager: DataManager object
    """
    for dest in data_manager.destinations:
        if not dest["iataCode"]:
            iata_code = FlightSearch.get_iata_code(dest["city"])
            data_manager.change_iata(dest["city"], iata_code)


def search_and_notify(data_manager, notification_manager, day_range: int = 180, trip_type: str = "round",
                      currency: str = "USD", max_layovers: int = 0):
    """
    This function calls `FlightSearch.search_flights` to search for flights meeting the search criteria. It sends an
    email to notify users if any flights are below the price threshold specified in the Google Spreadsheet.
    :param data_manager: DataManager object
    :param notification_manager: NotificationManager object
    :param day_range: The maximum number of days from tomorrow for which to include departure flights
    :param trip_type: "round" or "oneway"
    :param currency: currency code
    :param max_layovers: maximum number of layovers
    """
    print("Searching for flights...")
    for user in data_manager.users:
        message_text = ""
        for destination in data_manager.destinations:
            flight_info = FlightSearch.search_flights(destination["iataCode"], user["homeAirport"], day_range,
                                                      user["minLength"], user["maxLength"], trip_type, currency,
                                                      max_layovers)
            if not flight_info:
                print(f"No flights found for {destination['city']}")
                continue
            print(f"{destination['city']}: ${flight_info.price}")
            if flight_info.price <= destination['lowestPrice']:
                print("Good deal found")
                message_text += f"Low price alert! Only ${flight_info.price} to fly from {flight_info.departure_city}-" \
                                f"{flight_info.departure_iata} to {flight_info.arrival_city}-{flight_info.arrival_iata}, " \
                                f"from {flight_info.inbound_date} to {flight_info.outbound_date}\n"
                if flight_info.stop_overs != 0:
                    message_text += f"Flight has {flight_info.stop_overs} stop over, via {flight_info.via_city}\n"
        # if we found any deals, send them all in one email
        if message_text:
            notification_manager.send_message(message_text)
            # NotificationManager.send_email(message_text, user['email'])


def get_new_user_info(data_manager):
    """
    Asks user for their information and adds it to the Google sheet
    :param data_manager: DataManager object
    """
    first_name = input(FIRST_PROMPT)
    last_name = input("What is your last name?\n")
    email1 = input("What is your email?\n")
    email2 = input("Enter your email again to confirm\n")
    while email1 != email2:
        print("Those email addresses don't match. Let's try again.")
        email1 = input("What is your email?\n")
        email2 = input("Enter your email again to confirm\n")
    print("You're in the club! Just a few more questions...")
    home_airport = input("What airport do you fly out of? Enter the IATA code \n")
    min_desired_trip = int(input("What's the minimum number of nights you want to stay at your destination?"))
    max_desired_trip = int(input("What's the maximum number of nights you want to stay at your destination?"))
    data_manager.add_user(first_name, last_name, email1, home_airport, min_desired_trip, max_desired_trip)


# set up DataManager object, which will get the info from the Google Sheet
datamanager = DataManager()

# set up NotificationManager object
notificationmanager = NotificationManager()

# call Flight Search to fill in any missing IATA codes
fill_in_iata(datamanager)

# search for cheapest flights to our destinations and text user
search_and_notify(datamanager, notificationmanager)

# Get new user
get_new_user_info(datamanager)
