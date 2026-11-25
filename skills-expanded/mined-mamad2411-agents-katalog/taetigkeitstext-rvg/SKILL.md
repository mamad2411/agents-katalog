---
name: taetigkeitstext-rvg
description: "Formuliert aus Stichworten/Kalendereinträgen abrechnungsfähige Tätigkeitsbeschreibungen; Zeitwerte stammen ausschließlich aus dem Input, nie vom Modell — ein Provenienz-Gate erzwingt das maschinell gegen jede Zahl/jedes Datum im Text. Triggert bei Leistungsbeschreibung, Tätigkeitstext für Abrechnung, Zeitnarrativ, Leistungsnachweis formulieren."
status: beta
welle: 3
bereich: zeit-abrechnung
rdg_einordnung: "Sprachliche Aufbereitung interner Abrechnungstexte aus vorgegebenen Stichworten und Zeitwerten; keine rechtliche Bewertung der Tätigkeit, keine Gebührenberechnung (dafür rvg-gkg-rechner) und keine Empfehlung, was abgerechnet werden darf."
daten_hinweis: "Tätigkeitsbeschreibungen tragen Mandatsbezug (Aktenzeichen, Sachverhalts-Stichworte) — nur über DSGVO-/BRAO-konformen Modellzugang (AWS-Bedrock-Pfad) verarbeiten, § 203 StGB beachten. Der Executor arbeitet rein lokal, ohne Netzwerkzugriff, und liest nur die übergebenen Dateien."
haftung: "Der formulierte Text ist ein Entwurf — die Freigabe zur Rechnungsstellung (inhaltlich wie zeitlich) bleibt Kanzleisache. Zeitansätze stammen ausnahmslos aus dem Input (Kalender/Mail/manuelle Erfassung); der Executor erfindet nichts, das Provenienz-Gate ist Pflichtschritt vor jeder Ausgabe, ersetzt aber keine inhaltliche Prüfung der Abrechenbarkeit (RVG-Konformität, Zeitplausibilität) durch die Kanzlei."
---

# taetigkeitstext-rvg

