from datetime import datetime
import json
import os
import requests


def verstuur_weer_bericht():
  # 1. Bepaal de huidige datum
  vandaag = datetime.now().strftime("%d-%m")
  print(f"Zoeken naar records voor: {vandaag}")

  # 2. JSON inladen
  try:
    with open("weer_historie.json", "r", encoding="utf-8") as f:
      data = json.load(f)
  except Exception as e:
    print(f"Fout bij inladen JSON: {e}")
    return

  # 3. Gewenste volgorde en vertaallijst
  volgorde = [
      "hoogste_max",
      "laagste_max",
      "hoogste_min",
      "laagste_min",
      "hoogste_dagsom_neerslag",
      "minimum_10cm_temperatuur",
  ]

  labels = {
      "hoogste_max": "☀️ Hoogste maximum temperatuur",
      "laagste_max": "⛅ Laagste maximum temperatuur",
      "hoogste_min": "🌡️ Hoogste minimum temperatuur",
      "laagste_min": "❄️ Laagste minimum temperatuur",
      "hoogste_dagsom_neerslag": "🌧️ Hoogste dagsom",
      "minimum_10cm_temperatuur": "🌱 Laagste minimum temperatuur 10cm",
  }

  # 4. Zoeken naar matches
  webhook_url = os.environ.get("HISTORIE_WEBHOOK")
  if not webhook_url:
    print("Fout: HISTORIE_WEBHOOK niet gevonden in omgeving.")
    return

  # Maak een dictionary om records snel op te zoeken per record_type
  gevonden_records = {}
  for item in data:
    if isinstance(item, dict) and item.get("datum") == vandaag:
      record_type = item.get("record_type")
      if record_type:
        gevonden_records[record_type] = item

  # 5. Velden opbouwen in de exact ingestelde volgorde
  fields = []
  for record_type in volgorde:
    item = gevonden_records.get(record_type)
    if item:
      titel_tekst = labels.get(record_type, record_type)

      if "mm" in item or "mm" in str(item).lower():
        waarde = item.get("mm", "Onbekend")
        waarde_tekst = f"{waarde} mm"
      else:
        temperatuur = item.get("temperatuur", "")
        waarde_tekst = f"{temperatuur}°C"

      jaar = item.get("jaar", "")
      station = item.get("station", "")
      jaar_station = f"{jaar} ({station})" if station else str(jaar)

      waarde_regel = f"**{waarde_tekst}** in {jaar_station}"

      # Extra opmerking toevoegen bij de 10cm temperatuur
      if record_type == "minimum_10cm_temperatuur":
        waarde_regel += "\n*(Wordt bijgehouden sinds 1971)*"

      fields.append(
          {"name": titel_tekst, "value": waarde_regel, "inline": False}
      )

  # 6. Alles verzenden in ÉÉN bericht als er records zijn gevonden
  if fields:
    message = {
        "embeds": [{
            "title": f"Dagrecords - {vandaag}",
            "description": (
                "Alle weerrecords voor deze dag in de geschiedenis:"
            ),
            "color": 16753920,
            "fields": fields,
        }]
    }

    try:
      response = requests.post(webhook_url, json=message, timeout=10)
      response.raise_for_status()
      print(f"Verstuurd! Status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
      print(f"Fout bij versturen naar Discord webhook: {e}")
  else:
    print("Geen records gevonden voor vandaag.")


if __name__ == "__main__":
  verstuur_weer_bericht()
