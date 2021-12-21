# MTBMaker Example code for DHT22 temp/humidity sensor with 7 seg display output 
# Written for QTPY SAMD21e18 - not enough memory to load both sets of libraries at one time.
# Written for/with Circuit Python 6.3 - library build from 8/22/21 
# Requires Circuit python version <7.x
# note this code cannot run at the same time as the repl/serial out due to memory usage.

import board
import time
import adafruit_dht
from adafruit_ht16k33.segments import Seg7x4

waitInterval = 2
dht = adafruit_dht.DHT22(board.D3)
i2c = board.I2C()
display = Seg7x4(i2c)
rawBitH = "0b01110110"

while True:
    try:
        temperature = dht.temperature
        humidity = dht.humidity
        # print temp followed by C for Celsius
        # convert temp to F
        temperature = (temperature * 9/5) + 32
        tempString = "{:.1f}F".format(temperature)  
        display.print(tempString)
        time.sleep(waitInterval)
        # a little trickery used to display an H with the humidity reading 
        # as H is not supported navitely in the backpack
        display.fill(0)
        # 2 decimal places are used to position the reading across the display (7x4)
        humidString = "{:.2f}".format(humidity)
        display.print(humidString)
        # last digit(far right) is overwritten using a segement 'bit masking' to make H
        display.set_digit_raw(3, 0b01110110)
        time.sleep(waitInterval)
       
        # Print what we got to the REPL
        # print("Temp: {:.1f} *C \t Humidity: {}%".format(temperature, humidity))
    except RuntimeError as e:
        # Reading doesn't always work! Just print error and we'll try again
        print("Reading from DHT failure: ", e.args)

