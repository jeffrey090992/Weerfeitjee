import json
import datetime
import os

# 1. Bepaal de huidige datum in het formaat DD-MM
vandaag = datetime.datetime.now().strftime("%d-%m")
vandaag_zoekterm = vandaag.strip().lower()

def verstuur_weer_bericht():
    # 2. Zorg dat het pad correct is
    bestandspad = os.path.join(os.path.dirname(__file__), 'weer_historie.json')
    
    try:
        with open(bestandspad, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Fout bij het openen van JSON: {e}")
        return

    # 3. Veilige loop met type-controle
    for item in data:
        # Controleer of item een dictionary is
        if isinstance(item, dict):
            # Gebruik .get() veilig
            datum = item.get("datum", "")
            if datum.strip().lower() == vandaag_zoekterm:
                print(f"Match gevonden voor {vandaag}: {item}")
                # Hier komt jouw logica om het bericht te sturen via de webhook
                # bijv: requests.post(os.environ['HISTORIE_WEBHOOK'], json=item)
        else:
            # Als er per ongeluk een string in de lijst staat, negeren we deze
            print(f"Skipping ongeldig item: {type(item)} - {item}")

if __name__ == "__main__":
    verstuur_weer_bericht()
