# from tb_device_mqtt import TBDeviceMqttClient, TBPublishInfo

# class Data_Transfer:
#     client = None
#     def __init__(self, attributes):
#         try:
#             self.client = TBDeviceMqttClient("192.168.100.45", "syeLgLufPBBLAiRT5cxo")

#             self.client.connect()

#             self.client.send_attributes(attributes)

#             result = self.client.send_attributes(attributes)
#             print(result)
#             self.client.disconnect()
#         except:
#             pass
import requests
import base64
from file import File
from variable import * 
# file = File()

class ThingsboardAPI:

    def send_attributes(self, data):
        
        url = 'http://' + File.get_host() + ':' + '8080/api/v1/' + File.get_token() + '/attributes'

        try:
            requests.post(url, json = data)
        except:
            stop_thread()
            pass


    def send_telementry(self, data):

        url = 'http://' + File.get_host() + ':' + '8080/api/v1/' + File.get_token() + '/telemetry'
        
        try:
            requests.post(url, json = data)
        except:
            stop_thread()
            pass

    def send_image(self):

        with open("plant_yolov5_pi/runs/detect/exp/disease-detection.jpg", "rb") as img_file:
            my_string_64 = base64.b64encode(img_file.read())

        my_string = my_string_64.decode('utf-8')

        self.send_attributes({'disease_prediction_image': my_string})

        with open("pest_yolov5_pi/runs/detect/exp/pest_detection.jpg", "rb") as img_file:
            my_string_64 = base64.b64encode(img_file.read())

        my_string = my_string_64.decode('utf-8')

        self.send_attributes({'pest_prediction_image': my_string})

        with open("crop_growth/seg_image.jpg", "rb") as img_file:
            my_string_64 = base64.b64encode(img_file.read())

        my_string = my_string_64.decode('utf-8')

        self.send_attributes({'size_prediction_image': my_string})        
