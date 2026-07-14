import requests
import os
import time

# Dit script haalt de webhook-URL veilig uit de GitHub Secrets
WEBHOOK_URL = os.getenv('WEBHOOK_URL')

def send_radar():
    if not WEBHOOK_URL:
        print("FOUT: Geen WEBHOOK_URL gevonden!")
        return

    # De stabiele URL voor het actuele radarbeeld van Buienradar
    # De tijdstempel aan het einde voorkomt dat Discord een oud plaatje uit de cache laat zien
    radar_url = f"https://image.buienradar.nl/2.0/image/single/RadarMapNL?width=500&height=512&extension=png&renderType=block&_={int(time.time())}"
    
    payload = {
        "content": "Hier is het actuele radarbeeld:",
        "embeds": [{
            "title": "Buienradar Nederland",
            "image": {"url": radar_url},
            "footer": {"text": "Bron: Buienradar.nl"}
        }]
    }
    
    try:
        # We voegen een User-Agent toe zodat de API het verzoek niet blokkeert
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.post(WEBHOOK_URL, json=payload, headers=headers)
        
        if response.status_code == 204:
            print("Succesvol verstuurd naar Discord!")
        else:
            print(f"Fout bij versturen: {response.status_code}, {response.text}")
    except Exception as e:
        print(f"Er is een fout opgetreden: {e}")

if __name__ == "__main__":
    send_radar()
