import time
import board
import adafruit_bh1750

i2c = board.I2C()
def get_light_intensity():
    i = 0
    total = 0
    while i < 10:
        sensor = adafruit_bh1750.BH1750(i2c)
        total = total + sensor.lux
        #print("%.2f Lux" % sensor.lux)
        i = i + 1
        time.sleep(0.2)
        value = total / 10
    return value

#print("Final %.2f Lux" % get_light_intensity())
#print(get_light_intensity())    

    
    
    
    
    
    