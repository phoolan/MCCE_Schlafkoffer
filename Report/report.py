#!/usr/bin/python3
# encoding: utf-8
# Erstellt von Tatjana Baier 06/2024

import psycopg2

# Verbindung zur PostgreSQL-Datenbank herstellen
# Passen Sie diese Parameter an Ihre Datenbankkonfiguration an
conn = psycopg2.connect(
        dbname="rp1",
        user="USER",
        password="USER0",
        host="HOSTIP",
        port="5432"
)
cursor = conn.cursor()


#############
##### Raumtemperatur
#############

def raumtempi():

	cursor.execute("SELECT COUNT(*) FROM public.tbl_bmp WHERE EXTRACT(HOUR FROM timestamp) >= 22 OR EXTRACT(HOUR FROM timestamp) < 6;")
	total_count = cursor.fetchone()[0]

	# SQL-Abfrage ausführen
	cursor.execute("SELECT temp FROM tbl_bmp WHERE EXTRACT(HOUR FROM timestamp) >= 22 OR EXTRACT(HOUR FROM timestamp) < 6;")
	results = cursor.fetchall()

	# Definierten Zahlenwert
	vergleichmax = 20
	vergleichmin = 16
	countgroesser=0
	countkleiner=0
	countok=0
	sok=0
	snok=0
	summewerte=0
	druchschnittswert=0

	# Ergebnisse durchlaufen und vergleichen
	for row in results:
		temp = row[0]
		summewerte=summewerte+temp
		if temp > vergleichmin and temp < vergleichmax:
			countok+=1
		elif temp < vergleichmin:
			countkleiner+=1
		else:
			countgroesser+=1

	prozent_zu_hoch = 100 / total_count * countgroesser
	prozent_zu_niedrig = 100 / total_count * countkleiner
	durchschnittswert = summewerte / total_count

	if countkleiner+countgroesser >= countok: # bei der hälfte der Werte dei fehlerhaft sind ist das sensorergebnis nicht ok
		snok += 1
		print("  Raumtemperatur: Nicht OK")
		print(f"    Ihre Raumtemperatur entspricht nicht den Empfehlungen zwischen {vergleichmin} und {vergleichmax} Grad Celsius.");
		print(f"    Die Raumtemperatur ist zu hoch : (Abweichung in Prozent){prozent_zu_hoch:.2f} %");
		print(f"    Die Raumtemperatur ist zu niedrig (Abweichung in Prozent): {prozent_zu_niedrig:.2f} %");
		print(f"    Die durchschnittliche Raumtemperatur aus den Messungen beträgt: {durchschnittswert:.2f} Grad Celsius.\n")
	else:
		print("  Raumtemperatur: OK")
		print(f"    Ihre Raumtemperatur entspricht  den Empfehlungen zwischen {vergleichmin} und {vergleichmax} Grad Celsius.");
		print(f"    Die durchschnittliche Raumtemperatur aus den Messungen beträgt: {durchschnittswert:.2f} Grad Celsius.\n")
		sok += 1
	return sok, snok


	
#############
##### Luftfeuchtigkeit
#############

