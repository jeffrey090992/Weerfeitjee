import requests
import os
from datetime import datetime

WEBHOOK_URL = os.getenv("WEBHOOK_URL")

# RainViewer radar kaart Nederland
RADAR_URL = (
    "https://tilecache.rainviewer.com/v2/radar/"
    "latest/256/6/33/21/1/1_1.png"
)


def send_radar():
    if not WEBHOOK_URL:
        print("❌ WEBHOOK_URL ontbreekt")
        return

    try:
        radar = requests.get(RADAR_URL, timeout=15)
        radar.raise_for_status()
    except Exception as e:
        print("❌ Radar ophalen mislukt:", e)
        return

    payload = {
        "embeds": [
            {
                "title": "🌧️ Actueel radarbeeld",
                "description": datetime.now().strftime(
                    "Update: %d-%m-%Y %H:%M:%S"
                ),
                "image": {
                    "url": "attachment://radar.png"
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

    response = requests.post(
        WEBHOOK_URL,
        data={
            "payload_json": str(payload).replace("'", '"')
        },
        files=files
    )

    if response.status_code == 204:
        print("✅ Radar verstuurd")
    else:
        print("❌ Discord fout:", response.status_code)
        print(response.text)


if __name__ == "__main__":
    send_radar()
