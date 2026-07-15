import json
from datetime import datetime

# 1. JSON-bestand inladen
try:
    with open('weer_historie.json', 'r', encoding='utf-8') as f:
        # Dit bestand is een lijst van lijsten (data = [[{...}, {...}], [{...}]])
        data = json.load(f)
except FileNotFoundError:
    print("Fout: Het bestand 'weer_historie.json' is niet gevonden.")
    exit()

# 2. Huidige datum bepalen (bijv. "15 juli")
# Let op: Zorg dat je JSON-datumformaat ("15 juli") overeenkomt met de output hieronder
vandaag = datetime.now().strftime("%-d %B").lower() 

# 3. Zoekfunctie voor geneste lijst
gevonden_feiten = []

for sublijst in data:
    for item in sublijst:
        # Vergelijking maken (maak beide lowercase voor zekerheid)
        if item.get("datum", "").lower() == vandaag:
            gevonden_feiten.append(item)

# 4. Resultaat tonen
if gevonden_feiten:
    for feit in gevonden_feiten:
        print(f"--- {feit['titel']} ---")
        print(f"Datum: {feit['datum']} ({feit['jaar']})")
        print(f"Seizoen: {feit['seizoen']}")
        print(f"Tekst: {feit['tekst']}\n")
else:
    print(f"Geen historisch weerfeit gevonden voor {vandaag}.")
