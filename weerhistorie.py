import json
import requests
import os
from datetime import datetime

# 1. JSON-bestand inladen
try:
    with open('weer_historie.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
except FileNotFoundError:
    print("Fout: Het bestand 'weer_historie.json' is niet gevonden.")
    exit(1)

# 2. Webhook ophalen uit GitHub Secrets
webhook_url = os.getenv('HISTORIE_WEBHOOK')
if not webhook_url:
    print("Fout: Geen webhook URL gevonden in de omgeving.")
    exit(1)

# 3. Huidige datum bepalen (bijv. "15 juli")
vandaag = datetime.now().strftime("%-d %B").lower()

# 4. Zoeken en versturen
gevonden = False
for sublijst in data:
    for item in sublijst:
        if item.get("datum", "").lower() == vandaag:
            # Berichten opmaken inclusief de datum
            bericht = {
                "content": (
                    f"📅 **Datum:** {item['datum']}\n"
                    f"**{item['titel']}**\n"
                    f"Jaar: {item['jaar']}\n"
                    f"{item['tekst']}"
                )
            }
            
            # Versturen naar Discord
            response = requests.post(webhook_url, json=bericht)
            
            if response.status_code == 204:
                print(f"Succesvol verstuurd: {item['titel']}")
            else:
                print(f"Fout bij versturen: {response.status_code}, {response.text}")
            
            gevonden = True

if not gevonden:
    print(f"Geen weerfeit gevonden voor {vandaag}")
