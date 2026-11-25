---
name: datev-export
description: "Erzeugt aus strukturierten Buchungsdaten eine DATEV-EXTF-Buchungsstapel-Datei (Kategorie 21, Formatversion 700) zum Import beim Steuerberater — CP1252, Komma-Dezimal, streng validiert. Triggert bei DATEV-Export, EXTF, Buchungsstapel, Buchungssatz, an Steuerberater/Buchhaltung übergeben, Honorarrechnung verbuchen, DATEV-Import vorbereiten."
status: beta
welle: 4
bereich: zeit-abrechnung
rdg_einordnung: "Kaufmännische Hilfstätigkeit (Formatkonvertierung strukturierter Buchungsdaten in das DATEV-EXTF-Dateiformat) — keine Rechtsdienstleistung und keine Steuerberatung. Der Skill trifft keine buchhalterische Entscheidung (welches Konto/Gegenkonto, welcher BU-Schlüssel korrekt ist) — diese Zuordnung liefert die Kanzlei bzw. der Steuerberater als Eingabe; der Executor validiert nur deren Format."
daten_hinweis: "Belegfelder (Belegfeld 1/2, Buchungstext) enthalten typischerweise Rechnungsnummern und können Mandantennamen tragen. Speicherung/Verarbeitung nur innerhalb des dokumentierten Speicher-Perimeters (D10: Kanzleisoftware, lokal verschlüsseltes Kanzlei-Gerät, oder der Server, der ohnehin die Mandantendaten hostet/das Modell betreibt, z. B. AWS Bedrock Frankfurt) — kein neuer Speicherort außerhalb dieses Perimeters. Der Executor arbeitet rein lokal, ohne Netzwerkzugriff."
haftung: "Zweitkontrolle, zwingend: Das erzeugte EXTF ist vor dem Import in DATEV durch die Buchhaltung/den Steuerberater zu prüfen — insbesondere Konto-/Gegenkonto-Zuordnung, BU-Schlüssel und Buchungstext (der Executor validiert nur das Zahlenformat, nie die buchhalterische Richtigkeit). status: getestet vergibt der Maintainer erst nach einem echten, erfolgreichen DATEV-Import — automatisierte Tests (Spec-/Golden-File-Tests) rechtfertigen nur status: beta. ⚠️ Formatversion 700 und die Feldliste sind nicht primärquellen-verifiziert (developer.datev.de maschinell nicht lesbar) — vor dem ersten Echt-Import zwingend gegen die aktuelle DATEV-Dokumentation prüfen."
---

# datev-export

