import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

class Control:
    
    pin = None

    def __init__(self, gpio_pin):
        self.pin = gpio_pin
        GPIO.setup(self.pin, GPIO.OUT)
        GPIO.output(self.pin, True)

    def on(self):
        GPIO.output(self.pin, False)
        

    def off(self):
        GPIO.output(self.pin, True)

    def status(self):
        
        return GPIO.input(self.pin)
    
