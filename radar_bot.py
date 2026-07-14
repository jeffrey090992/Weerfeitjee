import requests
import os

WEBHOOK_URL = os.getenv('WEBHOOK_URL')

def send_radar():
    if not WEBHOOK_URL:
        return

    # Dit is een URL die een live snapshot van de KNMI-radar genereert
    radar_url = "https://cdn.knmi.nl/knmi/map/preview/radar/radar-loop.gif"
    
    payload = {
        "content": "Actueel radarbeeld (KNMI):",
        "embeds": [{
            "image": {"url": radar_url}
        }]
    }
    
    try:
        # Verstuur als JSON embed
        requests.post(WEBHOOK_URL, json=payload)
    except Exception as e:
        print(e)

if __name__ == "__main__":
    send_radar()
