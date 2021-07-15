import smbus
import time

class Aht15:
    bus = None
    config = None
    
    def __init__(self):
        self.bus = smbus.SMBus(3)
        self.config = [0x08, 0x00]
        
        self.bus.write_i2c_block_data(0x38, 0xE1, self.config)
        time.sleep(0.5)
        byt = self.bus.read_byte(0x38)
        MeasureCmd = [0x33, 0x00]
        self.bus.write_i2c_block_data(0x38, 0xAC, MeasureCmd)
        time.sleep(0.5)
        
    def get_temp(self):
        data = self.bus.read_i2c_block_data(0x38,0x00)
        temp = ((data[3] & 0x0F) << 16) | (data[4] << 8) | data[5]
        ctemp = ((temp*200) / 1048576) - 50
        return ctemp
       
    def get_humid(self):
        data = self.bus.read_i2c_block_data(0x38,0x00)
        tmp = ((data[1] << 16) | (data[2] << 8) | data[3]) >> 4
        hum = int(tmp * 100 / 1048576)

        return hum

# aht15 = Aht15()
# print(aht15.get_humid(), aht15.get_temp())


