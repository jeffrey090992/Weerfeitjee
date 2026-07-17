import json
import os
import requests
from datetime import datetime

def verstuur_weer_bericht():
    # 1. Bepaal de huidige datum
    vandaag = datetime.now().strftime("%d-%m")
    print(f"Zoeken naar records voor: {vandaag}")
    
    # 2. JSON inladen
    try:
        with open('weer_historie.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"Fout bij inladen JSON: {e}")
        return

    # 3. Vertaallijst voor mooiere teksten
    labels = {
        "hoogste_max": "☀️ Hoogste maximumtemperatuur",
        "laagste_min": "❄️ Laagste minimumtemperatuur"
    }

    # 4. Zoeken naar matches
    webhook_url = os.environ.get('HISTORIE_WEBHOOK')
    if not webhook_url:
        print("Fout: HISTORIE_WEBHOOK niet gevonden in omgeving.")
        return

    gevonden = False
    for item in data:
        if isinstance(item, dict) and item.get("datum") == vandaag:
            gevonden = True
            
            # Bepaal titel en kleur
            titel = labels.get(item['record_type'], item['record_type'])
            kleur = 16753920 if "hoogste" in item['record_type'] else 3447003
            
            # 5. Discord Embed opmaak
            message = {
                "embeds": [{
                    "title": "Weerfeitje van de dag 🌤️",
                    "description": f"Op deze dag in de geschiedenis:",
                    "color": kleur,
                    "fields": [
                        {"name": "Type record", "value": titel, "inline": False},
                        {"name": "Temperatuur", "value": f"{item['temperatuur']}°C", "inline": True},
                        {"name": "Jaar", "value": str(item['jaar']), "inline": True},
                        {"name": "Station", "value": item['station'], "inline": True}
                    ]
                }]
            }
            
            # Versturen
            response = requests.post(webhook_url, json=message)
            print(f"Verstuurd! Status code: {response.status_code}")

    if not gevonden:
        print("Geen records gevonden voor vandaag.")

if __name__ == "__main__":
    verstuur_weer_bericht()
