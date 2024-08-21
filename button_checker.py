import RPi.GPIO as GPIO
import time


class ButtonChecker:
    def __init__(self, pin: int):
        self.pin = pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    def is_pressed(self):
        return GPIO.input(self.pin) == GPIO.HIGH

