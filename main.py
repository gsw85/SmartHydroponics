import os
import sys
import json
import paho.mqtt.client as mqtt
import threading
import time
import sched
from telementry import send_telementry
from calibration_sensor import calibration_ph, calibration_ec, reset_calibration
from control import Control
from file import File
from variable import * 
import RPi.GPIO as GPIO
from send_data import ThingsboardAPI

s = sched.scheduler(time.time, time.sleep)
api = ThingsboardAPI()
# THINGSBOARD_HOST = 'localhost'
# ACCESS_TOKEN = 'JgtDl18UwIB9Wwts3SlT'

light_button = {'light_enabled': False}
ac_button = {'ac_enabled': False}
water_pump_button = {'water_enabled': False}
nutrient_pump_a_button = {'nutrient_enabled_a': False}
nutrient_pump_b_button = {'nutrient_enabled_b': False}
ph_down_pump_button = {'ph_down_pump_enabled': False}
ph_calibrate_button = {'calibrate_ph_status': False}
ec_calibrate_button = {'calibrate_ec_status': False}
reset_calibrate_button = {'reset_calibrate_button': False}
message = {'pH_message': '', 'ec_message': '', 'ph_calibrate_indicator': False, 'ec_calibrate_indicator': False}

#light = Control(23)
#ac = Control(18)
nutrient = Control(24)
water_pump = Control(18)

def timer(attr = None,control = None):
    time.sleep(2.5)
    
    api.send_attributes(attr)

    if(control):    
        control.off()
        print("OFF")


def set_light_value (params):
    light_button['light_enabled'] = params
    if light_button['light_enabled'] == True:
        print("LED light status : ON")
        #light.on()
        
    else:
        print("LED light status : OFF")
        #light.off()
        
def set_ac_value (params):
    ac_button['ac_enabled'] = params
    if ac_button['ac_enabled'] == True:
        print("AC status : ON")
        #ac.on()
    else:
        print("AC status : OFF")
        #ac.off()

def set_water_pump_value (params):
    water_pump_button['water_enabled'] = params
    if water_pump_button['water_enabled'] == True:
        print("Water Pump status : ON")
        water_pump.on()
    else:
        print("Water Pump status : OFF")
        water_pump.off()

def set_nutrient_pump_a_value (params):
    global s
    global api
    
    nutrient_pump_a_button['nutrient_enabled_a'] = params

    if nutrient_pump_a_button['nutrient_enabled_a'] == True:
        print("Nutrient pump A status : ON")
        # turn on nutrient pump
        nutrient.on()

        t = threading.Thread(target = timer, args = ({'nutrient_enabled_a': False}, nutrient,))
        t.start()
    else:
        print("Nutrient pump A status : OFF")      
        nutrient.off()

def set_nutrient_pump_b_value (params):
    nutrient_pump_b_button['nutrient_enabled_b'] = params
    if nutrient_pump_b_button['nutrient_enabled_b'] == True:
        print("Nutrient pump B status : ON") 
        # nutrient_pump_b_button['nutrient_enabled_b'] = False
        t = threading.Thread(target = timer, args = ({'nutrient_enabled_b': False},))
        t.start()
    else:
        print("Nutrient pump B status : OFF")      

def set_ph_down_pump_value (params):
    sc = sched.scheduler(time.time, time.sleep)
    global api
    
    ph_down_pump_button['ph_down_enabled'] = params
    if ph_down_pump_button['ph_down_enabled'] == True:
        print("Nutrient pump B status : ON") 
        t = threading.Thread(target = timer, args = ({'ph_down_enabled': False},))
        t.start()

    else:
        print("Nutrient pump B status : OFF")    


def set_calibrate_ph (params):
  
    ph_status = json.loads(params)

    ph_calibrate_button["calibrate_ph_status"]  = ph_status["calibrate_ph_status"]

    if ph_calibrate_button["calibrate_ph_status"] == True:
        x = threading.Thread(target = calibration_ph)
        x.start()

def set_calibrate_ec (params):
    
    ec_status = json.loads(params)
    # print(y)
    ec_calibrate_button["calibrate_ec_status"]  = ec_status["calibrate_ec_status"]

    if ec_calibrate_button["calibrate_ec_status"] == True:
        print("inside threading")
        x = threading.Thread(target = calibration_ec)
        x.start()

def reset_calibrate (params):
    reset_calibrate_status = json.loads(params)
    # print(y)
    reset_calibrate_button["reset_calibrate_button"]  = reset_calibrate_status["reset_calibrate_button"]

    if reset_calibrate_button["reset_calibrate_button"] == True:
        print("inside threading")
        x = threading.Thread(target = reset_calibration, args = ())
        x.start()

   
# MQTT on_connect callback function
def on_connect(client, userdata, flags, rc):
# ac = Control(18)flags, rc):
    client.subscribe('v1/devices/me/attributes')
    client.subscribe('v1/devices/me/rpc/request/+')
    
