import json
import requests
import os # Belangrijk voor het ophalen van de secret

# 1. Bestand inladen
with open('weer_historie.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 2. Haal de webhook op uit de omgeving (deze komt uit je secrets)
webhook_url = os.getenv('HISTORIE_WEBHOOK')

if not webhook_url:
    print("Fout: Geen webhook URL gevonden in de omgeving.")
    exit(1)

vandaag = "15 juli"

# 3. Zoeken en versturen
gevonden = False
for sublijst in data:
    for item in sublijst:
        if item["datum"] == vandaag:
            bericht = {
                "content": f"**{item['titel']}**\nJaar: {item['jaar']}\n{item['tekst']}"
            }
            
            response = requests.post(webhook_url, json=bericht)
            
            if response.status_code == 204:
                print(f"Succesvol verstuurd naar Discord: {item['titel']}")
            else:
                print(f"Fout bij versturen: {response.status_code}, {response.text}")
            
            gevonden = True

if not gevonden:
    print(f"Geen weerfeit gevonden voor {vandaag}")
