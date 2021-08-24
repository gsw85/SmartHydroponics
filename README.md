# Smart Hydroponic Farm Project
Smart Hydroponic Farm is a smart monitoring system with AI capabilities that are able to monitor plant conditions. This system consists of different types of sensors and cameras to monitor crop conditions. Apart from that, it consists of many AI models such as crops disease and pest detection, crops growth monitoring, and prediction of harvest time.

## Hardware
### 1. Sensors
* [Digital light intensity BH1750FVI sensor module](https://my.cytron.io/p-digital-light-intensity-bh1750fvi-sensor-module?r=1&gclid=CjwKCAiAxp-ABhALEiwAXm6IyS6LFau99xq8_qGCID0IJcsMB-0ZxKfH97uXnc2AfYRs4Ezid7yNPxoCFaoQAvD_BwE)
* [AHT15 temperature humidity Sensor](https://www.aliexpress.com/item/1005002434781439.html)
* [Water pH sensor](https://my.element14.com/dfrobot/sen0169/analogue-ph-sensor-meter-kit-arduino/dp/3517876)
* [NTC weaterproof 10K thermistor](https://shopee.com.my/NTC-Waterproof-Thermistor-1-10K-B3950-XH2.54-1M-i.55645224.6000095733)
* Conductivity sensor (EC)
* [Half effect water flow sensor](https://my.cytron.io/p-g1-2-half-effect-water-flow-sensor-yf-s201?search=water%20flow&description=1)
* [Water float sensor switch](https://my.cytron.io/p-water-float-or-level-sensor-switch)

### 2. Control Hardwares
* [Automatic low noise brushless water pump](https://shopee.com.my/Automatic-Low-Noise-Fountain-Mini-Aquarium-Brushless-With-Filter-DC-12V-Submersible-Water-Pump-i.165012281.4708447960)
* [Mini peristaltic pump](https://shopee.com.my/Kamoer-DC12V-NKP-Mini-Peristaltic-Pump-Water-Pump-Pam-Air-Kecil-Peristaltik--i.53171392.1982360128)
* [Waterproof full spectrum LED strip ](https://www.aliexpress.com/item/1005002434781439.html)
* Thermoelectric cooler
* [Mini brushless submersible water pump](https://shopee.com.my/-VAR-12V-DC-Mini-Brushless-Submersible-Water-Pump-240-L-H-for-Aquarium-Project-i.46042211.1843606969)
* [Raspberry Pi 8MP camera module v2](https://my.cytron.io/p-raspberry-pi-8mp-camera-module-v2?gclid=Cj0KCQiA34OBBhCcARIsAG32uvMfC7waAXCTFaOA7sig0mHfRgelbrT5UfQCn-6spLrDipXLEe0Q9XMaAjoREALw_wcB)


### 3. Other Hardwares
* [Raspberry Pi 4 model B - 8GB ](https://my.cytron.io/p-raspberry-pi-4-model-b?search=raspberry%20pi%204&description=1)
* [4 channels ADS1115 ADC module](https://my.cytron.io/p-4-channels-ads1115-adc-module)
* [2 channel DC 5V relay module](https://my.cytron.io/p-2-channel-dc-5v-relay-module?search=relay&description=1)
* [Meanwell switching power supply 12v](https://shopee.com.my/Meanwell-Mean-Well-LRS-150-150W-12V-24V-AC-DC-Switching-Power-Supply-i.61390848.1218190339)
* [DC-DC voltage regulator adjustable step down module](https://shopee.com.my/LM2596-DC-DC-Voltage-Regulator-Adjustable-Step-Down-Module-w-Display-i.33287405.2148334760)

## Software
### Thingsboard
[ThingsBoard](https://thingsboard.io/) is an open-source IoT platform for data collection, processing, visualization, and device management. All sensors values and AI model prediction result will be send to the Thingsboard dashboard. [Installation instruction.](https://thingsboard.io/docs/user-guide/install/installation-options/)

## Schematic Diagram
![alt text][schematic]

[schematic]: /Assets/schematic.PNG "Thingsboard dashboard"

## Step to Run on Raspberry Pi
### 1. Requirements
```
$ git clone https://github.com/SkymindCNS/SmartHydroponics/tree/test-push
$ pip install -r requirements.txt
$ gdown https://drive.google.com/file/d/1mJsf1OjjnKJ24vBGicuTfT5N0jZBHCvn/view?usp=sharing -O crop_growth/model_final.pth
$ gdown https://drive.google.com/file/d/1Pq-0WogvNwxCh-EMyLkqIr2_3NFvjfaV/view?usp=sharing -O pest_yolov5_pi/best.pt
$ gdown https://drive.google.com/file/d/1FQZKmES3XnjpsPyMxGAG3iyhdRokQY1l/view?usp=sharing -O plant_yolov5_pi/best.pt

```
### 2. Change Configuration File
Open config.yaml file and edit access token and ip address information.
```
thingsboard:
  ACCESS_TOKEN: THINGSBOARD_DEVICE_ID
  THINGSBOARD_HOST: THINGSBOARD_IP_ADDRESS
```
The below image showed steps on how to get device id at Thingsboard

![alt text][device]

[device]: /Assets/Device.PNG "Thingsboard device id"

### 3. Run 
```
$ python main.py
```
## Demo

### 1. Dashboard

![alt text][dashboard]

[dashboard]: /Assets/dashboard.PNG "Thingsboard dashboard"

### 2. Plant Diseases Result

![alt text](/Assets/plant_disease.PNG "Plant disease")

