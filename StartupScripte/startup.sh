#!/bin/bash
#Script 06/2024 Tatjana Baier

dateparam="$(date +%d-%m-%Y-%H-%M)"
#mkdir /home/sensoren/data_bak/bak-"$dateparam"
#mv /home/sensoren/data/bmp180/bmp180 /home/sensoren/data/bmp180/bmp180-"$dateparam"
#mv /home/sensoren/data/dht11/dht11 /home/sensoren/data/dht11/dht11-"$dateparam"
#mv /home/sensoren/data/pir/pir /home/sensoren/data/pir/pir-"$dateparam"
#mv /home/sensoren/data/resistor/resistor /home/sensoren/data/resistor/resistor-"$dateparam"
#mv /home/sensoren/data/sound/sound /home/sensoren/data/sound/sound-"$dateparam"
#mv /home/sensoren/data/vibration/vibration /home/sensoren/data/vibration/vibration-"$dateparam"

systemctl start INENI_led.service
systemctl start INENI_bmp.service
systemctl start INENI_dht11.service
systemctl start INENI_pir.service
systemctl start INENI_resistor.service
systemctl start INENI_sound.service
systemctl start INENI_vibration.service
