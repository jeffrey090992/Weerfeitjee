import requests
import os

WEBHOOK_URL = os.getenv('WEBHOOK_URL')

def send_radar():
    if not WEBHOOK_URL:
        return

    # Gebruik een proxy-link die Discord meestal wel accepteert
    radar_url = "https://images.weserv.nl/?url=https://cdn.weerplaza.nl/data/radar/netherlands/radar_512x512.png"
    
    payload = {
        "embeds": [{
            "title": "Actueel Radarbeeld",
            "image": {"url": radar_url}
        }]
    }
    
    requests.post(WEBHOOK_URL, json=payload)

if __name__ == "__main__":
    send_radar()
