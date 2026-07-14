import requests
import os
from datetime import datetime

WEBHOOK_URL = os.getenv("WEBHOOK_URL")

RADAR_URL = "https://cdn.weerplaza.nl/data/radar/netherlands/radar_512x512.png"


def send_radar():
    if not WEBHOOK_URL:
        print("❌ WEBHOOK_URL ontbreekt")
        return

    # Radarbeeld ophalen
    try:
        radar = requests.get(RADAR_URL, timeout=15)
        radar.raise_for_status()
    except Exception as e:
        print("❌ Radar ophalen mislukt:", e)
        return

    # Discord bericht
    payload = {
        "embeds": [
            {
                "title": "🌧️ Actueel Radarbeeld Nederland",
                "description": f"Laatste update: {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}",
                "image": {
                    "url": "attachment://radar.png"
                },
                "footer": {
                    "text": "Weerplaza radar"
                }
            }
        ]
    }

    # Afbeelding uploaden naar Discord
    files = {
        "file": (
            "radar.png",
            radar.content,
            "image/png"
        )
    }

    try:
        response = requests.post(
            WEBHOOK_URL,
            data={
                "payload_json": str(payload).replace("'", '"')
            },
            files=files,
            timeout=20
        )

        if response.status_code == 204:
            print("✅ Radar succesvol verstuurd")
        else:
            print("❌ Discord fout:", response.status_code)
            print(response.text)

    except Exception as e:
        print("❌ Webhook fout:", e)


if __name__ == "__main__":
    send_radar()