def dht_humidity():
	cursor.execute("SELECT COUNT(*) FROM public.tbl_dht11 WHERE EXTRACT(HOUR FROM timestamp) >= 22 OR EXTRACT(HOUR FROM timestamp) < 6;")
	total_count = cursor.fetchone()[0]

	# SQL-Abfrage ausführen
	cursor.execute("SELECT humidity FROM tbl_dht11 WHERE EXTRACT(HOUR FROM timestamp) >= 22 OR EXTRACT(HOUR FROM timestamp) < 6;")
	results = cursor.fetchall()

	# Definierten Zahlenwert
	vergleichmax = 60
	vergleichmin = 40
	countgroesser=0
	countkleiner=0
	countok=0
	sok=0
	snok=0
	summewerte=0
	druchschnittswert=0

	# Ergebnisse durchlaufen und vergleichen
	for row in results:
		humidity = row[0]
		summewerte=summewerte+humidity
		if humidity > vergleichmin and humidity < vergleichmax:
			countok+=1
		elif humidity < vergleichmin:
			countkleiner+=1
		else:
			countgroesser+=1

	prozent_zu_hoch = 100 / total_count * countgroesser
	prozent_zu_niedrig = 100 / total_count * countkleiner
	durchschnittswert = summewerte / total_count

	if countkleiner+countgroesser >= countok:
		snok += 1
		print("  Luftfeuchtigkeit: Nicht OK")
		print(f"    Die Luftfeuchtigkeit entspricht nicht den Empfehlungen zwischen {vergleichmin} und {vergleichmax} %.");
		print(f"    Die Luftfeuchtigkeit ist zu hoch : (Abweichung in Prozent){prozent_zu_hoch:.2f} %");
		print(f"    Die Luftfeuchtigkeit ist zu niedrig (Abweichung in Prozent): {prozent_zu_niedrig:.2f} %");
		print(f"    Die durchschnittliche Luftfeuchtigkeit aus den Messungen beträgt: {durchschnittswert:.2f} %.\n")
	else:
		sok += 1
		print("  Luftfeuchtigkeit: OK")
		print(f"    Die Luftfeuchtigkeit entspricht den Empfehlungen zwischen {vergleichmin} und {vergleichmax} %.");
		print(f"    Die durchschnittliche Luftfeuchtigkeit aus den Messungen beträgt: {durchschnittswert:.2f} %.\n")
	
	return sok, snok


#############
##### Bewegungssensor
#############

def pir():
	cursor.execute("SELECT COUNT(*) FROM public.tbl_pir WHERE EXTRACT(HOUR FROM timestamp) >= 22 OR EXTRACT(HOUR FROM timestamp) < 6;")
	total_count = cursor.fetchone()[0]

	# SQL-Abfrage ausführen
	cursor.execute("SELECT pir FROM tbl_pir WHERE EXTRACT(HOUR FROM timestamp) >= 22 OR EXTRACT(HOUR FROM timestamp) < 6;")
	results = cursor.fetchall()

	    # Definierten Zahlenwert
	countnok=0
	countok=0
	sok=0
	snok=0
	summewerte=0

    # Ergebnisse durchlaufen und vergleichen
	for row in results:
		pir = row[0]
		summewerte=summewerte+pir
		if pir == 0:
			countok+=1
		else:
			countnok+=1

    # weil es im selben zuge wo er eine bewegung misst auch keine misst, messfehler korrektur
	countok = countok - countnok
	total_count = total_count - countnok

	prozent = 100 / total_count * countnok

	if countnok >= countok:
		snok += 1
		print("  Bewegung: Nicht OK")
		print(f"    Die gemessene Bewegung ist höher als 50% der Messwerte.");
		print(f"    Die durchschnittliche Bewegung aus den Messungen beträgt: {prozent:.2f} %.\n")
	else:
		sok += 1
		print("  Bewegung: OK")
		print(f"    Die gemessene Bewegung ist niedriger als 50% der Messwerte.");
		print(f"    Die durchschnittliche Bewegung aus den Messungen beträgt: {prozent:.2f} %.\n")

	return sok, snok


#############
##### Bewegungssensor
#############

