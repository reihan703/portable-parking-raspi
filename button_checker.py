from gpiozero import Button


class ButtonChecker:
    def __init__(self, pin: int):
        self.pin = pin
        self.button = Button(pin=self.pin)

    def is_pressed(self):
        return self.button.is_pressed

