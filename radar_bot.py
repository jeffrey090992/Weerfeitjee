import requests
import os
import json
from datetime import datetime

WEBHOOK_URL = os.getenv("WEBHOOK_URL")


def get_radar_image():
    # RainViewer actuele radar informatie
    api_url = "https://api.rainviewer.com/public/weather-maps.json"

    data = requests.get(api_url, timeout=20).json()

    host = data["host"]
    latest = data["radar"]["past"][-1]

    path = latest["path"]

    # Nederland centrum:
    # size / zoom / latitude / longitude / kleur / opties
    radar_url = (
        f"{host}{path}/512/6/52.2/5.3/2/1_1.png"
    )

    print("Radar URL:")
    print(radar_url)

    image = requests.get(radar_url, timeout=20)
    image.raise_for_status()

    return image.content


def send_radar():

    if not WEBHOOK_URL:
        print("❌ WEBHOOK_URL ontbreekt")
        return

    try:
        image = get_radar_image()
        print("✅ Radar afbeelding opgehaald")

    except Exception as e:
        print("❌ Radar ophalen mislukt:", e)
        return


    payload = {
        "embeds": [
            {
                "title": "🌧️ Actueel weerradar Nederland",
                "description": datetime.now().strftime(
                    "Update: %d-%m-%Y %H:%M:%S"
                ),
                "image": {
                    "url": "attachment://radar.png"
                },
                "footer": {
                    "text": "Bron: RainViewer"
                }
            }
        ]
    }


    files = {
        "file": (
            "radar.png",
            image,
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
        print("✅ Radar verstuurd naar Discord")
    else:
        print("❌ Discord fout:", response.status_code)
        print(response.text)


if __name__ == "__main__":
    send_radar()
