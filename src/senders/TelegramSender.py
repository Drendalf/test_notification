import os
from dataclasses import dataclass

import requests


@dataclass
class TelegramSender:
    TIME_OUT = 5
    telegram_bot_token: str = os.environ["TELEGRAM_BOT_TOKEN"]

    def send_telegram_message(self, chat_id: str, message: str) -> bool:
        try:
            response = requests.post(
                f"https://api.telegram.org/bot{self.telegram_bot_token}/sendMessage",
                json={"chat_id": chat_id, "text": message},
                timeout=self.TIME_OUT,
            )
            if response.status_code != 200:
                raise ValueError("Ошибка отправки сообщения")

            return True
        except Exception as e:
            print(f"Ошибка отправки Telegram-сообщения: {e}")
            return False
