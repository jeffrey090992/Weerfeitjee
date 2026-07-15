import json
import requests
import os
from datetime import datetime

# 1. JSON inladen
with open('weer_historie.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

webhook_url = os.getenv('HISTORIE_WEBHOOK')

# 2. Vandaag bepalen (Nederlandse datum naar jouw JSON-formaat)
maanden = {
    "january": "januari", "february": "februari", "march": "maart", 
    "april": "april", "may": "mei", "june": "juni", 
    "july": "juli", "august": "augustus", "september": "september", 
    "october": "oktober", "november": "november", "december": "december"
}

nu = datetime.now()
dag = nu.strftime("%d") # bijv. "15"
maand_engels = nu.strftime("%B").lower() # bijv. "july"
vandaag_zoekterm = f"{dag.lstrip('0')} {maanden[maand_engels]}" # "15 juli"

# 3. Zoeken en versturen
gevonden = False
for sublijst in data:
    for item in sublijst:
        # Vergelijken zonder hoofdletters/spaties
        if item.get("datum", "").strip().lower() == vandaag_zoekterm:
            bericht = {
                "content": (
                    f"📅 **Datum:** {item['datum']}\n"
                    f"**{item['titel']}**\n"
                    f"Jaar: {item['jaar']}\n"
                    f"{item['tekst']}"
                )
            }
            requests.post(webhook_url, json=bericht)
            gevonden = True

if not gevonden:
    print(f"Geen feit gevonden voor vandaag: '{vandaag_zoekterm}'")
