import json
import random
import requests
import os

# Laad de vragenlijst
with open('vragen.json', 'r', encoding='utf-8') as f:
    vragen_lijst = json.load(f)

# Kies een willekeurige vraag
item = random.choice(vragen_lijst)

# Gebruik de correcte env-naam
webhook_url = os.environ['VRAGEN_WEBHOOK']

# Bouw de embed
embed = {
    "title": "Raad het weer!",
    "description": item["vraag"],
    "color": 3447003
}

# Voeg alleen een afbeelding toe als er een url is ingevuld
if item.get("image_url"):
    embed["image"] = {"url": item["image_url"]}

data = {
    "content": "🌤️ **Dagelijkse Weer-Quiz:**",
    "embeds": [embed]
}

# Verstuur naar Discord
response = requests.post(webhook_url, json=data)
response.raise_for_status()
