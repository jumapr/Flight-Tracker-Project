from twilio.rest import Client
import smtplib
import os

# Twilio info
TWILIO_SID = os.environ.get('TWILIO_SID')
TWILIO_AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN')
TWILIO_ENDPOINT = os.environ.get('TWILIO_ENDPOINT')
# these are dummy numbers
TO_NUMBER = "+17341231234"
FROM_NUMBER = "+17341231234"

# Gmail account info
my_email = "julia.prisby@gmail.com"
my_password = os.environ.get('GMAIL_PASSWORD')


class NotificationManager:
    # This class is responsible for sending notifications with the deal flight details.
    def __init__(self):
        """
        Creates Twilio client
        """
        self.client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

    def send_message(self, message_body):
        """
        Sends text message
        :param message_body: text message body
        """
        message = self.client.messages.create(body=message_body, from_=FROM_NUMBER, to=TO_NUMBER)

    @staticmethod
    def send_email(message_body, to_address_list):
        """
        Sends email notification
        :param message_body: email message body
        :param to_address_list: lists of email addreeses to send notifications to
        """
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=my_email, password=my_password)
            for to_address in to_address_list:
                connection.sendmail(from_addr=my_email, to_addrs=to_address,
                                    msg=f"Subject: Julia's Flight Club Deals \n\n {message_body}")

