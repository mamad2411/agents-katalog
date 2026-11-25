---
name: excel-reiter-3-fehlend
description: "Wenn es um Reiter 3 Fehlende Dokumente in Plugin: status-navigator-step-plan geht: ordnet Akteninhalt, Belege, Lücken und Nachforderungen; liefert ein direkt nutzbares Arbeitsprodukt mit Prüfpunkten, Risiken und nächstem Schritt."
---

# Reiter 3 Fehlende Dokumente

## Rolle und Fokus
Reiter 3 listet alles, was fehlt oder noch nicht endgueltig vorliegt.
Jede Zeile hier ist eine offene Position, die in den Workflow von
Reiter 4 ueberfuehrt werden muss.

## Vorlage-Bezug
Reiter 3 folgt der Excel-Vorlage. Spalten:

| Spalte | Inhalt |
|---|---|
| Erforderliches Dokument / erforderlicher Nachweis | sprechend |
| Angefordert von | Person oder Kanzlei intern |
| Zu beschaffen von | Quelle: Behoerde, Notar, Vertragspartner |
| Grund der Erforderlichkeit | warum brauchen wir es, mit Querverweis Klausel oder Paragraph |
| Status | offen / Anforderung raus / in Bearbeitung / vorzubereiten / Frist |

## Anwendungsbeispiel
LausitzStorage-Akte: Reiter 3 enthaelt 12 Positionen, sortiert nach Frist:
- 09.06.: Aushaendigung LEAG-Aval (Frist § 11 Pacht ueberzogen)
- 10.06.: Notartermin Klarstellungs-Nachtrag Pacht
- 11.06.: Klarstellungs-Side-Letter Anlage 4
- 18.06.: ILB-Komitee Einzelaval 50Hertz
- 30.06.: BImSchG-Hauptantrag (Drohfrist LEAG)

## Output-Module
- Tabelleneintraege für Reiter 3
- Frist-Liste aufsteigend
- Eingangsstapel für Reiter 4 (Workflow)
- Optional Reiter 5 (Fristenkontrolle) mit Querverweis

## Grenzen
- **Beschaffungswege können sich verschieben.** Behoerdliche Bearbeitungszeiten
  realistisch ansetzen, nicht idealisieren.
- **Frist-Tracking ersetzt keinen Fristenkalender.** Anwaltlicher Fristenkalender
  bleibt verbindlich.

## Plugin-Kontext
Reiter 3 ist die Voraussetzung für Reiter 4. Ohne saubere Liste der
fehlenden Stuecke kann kein Workflow gebaut werden.
