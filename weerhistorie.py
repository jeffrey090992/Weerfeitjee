import json
from datetime import datetime

# 1. JSON-bestand inladen
try:
    with open('weer_historie.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
except FileNotFoundError:
    print("Fout: Het bestand 'weer_historie.json' is niet gevonden.")
    exit()

# 2. Huidige datum bepalen (bijv. "07-15")
vandaag = datetime.now().strftime("%m-%d")

# 3. Zoekfunctie
gevonden_feit = None

# Doorloop de seizoenen en vervolgens de dagen per seizoen
for seizoen, dagen_lijst in data.items():
    for item in dagen_lijst:
        # Hier checken we de datum binnen het item
        if item.get("datum") == vandaag:
            gevonden_feit = item
            break
    if gevonden_feit:
        break

# 4. Resultaat tonen
if gevonden_feit:
    print(f"Datum: {gevonden_feit['datum']}")
    print(f"Titel: {gevonden_feit['titel']}")
    print(f"Tekst: {gevonden_feit['tekst']}")
else:
    print(f"Geen historisch weerfeit gevonden voor {vandaag}.")
