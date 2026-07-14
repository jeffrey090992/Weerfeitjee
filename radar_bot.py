import requests
import os
import time

# Je webhook URL uit de Secrets
WEBHOOK_URL = os.getenv('WEBHOOK_URL')

def send_radar():
    # De URL van Buienradar met een tijdstempel om caching te voorkomen
    # Discord refresht het plaatje soms niet als de URL exact hetzelfde blijft
    radar_url = f"https://api.buienradar.nl/image/1.0/RadarMapNL?w=500&h=512&t={int(time.time())}"
    
    payload = {
        "content": "Hier is het actuele radarbeeld:",
        "embeds": [{
            "title": "Buienradar Nederland",
            "image": {"url": radar_url},
            "footer": {"text": "Bron: Buienradar.nl"}
        }]
    }
    
    requests.post(WEBHOOK_URL, json=payload)

if __name__ == "__main__":
    send_radar()
