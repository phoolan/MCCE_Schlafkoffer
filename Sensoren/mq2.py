#Edit 06/2024 Tatjana Baier
#   add write output to file

# Bibliotheken laden
import RPi.GPIO as GPIO
import time
import sys
from datetime import datetime

analogPin = 13 

GPIO.setmode(GPIO.BCM)
GPIO.setup(analogPin, GPIO.IN)

# Wiederholung (Endlos-Schleife)
while True:
    value = GPIO.input(analogPin)
    timestamp = datetime.now()
    with open("/home/sensoren/data/mq2", "a") as file:
        sys.stdout = file
        print(timestamp,"; ", value)
    time.sleep(3)
