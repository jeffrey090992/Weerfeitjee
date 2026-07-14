import requests
import os

# Haalt de webhook-URL uit de GitHub Secrets
WEBHOOK_URL = os.getenv('WEBHOOK_URL')

def send_radar():
    if not WEBHOOK_URL:
        print("FOUT: Geen WEBHOOK_URL gevonden!")
        return

    # De directe link naar het plaatje
    radar_url = "https://cdn.weerplaza.nl/data/radar/netherlands/radar_512x512.png"
    
    # 1. Download het plaatje naar een tijdelijk bestand
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(radar_url, headers=headers)
        if response.status_code == 200:
            with open("radar.png", "wb") as f:
                f.write(response.content)
        else:
            print(f"Kon plaatje niet downloaden, status: {response.status_code}")
            return
    except Exception as e:
        print(f"Fout bij downloaden: {e}")
        return

    # 2. Verstuur het bestand naar Discord
    # We sturen GEEN json, maar data + files
    with open("radar.png", "rb") as f:
        files = {'file': ('radar.png', f, 'image/png')}
        data = {"content": "Hier is het actuele radarbeeld van Weerplaza:"}
        
        response = requests.post(WEBHOOK_URL, data=data, files=files)
        
        if response.status_code in [200, 204]:
            print("Succesvol verstuurd als bestand!")
        else:
            print(f"Fout bij versturen naar Discord: {response.status_code}, {response.text}")

if __name__ == "__main__":
    send_radar()
