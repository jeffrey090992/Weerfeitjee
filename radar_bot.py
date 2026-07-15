import os
import requests
from datetime import datetime

# Discord webhook uit GitHub Secret
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

# Nederlandse radarafbeelding
RADAR_URL = "https://cdn.knmi.nl/knmi/map/page/weer/weerkaarten/radar/ani-radar-loop.gif"


def verstuur_radar():
    tijd = datetime.now().strftime("%d-%m-%Y %H:%M")

    bericht = {
        "username": "🇳🇱 Nederlandse Weerradar",
        "embeds": [
            {
                "title": "📡 Nederlandse Weerradar",
                "description": f"Laatste radarupdate\n🕒 {tijd}",
                "color": 3447003,
                "image": {
                    "url": RADAR_URL
                },
                "footer": {
                    "text": "Automatische weerupdate"
                }
            }
        ]
    }

    response = requests.post(
        WEBHOOK_URL,
        json=bericht
    )

    if response.status_code == 204:
        print("Radar succesvol verstuurd")
    else:
        print("Fout:", response.status_code)
        print(response.text)


if __name__ == "__main__":
    verstuur_radar()
