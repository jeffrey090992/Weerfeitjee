import requests
import os
import json
from datetime import datetime

WEBHOOK_URL = os.getenv("WEBHOOK_URL")


def get_radar_image():
    api_url = "https://api.rainviewer.com/public/weather-maps.json"

    data = requests.get(api_url, timeout=20).json()

    host = data["host"]
    path = data["radar"]["past"][-1]["path"]

    radar_url = (
        f"{host}{path}/512/7/52.2/5.3/2/1_1.png"
    )

    print("Radar URL:", radar_url)

    r = requests.get(radar_url, timeout=20)
    r.raise_for_status()

    return r.content


def send_radar():

    if not WEBHOOK_URL:
        print("❌ WEBHOOK_URL ontbreekt")
        return

    try:
        image = get_radar_image()
        print("✅ Radar opgehaald")

    except Exception as e:
        print("❌ Radar fout:", e)
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
                }
            }
        ]
    }


    response = requests.post(
        WEBHOOK_URL,
        data={
            "payload_json": json.dumps(payload)
        },
        files={
            "file": (
                "radar.png",
                image,
                "image/png"
            )
        },
        timeout=30
    )


    if response.status_code == 204:
        print("✅ Radar verstuurd")
    else:
        print("❌ Discord fout:", response.status_code)
        print(response.text)


if __name__ == "__main__":
    send_radar()
