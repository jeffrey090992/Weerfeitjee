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

    # 3. Vertaallijst
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

    fields = []
    for item in data:
        if isinstance(item, dict) and item.get("datum") == vandaag:
            record_type = item.get('record_type', '')
            titel_tekst = labels.get(record_type, record_type)
            
            # Bepaal of het om temperatuur of millimeters (neerslag) gaat
            if "mm" in item:
                waarde_tekst = f"{item['mm']} mm"
                veld_naam = "Neerslag"
            else:
                waarde_tekst = f"{item.get('temperatuur', '')}°C"
                veld_naam = "Temperatuur"
            
            jaar_station = f"{item.get('jaar', '')} ({item.get('station', '')})"
            
            # Voeg velden toe aan de lijst in plaats van direct te versturen
            fields.append({
                "name": titel_tekst, 
                "value": f"**{waarde_tekst}** in {jaar_station}", 
                "inline": False
            })

    # 5. Alles verzenden in ÉÉN bericht als er records zijn gevonden
    if fields:
        message = {
            "embeds": [{
                "title": f"Dagrecords - {vandaag}",
                "description": "Alle weerrecords voor deze dag in de geschiedenis:",
                "color": 16753920,
                "fields": fields
            }]
        }
        
        response = requests.post(webhook_url, json=message)
        print(f"Verstuurd! Status code: {response.status_code}")
    else:
        print("Geen records gevonden voor vandaag.")

if __name__ == "__main__":
    verstuur_weer_bericht()
