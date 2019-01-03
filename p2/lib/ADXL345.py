import time

import sys

import pigpio # official ) http://abyz.co.uk/rpi/pigpio/python.html

if sys.version > '3':
   buffer = memoryview

class ADXL345:
    ADXL345_I2C_ADDR=0x1d
    # RUNTIME=60.0
    BUS=1

    def __init__(self):
        self.pi = pigpio.pi() # open local Pi
        self.h = self.pi.i2c_open(self.BUS, self.ADXL345_I2C_ADDR)

        if self.h >= 0 : # Connected OK?
            # Initialise ADXL345.
            self.pi.i2c_write_byte_data(self.h, 0x2d, 0)  # POWER_CTL reset.
            self.pi.i2c_write_byte_data(self.h, 0x2d, 8)  # POWER_CTL measure.
            self.pi.i2c_write_byte_data(self.h, 0x31, 0)  # DATA_FORMAT reset.
            self.pi.i2c_write_byte_data(self.h, 0x31, 11) # DATA_FORMAT full res +/- 16g.

            self.read = 0
            self.start_time = time.time()
        else :
            self.pi.stop()