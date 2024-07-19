#!/usr/bin/python
#Edit 06/2024 Tatjana Baier
#   add write output to file
import RPi.GPIO as GPIO
import time
import sys
from datetime import datetime

#GPIO SETUP
channel = 27
GPIO.setmode(GPIO.BCM)
GPIO.setup(channel, GPIO.IN)

def callback(channel):
        if GPIO.input(channel):
                timestamp = datetime.now()
                with open("/home/sensoren/data/vibration/vibration", "a") as file:
                    sys.stdout = file
                    print(timestamp,"; 1")
        else:
            timestamp = datetime.now()
            with open("/home/sensoren/data/vibration/vibration", "a") as file:
                sys.stdout = file
                print(timestamp,"; 1")


GPIO.add_event_detect(channel, GPIO.BOTH, bouncetime=300)  # let us know when the pin goes HIGH or LOW
GPIO.add_event_callback(channel, callback)  # assign function to GPIO PIN, Run function on change

# infinite loop
while True:
        time.sleep(3)
        timestamp = datetime.now()
        with open("/home/sensoren/data/vibration/vibration", "a") as file:
            sys.stdout = file
            print(timestamp,"; 0")