> **Status: `beta`** — automatisierte Tests laufen grün in CI
> (`tests/`, inkl. Unit-Tests für `core/calc/zeit/`). Noch **nicht** händisch
> abgenommen — `status: getestet` vergibt erst der Maintainer nach eigener
> Prüfung (siehe
> [CONVENTIONS.md](https://github.com/eliasreiche/legal-ops-germany/blob/main/CONVENTIONS.md), Reifegrad-Leiter).

## Zweck

Formuliert aus Stichworten und Kalender-/Mail-Einträgen abrechnungsfähige
Tätigkeitsbeschreibungen je Aktenzeichen. **Zeitwerte kommen ausschließlich
aus dem Input, nie vom Modell** (Deterministik-Grenze, P3): ein Executor
berechnet Minuten (aus direkter Angabe oder aus `start`/`ende`), rundet
optional auf einen Abrechnungstakt und aggregiert Summen je Aktenzeichen und
je (Aktenzeichen, Datum). Claude liest ausschließlich diesen Report und
formuliert daraus **sachliche** Tätigkeitsbeschreibungen — ohne rechtliche
Bewertung und ohne erfundene Tätigkeiten. Ein zweiter Executor-Lauf (das
**Provenienz-Gate**) prüft den fertigen Text maschinell gegen den Report,
bevor er ausgegeben wird.

**Keine Gebührenberechnung.** Ob und wie eine Tätigkeit nach RVG abrechenbar
ist, entscheidet der Skill [`rvg-gkg-rechner`](../rvg-gkg-rechner/SKILL.md)
bzw. die Kanzlei — dieser Skill liefert nur den Beschreibungstext und die
belegten Zeitwerte.

## Eingaben (Datei-Kontrakt, P2)

| Eingabe | Pflicht | Format | Beschreibung |
|---|---|---|---|
| Leistungen | ja (Modus 1) | `.json` | Liste von Zeit-Einträgen mit Stichworten. **Das ist die Schnittstelle zu `passive-zeiterfassung`** — Struktur: [`schema/README.md`](schema/README.md), Beispiel: [`schema/beispiel-leistungen.json`](schema/beispiel-leistungen.json). |
| Entwurfs-Text | ja (Modus 2) | `.md` / `.txt` | Der von Claude formulierte Leistungsnachweis, der gegen den Report aus Modus 1 geprüft wird. Beispiel: [`schema/beispiel-entwurf.md`](schema/beispiel-entwurf.md). |

Die Dauer-Berechnung und Taktung übernimmt die wiederverwendbare Bibliothek
[`core/calc/zeit/`](../../core/calc/zeit/) — reine Funktionen, keine
Datei-E/A, damit sie auch der Skill `passive-zeiterfassung` (dieselbe Welle)
nutzen kann.

## Ablauf

1. **Claude schreibt die Leistungen-JSON** aus dem, was Nutzer, Kalender
   oder Mail hergeben (nach [`schema/README.md`](schema/README.md)). Für
   jeden Eintrag entweder `minuten` **oder** `start`+`ende` — nie beides,
   nie geraten. Fehlt ein Aktenzeichen, bleibt `az: null` (Lücke, nie
   raten). `stichworte` sind wörtliches Rohmaterial, keine Interpretation.

2. **Claude ruft den Executor im Rechen-Modus auf** (kein eigenes Rechnen
   durch das Modell, P3):

   ```bash
   python3 ${CLAUDE_PLUGIN_ROOT}/skills/taetigkeitstext-rvg/executor.py \
     --input <leistungen.json> --output <report.json>
   ```

   Der Executor validiert streng (unbekannte/fehlende Felder → Exit 2),
   berechnet die Minuten je Eintrag (`core/calc/zeit`), wendet die Taktung
   an (`config.takt_minuten`, **immer aufgerundet** — Kanzlei-Konvention,
   keine RVG-Vorgabe), aggregiert die Summen je Aktenzeichen und je
   (Aktenzeichen, Datum) und echot `stichworte` unverändert. Einträge ohne
   Aktenzeichen landen in `ohne_az[]`.

3. **Claude formuliert je Eintrag bzw. je Akte einen sachlichen
   Tätigkeitstext** — **ausschließlich** aus den `stichworte`n des jeweiligen
   Eintrags:
   - **Keine rechtliche Bewertung, keine erfundenen Tätigkeiten.** Was nicht
     in den Stichworten steht, wird nicht ergänzt.
   - **Dünne Stichworte → knapper Text.** Ein einzelnes, kurzes Stichwort
     ergibt einen entsprechend kurzen Satz — nie ausschmücken, um den Text
     „runder" wirken zu lassen.
   - **Zeitwerte wörtlich aus dem Report** — `minuten`/`minuten_getaktet`,
     `datum` und die Summen werden unverändert übernommen, nie neu berechnet
     oder gerundet.
   - Einträge in `ohne_az[]` werden im Text als Lücke ausgewiesen
     (Aktenzeichen fehlt), nie stillschweigend einer Akte zugeordnet.

4. **Pflichtschritt: Provenienz-Gate.** Claude ruft den Executor im
   Prüf-Modus mit dem gerade formulierten Text auf:

   ```bash
   python3 ${CLAUDE_PLUGIN_ROOT}/skills/taetigkeitstext-rvg/executor.py \
     --pruefe-text <entwurf.md> --report <report.json> --output <pruef-report.json>
   ```

   Der Executor prüft **jede** Zahl (Minuten/Stunden, inkl. der
   Äquivalenz „1,5 Stunden" ≡ „90 Minuten") und **jedes** Datum im Text
   gegen die Executor-Werte aus dem Report sowie jedes Aktenzeichen gegen
   die im Report vorkommenden. **Erst bei Exit 0 (`ergebnis: "sauber"`) gibt
   Claude den Text aus.** Meldet das Gate einen Befund (`ergebnis:
   "abweichend"`, Exit 1) — eine fremde Zahl, ein fremdes Datum oder ein
   fremdes Aktenzeichen —, korrigiert Claude den Text (den erfundenen Wert
   durch den tatsächlichen Report-Wert ersetzen oder streichen) und lässt
   das Gate erneut laufen, bis es sauber ist. Ein Report, der nicht von
   diesem Executor stammt, wird im Prüf-Modus abgelehnt (Exit 2).

## Output-Format

**Rechen-Report** (Modus 1): JSON nach [`schema/README.md`](schema/README.md),
Beispiel: [`schema/beispiel-report.json`](schema/beispiel-report.json)
(erzeugt aus [`schema/beispiel-leistungen.json`](schema/beispiel-leistungen.json)).
Kernfelder: `eintraege[]` (nur mit Aktenzeichen, je mit `minuten`,
`minuten_getaktet`, `stichworte`, `quelle_zeit`), `ohne_az[]`, `summen.je_az`,
`summen.je_az_und_datum`, `zusammenfassung`. Jeder Zahlen-/Datumswert trägt
implizit `quelle: executor` über `meta.erzeugt_von` (P3).

**Prüf-Report** (Modus 2): JSON, Beispiel:
[`schema/beispiel-pruef-report.json`](schema/beispiel-pruef-report.json)
(erzeugt aus [`schema/beispiel-entwurf.md`](schema/beispiel-entwurf.md) gegen
[`schema/beispiel-report.json`](schema/beispiel-report.json)). Kernfelder:
`gefundene_werte` (Minuten/Daten/Aktenzeichen je mit `status: belegt|fremd`),
`befunde[]`, `ergebnis: sauber|abweichend`.

## Beispiele

### Beispiel 1 — gemischte Zeitquellen, Taktung, Lücke ohne Aktenzeichen

Eingabe [`schema/beispiel-leistungen.json`](schema/beispiel-leistungen.json):
fünf Einträge — ein Kalendertermin mit `start`/`ende` (47 Minuten), ein
manueller Eintrag mit `minuten: 30`, ein Mail-Eintrag (15 Minuten), ein
Eintrag ohne Aktenzeichen (20 Minuten) sowie ein weiterer Kalendertermin
(22 Minuten), Taktung `takt_minuten: 6`.

Der Executor liefert (Auszug aus
[`schema/beispiel-report.json`](schema/beispiel-report.json)):

| az | Datum | Minuten (roh) | Minuten (getaktet) |
|---|---|---|---|
| `12/2026` | 2026-07-01 | 47 | 48 |
| `12/2026` | 2026-07-01 | 30 | 30 |
| `34/2026` | 2026-07-02 | 15 | 18 |
| `34/2026` | 2026-07-03 | 22 | 24 |
| *(ohne az)* | 2026-07-03 | 20 | 24 |

Summen: `12/2026` → 78 Minuten, `34/2026` → 42 Minuten. Der Eintrag ohne
Aktenzeichen fließt in keine Summe ein, sondern bleibt als Lücke in
`ohne_az[]` ausgewiesen.

Aus diesem Report formuliert Claude je Akte einen Text (Beispiel:
[`schema/beispiel-entwurf.md`](schema/beispiel-entwurf.md)), z. B. für
`12/2026`:

> Am 01.07.2026 wurde ein Telefonat mit dem Mandanten geführt und der
> Sachstand zur Kündigungsschutzklage besprochen (47 Minuten). Im Anschluss
> wurde die Fristenkontrolle zur Klageerwiderung geprüft (30 Minuten). Für
> den 01.07.2026 ergeben sich in Summe 78 Minuten (1,3 Stunden).

Das Provenienz-Gate ([`schema/beispiel-pruef-report.json`](schema/beispiel-pruef-report.json))
läuft sauber durch: alle Zahlen (inkl. der Stunden-Äquivalenz „1,3 Stunden"
= 78 Minuten), Daten und Aktenzeichen sind belegt, `ergebnis: "sauber"`,
Exit 0.

### Beispiel 2 — Provenienz-Gate fängt eine erfundene Zahl ab

Enthält der Entwurfstext statt „47 Minuten" versehentlich „50 Minuten" (ein
Wert, der in keinem Report-Feld vorkommt), meldet das Gate einen Befund
`{"typ": "fremde_zahl", "roh": "50 Minuten", ...}`, `ergebnis: "abweichend"`,
Exit 1. Claude übernimmt einen solchen Wert nie, sondern ersetzt ihn durch
den tatsächlichen Report-Wert und lässt das Gate erneut laufen.

## Grenzen (bewusst)

- **Keine Gebührenberechnung** — für die RVG-Vergütung ist ausschließlich
  [`rvg-gkg-rechner`](../rvg-gkg-rechner/SKILL.md) zuständig.
- **Keine Bewertung der Abrechenbarkeit** — ob eine Tätigkeit in dieser Form
  und Dauer abrechenbar ist, entscheidet die Kanzlei vor Rechnungsstellung.
- **Aktenzeichen-Erkennung im Provenienz-Gate ist eine Heuristik**
  (Ziffern/Jahr-Muster wie `12/2026`) — andere Kanzlei- oder Gerichts-
  Aktenzeichen-Formate erkennt sie nicht (Details:
  [`schema/README.md`](schema/README.md) „Bewusste Grenzen").
- **`belegt` ist ein Vorkommens-, kein Richtigkeitsnachweis** — das Gate
  prüft nur, ob ein Wert im Report existiert, nicht ob er zum richtigen
  Absatz oder zur richtigen Tätigkeit gehört.
- **Taktung ist Hauskonvention, keine Rechtsvorgabe** — das RVG kennt keinen
  Abrechnungstakt; `takt_minuten` bildet ausschließlich eine
  Kanzlei-Abrechnungspraxis ab und wird im Output nie als Norm dargestellt.
