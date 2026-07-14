import requests
import os
import json
from datetime import datetime

WEBHOOK_URL = os.getenv("WEBHOOK_URL")


def get_radar_image():
    # RainViewer API voor actuele radar
    api_url = "https://api.rainviewer.com/public/weather-maps.json"

    response = requests.get(api_url, timeout=20)
    response.raise_for_status()

    data = response.json()

    # Laatste beschikbare radarbeeld
    host = data["host"]
    path = data["radar"]["past"][-1]["path"]

    # Nederland gecentreerd
    # zoom 7 = dichterbij Nederland
    radar_url = (
        f"{host}{path}/512/7/52.2/5.3/2/1_1.png"
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

    # Radar ophalen
    try:
        image = get_radar_image()
        print("✅ Radar opgehaald")

    except Exception as e:
        print("❌ Radar ophalen mislukt:", e)
        return


    # Discord embed
    payload = {
        "embeds": [
            {
                "title": "🌧️ Actueel weerradar Nederland",
                "description": (
                    "Update: "
                    + datetime.now().strftime("%d-%m-%Y %H:%M:%S")
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


    # Afbeelding uploaden
    files = {
        "file": (
            "radar.png",
            image,
            "image/png"
        )
    }


    result = requests.post(
        WEBHOOK_URL,
        data={
            "payload_json": json.dumps(payload)
        },
        files=files,
        timeout=30
    )


    if result.status_code == 204:
        print("✅ Radar verstuurd naar Discord")
    else:
        print("❌ Discord fout:", result.status_code)
        print(result.text)


if __name__ == "__main__":
    send_radar()