# MQTT on_message caallback function
def on_message(client, userdata, msg):
    if msg.topic.startswith('v1/devices/me/rpc/request/'):
        requestId = msg.topic[len('v1/devices/me/rpc/request/'):len(msg.topic)]
        data = json.loads(msg.payload)
        
        # Light RPC
        if data['method'] == 'get_light_value':
            client.publish('v1/devices/me/rpc/response/'+requestId, json.dumps(light_button), 1)
        if data['method'] == 'set_light_value':
            params = data['params']
            set_light_value(params)
            client.publish('v1/devices/me/attributes', json.dumps(light_button), 1)

        # AC RPC
        if data['method'] == 'get_ac_value':
            client.publish('v1/devices/me/rpc/response/'+requestId, json.dumps(ac_button), 1)

        if data['method'] == 'set_ac_value':
    
            params = data['params']
            set_ac_value(params)
            client.publish('v1/devices/me/attributes', json.dumps(ac_button), 1) 

        # Water Pump RPC
        if data['method'] == 'get_water_pump':
            client.publish('v1/devices/me/rpc/response/'+requestId, json.dumps(water_pump_button), 1)

        if data['method'] == 'set_water_pump':
            params = data['params']
            set_water_pump_value(params)
            client.publish('v1/devices/me/attributes', json.dumps(water_pump_button), 1) 

        #Nutrient Pump RPC
        if data['method'] == 'get_nutrient_pump_a':
            client.publish('v1/devices/me/rpc/response/'+requestId, json.dumps(nutrient_pump_a_button), 1)

        if data['method'] == 'set_nutrient_pump_a':
            params = data['params']
            set_nutrient_pump_a_value(params)
            client.publish('v1/devices/me/attributes', json.dumps(nutrient_pump_a_button), 1) 

        if data['method'] == 'get_nutrient_pump_b':
            client.publish('v1/devices/me/rpc/response/'+requestId, json.dumps(nutrient_pump_b_button), 1)

        if data['method'] == 'set_nutrient_pump_b':
            params = data['params']
            set_nutrient_pump_b_value(params)
            client.publish('v1/devices/me/attributes', json.dumps(nutrient_pump_b_button), 1) 

        if data['method'] == 'get_ph_down_pump':
            client.publish('v1/devices/me/rpc/response/'+requestId, json.dumps(ph_down_pump_button), 1)

        if data['method'] == 'set_ph_down_pump':
            params = data['params']
            set_ph_down_pump_value(params)
            client.publish('v1/devices/me/attributes', json.dumps(ph_down_pump_button), 1) 

        #ph calibrate 1
        if data['method'] == 'get_ph_calibration':
            client.publish('v1/devices/me/rpc/response/'+requestId, json.dumps(ph_calibrate_button), 1)

        if data['method'] == 'set_ph_calibration':
            params = data['params']
            set_calibrate_ph(params)
            client.publish('v1/devices/me/attributes', json.dumps(ph_calibrate_button), 1) 

        #ec calibrate 1
        if data['method'] == 'get_ec_calibration':
            client.publish('v1/devices/me/rpc/response/'+requestId, json.dumps(ec_calibrate_button), 1)

        if data['method'] == 'set_ec_calibration':
            params = data['params']
            set_calibrate_ec(params)
            client.publish('v1/devices/me/attributes', json.dumps(ec_calibrate_button), 1) 

        if data['method'] == 'get_reset_calibrate_button':
            client.publish('v1/devices/me/rpc/response/'+requestId, json.dumps(ec_calibrate_button), 1)

        if data['method'] == 'set_reset_calibrate_button':
            params = data['params']
            reset_calibrate(params)
            client.publish('v1/devices/me/attributes', json.dumps(ec_calibrate_button), 1) 

def setup():

    print("System are starting")

    try:
        # Thingsboard platform credentials
        THINGSBOARD_HOST = File.get_host()
        ACCESS_TOKEN = File.get_token()
        # start the client instance
        client = mqtt.Client()

        # registering the callbacks
        client.on_connect = on_connect
        client.on_message = on_message

        client.username_pw_set(ACCESS_TOKEN)
        client.connect(THINGSBOARD_HOST,1883,60)

        message['pH_message'] = "Press calibrate pH button to start calibration"
        message['ec_message'] = "Press calibrate EC button to start calibration"

        client.publish('v1/devices/me/attributes', json.dumps(message), 1)


        x = threading.Thread(target = send_telementry, args = (client,))
        x.start()
        client.loop_forever()   
        
        if (thread_state()):
            print("Fail to connect")
            stop_thread()
            return False

    except KeyboardInterrupt:
        stop_thread()
        # x.join()
        GPIO.cleanup()
        client.disconnect()
        return True

    except:
        print("Fail to connect")
        stop_thread()
        client.disconnect()
        # x.join()
        return False

while True:
    start_thread()
    
    status = setup()

    if(status == True):
        print("System are shutting down")
        break
    
    if(status == False):
        print("Reconnect")

    time.sleep(5)




