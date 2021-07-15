
#!/usr/bin/python
#flowsensor.py
import RPi.GPIO as GPIO
import time, sys
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

FLOW_SENSOR = 21

#GPIO.setmode(GPIO.BCM)
#GPIO.setup(FLOW_SENSOR, GPIO.IN, pull_up_down = GPIO.PUD_UP)

global count
count = 0
global start_counter

def countPulse(channel):
   global count 
   if start_counter == 1:
        count = count+1
        #print(count)
        #flow = count / (60 * 7.5)
        #print(flow)

def get_water_flow():

    try:
   
        GPIO.setup(FLOW_SENSOR, GPIO.IN, pull_up_down = GPIO.PUD_UP)

        global start_counter
        global count 
    
        GPIO.add_event_detect(FLOW_SENSOR, GPIO.FALLING, callback=countPulse)
        start_counter = 1
        time.sleep(1)
        start_counter = 0
        flow = (count * 60 * 2.25 / 1000)
        #print("The flow is: %.3f Liter/min" % (flow))
        count = 0
        time.sleep(2)
        GPIO.cleanup(FLOW_SENSOR)
        
    except:
    
        pass

        flow = 0

#while True:

    #GPIO.input(FLOW_SENSOR, GPIO.LOW)   
    return flow