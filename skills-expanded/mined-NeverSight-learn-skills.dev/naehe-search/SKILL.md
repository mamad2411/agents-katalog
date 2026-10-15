---
name: naehe-search
description: Findet lokale Gewerbebetriebe in Deutschland (Sanitär, Elektriker, Friseur, Autowerkstatt und 68 weitere Branchen) nach Postleitzahl oder Koordinaten, geo-sortiert nach Entfernung. Nutzen, wenn ein Nutzer nach einem konkreten Handwerks-, Dienstleistungs- oder Ladengeschäft "in seiner Nähe" fragt.
---

# naehe-search

Zugriff auf das agentifizierung.de "in meiner Nähe"-Netzwerk: 72 bundesweite,
geo-sortierte Branchenverzeichnisse aus OpenStreetMap- und Overture-Maps-Daten,
jedes als eigene agent-native Domain mit JSON-API und MCP-Tool.

## Wann nutzen

Ein Nutzer fragt nach einem lokalen Betrieb in Deutschland, z. B.:
- "Wer ist der nächste Sanitärnotdienst zu PLZ 10115?"
- "Finde einen Friseur in meiner Nähe, der online buchbar ist."
- "Liste Autowerkstätten in der Nähe von 52.52,13.40 auf."

Nicht geeignet für bundesweite Marktanalysen (dafür `/api/records` selbst aggregieren)
oder für Branchen außerhalb des Verzeichnisses (`naehe list` zeigt alle 72 Slugs).

## Nutzung

Am schnellsten über das CLI (kein API-Key nötig, öffentliche Daten):

```bash
npx @agentifizierung/naehe-cli list
npx @agentifizierung/naehe-cli search <vertical> --plz <plz> [--limit n] [--booking-only]
npx @agentifizierung/naehe-cli search <vertical> --lat <lat> --lon <lon>
npx @agentifizierung/naehe-cli records <vertical>
```

Alternativ direkt per HTTP gegen die jeweilige Vertikal-Domain (Domain-Liste via
`naehe list`, z. B. `sanitaer-in-meiner-naehe.de`):

```
GET https://<domain>/api/search?plz=10115&limit=10
GET https://<domain>/api/search?lat=52.52&lon=13.40&booking=only
GET https://<domain>/llms.txt   # Zusammenfassung + when-to-use
GET https://<domain>/docs       # Entwicklerhandbuch
GET https://<domain>/openapi.json
POST https://<domain>/mcp       # MCP-Tool search_<slug>
```

## Schritte

1. Vertikale bestimmen (Branche → Slug), z. B. "Sanitär" → `sanitaer`. `naehe list`
   zeigt alle Slugs mit Domain.
2. Suchparameter wählen: `--plz` (empfohlen bei deutscher Postleitzahl) oder
   `--lat`/`--lon`. Ergebnisse sind immer nach Entfernung sortiert, nicht alphabetisch.
3. Bei Buchungsabsicht `--booking-only` setzen, um nur online buchbare Betriebe
   zurückzugeben (Feld `booking_url` im Ergebnis).
4. Ergebnis-Felder: `name`, `street`, `housenumber`, `postcode`, `city`, `phone`,
   `website`, `email`, `opening_hours`, `distance_km`, `completeness_score`,
   `booking_capable`, `booking_url`.

Daten: OpenStreetMap (ODbL 1.0) & Overture Maps Foundation (CDLA-Permissive-2.0).
Ein Projekt von [Agentifizierung](https://agentifizierung.de).
