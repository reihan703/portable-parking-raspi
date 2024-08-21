import socket
from datetime import datetime
import random
import string
from time import sleep
import requests
import os
from dotenv import load_dotenv


class TicketDispenser():
    def __init__(self) -> None:
        self.web_address = os.getenv('WEBAPP_ADDRESS')
        self.web_port = os.getenv('WEBAPP_PORT')
        self.web_hook = os.getenv('WEBAPP_HOOK')
        self.url = f'http://{self.web_address}:{self.web_port}/{self.web_hook}'
        self.ip = self.get_current_ip()

    def send_event_to_webapp(self, data) -> None:
        response = requests.post(self.url, json=data)
        print(f'Response: {response.status_code}, {response.text}')

    def generate_random_string(self) -> str:
        letters = string.ascii_letters + string.digits
        return ''.join(random.choice(letters) for i in range(16))

    def get_current_ip(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            # This doesn't need to actually connect to anything, just to pick the correct interface
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
        except Exception:
            ip = "127.0.0.1"
        finally:
            s.close()
        return ip

    def prepare_payload(self) -> dict:
        now = datetime.now()
        created_at = now.strftime('%Y-%m-%d %H:%M')
        transaction_id = self.generate_random_string()
        local_port = os.getenv("LOCAL_PORT")
        ip_address = self.ip

        image_path = f"http://{ip_address}:{local_port}/images/{transaction_id}.jpeg"
        data = {
            "event": "create_transaction",
            "transaction_id": transaction_id,
            "location_id": os.getenv('LOCATION_ID'),
            "image_path": image_path,
            "vehicle_code": os.getenv('VEHICLE_CODE_1'),
            "created_at": created_at,
        }
        return data

    def execute(self):
        # Send data to webapp
        data = self.prepare_payload()
        self.send_event_to_webapp(data=data)


if __name__ == "__main__":
    # get env
    load_dotenv()
    dispenser = TicketDispenser()
    while True:
        dispenser.execute()
        sleep(.3)
