import os
import json
import requests
from datetime import datetime

WEBHOOK = os.getenv("HISTORIE_WEBHOOK")

if not WEBHOOK:
    raise Exception("Webhook ontbreekt")

# Database laden
with open("historie.json", "r", encoding="utf-8") as bestand:
    historie = json.load(bestand)

# Datum van vandaag
vandaag = datetime.now().strftime("%d %B")

# Zoek gebeurtenis van vandaag
gevonden = None

for item in historie:
    if item["datum"] == vandaag:
        gevonden = item
        break


# Als er geen gebeurtenis is
if gevonden is None:
    gevonden = {
        "seizoen": "📜 Weerhistorie",
        "jaar": "",
        "titel": "Geen gebeurtenis gevonden",
        "tekst": "Voor deze datum staat nog geen historische gebeurtenis in de database."
    }


bericht = {
    "username": "📜 Weerhistorie Nederland",
    "embeds": [
        {
            "title": gevonden["titel"],
            "description": (
                f"📅 **Datum:** {vandaag}\n"
                f"📆 **Jaar gebeurtenis:** {gevonden.get('jaar','')}\n"
                f"🍂 **Seizoen:** {gevonden.get('seizoen','')}\n\n"
                f"{gevonden['tekst']}"
            ),
            "footer": {
                "text": "Nederlandse Weerhistorie"
            },
            "timestamp": datetime.utcnow().isoformat()
        }
    ]
}


response = requests.post(
    WEBHOOK,
    json=bericht
)

if response.status_code == 204:
    print("✅ Historisch weerbericht verstuurd")
else:
    print("❌ Fout:", response.status_code)
    print(response.text)
