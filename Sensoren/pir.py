#Edit 06/2024 Tatjana Baier
#   add write output to file

import RPi.GPIO as GPIO
import time
import sys
from datetime import datetime

SENSOR_PIN = 18
 
GPIO.setmode(GPIO.BCM)
GPIO.setup(SENSOR_PIN, GPIO.IN)

def mein_callback(channel):
    timestamp = datetime.now()
    with open("/home/sensoren/data/pir/pir", "a") as file:
        sys.stdout = file
        print(timestamp,"; 1")

try:
    GPIO.add_event_detect(SENSOR_PIN , GPIO.RISING, callback=mein_callback)
    while True:
        timestamp = datetime.now()
        with open("/home/sensoren/data/pir/pir", "a") as file:
            sys.stdout = file
            print(timestamp,"; 0")
        time.sleep(3)
except KeyboardInterrupt:
    GPIO.cleanup()
