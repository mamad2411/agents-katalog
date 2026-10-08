---
name: termin-assistent
description: "Schlägt Termine unter Berücksichtigung von Gerichtsterminen, Fristen und Kanzlei-Kalender (MS Graph oder iCal) vor. Triggert bei Terminvorschlag, Terminfindung, Kalender-Planung, freie Slots. Work-in-progress (Welle 5)."
status: Work-in-progress
welle: 5
bereich: fristen-termine
rdg_einordnung: "Organisatorische Terminfindung; keine Rechtsdienstleistung."
daten_hinweis: "Kalenderdaten des Kanzlei-Tenants — DSGVO beachten."
haftung: "Terminvorschläge kollidierende Fristen sind Hinweise; Bestätigung durch die Kanzlei erforderlich."
---

# termin-assistent

> **Status: `Work-in-progress`** — Stub aus dem Repo-Gerüst (Welle-1-Fundament). Implementierung folgt gemäß Build-Reihenfolge (Welle 5).

## Zweck

Schlägt Termine unter Berücksichtigung von Gerichtsterminen, Fristen und Kanzlei-Kalender (MS Graph oder iCal-Datei) vor.

## Eingaben (Datei-Kontrakt, P2)

*Noch zu spezifizieren in `schema/` — jeder Skill definiert Ein-/Ausgaben als Dateien; Live-Connectoren sind optionale Adapter.*

## Ablauf

*Folgt mit der Implementierung.*

## Output-Format

*Folgt mit der Implementierung. Deterministik-Grenze (P3): Jeder Zahlen-/Datums-/Geldwert im Output stammt aus einem Executor und ist als solcher markiert.*
