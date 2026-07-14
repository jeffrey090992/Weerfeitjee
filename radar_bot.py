import requests
import os
import time

# Haalt de webhook-URL uit de GitHub Secrets
WEBHOOK_URL = os.getenv('WEBHOOK_URL')

def send_radar():
    if not WEBHOOK_URL:
        print("FOUT: Geen WEBHOOK_URL gevonden!")
        return

    # Directe URL naar het .png bestand met cache-busting
    radar_url = f"https://image.buienradar.nl/2.0/image/single/RadarMapNL?width=500&height=512&extension=png&renderType=block&_={int(time.time())}"
    
    payload = {
        "content": "Hier is het actuele radarbeeld:",
        "embeds": [{
            "title": "Buienradar Nederland",
            "image": {"url": radar_url},
            "footer": {"text": "Bron: Buienradar.nl"}
        }]
    }
    
    # Discord vereist vaak een User-Agent om afbeeldingen correct in te laden
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
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
