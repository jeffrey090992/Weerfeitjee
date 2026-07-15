import os
import requests
from datetime import datetime

WEBHOOK = os.getenv("HISTORIE_WEBHOOK")

if not WEBHOOK:
    raise Exception("Webhook ontbreekt")

# Nederlandse weerhistorie per seizoen
historie = {

    "winter": [
        {
            "datum": "1 februari 1953",
            "titel": "🌊 Watersnoodramp",
            "tekst": "Een zware stormvloed veroorzaakte grote overstromingen in Zeeland en Zuid-Holland."
        },
        {
            "datum": "1963",
            "titel": "❄️ Strenge winter 1963",
            "tekst": "Een van de strengste winters ooit gemeten in Nederland met veel ijs en sneeuw."
        },
        {
            "datum": "18 januari 2018",
            "titel": "🌪️ Storm Friederike",
            "tekst": "Een zware storm trok over Nederland met zeer zware windstoten."
        }
    ],

    "lente": [
        {
            "datum": "31 maart 1975",
            "titel": "❄️ Late winterkou",
            "tekst": "Een koude periode zorgde voor uitzonderlijk lage lentetemperaturen."
        },
        {
            "datum": "April 1991",
            "titel": "☀️ Zeer warme lente",
            "tekst": "Een uitzonderlijk warme periode met zomerse temperaturen."
        }
    ],

    "zomer": [
        {
            "datum": "25 juli 2019",
            "titel": "🔥 Nationaal warmterecord",
            "tekst": "Nederland bereikte tijdens een extreme hittegolf recordtemperaturen."
        },
        {
            "datum": "5 juli 2023",
            "titel": "🌪️ Zomerstorm Poly",
            "tekst": "Een uitzonderlijk zware zomerstorm veroorzaakte veel schade."
        },
        {
            "datum": "2018",
            "titel": "☀️ Droogte van 2018",
            "tekst": "Een langdurige droge zomer zorgde voor lage waterstanden."
        },
        {
            "datum": "Juli 2010",
            "titel": "⛈️ Zware zomerbuien",
            "tekst": "Zware onweersbuien met hagel en wateroverlast trokken over Nederland."
        }
    ],

    "herfst": [
        {
            "datum": "25 januari 1990",
            "titel": "🌪️ Storm van 1990",
            "tekst": "Een van de zwaarste stormen van de twintigste eeuw trof Nederland."
        },
        {
            "datum": "28 oktober 2013",
            "titel": "🌪️ Herfststorm",
            "tekst": "Een krachtige storm veroorzaakte schade en verkeersproblemen."
        }
    ]
}


def seizoen():
    maand = datetime.now().month

    if maand in [12, 1, 2]:
        return "winter"
    elif maand in [3, 4, 5]:
        return "lente"
    elif maand in [6, 7, 8]:
        return "zomer"
    else:
        return "herfst"


# Kies dagelijks een andere gebeurtenis
vandaag = datetime.now().timetuple().tm_yday

lijst = historie[seizoen()]

gebeurtenis = lijst[vandaag % len(lijst)]


bericht = {
    "username": "📜 Weerhistorie Nederland",
    "embeds": [
        {
            "title": gebeurtenis["titel"],
            "description": (
                f"📅 **Datum:** {gebeurtenis['datum']}\n\n"
                f"{gebeurtenis['tekst']}\n\n"
                "🇳🇱 Nederlandse Weerhistorie"
            ),
            "color": 3447003,
            "footer": {
                "text": f"Seizoen: {seizoen().capitalize()}"
            },
            "timestamp": datetime.utcnow().isoformat()
        }
    ]
}


response = requests.post(
    WEBHOOK,
    json=bericht
)

if response.status_code == 204:
    print("✅ Weerhistorie verstuurd")
else:
    print("❌ Fout:", response.status_code)
    print(response.text)
