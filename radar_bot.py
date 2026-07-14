import requests

RADAR_URL = "https://www.meteologix.com/nl/weerkaart"

r = requests.get(
    RADAR_URL,
    headers={
        "User-Agent": "Mozilla/5.0"
    },
    timeout=20
)

print("Status:", r.status_code)
print("Type:", r.headers.get("content-type"))
print("Grootte:", len(r.content))
