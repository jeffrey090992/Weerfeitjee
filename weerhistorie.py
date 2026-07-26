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

    # 3. Vertaallijst (uitgebreid met alle recordtypes)
    labels = {
        "hoogste_max": "☀️ Hoogste maximumtemperatuur",
        "laagste_min": "❄️ Laagste minimumtemperatuur",
        "laagste_max": "⛅ Laagste maximumtemperatuur",
        "hoogste_min": "🌡️ Hoogste minimumtemperatuur",
        "hoogste_dagsom_neerslag": "🌧️ Hoogste dagsom neerslag",
        "minimum_10cm_temperatuur": "🌱 Minimum temperatuur op 10 cm"
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
            record_type = item.get('record_type', '')
            titel_tekst = labels.get(record_type, record_type)
            kleur = 16753920 if "hoogste" in record_type else 3447003
            
            # Bepaal of het om temperatuur of millimeters (neerslag) gaat
            if "mm" in item:
                waarde_tekst = f"{item['mm']} mm"
                veld_naam = "Neerslag"
            else:
                waarde_tekst = f"{item.get('temperatuur', '')}°C"
                veld_naam = "Temperatuur"
            
            # 5. Discord Embed opmaak
            message = {
                "embeds": [{
                    "title": f"Dagrecord - {vandaag}",
                    "description": f"Op deze dag in de geschiedenis:",
                    "color": kleur,
                    "fields": [
                        {"name": "Type record", "value": titel_tekst, "inline": False},
                        {"name": veld_naam, "value": waarde_tekst, "inline": True},
                        {"name": "Jaar", "value": str(item.get('jaar', '')), "inline": True},
                        {"name": "Station", "value": item.get('station', ''), "inline": True}
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
