---
name: szenario-cap-table-bereinigung
description: "Wenn es um Szenario Cap Table Bereinigung in Plugin: status-navigator-step-plan geht: prüft Frist, Form, Zuständigkeit, Rechtsweg und Sofortmaßnahmen; liefert eine Fristen- und Risikoampel mit Sofortschritten."
---

# Szenario Cap Table Bereinigung

## Rolle und Fokus
Bereinigung mehrerer widerspruechlicher Cap Tables. Status-Navigator vergleicht Cap Tables miteinander und mit den zugrundeliegenden Vertraegen.

## Anwendungsbeispiel
LausitzStorage Cap-Table-Bereinigung: drei Versionen (siehe `diskrepanzen-aufdecken`) zeigen die NordCap-Schwankung 48/51/48 %. Prüfung ergibt: keine Wandlung dokumentiert; v2 stammt aus NordCap-Datenraum und enthielt einen Tippfehler bei Konsortium Stadtwerke-Cottbus-Anteil; v3 ist die fehlerbereinigte Investor-Update-Version. Empfehlung Soll-Cap-Table = v3 mit Vermerk.

## Output-Module
- Soll-Cap-Table mit Quellnachweis je Zeile
- Abweichungs-Memo zu den abweichenden Versionen
- Querverweis an Skill `dokumententyp-beschluesse` bei vermuteter Wandlung
