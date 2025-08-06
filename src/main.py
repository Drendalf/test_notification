import argparse
import json
import os

from dotenv import load_dotenv
from exceptions import BadUserData
from notification import NotificationService


basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, "dev.env"))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Parser for notification.")
    parser.add_argument("--user", type=str, help="user data")
    parser.add_argument("--subject", help="subject for mail")
    parser.add_argument("--message", help="message")
    args = parser.parse_args()

    try:
        user_data = json.loads(args.user)
    except json.decoder.JSONDecodeError as ex:
        raise BadUserData(f"{args.user} wrong data. {repr(ex)}")

    service = NotificationService(user_data)

    service.notify_user(args.subject, args.message)
