import json

# 1. Bestand inladen
with open('weer_historie.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 2. Vandaag vastleggen (exact zoals in jouw JSON)
vandaag = "15 juli"

# 3. Zoeken in de geneste lijst
gevonden = False
for sublijst in data:
    for item in sublijst:
        if item["datum"] == vandaag:
            print(f"Gevonden: {item['titel']}")
            print(f"Jaar: {item['jaar']}")
            print(f"Tekst: {item['tekst']}")
            gevonden = True

if not gevonden:
    print(f"Geen weerfeit gevonden voor {vandaag}")
