import requests
import os

# Haalt de webhook-URL uit de GitHub Secrets
WEBHOOK_URL = os.getenv('WEBHOOK_URL')

def send_radar():
    if not WEBHOOK_URL:
        print("FOUT: Geen WEBHOOK_URL gevonden!")
        return

    # De directe link naar het actuele radarbeeld van Weerplaza
    radar_url = "https://cdn.weerplaza.nl/data/radar/netherlands/radar_512x512.png"
    
    # We sturen een embed omdat dit het plaatje direct in Discord laat zien
    payload = {
        "content": "Hier is het actuele radarbeeld van Weerplaza:",
        "embeds": [{
            "title": "Actuele Buienradar",
            "image": {"url": radar_url},
            "footer": {"text": "Bron: Weerplaza.nl"}
        }]
    }
    
    headers = {"User-Agent": "Mozilla/5.0"}
    
    try:
        response = requests.post(WEBHOOK_URL, json=payload, headers=headers)
        if response.status_code == 204:
            print("Succesvol verstuurd naar Discord!")
        else:
            print(f"Fout bij versturen: {response.status_code}, {response.text}")
    except Exception as e:
        print(f"Er is een fout opgetreden: {e}")

if __name__ == "__main__":
    send_radar()
