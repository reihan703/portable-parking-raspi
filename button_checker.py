import RPi.GPIO as GPIO
from gpiozero import DigitalInputDevice


class ButtonChecker:
    def __init__(self, pin: int):
        self.pin = pin
        # GPIO.setmode(GPIO.BCM)
        # GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        self.button = DigitalInputDevice(pin=self.pin, pull_up=True)

    # def is_pressed(self):
    #     return GPIO.input(self.pin) == GPIO.HIGH
    def is_pressed(self):
        if self.button.is_active:
            return True
        return False

