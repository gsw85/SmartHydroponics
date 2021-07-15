import yaml
import time
import json
import os
from ads import Analog
from send_data import ThingsboardAPI

dir_path = os.path.dirname(os.path.realpath(__file__)) + '/config.yaml'

ph_calibrate_button = {'calibrate_ph_status': False}
ec_calibrate_button = {'calibrate_ec_status': False}
ph_calibrate_indicator = {'ph_calibrate_indicator': False}
ec_calibrate_indicator = {'ec_calibrate_indicator': False}
#message = {'pH_message': '', 'ec_message': ''}
ph_calibrate_track = 0
ec_calibrate_track = 0  
reset = False

analog = Analog()
api = ThingsboardAPI()

def calibration_ph():

    global reset
    
    global ph_calibrate_track
    print("here 1")
    if ph_calibrate_track == 0:
        print("At condition 1")
        api.send_attributes({ 'pH_message': '1. Please clean the pH sensor with distilled water',
                        'calibrate_ph_status': False,
                        'ph_calibrate_indicator': True
                        })
        ph_calibrate_track = 1

    elif ph_calibrate_track == 1:
        print("At condition 2")
        api.send_attributes({ 'pH_message': '2. Please submerge the pH sensor into 4.01 pH solution',
                        'calibrate_ph_status': False
                        })
        ph_calibrate_track = 2

    elif ph_calibrate_track == 2:
        api.send_attributes({ 'pH_message': '3. First calibration start (Please wait)'})
    
        i = 0
        current = 0.0000
        prev = 0.00000
        track = False
        
        while i < 5:
            if(reset == False):
                current = analog.read_raw_ph()
                current_str = str(current)
                prev_str = str(prev) 
                
                j = 0

                for j in range(3):
                    if current_str[j] == prev_str[j]:
                        track = True
                    else:
                        track = False
                        break          
                if(track == True):
                    print("Calibrating...")
                    i = i + 1
                prev = current    
                time.sleep(3)
            else:
                reset = False
                return

        with open(r''+dir_path) as file:
            documents = yaml.full_load(file)

        documents['calibration']['ph']['x'][0] = current

        dict_file = documents

    # # windows
        with open(r''+dir_path, 'w') as file:
            documents = yaml.dump(dict_file, file)
        api.send_attributes({ 'pH_message': 'First calibration completed',
                        'calibrate_ph_status': False
                        })
        ph_calibrate_track = 3

    elif ph_calibrate_track == 3:
        api.send_attributes({ 'pH_message': '4. Please clean the pH sensor with distilled water',
                        'calibrate_ph_status': False
                    })
        ph_calibrate_track = 4

    elif ph_calibrate_track == 4:

        api.send_attributes({ 'pH_message': '5. Please submerge the pH sensor into 9.18 pH solution',
                    'calibrate_ph_status': False
                })
        ph_calibrate_track = 5


    elif ph_calibrate_track == 5:
        api.send_attributes({ 'pH_message': '6. Second calibration start (Please wait)' 
                })

        i = 0
        current = 0.0000
        prev = 0.00000
        track = False
        
        while i < 5:
            if(reset == False):
                current = analog.read_raw_ph()
                current_str = str(current)
                prev_str = str(prev)
                j = 0

                for j in range(3):
                    if current_str[j] == prev_str[j]:
                        track = True
                    else:
                        track = False
                        break          
                if(track == True):
                    print("Calibrating...")
                    i = i + 1

                prev = current
                time.sleep(3)
            
            else:
                reset = False
                return
            
        with open(r''+dir_path) as file:
            documents = yaml.full_load(file)

        documents['calibration']['ph']['x'][1] = current
        0.2331
        documents['calibration']['ph']['m'][0] = (documents['calibration']['ph']['y'][0] - documents['calibration']['ph']['y'][1]) / (documents['calibration']['ph']['x'][0] - documents['calibration']['ph']['x'][1])
        documents['calibration']['ph']['c'][0] = documents['calibration']['ph']['y'][0] - (documents['calibration']['ph']['m'][0] * documents['calibration']['ph']['x'][0])
        
        dict_file = documents
    # # windows
        with open(r''+dir_path, 'w') as file:
            documents = yaml.dump(dict_file, file)

        api.send_attributes({ 'pH_message': 'Second calibration completed',
                'calibrate_ph_status': False,
                'ph_calibrate_indicator': False
            })
            
        ph_calibrate_track = 0
        time.sleep(2)

        api.send_attributes({ 'pH_message': 'Press calibrate pH button to start calibration'
            })
  


