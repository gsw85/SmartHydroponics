
import sys
import os
import random
import time
import json

sys.path.insert(0, './plant_yolov5_pi')
sys.path.insert(0, './pest_yolov5_pi')

from intensity import get_light_intensity
from ads import Analog
from temp_hum import Aht15
from water_flow import get_water_flow
from water_level import  get_water_level
from control import Control
from file import File
from timestamp import get_timestamp
from send_data import ThingsboardAPI
from plant_yolov5_pi import detect as disease
from pest_yolov5_pi import detect as pest
from crop_growth.inference import CropGrowth
from variable import * 


a = Analog()
aht15 = Aht15()
# light = Control(23)
api = ThingsboardAPI()
growth = CropGrowth()

sensor_data = {'temperature': 0, 'humidity': 0, 'water_pH': 0, 'water_temp': 0, 'light_intensity': 0, 'ec': 0, 'ec_gain': 0, 'water_level':"", 'water_flow': 0}
# control = {'light_enabled': False, 'ac_enabled': False, 'water_enabled': False, 'nutrient_enabled_a': False, 'nutrient_enabled_b': False, 'ph_down_pump_enabled': False}


light_button = {'light_enabled': False}
ac_button = {'ac_enabled': False}
water_pump_button = {'water_enabled': False}
nutrient_pump_a_button = {'nutrient_enabled_a': False}
nutrient_pump_b_button = {'nutrient_enabled_b': False}
ph_down_pump_button = {'ph_down_pump_enabled': False}

now = None
time_track = 0
ph_down_flag = False
ec_flag = False

