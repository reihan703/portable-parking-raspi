import socket
from datetime import datetime
import random
import string
from time import sleep
import requests
import os
from dotenv import load_dotenv
from gpiozero import Button

from button_checker import ButtonChecker
from camera import Camera
from printer import Printer


class TicketDispenser():
    def __init__(self) -> None:
        # get env
        load_dotenv()
        self.web_address = os.getenv('WEBAPP_ADDRESS')
        self.web_port = os.getenv('WEBAPP_PORT')
        self.web_hook = os.getenv('WEBAPP_HOOK')
        self.vendor_id = os.getenv('VENDOR_ID')
        self.product_id = os.getenv('PRODUCT_ID')
        self.button_pin_1 = int(os.getenv('BUTTON_PIN_1'))
        self.button_pin_2 = int(os.getenv('BUTTON_PIN_2'))

        self.url = f'http://{self.web_address}:{self.web_port}/{self.web_hook}'
        self.ip = self.get_current_ip()

        # define button
        self.button1 = ButtonChecker(self.button_pin_1)
        self.button2 = ButtonChecker(self.button_pin_2)

        # define printer
        self.printer = Printer(vendor_id=self.vendor_id,
                               product_id=self.product_id)

        # define camera
        self.camera = Camera()

        # define the vehicle
        self.vehicle_code_1 = os.getenv('VEHICLE_CODE_1')
        self.vehicle_code_2 = os.getenv('VEHICLE_CODE_2')

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

    def prepare_payload(self, random_transaction_id, vehicle_code, created_time) -> dict:
        created_at = created_time.strftime('%Y-%m-%d %H:%M')
        transaction_id = random_transaction_id
        local_port = os.getenv("LOCAL_PORT")
        ip_address = self.ip

        image_path = f"http://{ip_address}:{local_port}/images/{transaction_id}.jpeg"
        data = {
            "event": "create_transaction",
            "transaction_id": transaction_id,
            "location_id": os.getenv('LOCATION_ID'),
            "image_path": image_path,
            "vehicle_code": vehicle_code,
            "created_at": created_at,
        }
        return data

    def execute(self):
        vehicle_code = self.vehicle_code_1
        if self.button1.is_pressed():
            vehicle_code = self.vehicle_code_1
        elif self.button2.is_pressed():
            vehicle_code = self.vehicle_code_2
        else:
            # Nothing was pressed
            return

        # generate transaction id
        transaction_id = self.generate_random_string()
        # create string date time
        now = datetime.now()
        created_time = now.strftime('%Y-%m-%d %H:%M:%S')

        try:
            # Print ticket
            self.printer.print_ticket(transaction_id=transaction_id, vehicle_code=vehicle_code, created_time=created_time)
        except Exception as e:
            print(f"Failed to print, transaction invalid: {e}")
            return
        # Capture image
        self.camera.capture(transaction_id=transaction_id)

        # Send data to webapp
        data = self.prepare_payload(
            random_transaction_id=transaction_id, vehicle_code=vehicle_code, created_time=now)
        self.send_event_to_webapp(data=data)


if __name__ == "__main__":
    dispenser = TicketDispenser()
    while True:
        dispenser.execute()
        sleep(3)
