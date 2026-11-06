---
name: dokumententyp-cap-tables
description: "Wenn es um Dokumententyp Cap Tables in Plugin: status-navigator-step-plan geht: ordnet Akteninhalt, Belege, Lücken und Nachforderungen; liefert ein direkt nutzbares Arbeitsprodukt mit Prüfpunkten, Risiken und nächstem Schritt."
---

# Dokumententyp Cap Tables

## Rolle und Fokus
Erkennt Cap Tables in beliebigem Format (Excel, PDF, eingebettete Tabellen). Erfasst Stichdatum, Gesellschafter, Anteile. Vorbereitung für Konsistenzvergleich mehrerer Versionen.

## Anwendungsbeispiel
LausitzStorage: drei Cap-Table-Versionen liegen vor. v1 (31.12.2025, von Mandantin), v2 (30.04.2026, von NordCap-Datenraum), v3 (Mai 2026, aus Investor-Update). Vergleich liefert die in `diskrepanzen-aufdecken` aufgenommene 48/51/48-Abweichung.

## Output-Module
- Versionsregister mit Stichdatum, Quelle, Status
- Normalisierte Cap-Table als Vorlage für den Konsistenzvergleich
- Querliste an `szenario-cap-table-bereinigung` wenn Abweichungen materiell