def calibration_ec():

    global reset

    global ec_calibrate_track
    print("here 1")
    if ec_calibrate_track == 0:
        print("At condition 1")
        api.send_attributes({ 'ec_message': '1. Please clean the ec sensor with distilled water',
                        'calibrate_ec_status': False,
                        'ec_calibrate_indicator': True
                        })
        ec_calibrate_track = 1

    elif ec_calibrate_track == 1:
        print("At condition 2")
        api.send_attributes({ 'ec_message': '2. Please submerge the ec sensor into 84 us/cm solution',
                        'calibrate_ec_status': False
                        })
        ec_calibrate_track = 2

    elif ec_calibrate_track == 2:
        api.send_attributes({ 'ec_message': '3. First calibration start (Please wait)'})
        
        i = 0
        current = 0.0000
        prev = 0.00000
        track = False
        
        while i < 5:
            if(reset == False):
                current = analog.read_raw_ec()
                current_str = str(current)
                prev_str = str(prev)
                
                j = 0

                for j in range(3):
                    if current_str[j] == prev_str[j]:
                        track = True
                    else:
                        track = False
                        break          
                if(track == True):
                    print("Calibrating...")
                    i = i + 1
                prev = current    
                time.sleep(3)

            else:
                reset = False
                return

        with open(r''+dir_path) as file:
            documents = yaml.full_load(file)

        documents['calibration']['ec']['x'][0] = current

        dict_file = documents

    # # windows
        with open(r''+dir_path, 'w') as file:
            documents = yaml.dump(dict_file, file)
        api.send_attributes({ 'ec_message': 'First calibration completed',
                        'calibrate_ec_status': False
                        })
        ec_calibrate_track = 3

    elif ec_calibrate_track == 3:
        api.send_attributes({ 'ec_message': '4. Please clean the ec sensor with distilled water',
                        'calibrate_ec_status': False
                    })
        ec_calibrate_track = 4

    elif ec_calibrate_track == 4:

        api.send_attributes({ 'ec_message': '5. Please submerge the ec sensor into 1443 uS/cm solution',
                    'calibrate_ec_status': False
                })
        ec_calibrate_track = 5


    elif ec_calibrate_track == 5:
        api.send_attributes({ 'ec_message': '6. Second calibration start (Please wait)' 
                })

        i = 0
        current = 0.0000
        prev = 0.00000
        track = False
        
        while i < 5:
            if(reset == False):
                current = analog.read_raw_ec()
                current_str = str(current)
                prev_str = str(prev)
                j = 0

                for j in range(3):
                    if current_str[j] == prev_str[j]:
                        track = True
                    else:
                        track = False
                        break          
                if(track == True):
                    print("Calibrating...")
                    i = i + 1

                prev = current
                time.sleep(3)

            else:
                reset = False
                return
            
        with open(r''+dir_path) as file:
            documents = yaml.full_load(file)

        documents['calibration']['ec']['x'][1] = current
        documents['calibration']['ec']['m'][0] = (documents['calibration']['ec']['y'][0] - documents['calibration']['ec']['y'][1]) / (documents['calibration']['ec']['x'][0] - documents['calibration']['ec']['x'][1])
        documents['calibration']['ec']['c'][0] = documents['calibration']['ec']['y'][0] - (documents['calibration']['ec']['m'][0] * documents['calibration']['ec']['x'][0])
        
        dict_file = documents

        with open(r''+dir_path, 'w') as file:
            documents = yaml.dump(dict_file, file)

        api.send_attributes({ 'ec_message': 'Second calibration completed',
                'calibrate_ec_status': False,
                'ec_calibrate_indicator': False
            })
            
        ec_calibrate_track = 0
        time.sleep(2)

        api.send_attributes({ 'ec_message': 'Press calibrate ec button to start calibration'
            })
  
def reset_calibration():
    global ph_calibrate_track, ec_calibrate_track,reset

    reset = True
    ph_calibrate_track = 0
    ec_calibrate_track = 0 

    api.send_attributes({ 'ec_message': 'Press calibrate ec button to start calibration',
                    'pH_message': 'Press calibrate pH button to start calibration',
                    'ph_calibrate_indicator': False, 
                    'ec_calibrate_indicator': False
                    })
