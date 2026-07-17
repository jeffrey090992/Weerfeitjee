import json
import os
import requests
from datetime import datetime

def verstuur_weer_bericht():
    # 1. Bepaal de huidige datum (DD-MM)
    vandaag = datetime.now().strftime("%d-%m")
    print(f"DEBUG: Zoeken naar records voor datum: {vandaag}")
    
    # 2. JSON bestand inladen
    try:
        with open('weer_historie.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"ERROR: Kon JSON niet laden: {e}")
        return

    # 3. Zoeken naar matches
    gevonden = False
    webhook_url = os.environ.get('HISTORIE_WEBHOOK')

    for item in data:
        # We vergelijken de string direct
        if item.get("datum") == vandaag:
            gevonden = True
            print(f"MATCH gevonden: {item}")
            
            # 4. Bericht opstellen
            message = {
                "content": (f"**Weerfeitje voor {vandaag}:**\n"
                            f"Record: {item['record_type']}\n"
                            f"Temperatuur: {item['temperatuur']}°C\n"
                            f"Jaar: {item['jaar']}\n"
                            f"Station: {item['station']}")
            }
            
            # 5. Versturen naar Discord
            if webhook_url:
                response = requests.post(webhook_url, json=message)
                print(f"Discord API status: {response.status_code}")
            else:
                print("ERROR: HISTORIE_WEBHOOK ontbreekt.")

    if not gevonden:
        print(f"Geen records gevonden voor {vandaag}. Controleer je JSON-formaat.")

if __name__ == "__main__":
    verstuur_weer_bericht()