> **Status: `beta`** — automatisierte Tests laufen grün in CI (Spec-Tests,
> Golden-File-Tests, Reject-Tests, Idempotenz, `tests/`). Noch **nicht**
> händisch abgenommen — `status: getestet` vergibt der Maintainer erst nach
> einem echten DATEV-Import durch eine Steuerberatung (siehe
> [CONVENTIONS.md](https://github.com/eliasreiche/legal-ops-germany/blob/main/CONVENTIONS.md),
> Reifegrad-Leiter).
>
> ⚠️ **Formatversion 700 ist nicht primärquellen-verifiziert.**
> developer.datev.de blockt automatisierten Zugriff; die Header- und
> Spaltenliste wurden aus drei Sekundärquellen rekonstruiert und mit der
> Feldstruktur von [github.com/ledermann/datev](https://github.com/ledermann/datev)
> (MIT, Ruby) als reine Strukturreferenz abgeglichen — kein Code
> übernommen. **Vor dem ersten echten Import zwingend gegen die aktuelle
> DATEV-Dokumentation prüfen.**

## Zweck

Erzeugt aus strukturierten Buchungsdaten eine importierbare
**DATEV-EXTF-Datei** (Buchungsstapel, Kategorie 21, Formatversion 700) über
den Executor [`core/calc/extf/`](../../core/calc/extf/README.md) — CSV,
CP1252-kodiert, Semikolon-getrennt, Textfelder in doppelten
Anführungszeichen, Beträge als Komma-Dezimal (nie `float`).

**Scope-Grenze (bewusst, Maintainer-Entscheidung D20): nur
Buchungsstapel-Export.** Kein Parser für Rechnungen (das übernimmt Claude im
Ablauf unten, als Entwurf), keine Stammdaten-Übergabe (Kategorie 16,
Debitoren-/Kreditorenkonten) und kein Import — dieser Skill schreibt eine
Datei, die die Kanzlei bzw. der Steuerberater in DATEV **einliest**; der
Import selbst findet außerhalb dieses Repos statt.

**Kontenrahmen: konfigurierbar ohne Vorgabe.** Konto und Gegenkonto sind
Pflichteingaben — sie kommen von der Kanzlei bzw. vom Steuerberater. Der
Executor validiert **nur das Format** (numerisch, Länge konsistent zur
Header-Sachkontenlänge) und rät **niemals** einen SKR03- oder
SKR04-Kontenrahmen oder eine konkrete Kontonummer.

**Validierung streng.** Jeder Formatfehler (Betrag ≤ 0, nicht-numerisches
Konto, Belegdatum außerhalb des Buchungszeitraums, Buchungstext > 60
Zeichen, nicht-CP1252-Zeichen, unbestätigte Modell-Extraktion, …) führt zu
Exit 2 — **keine** Datei wird geschrieben. Ein defektes EXTF beim
Steuerberater ist teurer als eine saubere Ablehnung.

## Eingaben (Datei-Kontrakt, P2)

| Eingabe | Pflicht | Format | Beschreibung |
|---|---|---|---|
| Buchungsdaten-Anfrage | ja | `.json` | Eigenes Schema: `header` (Metadaten für die EXTF-Kopfzeile) + `buchungen` (Liste von Buchungssätzen). Vollständiges Schema: [`schema/README.md`](schema/README.md), Beispiel: [`schema/beispiel-eingabe.json`](schema/beispiel-eingabe.json). |

Kurzfassung: `header` verlangt u. a. `erzeugt_am` (ISO-Datum+Zeit — Stichtag
aus der Eingabe, **nie** die Wall-Clock, für byte-stabile
Re-Exporte/Idempotenz), `exportiert_von`, `beraternummer`,
`mandantennummer`, `wirtschaftsjahresbeginn`, `buchungszeitraum_von`/`_bis`
und `bezeichnung`. Jede Buchung verlangt u. a. `umsatz` (Decimal-String,
> 0), `soll_haben` (`S`/`H`), `konto`/`gegenkonto` (numerisch, Länge
passend zur Sachkontenlänge) und `belegdatum` (volles ISO-Datum — der
Executor prüft, dass es im Buchungszeitraum liegt, bevor er es auf `TTMM`
kürzt).

**Ausschließlich JSON — kein PDF/Text direkt.** Wenn nur eine Rechnung
(PDF/Text) vorliegt, erstellt Claude daraus zunächst einen JSON-Entwurf
(Ablauf-Schritt 1 unten); der Executor selbst liest nie ein Dokument.

## Ablauf

1. **Wenn nur eine Rechnung vorliegt (kein fertiges JSON): Claude entwirft
   die Buchungsdaten als JSON**, nach [`schema/README.md`](schema/README.md).
   Jede Zahl, die Claude dabei aus dem Dokument **ausliest statt vom Nutzer
   strukturiert zu bekommen**, markiert Claude in der betroffenen Buchung
   mit `"quelle": "modell-extraktion"` — noch **ohne** `"bestaetigt": true`.
   Claude legt diesen Entwurf dem Nutzer vor (Beträge, Konto/Gegenkonto,
   Belegnummer, Datum) und fragt ausdrücklich nach Bestätigung. Erst wenn
   der Nutzer bestätigt, setzt Claude `"bestaetigt": true` auf der
   jeweiligen Buchung — der Executor **lehnt sonst ab (Exit 2)** und
   exportiert nie unbestätigte modellgenerierte Zahlen (P3-Wahrung, D20).
   Direkt strukturiert gelieferte Buchungsdaten (Nutzer diktiert/liefert die
   Werte direkt) brauchen kein `quelle`-Feld.
2. **Claude ruft den Executor auf** (kein eigenes Rechnen/Formatieren durch
   das Modell):

   ```bash
   python3 ${CLAUDE_PLUGIN_ROOT}/core/calc/extf/executor.py \
     --input <buchungen.json> \
     --output <stapel.csv> \
     --output-report <report.json>
   ```

3. **Bei Exit 0**: Claude liest den JSON-Report und stellt dem Nutzer
   zusammen, was erzeugt wurde — Anzahl Buchungen, Buchungszeitraum,
   Bezeichnung, Beraternummer/Mandantennummer, sowie **immer**:
   - den ⚠️-Formatversions-Vorbehalt (`meta.formatversion_hinweis`),
   - den Zweitkontroll-Hinweis aus `haftung` (vor jedem Import prüfen),
   - dass der Skill nur den Buchungsstapel erzeugt hat — der Import selbst
     ist Sache der Kanzlei/des Steuerberaters.
4. **Bei Exit 2** (Eingabe-/Formatfehler): Claude gibt die Fehlermeldung
   unverändert wieder und korrigiert die Eingabe bzw. fragt nach — er rät
   kein Ersatz-Konto, keinen Ersatz-Betrag und exportiert keine Teil-Datei.
   Häufige Fälle: Betrag ≤ 0, Konto/Gegenkonto nicht numerisch oder falsche
   Stellenzahl, Belegdatum außerhalb `buchungszeitraum_von`/`_bis`,
   Buchungstext > 60 Zeichen, ein nicht CP1252-kodierbares Zeichen, oder
   eine Buchung mit `"quelle": "modell-extraktion"` ohne
   `"bestaetigt": true`.

## Output-Format

Zwei Dateien, beide aus [`core/calc/extf/executor.py`](../../core/calc/extf/executor.py) (P3):

- **EXTF-Datei** (`--output`): CSV, CP1252, Semikolon-getrennt — Zeile 1
  Metadaten-Header (31 Felder, [`header_format_700.json`](../../core/calc/extf/header_format_700.json)),
  Zeile 2 Spaltenköpfe, ab Zeile 3 ein Datensatz je Buchung (20 Spalten,
  [`buchungssatz_spalten_700.json`](../../core/calc/extf/buchungssatz_spalten_700.json)).
  Beispiel: [`schema/beispiel-stapel.csv`](schema/beispiel-stapel.csv).
- **JSON-Report** (`--output-report`, sonst stdout): `meta` (u. a.
  `formatversion_hinweis`, `scope_hinweis`), normalisiertes `header`, sowie
  `buchungen` (je Buchung Konto/Gegenkonto, TTMM-Belegdatum,
  `quelle: "executor"`). Beispiel: [`schema/beispiel-report.json`](schema/beispiel-report.json).

## Grenzen (bewusst)

- **Nur Buchungsstapel** — kein Rechnungsparser als eigener Executor (Claude
  erstellt bei Bedarf einen JSON-Entwurf, siehe Ablauf), keine Stammdaten
  (Kategorie 16), kein Import.
- **Nur die ersten 20 Buchungssatz-Spalten** implementiert (Umsatz bis
  Beleglink) — Kostenstellen (KOST1/KOST2), Beleginfo-Paare, EU-USt-Felder
  und weitere Erweiterungen der realen (weit über 100 Spalten
  umfassenden) DATEV-Schnittstelle sind nicht unterstützt.
- **Kein Kontenrahmen-Raten** — Konto/Gegenkonto nur formatgeprüft, nie
  SKR03/SKR04 zugeordnet.
- **⚠️ Formatversion 700 nicht primärquellen-verifiziert** — vor jedem
  echten Import gegen aktuelle DATEV-Dokumentation prüfen (siehe oben).
- **`status: getestet` erst nach echtem DATEV-Import** durch eine
  Steuerberatung — nie durch automatisierte Tests allein.

## Beispiele

### Beispiel — Grundfall: eine Honorarrechnung

Eingabe ([`schema/beispiel-eingabe.json`](schema/beispiel-eingabe.json)):
Buchungszeitraum 2026 (voll), eine Buchung — Umsatz 952,50 €, Soll, Konto
1200 (Bank) an Gegenkonto 8400 (Erlöse), Belegdatum 15.03.2026, Belegfeld 1
„RE-2026-042", Buchungstext „Honorar Müller ./. Schmidt".

Von Claude präsentiertes Ergebnis (aus dem Report übernommen): 1 Buchung
erzeugt, Buchungszeitraum 01.01.2026–31.12.2026, Belegdatum im Export als
`1503` (TTMM). Claude weist darauf hin: „⚠️ Formatversion 700 ist nicht
primärquellen-verifiziert — vor dem Import bitte gegen die aktuelle
DATEV-Dokumentation prüfen. Bitte das EXTF vor dem Import zusätzlich durch
die Buchhaltung/den Steuerberater gegenprüfen (Konto/Gegenkonto,
BU-Schlüssel, Buchungstext)."

### Beispiel — Reject: unbestätigte Modell-Extraktion

Claude liest aus einer eingescannten Rechnung einen Betrag aus und trägt
`"quelle": "modell-extraktion"` ein, ohne den Nutzer vorher zu fragen. Der
Executor lehnt ab: „Buchung 1: als 'quelle': 'modell-extraktion' markiert,
aber nicht 'bestaetigt': true — modellgenerierte Zahlenfelder dürfen erst
nach Nutzer-Bestätigung exportiert werden (P3)." Claude holt die Bestätigung
nach, statt den Betrag stillschweigend zu exportieren.