def resistor():
	cursor.execute("SELECT COUNT(*) FROM public.tbl_resistor WHERE EXTRACT(HOUR FROM timestamp) >= 22 OR EXTRACT(HOUR FROM timestamp) < 6;")
	total_count = cursor.fetchone()[0]

	# SQL-Abfrage ausführen
	cursor.execute("SELECT resistor FROM tbl_resistor WHERE EXTRACT(HOUR FROM timestamp) >= 22 OR EXTRACT(HOUR FROM timestamp) < 6;")
	results = cursor.fetchall()

	 # Definierten Zahlenwert
	vergleichmax = 10
	countnok=0
	countok=0
	sok=0
	snok=0
	summewerte=0
	durchschnittswert=0

    # Ergebnisse durchlaufen und vergleichen
	for row in results:
		resistor = row[0]
		summewerte=summewerte+resistor
		if resistor < vergleichmax:
			countok+=1
		else:
			countnok+=1

	durchschnittswert = summewerte / total_count

	if countnok >= countok:
		snok += 1
		print("  Helligkeit: Nicht OK")
		print(f"    Die gemessene Helligkeit ist bei 50% der Messwerte höher als der empfohlene Wert {vergleichmax}.");
		print(f"    Die durchschnittliche Helligkeit aus den Messungen beträgt: {durchschnittswert:.2f} .\n")
	else:
		sok += 1
		print("  Helligkeit: OK")
		print(f"    Die gemessene Helligkeit ist bei 50% der Messwerte niedriger als dem empfohlene Wert {vergleichmax}.");
		print(f"    Die durchschnittliche Helligkeit aus den Messungen beträgt: {durchschnittswert:.2f} .\n")

	return sok, snok


#############
##### SoundSensor
#############

def sound():
	cursor.execute("SELECT COUNT(*) FROM public.tbl_sound WHERE EXTRACT(HOUR FROM timestamp) >= 22 OR EXTRACT(HOUR FROM timestamp) < 6;")
	total_count = cursor.fetchone()[0]

	# SQL-Abfrage ausführen
	cursor.execute("SELECT sound FROM tbl_sound WHERE EXTRACT(HOUR FROM timestamp) >= 22 OR EXTRACT(HOUR FROM timestamp) < 6;")
	results = cursor.fetchall()

	# Definierten Zahlenwert
	countnok=0
	countok=0
	sok=0
	snok=0
	summewerte=0

    # Ergebnisse durchlaufen und vergleichen
	for row in results:
		sound = row[0]
		summewerte=summewerte+sound
		if sound == 0:
			countok+=1
		else:
			countnok+=1

	prozent = 100 / total_count * countnok

	if countnok >= countok:
		snok += 1
		print("  Geräuscherkennung: Nicht OK")
		print(f"    Die gemessene Geräuscherkennung ist höher als 50% der Messwerte.");
		print(f"    Die durchschnittliche Geräuscherkennung aus den Messungen beträgt: {prozent:.2f} %.\n")
	else:
		sok += 1
		print("  Geräuscherkennung: OK")
		print(f"    Die gemessene Geräuscherkennung ist niedriger als 50% der Messwerte.");
		print(f"    Die durchschnittliche Geräuscherkennung aus den Messungen beträgt: {prozent:.2f} %.\n")

	return sok, snok


#############
##### Vibrationssensor
#############

def vibration():
	cursor.execute("SELECT COUNT(*) FROM public.tbl_vibration WHERE EXTRACT(HOUR FROM timestamp) >= 22 OR EXTRACT(HOUR FROM timestamp) < 6;")
	total_count = cursor.fetchone()[0]

	# SQL-Abfrage ausführen
	cursor.execute("SELECT vibration FROM tbl_vibration WHERE EXTRACT(HOUR FROM timestamp) >= 22 OR EXTRACT(HOUR FROM timestamp) < 6;")
	results = cursor.fetchall()

	# Definierten Zahlenwert
	countnok=0
	countok=0
	sok=0
	snok=0
	summewerte=0

    # Ergebnisse durchlaufen und vergleichen
	for row in results:
		vibration = row[0]
		summewerte=summewerte+vibration
		if vibration == 0:
			countok+=1
		else:
			countnok+=1

	prozent = 100 / total_count * countnok

	if countnok >= countok:
		snok += 1
		print("  Virbrationserkennung: Nicht OK")
		print(f"    Die gemessene Virbrationserkennung ist höher als 50% der Messwerte.");
		print(f"    Die durchschnittliche Virbrationserkennung aus den Messungen beträgt: {prozent:.2f} %.\n")
	else:
		sok += 1
		print("  Virbrationserkennung: OK")
		print(f"    Die gemessene Virbrationserkennung ist niedriger als 50% der Messwerte.");
		print(f"    Die durchschnittliche Virbrationserkennung aus den Messungen beträgt: {prozent:.2f} %.\n")

	return sok, snok



