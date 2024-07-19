#Edit 06/2024 Tatjana Baier
#   add write output to file

import RPi.GPIO as GPIO
import dht11
import time
import sys
from datetime import datetime

# initialize GPIO
GPIO.setwarnings(True)
GPIO.setmode(GPIO.BOARD)

# read data using pin 7
instance = dht11.DHT11(pin=7)

try:
	while True:
	    result = instance.read()
	    if result.is_valid():
		    timestamp = datetime.now()
		    with open("/home/sensoren/data/dht11/dht11", "a") as file:
			    sys.stdout = file
			    print(timestamp,"; ",result.humidity,"; ",result.temperature)
	    time.sleep(2)

except KeyboardInterrupt:
    #print("Cleanup")
    GPIO.cleanup(0)
    file.close()

