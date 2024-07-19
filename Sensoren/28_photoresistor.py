#!/usr/bin/env python

#Edit 06/2024 Tatjana Baier
#   add write output to file

import ADC0832_resistor
import time
import sys
from datetime import datetime

def init():
	ADC0832_resistor.setup()

def loop():
	while True:
		res = ADC0832_resistor.getResult() - 80
		timestamp = datetime.now()
		with open("/home/sensoren/data/resistor/resistor", "a") as file:
			sys.stdout = file
			if res < 0:
				res = 0
			if res > 1000:
				res = 1000
			print(timestamp,"; ",res)
		time.sleep(0.75)

if __name__ == '__main__':
	init()
	try:
		loop()
	except KeyboardInterrupt: 
		ADC0832_resistor.destroy()
