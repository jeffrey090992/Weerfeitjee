import os
import requests
from datetime import datetime

WEBHOOK = os.getenv("HISTORIE_WEBHOOK")

bericht = {
    "username": "📜 Weerhistorie Nederland",
    "embeds": [
        {
            "title": "🔥 Historisch weerfeit",
            "description": (
                "📅 25 juli 2019\n\n"
                "Nederland beleefde een extreme hittegolf "
                "met zeer hoge temperaturen."
            ),
            "color": 16753920
        }
    ]
}

requests.post(WEBHOOK, json=bericht)

print("Verstuurd")
