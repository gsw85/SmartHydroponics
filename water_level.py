from gpiozero import Button
from time import sleep


button = Button(26)

def get_water_level():
    # if(button.value == 0):
    #     return "Full"

    # if(button.value == 1):
    #     return "Low"

    return button.value
  