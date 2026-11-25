---
name: review-durchfuehren
description: "Wenn es um /tabellenreview-3d:review-durchführen in Tabellenreview 3D geht: prüft Frist, Form, Zuständigkeit, Rechtsweg und Sofortmaßnahmen; liefert eine Fristen- und Risikoampel mit Sofortschritten."
---

# /tabellenreview-3d:review-durchführen

## Triage zu Beginn

1. Welchen Teil des 3D-Wuerfels betrifft diese Operation?
2. Ist die Operation auditpflichtig? (alle Wuerfeloperationen sind zu protokollieren)
3. Wird das Ergebnis in die Mandatsakte aufgenommen?
4. Sind berufsrechtliche Sorgfaltspflichten einzuhalten? (§ 43 BRAO, § 50 BRAO)

## Rechtliche Grundlagen

- Rechtsprechung: keine Entscheidung aus Modellwissen zitieren; vor Ausgabe über offizielle oder frei zugängliche Quelle mit Gericht, Entscheidungsform, Datum, Aktenzeichen und tragender Aussage verifizieren.

## Eingaben

- `wuerfel-schema.yaml`
- `spaltenprompts.yaml`
- `zeilenprompts.yaml`
- `arbeitsblaetter.yaml`
- `zeilen-inventar.yaml`
- Praxisprofil unter `~/.claude/plugins/config/claude-fuer-deutsches-recht/tabellenreview-3d/CLAUDE.md`

## Ablauf pro Zelle

1. **Prompt zusammenführen:** Arbeitsblatt-Perspektive vor Spaltenprompt vor Zeilenprompt. Konflikte protokollieren.
2. **Quelldokument öffnen:** Pfad + Hash gegen Inventar abgleichen — falls Hash abweicht: Belegkette unterbrochen Prüfer-Flag setzen.
3. **Antwort extrahieren:** Antworttyp aus Spaltenprompt-Definition beachten (Freitext / zitat-mit-fundstelle / ja-nein / Datum / Geldbetrag / Aufzählung).
4. **Belegkette schreiben:** wörtliches Zitat in Anführungszeichen, danach Fundstelle (Datei-ID + Seite + Absatz + ggf. Ziffer).
5. **Ampel setzen:** anhand `ampel-regel` aus dem Spaltenprompt (rot / gelb / grün).
6. **Prüfer-Flag setzen wenn:**
 - OCR-Konfidenz unter 90 Prozent
 - Antworttyp `zitat-mit-fundstelle` aber kein Zitat extrahierbar
 - Konflikt zwischen Spalten- und Zeilenprompt
 - Mehrdeutigkeit (mehrere plausible Antworten im Dokument)
7. **Querweis aufbauen:** wenn Zellen-Ergebnis auf anderen Vertrag referenziert (`siehe Anlage 7 zu Vertrag X`) als Cross-Ref vermerken.
8. **Cache prüfen:** bei Quasi-Duplikaten (Ähnlichkeit über 95 Prozent) zur Zelle eines bereits geprüften Dokuments Cache-Treffer vorschlagen — Prüfer entscheidet ob übernommen.

## Reihenfolge

Standard: Arbeitsblatt-außen, Zeile-mittel, Spalte-innen. Optional: Spalte-außen wenn Spaltenprompt aufwaendig (z. B. Volltext-Indexierung) und über den Stapel gemeinsam profitiert.

## Grenzen

Jede Zelle ist ein Hinweis kein Befund. Prüfer-Flags sind die wichtigste Ausgabe — sie sagen wo der menschliche Prüfer hinschauen muss. Untermarkierung ist eine Einbahnstraße; Übermarkierung ist eine Zweiwegtür die ein Anwalt in 30 Sekunden schließt.