def send_telementry(client):
    global time_track
    global ec_flag
    global ph_down_flag
   
    
    while True:

            if(thread_status()):
                print("Stop telementry")
                client.loop_stop()
                client.disconnect()
                break
        # try:
            print("sending data to thingsboard")
            documents = File.read_file()

            humidity = aht15.get_humid()
            temperature = aht15.get_temp()
            # humidity = random.randrange(45, 65)	
            # temperature = random.randrange(26, 32)	
            water_pH = a.get_ph()
            water_temp = a.read_temp()
            ec_gain = a.get_ec_gain() 
            ec = a.get_ec() 
            water_level = get_water_level()  
            water_flow = get_water_flow()        
            light_intensity = get_light_intensity()
            
            
            
            if((get_timestamp() - documents['detection']['timestamp']) > 600):
                plant_disease_info = disease.perform_disease_detection()
                pest_info = pest.perform_pest_detection()
                print('Prediction result', plant_disease_info, pest_info)
                growth_info = growth.perform_plant_growth_prediction()
                api.send_attributes({'growth_info' : growth_info})
                api.send_attributes({'plant_disease_info': plant_disease_info})
                api.send_attributes({'pest_info': pest_info})
                api.send_image()
                documents['detection']['timestamp'] = get_timestamp()


            # if (get_timestamp() - documents['timestamp'][0] > 180):
            print("controlling device")

            # if (documents['data']['ec'][0] < 1000.0) and (documents['data']['ec'][1] < 1000.0) and (documents['data']['ec'][2] < 1000.0):
            #     if(ec_flag):
            #         if(get_timestamp() - documents['ph_flag_timestamp'] > 300):
            #             nutrient_pump_a_button['nutrient_enabled_a'] = True
            #             nutrient_pump_b_button['nutrient_enabled_b'] = True
            #             api.send_attributes(nutrient_pump_a_button)
            #             api.send_attributes(nutrient_pump_b_button)
            #             time.sleep(7)
            #             nutrient_pump_a_button['nutrient_enabled_a'] = False
            #             nutrient_pump_b_button['nutrient_enabled_b'] = False
            #             api.send_attributes(nutrient_pump_a_button)
            #             api.send_attributes(nutrient_pump_b_button)

            #     else:
            #         ec_flag = True
            #         nutrient_pump_a_button['nutrient_enabled_a'] = True
            #         nutrient_pump_b_button['nutrient_enabled_b'] = True
            #         api.send_attributes(nutrient_pump_a_button)
            #         api.send_attributes(nutrient_pump_b_button)
            #         time.sleep(7)
            #         nutrient_pump_a_button['nutrient_enabled_a'] = False
            #         nutrient_pump_b_button['nutrient_enabled_b'] = False
            #         api.send_attributes(nutrient_pump_a_button)
            #         api.send_attributes(nutrient_pump_b_button) 
            #         documents['ph_flag_timestamp']  = get_timestamp()              
            # else:
            #     nutrient_pump_a_button['nutrient_enabled_a'] = False
            #     nutrient_pump_b_button['nutrient_enabled_b'] = False
            #     api.send_attributes(nutrient_pump_a_button)
            #     api.send_attributes(nutrient_pump_b_button) 
            #     ec_flag = False


            if (documents['data']['ph'][0] > 6.5) and (documents['data']['ph'][1] > 6.5) and (documents['data']['ph'][2] > 6.5):
                if(ph_down_flag):
                    if(get_timestamp() - documents['ph_flag_timestamp'] > 300):
                        ph_down_pump_button['ph_down_pump_enabled'] = True
                        api.send_attributes(ph_down_pump_button)
                        time.sleep(0.5) # ~0.6ml
                        ph_down_pump_button['ph_down_pump_enabled'] = False
                        api.send_attributes(ph_down_pump_button)
                else:
                    ph_down_flag = True
                    ph_down_pump_button['ph_down_pump_enabled'] = True
                    api.send_attributes(ph_down_pump_button)
                    time.sleep(0.5)
                    ph_down_pump_button['ph_down_pump_enabled'] = False
                    api.send_attributes(ph_down_pump_button)     

                documents['ph_flag_timestamp'] = get_timestamp()               
            else:
                ph_down_flag = False
                ph_down_pump_button['ph_down_pump_enabled'] = False
                api.send_attributes(ph_down_pump_button)    
                


            if (documents['data']['light_intensity'][0] < 1000) and (documents['data']['light_intensity'][1] < 1000) and (documents['data']['light_intensity'][2] < 1000):
                documents['timer']['light_intensity']['initial'][0] = get_timestamp()
                documents['timer']['light_intensity']['timer_status'][0] = 1
                light_button['light_enabled'] = True
                # light.on()
                api.send_attributes(light_button)  
            else:
                if(documents['timer']['light_intensity']['timer_status'][0] == 1):
                    if(get_timestamp() - documents['timer']['light_intensity']['initial'][0] > 1800):
                        light_button['light_enabled'] = False
                        documents['timer']['light_intensity']['timer_status'][0] = 0
                        # light.off()
                        api.send_attributes(light_button)  
                else:
                        # light.off()
                        print("light off")
            
            if (documents['data']['water_temp'][0] > 27) and (documents['data']['water_temp'][1] > 27) and (documents['data']['water_temp'][2] > 27):
                ac_button['ac_enabled'] = True
                api.send_attributes(ac_button)  
            else:
                ac_button['ac_enabled'] = False
                api.send_attributes(ac_button)  
            
            # documents['timestamp'][0] = get_timestamp()
        
            # api.send_attributes(control)


            sensor_data['temperature'] = temperature
            sensor_data['humidity'] = humidity
            sensor_data['water_pH'] = water_pH
            sensor_data['water_temp'] = water_temp
            sensor_data['light_intensity'] = light_intensity
            sensor_data['ec'] = ec
            sensor_data['ec_gain'] = ec_gain
            sensor_data['water_level'] = water_level
            sensor_data['water_flow'] = water_flow
            
            # Sending all sensor data to ThingsBoard telemetry
            api.send_telementry(sensor_data)
            # client.publish('v1/devices/me/telemetry', json.dumps(sensor_data), 1)
           
 
            # Store 3 value to file with 1 minute interval
            if (get_timestamp() - documents['data']['data_timestamp']) > 60:
                print("save value to file ", time_track)
                documents['data']['temp'][time_track] = temperature
                documents['data']['humidity'][time_track] = humidity
                documents['data']['ph'][time_track] = water_pH
                documents['data']['water_temp'][time_track] = water_temp
                documents['data']['light_intensity'][time_track] = light_intensity
                documents['data']['water_level'][time_track] = water_level
                documents['data']['water_flow'][time_track] = water_flow
                documents['data']['ec'][time_track] = ec

                documents['data']['data_timestamp'] = get_timestamp()

                time_track = time_track + 1

                if  time_track == 3:
                    time_track = 0

            dict_file = documents
            File.write_file(dict_file, documents)

        # except KeyboardInterrupt:
        #     break