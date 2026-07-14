import requests
import os
import json
from datetime import datetime

WEBHOOK_URL = os.getenv("WEBHOOK_URL")

# RainViewer radarbeeld
RADAR_URL = "https://tilecache.rainviewer.com/v2/radar/latest/256/6/33/21/1/1_1.png"


def send_radar():
    if not WEBHOOK_URL:
        print("❌ WEBHOOK_URL ontbreekt")
        return

    # Radar ophalen
    try:
        radar = requests.get(RADAR_URL, timeout=20)
        radar.raise_for_status()

        if "image" not in radar.headers.get("content-type", ""):
            print("❌ Geen afbeelding ontvangen")
            print(radar.headers.get("content-type"))
            return

    except Exception as e:
        print("❌ Radar ophalen mislukt:", e)
        return

    payload = {
        "embeds": [
            {
                "title": "🌧️ Actueel weerradarbeeld",
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
            radar.content,
            "image/png"
        )
    }

    try:
        response = requests.post(
            WEBHOOK_URL,
            data={
                "payload_json": json.dumps(payload)
            },
            files=files,
            timeout=30
        )

        if response.status_code == 204:
            print("✅ Radar verstuurd naar Discord")
        else:
            print("❌ Discord fout:", response.status_code)
            print(response.text)

    except Exception as e:
        print("❌ Webhook fout:", e)


if __name__ == "__main__":
    send_radar()
