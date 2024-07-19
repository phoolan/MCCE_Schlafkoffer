#!/usr/bin/env python3
# Erstellt von Tatjana Baier 06/2024

import subprocess
import os
import json
import sys

def main():
    try:
        # Unterdrücke alle Druckausgaben oder unerwünschte Ausgaben
        result = subprocess.run(['python3', 'createpdf.py'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        pdf_path = '/var/www/html/report/Report_Customer1.pdf'  # Stellen Sie sicher, dass dies der richtige Pfad ist

        if os.path.exists(pdf_path):
            response = {'success': True, 'pdf_url': f'/report/Report_Customer1.pdf'}
        else:
            response = {'success': False, 'error': 'PDF-Datei nicht gefunden'}
    except subprocess.CalledProcessError as e:
        response = {'success': False, 'error': f'CalledProcessError: {e}'}
    except Exception as e:
        response = {'success': False, 'error': f'Exception: {e}'}

    # Setze den Content-Type-Header
    sys.stdout.write("Content-Type: application/json\n\n")
    sys.stdout.write(json.dumps(response))
    sys.stdout.flush()

if __name__ == "__main__":
    main()
