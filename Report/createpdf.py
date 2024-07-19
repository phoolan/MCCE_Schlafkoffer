#!/usr/bin/env python3
# Erstellt von Tatjana Baier 06/2024
from fpdf import FPDF, XPos, YPos
import subprocess

def get_report_output():
    result = subprocess.run(['python3', 'report.py'], stdout=subprocess.PIPE, text=True)
    return result.stdout

# Ausgabe des report.py-Skripts erfassen
report_output = get_report_output()

# Erstellen einer Klasse, die von FPDF erbt
class PDF(FPDF):
    def header(self):
        # Logo
        self.image('FirmenLogo.png', 10, 8, 33)  # Pfad zum Logo, x-Position, y-Position, Breite
        self.set_font('Helvetica', 'B', 12)
        self.cell(0, 10, 'Bericht Customer 1:', 0, new_x=XPos.LMARGIN, align='C')
        self.ln(8)  # Fügt eine Zeile hinzu, um Platz nach der ersten Zeile zu schaffen
        self.cell(0, 10, 'Auswertung der Sensoren zur Schlafüberwachung', 0, new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')
        self.ln(20)  # Fügt eine Zeile hinzu, um Platz nach dem Header zu schaffen

    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.cell(0, 10, f'Seite {self.page_no()}', 0, new_x=XPos.RIGHT, new_y=YPos.TOP, align='C')

# Eine Instanz von FPDF erzeugen
pdf = PDF()
pdf.add_page()

# Schriftart festlegen
pdf.set_font('Helvetica', '', 10)

# Setzt die Y-Position nach unten, um Platz für das Logo zu lassen
pdf.set_y(50)

# Daten aus Ihrem Script
text = report_output

# Text zum PDF hinzufügen
pdf.multi_cell(0, 5, text)

# PDF speichern
pdf.output('/var/www/html/report/Report_Customer1.pdf')

print("PDF wurde erfolgreich erstellt.")