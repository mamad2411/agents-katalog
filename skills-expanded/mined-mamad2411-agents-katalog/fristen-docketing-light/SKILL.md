---
name: fristen-docketing-light
description: "Export berechneter Fristen als iCal/CSV — in fristenrechner integriert (calc → export in einem Skill). Dieser Eintrag bleibt Platzhalter für erweitertes Docketing (Sammel-Export, Import-Profile). Work-in-progress (Welle 4)."
status: Work-in-progress
welle: 4
bereich: fristen-termine
rdg_einordnung: "Technischer Export rechnerisch ermittelter Termine; keine Fristenverwaltung als Dienstleistung."
daten_hinweis: "Fristdaten können Aktenzeichen tragen — Exportdateien wie Akten behandeln."
haftung: "Import und Kontrolle im Zielsystem verantwortet die Kanzlei; ersetzt keinen Fristenkalender mit Vier-Augen-Prinzip."
---

# fristen-docketing-light

> **Status: `Work-in-progress` — in [`fristenrechner`](../fristenrechner/SKILL.md) integriert.**
> Der iCal-/CSV-Export ist als **zweite Stufe** direkt in den Fristenrechner
> gewandert (calc → export in einem Skill), damit die Berechnung unmittelbar
> einen Kalender-Export erzeugt und nur bei einer Korrektur einen neuen. Dieser
> Eintrag bleibt als Platzhalter für darüber hinausgehende Docketing-Funktionen
> (z. B. Sammel-Export mehrerer Fristen, systemspezifische Import-Profile);
> ob er eigenständig bleibt oder entfällt, entscheidet der Maintainer.

## Zweck

Export berechneter Fristen als iCal/CSV zum Import in Kanzlei-Kalender oder
Kanzleisoftware. Die **Einzel-Frist**-Ausprägung dieser Funktion ist umgesetzt
in [`fristenrechner`](../fristenrechner/SKILL.md) über
`core/calc/fristen/kalender_executor.py` (Format-/Feld-/UID-Kontrakt:
[`fristenrechner/schema/README.md`](../fristenrechner/schema/README.md)).

## Eingaben (Datei-Kontrakt, P2)

*Für den Einzel-Frist-Export: der JSON-Report aus `core/calc/fristen/executor.py`
(siehe fristenrechner). Eine mögliche Erweiterung dieses Skills — Sammel-
Export mehrerer Reports / systemspezifische Profile — ist noch zu spezifizieren.*

## Ablauf

*Einzel-Frist: siehe [`fristenrechner`](../fristenrechner/SKILL.md),
Abschnitt „Ablauf" (Schritte 5–6). Erweiterungen folgen mit der Implementierung.*

## Output-Format

*iCal `.ics` / CSV wie in fristenrechner. Deterministik-Grenze (P3): Jeder
Datums-/Zahlenwert im Output stammt aus einem Executor und ist als solcher
markiert.*
