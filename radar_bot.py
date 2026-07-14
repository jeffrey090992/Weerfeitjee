import requests
import os
import json
from datetime import datetime

WEBHOOK_URL = os.getenv("WEBHOOK_URL")

# RainViewer radar tegel (Nederland/regio)
RADAR_URL = "https://tilecache.rainviewer.com/v2/radar/latest/256/6/33/21/1/1_1.png"


def send_radar():
    if not WEBHOOK_URL:
        print("❌ WEBHOOK_URL ontbreekt")
        return

    # Radar ophalen
    try:
        r = requests.get(RADAR_URL, timeout=20)
        r.raise_for_status()

        if "image" not in r.headers.get("content-type", ""):
            print("❌ Geen afbeelding ontvangen")
            print(r.text[:200])
            return

    except Exception as e:
        print("❌ Radar ophalen mislukt:", e)
        return

    # Discord bericht
    payload = {
        "embeds": [
            {
                "title": "🌧️ Actueel Weerradarbeeld",
                "description": datetime.now().strftime(
                    "Update: %d-%m-%Y %H:%M:%S"
                ),
                "image": {
                    "url": "attachment://radar.png"
                },
                "footer": {
                    "text": "Radar via RainViewer"
                }
            }
        ]
    }

    files = {
        "file": (
            "radar.png",
            r.content,
            "image/png"
        )
    }

    response = requests.post(
        WEBHOOK_URL,
        data={
            "payload_json": json.dumps(payload)
        },
        files=files,
        timeout=30
    )

    if response.status_code == 204:
        print("✅ Radar succesvol naar Discord gestuurd")
    else:
        print("❌ Discord fout:", response.status_code)
        print(response.text)


if __name__ == "__main__":
    send_radar()