#################-------------------------------------------
##### Zur informtationszwecken, oder als referenz

#############
##### Luftdruck
#############

def luftdruck():
	cursor.execute("SELECT COUNT(*) FROM public.tbl_bmp WHERE EXTRACT(HOUR FROM timestamp) >= 22 OR EXTRACT(HOUR FROM timestamp) < 6;")
	total_count = cursor.fetchone()[0]

	# SQL-Abfrage ausführen
	cursor.execute("SELECT pressure FROM tbl_bmp WHERE EXTRACT(HOUR FROM timestamp) >= 22 OR EXTRACT(HOUR FROM timestamp) < 6;")
	results = cursor.fetchall()

	# Definierten Zahlenwert
	vergleichmax = 1016
	vergleichmin = 1015
	countgroesser=0
	countkleiner=0
	countok=0
	summewerte=0
	druchschnittswert=0

	# Ergebnisse durchlaufen und vergleichen
	for row in results:
		druck = row[0]
		summewerte=summewerte+druck

	durchschnittswert = summewerte / total_count

	print(f"    Der Luftdruck in Eisenstadst ist mit 1015.5 hPa lt. Statistik definiert.");
	print(f"    Der durchschnittliche Luftdruckwert aus den Messungen beträgt: {durchschnittswert:.2f} hPa.\n")


#############
##### Raumtemperatur Referenz Sensor DHT11
#############

def raumtempi_dht11():

	cursor.execute("SELECT COUNT(*) FROM public.tbl_dht11 WHERE EXTRACT(HOUR FROM timestamp) >= 22 OR EXTRACT(HOUR FROM timestamp) < 6;")
	total_count = cursor.fetchone()[0]

	# SQL-Abfrage ausführen
	cursor.execute("SELECT temperature FROM tbl_dht11 WHERE EXTRACT(HOUR FROM timestamp) >= 22 OR EXTRACT(HOUR FROM timestamp) < 6;")
	results = cursor.fetchall()

	# Definierten Zahlenwert
	vergleichmax = 20
	vergleichmin = 16
	countgroesser=0
	countkleiner=0
	countok=0
	summewerte=0
	druchschnittswert=0

	# Ergebnisse durchlaufen und vergleichen
	for row in results:
		temp = row[0]
		summewerte=summewerte+temp
		if temp > vergleichmin and temp < vergleichmax:
			countok+=1
		elif temp < vergleichmin:
			countkleiner+=1
		else:
			countgroesser+=1

	prozent_zu_hoch = 100 / total_count * countgroesser
	prozent_zu_niedrig = 100 / total_count * countkleiner
	durchschnittswert = summewerte / total_count

	print("    Der zweite Temperatursensor DTH11 hat folgende Messungen protokolliert:")

	if countkleiner+countgroesser >= countok: # bei der hälfte der Werte dei fehlerhaft sind ist das sensorergebnis nicht ok
		print("    Raumtemperatur: Nicht OK")
		print(f"    Die durchschnittliche Raumtemperatur aus den Messungen beträgt: {durchschnittswert:.2f} Grad Celsius.\n")
	else:
		print("  Raumtemperatur: OK")
		print(f"    Die durchschnittliche Raumtemperatur aus den Messungen beträgt: {durchschnittswert:.2f} Grad Celsius.\n")


############### ------------------------------------
###############
###### Hauptfunktion

