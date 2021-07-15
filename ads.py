from time import sleep
import board
import busio
import math
import yaml
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

i2c = busio.I2C(board.SCL, board.SDA)
ads = ADS.ADS1115(i2c)


class Analog:
    
    current_nutrient = None
    initial = True
    
    def steinhart_temperature_C(self, r):
        Ro=100000.0 
        To=25.0
        beta=3950.0
       
    
        steinhart = math.log(r / Ro) / beta      # log(R/Ro) / beta

        steinhart += 1.0 / (To + 273.15)         # log(R/Ro) / beta + 1/To
        steinhart = (1.0 / steinhart) - 273.15   # Invert, convert to C
        return steinhart

    def read_temp(self):
        temp = AnalogIn(ads, ADS.P2)
        value = temp.value

        try:
            R = (100000 / (65535/value - 1)) 
        except ZeroDivisionError:
            pass
            R = 1

        actual_temp = self.steinhart_temperature_C(R) - 65
        return actual_temp
    

    def read_raw_ph(self):
        voltage = AnalogIn(ads, ADS.P0)
       
        return voltage.voltage

    def read_raw_ec(self):

        voltage = AnalogIn(ads,ADS.P1)

        return voltage.voltage

    def get_ph(self):
        with open(r'/home/pi/Desktop/hydroponic/config.yaml') as file:
            documents = yaml.full_load(file)
        
        raw_ph = self.read_raw_ph()
        m = documents['calibration']['ph']['m'][0]
        c = documents['calibration']['ph']['c'][0]

        ph = (m * raw_ph) + c
        return ph 

    def get_ec(self):

        with open(r'/home/pi/Desktop/hydroponic/config.yaml') as file:
            documents = yaml.full_load(file)

        m = documents['calibration']['ec']['m'][0]
        c = documents['calibration']['ec']['c'][0]

        ec_list = []
        i = 0 

        while(i != 10):
            
            raw_ec = self.read_raw_ec()
            ec = (m * raw_ec) + c
            ec_list.append(ec)
            i = i + 1
            sleep(0.2)

        average_ec = sum(ec_list) / len(ec_list)

        if average_ec < 0:
            average_ec = 0

        return average_ec

    def get_ec_gain(self):

        with open(r'/home/pi/Desktop/hydroponic/config.yaml') as file:
            documents = yaml.full_load(file)

        m = documents['calibration']['ec']['m'][0]
        c = documents['calibration']['ec']['c'][0]

        voltage = self.read_raw_ec()

        nutrient = (m * voltage) + c
      
        if (self.initial):
            self.current_nutrient = nutrient
            self.initial = False
        
        else:
            dif = nutrient - self.current_nutrient
            div = dif / 1000
            self.current_nutrient = self.current_nutrient + div

        return self.current_nutrient
         