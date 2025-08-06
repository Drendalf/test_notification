import smtplib
from dataclasses import dataclass
import os


@dataclass
class EmailSender:
    email_host: str = os.environ['EMAIL_HOST']
    email_port: int = os.environ['EMAIL_PORT']
    email_user: str = os.environ['EMAIL_USER']
    email_password: str = os.environ['EMAIL_PASSWORD']


    def send_email(self, email_recipient:str, subject:str, message:str)->bool:
        try:
            with smtplib.SMTP(self.email_host, self.email_port) as server:
                server.starttls()
                server.login(self.email_user, self.email_password)
                server.sendmail(self.email_user, email_recipient, f'Subject: {subject}\n\n{message}')
            return True
        except Exception as e:
            print(f'Ошибка отправки письма: {e}')
            return False