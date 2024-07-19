#!/bin/bash
#Script 06/2024 Tatjana Baier

systemctl stop INENI_led.service
systemctl stop INENI_bmp.service
systemctl stop INENI_dht11.service
systemctl stop INENI_pir.service
systemctl stop INENI_resistor.service
systemctl stop INENI_sound.service
systemctl stop INENI_vibration.service