def main ():

	# Allg Counter Sensoren 7
	gesamtok = 0 # wieviele sensoren ok sind
	gesamtnok = 0 # wieviele sensoren nicht ok sind
	sok=0
	snok=0
	resultat=0 # ergebnis der schlafbewertung: 1 ok; 2 warning; 3 critical

	print("Bericht Customer 1:\nAuswertung der Sensoren zur Schlafüberwachung:\n")
	print("Das mobile Schlaflabor war druchgehend in Betrieb und die Daten sind über das Dashboard einsehbar, für den Bericht jedoch wird nur die Zeit zwischen 22:00 und 06:00 herangezogen.\n")
	print("Die Auswertung der Sensoren erfolgt auf Basis von Durchschnittswerten.\nDiese Information bezieht sich ausschließlich auf die Messergebnisse, welche erzielt wurden. Dies kann beeinflusst werden durch entsprechende Positionierung des Koffers.\nDas Ergebnis ersetzt nicht das ärztliche Gespräch mit dem Patienten.\nEs können, unabhängig davon, ob Auffälligkeiten durch die Sensoren aufgezeichnet wurden, Schlafprobleme vorliegen. Innere Unruhe im Körper wird durch Raumsensoren nicht erkannt.\nDer Koffer dient ausschließlich zur Erstabklärung und zum Ausschluss externer Faktoren.\n")

	
	print("Detailbewertung:\n")
	# Temp
	sok, snok = raumtempi()
	gesamtok = gesamtok + sok
	gesamtnok = gesamtnok + snok


	# Luftfeuchtigkeit
	sok, snok = dht_humidity()
	gesamtok = gesamtok + sok
	gesamtnok = gesamtnok + snok

	# Bewegungssensor
	sok, snok = pir()
	gesamtok = gesamtok + sok
	gesamtnok = gesamtnok + snok

	# Resistor
	sok, snok = resistor()
	gesamtok = gesamtok + sok
	gesamtnok = gesamtnok + snok
	
	# Sound
	sok, snok = sound()
	gesamtok = gesamtok + sok
	gesamtnok = gesamtnok + snok
	
	# Vibration
	sok, snok = vibration()
	gesamtok = gesamtok + sok
	gesamtnok = gesamtnok + snok


	###### Gesamtbewertung

	if gesamtnok > 1 and gesamtnok < 3:
		resultat = 2
	elif gesamtnok >= 3:
		resultat = 3
	else:
		resultat = 1
	
	print("\n---------\nDas Ergebnis ihrer Schlafüberwachung wird gesamt mit", resultat, "bewertet.")
	if resultat == 1:
		print("Ein Ergebnis mit Wert: ", resultat, " bedeutet, dass ihre Schlafüberwachung keine Auffälligkeiten aufzeichnen konnte.\n")
		print("\nStatus: Grün")
	elif resultat == 2:
		print("Ein Ergebnis mit Wert: ", resultat, " bedeutet, dass ihre Schlafüberwachung teilweise Auffälligkeiten aufzeichnen konnte.\n")
		print("\nStatus: Gelb")
	elif resultat == 3:
		print("Ein Ergebnis mit Wert: ", resultat, " bedeutet, dass ihre Schlafüberwachung über der hälfte an zu messenden Sensoren Auffälligkeiten aufzeichnen konnte.\n")
		print("\nStatus: Rot")
	else:
		print("Programmfehler\n")



	print("---------\n\n\nZusätzlich haben die Sensoren noch folgende Informationen ausgelesen:\n")


	# Vergleichsmessungen od nicht beeinflussbares
	
	# Druck
	luftdruck()
	raumtempi_dht11()

	print("Guten Schlaf wünscht Ihnen Ihr Schlafkoffer.\nMit freundlichen Grüßen, das Mobile Schlaflabor.")


############
###### Start Programm


if __name__ == "__main__":
    main()


# Verbindung zur Datenbank schließen
cursor.close()
conn.close()