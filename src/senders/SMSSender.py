from twilio.rest import Client
from dataclasses import dataclass
import os


@dataclass
class SMSSender:
    twilio_account_sid: str = os.environ['TWILIO_ACCOUNT_SID']
    twilio_auth_token: str = os.environ['TWILIO_AUTH_TOKEN']
    twilio_phone_number: str =os.environ['TWILIO_PHONE_NUMBER']

    def send_sms(self, phone_number:str, message:str)->bool:
        client = Client(self.twilio_account_sid, self.twilio_auth_token)
        try:
            client.messages.create(
                to=phone_number,
                from_=self.twilio_phone_number,
                body=message
            )
            return True
        except Exception as e:
            print(f'Ошибка отправки SMS: {e}')
            return False