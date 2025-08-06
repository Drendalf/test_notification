import re
from dataclasses import dataclass
from dotenv import load_dotenv
from exceptions import BadEmailFormat, BadUserData
from reg import regex
from senders.EmailSender import EmailSender
from senders.SMSSender import SMSSender
from senders.TelegramSender import TelegramSender
import argparse
import os
import json


@dataclass
class NotificationService:
    user_data: dict

    def _check_email_format(self, email: str) -> None:
        if not re.match(regex, email):
            raise BadEmailFormat(f"{email} have wrong format.")

    def notify_user(self, subject: str, message: str) -> None:
        self._check_email_format(self.user_data["email"])

        methods = [
            (
                "email",
                lambda: EmailSender.send_email(
                    self.user_data["email"], subject, message
                ),
            ),
            ("sms", lambda: SMSSender.send_sms(self.user_data["phone"], message)),
            (
                "telegram",
                lambda: TelegramSender.send_telegram_message(
                    self.user_data["telegram_chat_id"], message
                ),
            ),
        ]

        for method_name, send_func in methods:
            success = send_func()
            if success:
                print(f"{method_name.capitalize()} успешно отправлен.")
                break
            else:
                print(
                    f"{method_name.capitalize()} не удался. Переходим к следующему..."
                )
        else:
            print("Все способы отправки завершились неудачей.")


if __name__ == "__main__":
    basedir = os.path.abspath(os.path.dirname(__file__))
    load_dotenv(os.path.join(basedir, 'dev.env'))

    parser = argparse.ArgumentParser(description="Parser for notification.")
    parser.add_argument("--user",type=str, help="user data")
    parser.add_argument("--subject", help="subject for mail")
    parser.add_argument("--message", help="message")
    args = parser.parse_args()

    try:
        user_data = json.loads(args.user)
    except json.decoder.JSONDecodeError as ex:
        raise BadUserData(f'{args.user} wrong data. {repr(ex)}')

    service = NotificationService(user_data)

    service.notify_user(args.subject, args.message)
