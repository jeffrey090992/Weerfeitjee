import requests
import os
import time

# Dit script haalt de waarde uit de omgeving (via de workflow aangestuurd)
WEBHOOK_URL = os.getenv('WEBHOOK_URL')

def send_radar():
    if not WEBHOOK_URL:
        print("FOUT: Geen WEBHOOK_URL gevonden!")
        return

    # De URL van Buienradar met een tijdstempel om caching te voorkomen
    radar_url = f"https://api.buienradar.nl/image/1.0/RadarMapNL?w=500&h=512&t={int(time.time())}"
    
    payload = {
        "content": "Hier is het actuele radarbeeld:",
        "embeds": [{
            "title": "Buienradar Nederland",
            "image": {"url": radar_url},
            "footer": {"text": "Bron: Buienradar.nl"}
        }]
    }
    
    response = requests.post(WEBHOOK_URL, json=payload)
    if response.status_code == 204:
        print("Succesvol verstuurd naar Discord!")
    else:
        print(f"Fout bij versturen: {response.status_code}, {response.text}")

if __name__ == "__main__":
    send_radar()
