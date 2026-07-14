import requests
import os

WEBHOOK_URL = os.getenv('WEBHOOK_URL')

def send_radar():
    if not WEBHOOK_URL:
        print("FOUT: Geen WEBHOOK_URL gevonden!")
        return

    # De URL van het plaatje
    radar_url = "https://image.buienradar.nl/2.0/image/single/RadarMapNL?width=500&height=512&extension=png&renderType=block"
    
    # 1. Download het plaatje naar een tijdelijk bestand
    response = requests.get(radar_url, headers={"User-Agent": "Mozilla/5.0"})
    if response.status_code == 200:
        with open("radar.png", "wb") as f:
            f.write(response.content)
    else:
        print("Kon plaatje niet downloaden")
        return

    # 2. Verstuur het bestand naar Discord
    with open("radar.png", "rb") as f:
        files = {'file': ('radar.png', f, 'image/png')}
        payload = {"content": "Hier is het actuele radarbeeld:"}
        response = requests.post(WEBHOOK_URL, data=payload, files=files)
        
        if response.status_code == 200:
            print("Succesvol verstuurd als bestand!")
        else:
            print(f"Fout: {response.status_code}")

if __name__ == "__main__":
    send_radar()
