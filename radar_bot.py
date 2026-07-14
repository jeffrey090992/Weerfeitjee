import requests
import os

WEBHOOK_URL = os.getenv('WEBHOOK_URL')

def send_radar():
    if not WEBHOOK_URL:
        print("FOUT: Geen WEBHOOK_URL gevonden!")
        return

    # De URL van het plaatje
    radar_url = "https://image.buienradar.nl/2.0/image/single/RadarMapNL?width=500&height=512&extension=png&renderType=block"
    
    # 1. Download het plaatje
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(radar_url, headers=headers)
    
    if response.status_code == 200:
        with open("radar.png", "wb") as f:
            f.write(response.content)
    else:
        print(f"Kon plaatje niet downloaden, status: {response.status_code}")
        return

    # 2. Verstuur het bestand naar Discord
    # BELANGRIJK: Gebruik 'data' en 'files', maar GEEN 'json'
    with open("radar.png", "rb") as f:
        files = {'file': ('radar.png', f, 'image/png')}
        data = {"content": "Hier is het actuele radarbeeld:"}
        
        response = requests.post(WEBHOOK_URL, data=data, files=files)
        
        if response.status_code == 200 or response.status_code == 204:
            print("Succesvol verstuurd als bestand!")
        else:
            print(f"Fout bij versturen naar Discord: {response.status_code}, {response.text}")

if __name__ == "__main__":
    send_radar()
