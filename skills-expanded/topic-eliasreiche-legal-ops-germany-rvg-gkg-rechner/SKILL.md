---
name: rvg-gkg-rechner
description: "Berechnet RVG-Anwaltsvergütung und GKG-Gerichtskosten (Wertgebühren, Zivilsachen) deterministisch mit nachvollziehbarer Rechenkette — Tabellenstand nach Stichtag (KostRÄG 2021 / KostBRÄG 2025), Gebührensätze, Anrechnung, Auslagen, USt. Triggert bei RVG berechnen, Gerichtskosten/GKG, Anwaltsvergütung, Streitwert zu Gebühren, Kostennote, Vergütungsberechnung."
status: getestet
haendisch_getestet: 2026-09-22
welle: 1
bereich: zeit-abrechnung
rdg_einordnung: "Rechnerische Gebührenermittlung nach den gesetzlichen Wertgebührentabellen (§ 13 RVG / Anlage 2 RVG, § 34 GKG / Anlage 2 GKG) und einem festen Katalog von VV-RVG-/KV-GKG-Positionen — keine Beratung zur Gebührenstrategie, keine Billigkeitsentscheidung nach § 14 RVG (z. B. Satz der Geschäftsgebühr) und keine Kostenverteilungsentscheidung (§ 91 ff. ZPO)."
daten_hinweis: "Benötigt nur Streitwert, Stichtag und Gebührentatbestände — keine Mandantendaten erforderlich. Der Executor arbeitet rein lokal, ohne Netzwerkzugriff."
haftung: "Zweitkontrolle, zwingend: Der Rechner ersetzt keine anwaltliche Prüfung der Kostenrechnung. Es geht um Geld (Anwalts- und Gerichtskosten) — jeder Betrag ist vor Versand/Festsetzung von der Kanzlei gegenzuprüfen, insbesondere Satzwahl bei Rahmengebühren, Anrechnung und Tabellenstand."
---

# rvg-gkg-rechner

> **Status: `beta`** — automatisierte Tests laufen grün in CI (`tests/`,
> inkl. Orakel-Fälle gegen borghei `legal_calc`). Noch **nicht** händisch
> abgenommen — `status: getestet` vergibt erst der Maintainer nach eigener
> Prüfung (siehe [CONVENTIONS.md](https://github.com/eliasreiche/legal-ops-germany/blob/main/CONVENTIONS.md), Reifegrad-Leiter).

## Zweck

Berechnet RVG-Anwaltsvergütung und GKG-Gerichtskosten (jeweils nur
**Wertgebühren, Zivilsachen**) deterministisch über die Executoren
[`core/calc/rvg/`](../../core/calc/rvg/) und
[`core/calc/gkg/`](../../core/calc/gkg/) — mit vollständiger,
nachvollziehbarer **Rechenkette**: Tabellenstand-Wahl nach Stichtag,
1,0-Gebühr nach der gesetzlichen Stufenformel (§ 13 Abs. 1 RVG / § 34 Abs. 1
GKG), je Gebührenposition Satz × 1,0-Gebühr (mit Mindestbetrags-Floor),
optionale Anrechnung der Geschäftsgebühr auf die Verfahrensgebühr (Vorbem. 3
Abs. 4 VV RVG), optionale Anrechnung der Mahnverfahrensgebühr auf die
Gerichtsgebühr des Streitverfahrens (Anmerkung Abs. 1 zu KV 1210 GKG),
Auslagenpauschale und Umsatzsteuer.

Die Gebührentabellen liegen als **Formel + versionierte Parameterdaten** vor
(`core/calc/rvg/gebuehrentabelle.json`, `core/calc/gkg/gebuehrentabelle.json`)
— zwei Stände: **KostRÄG 2021** (01.01.2021–31.05.2025) und **KostBRÄG 2025**
(ab 01.06.2025), beide gegen gesetze-im-internet.de bzw.
Wayback-Machine-Schnappschüsse web-verifiziert. Der Stichtag entscheidet, nie
eine Annahme: § 60 Abs. 1 RVG (Auftragserteilung) für den RVG-Block,
§ 71 Abs. 1 GKG (Anhängigkeit der Rechtsstreitigkeit) für den GKG-Block —
zwei unterschiedliche Regeln, deshalb zwei getrennte Datumsfelder.

**Positionierung: strikt Zweitkontrolle.** Das Modell rechnet nie selbst —
kein Kopfrechnen, kein Schätzen von Gebührensätzen, auch nicht bei
„einfachen" Fällen. Jeder Geldbetrag in der Antwort stammt unverändert aus
dem Executor-Report. Der Rechner trifft keine Billigkeitsentscheidung (§ 14
RVG) — bei der Geschäftsgebühr (Nr. 2300, Satzrahmen 0,5–2,5) ist der Satz
Pflichteingabe, nie eine automatische Annahme des Regelsatzes 1,3.

**Angelegenheiten (§§ 16 ff. RVG):** Außergerichtliche Vertretung (Teil 2 VV
RVG) und gerichtliches Verfahren (Teil 3 VV RVG) sind verschiedene
Angelegenheiten — mit je **eigener** Auslagenpauschale Nr. 7002 (je 20 %,
max. je 20 €) und je **eigener** USt-Basis. Die Anfrage gruppiert deshalb in
`angelegenheiten`; Teil-2- und Teil-3-Tatbestände in derselben Angelegenheit
sind ein Eingabefehler, nie ein stilles Zusammenrechnen. Der Report weist je
Angelegenheit einen Block aus plus eine Gesamtvergütung (Summe über die
Angelegenheiten, gleicher Gläubiger — als solche beschriftet).

**Instanzenzug (§ 17 Nr. 1 RVG):** Der Katalog deckt erste Instanz
(Nr. 3100/3104), Berufung (Nr. 3200/3201/3202) und Revision (Nr. 3206–3210,
mit erhöhtem Satz Nr. 3208/3209 bei BGH-Vertretungszwang in der Zivilrevision)
ab. **Jeder Rechtszug ist eine eigene Angelegenheit** — Teil-3-Tatbestände
verschiedener Instanzen in derselben Angelegenheit sind ein Eingabefehler (je
Instanz eigene Auslagenpauschale Nr. 7002 und eigene USt-Basis); mehrere
Instanzen gehören in getrennte `angelegenheiten`. Die Einigungsgebühr
Nr. 1004 (erhöhter Satz) ist nur in einer Angelegenheit mit einem
Berufungs-/Revisions-Tatbestand zulässig (sonst Nr. 1000/1003). Die Anrechnung
(Vorbem. 3 Abs. 4 VV RVG) erfolgt ausschließlich auf die Verfahrensgebühr des
**ersten** Rechtszugs (Nr. 3100), nie auf Nr. 3200/3206/3208 — eine
Anrechnungs-Anforderung ohne Nr. 3100, aber mit höherinstanzlicher
Verfahrensgebühr, wird als Eingabefehler abgelehnt.

**Mahnverfahren → streitiges Verfahren (GKG):** Geht der Sache ein
Mahnbescheid voraus und wird nach Widerspruch/Einspruch streitig verhandelt,
wird die Gerichtsgebühr KV 1100 (0,5) auf die Gebühr KV 1210 (3,0)
**angerechnet** — Anmerkung Abs. 1 zu KV 1210 GKG: „… in diesem Fall wird
eine Gebühr 1100 nach dem Wert des Streitgegenstands angerechnet, der in das
Prozessverfahren übergegangen ist." Die Norm ordnet eine Anrechnung an, keine
Ermäßigung: der Satz 3,0 bleibt unverändert, abgezogen wird der Betrag der
Gebühr KV 1100 (inklusive deren Mindestbetrag). Angefordert wird das über
`gkg.anrechnung_1100_auf_1210: true` — nie automatisch, weil die Frage, ob
derselbe Streitgegenstand vorausgegangen und welcher Wert übergegangen ist,
keine Rechenfrage ist. Fehlt eine der beiden Positionen, ist das ein
Eingabefehler (Exit 2). **Bewusste Grenze — kein Teilübergang:** Die
Anrechnung setzt den vollständigen Übergang voraus. Ist nur ein Teil des
Mahnverfahrens-Streitgegenstands übergegangen, wäre die Anrechnungsbasis der
kleinere übergegangene Wert; verschiedene Werte an KV 1100 und KV 1210 bei
angeforderter Anrechnung sind ein Eingabefehler. Diesen Fall rechnet der
Executor nicht; er bleibt händisch/anwaltlich zu ermitteln.

**Teilwerte je Position:** `streitwert` ist der Default. Hat ein Tatbestand
bzw. eine GKG-Position einen **anderen** Wert (Mehrwert eines Vergleichs,
Terminsgebühr aus anhängigem Wert + Mehrwert, vorgerichtliche Tätigkeit über
eine Restforderung), bekommt er ein eigenes `gegenstandswert` — nie einen
Mischwert bilden, nie Werte in zwei Aufrufe aufteilen, die in eine
Angelegenheit gehören. Die Rechenkette nennt je Zeile den verwendeten Wert.
Anrechnung (2300 → 3100, KV 1100 → 1210) bei verschiedenen Werten ist ein
Eingabefehler (keine Teilanrechnung); mit Teilwerten wird jeder Wert über
30 Mio. € abgelehnt statt gekappt.

**Vergleich mit Mehrwert** (Vergleich im Prozess erledigt auch nicht
rechtshängige Ansprüche): **eine** Angelegenheit, kein Nr. 2300, keine
Aufteilung. Verfahrensgebühr Nr. 3100 aus dem anhängigen Wert **plus**
Nr. 3101 (0,8) aus dem Mehrwert; Terminsgebühr Nr. 3104 aus anhängigem Wert
+ Mehrwert; Einigungsgebühr Nr. 1003 aus dem anhängigen, Nr. 1000 aus dem
nicht anhängigen Teil — jede Position mit `gegenstandswert`. Der Executor
kappt Verfahrens- und Einigungsgebühren nach **§ 15 Abs. 3 RVG** und zeigt
die Kappung als eigene Zeile, auch wenn sie nicht greift. GKG: zusätzlich
KV 1900 (0,25) mit dem Mehrwert als `gegenstandswert`; die Grenze nach § 36
Abs. 3 GKG (Anm. zu KV 1900) rechnet der Executor mit.

**Wert-Obergrenzen (Kappung, sichtbar):** Gegenstandswerte über 30 Mio. €
werden nach § 22 Abs. 2 Satz 1 RVG bzw. § 39 Abs. 2 GKG auf 30 Mio. €
**gekappt** — als eigene Rechenketten-Zeile mit Warnung und
`wertkappung`-Block im Report, nie still. Ausnahme: Erhöhungsgebühr Nr. 1008
in Kombination mit einem Wert über 30 Mio. € wird abgelehnt, weil § 22
Abs. 2 Satz 2 RVG (je Auftraggeber 30 Mio. €, insgesamt höchstens
100 Mio. €) nicht modelliert ist — anwaltlich prüfen.

**Scope-Grenze (bewusst und geprüft):** Nur Wertgebühren in Zivilsachen.
Betragsrahmengebühren (Straf-/Sozialrecht), PKH-Vergütung (§ 49 RVG) und
Beratungshilfe sind **nicht unterstützt** — eine entsprechende Anfrage
liefert einen sauberen Eingabefehler mit Begründung, nie einen geratenen
Betrag.

## Eingaben (Datei-Kontrakt, P2)

| Eingabe | Pflicht | Format | Beschreibung |
|---|---|---|---|
| RVG-/GKG-Anfrage | ja (mind. ein Block) | `.json` | Blöcke `rvg` und/oder `gkg`. Vollständiges Schema: [`schema/README.md`](schema/README.md), Beispiele: [`schema/beispiel-eingabe.json`](schema/beispiel-eingabe.json) (Grundfall, eine Angelegenheit), [`schema/beispiel-eingabe-anrechnung.json`](schema/beispiel-eingabe-anrechnung.json) (zwei Angelegenheiten, Anrechnung + Erhöhungsgebühr), [`schema/beispiel-eingabe-berufung.json`](schema/beispiel-eingabe-berufung.json) (Instanzenzug: erste Instanz + Berufung, GKG-Berufung). |

Kurzfassung der Pflichtfelder:

- **`rvg`**: `auftragsdatum` (ISO-Datum), `streitwert` (Dezimalstring),
  dazu **entweder** `angelegenheiten` (Liste, je Angelegenheit eigene
  `tatbestaende`) **oder** `tatbestaende` flach (Kurzform für genau eine
  Angelegenheit). VV-RVG-Positionen aus dem
  [Katalog](../../core/calc/rvg/vv-katalog.json): `2300` (Teil 2),
  Teil 3 nach Instanz — erste Instanz `3100`/`3101`/`3104`, Berufung
  `3200`/`3201`/`3202`, Revision `3206`–`3210` (`3208`/`3209` bei
  BGH-Vertretungszwang), `1000`, `1003`, `1004`, `1008` (Teil 1, in jeder
  Angelegenheit zulässig; `1004` nur mit Berufungs-/Revisions-Tatbestand).
- **`gkg`**: `verfahrenseinleitungsdatum` (ISO-Datum, **nicht** dasselbe wie
  `auftragsdatum`), `streitwert`, `positionen` (Liste von KV-GKG-Positionen
  aus dem [Katalog](../../core/calc/gkg/kv-katalog.json): `1100`,
  `1210`, `1211`, `1220`, `1222`, `1230`, `1232`, `1900`); optional
  `anrechnung_1100_auf_1210` (Anrechnung der Mahnverfahrensgebühr, verlangt
  `1100` und `1210`).
- **Teilwerte** (beide Blöcke, optional): `gegenstandswert` je Tatbestand
  bzw. Position; Pflicht bei `3100`/`3101` bzw. `1000`/`1003`/`1004`, wenn
  sie zusammen in einer Angelegenheit stehen, und bei KV `1900`.

Beide Blöcke werden **strikt** validiert: ein nicht vorgesehener Key (z. B.
ein Tippfehler `anrechnung_1100_1210`) führt zu Exit 2 mit Nennung des Keys —
er wird nie stillschweigend ignoriert, sonst rechnete der Report im Geldpfad
ohne die gewollte Anrechnung weiter.

Geldbeträge und Sätze **immer als JSON-String** (z. B. `"5000.00"`), nie als
`float` — der Executor lehnt `float`-Eingaben strikt ab (Rundungsfehler wie
0,1+0,2 sind bei Geldbeträgen ein Haftungsrisiko, keine stille Ungenauigkeit).

## Ablauf

1. **Claude schreibt die Anfrage als JSON-Datei** (nach
   [`schema/README.md`](schema/README.md)). Fehlende Pflichtangaben
   (Streitwert, Stichtag, Gebührentatbestände, bei `2300` der Satz) werden
   beim Nutzer erfragt, nie ergänzt oder geschätzt (Anti-Halluzination).
2. **Claude ruft den Executor auf** (kein eigenes Rechnen durch das Modell):

   ```bash
   python3 ${CLAUDE_PLUGIN_ROOT}/core/calc/rvg/executor.py \
     --input <anfrage.json> \
     --output <report.json>
   ```

3. **Der Executor entscheidet jeden Betrag deterministisch** (P3). Claude
   liest ausschließlich den JSON-Report und übernimmt Tabellenstand,
   1,0-Gebühr, Positionsbeträge, Anrechnung, Zwischensummen und Gesamtbetrag
   unverändert.
4. **Claude stellt den Report als Rechenkette dar**: jeder Schritt mit Norm
   und Zwischenergebnis, alle `warnungen` und `hinweise` sichtbar. Dabei
   immer ausweisen:
   - **welcher Tabellenstand** angewendet wurde und weshalb (Stichtag),
   - **Wert-Kappung** (§ 22 Abs. 2 S. 1 RVG / § 39 Abs. 2 GKG), wenn der
     `wertkappung`-Block gefüllt ist — eingegebenen und angewendeten Wert
     nennen,
   - **je Angelegenheit** die eigene Zwischensumme, Auslagenpauschale und
     USt — und die Gesamtvergütung ausdrücklich als Summe über getrennte
     Angelegenheiten beschriften,
   - **Mindestbetrag-Floor**, wenn eine Position darunter lag
     (`mindestbetrag_gegriffen`),
   - **Kappung der Erhöhungsgebühr** (Nr. 1008) auf Gebührensatz 2,0, wenn
     eingetreten,
   - **§ 15 Abs. 3 RVG / § 36 Abs. 3 GKG** (`kappungen_15_abs_3`,
     `kappung_36_abs_3`): Summe der Einzelgebühren, Höchstbetrag, ob die
     Kappung greift — und bei Teilwerten den Wert jeder Position,
   - **Anrechnung**, wenn angefordert: beim RVG beteiligte Angelegenheiten,
     Satz, Betrag, Verfahrensgebühr vor/nach Anrechnung; beim GKG
     (`gkg.anrechnung`) Anrechnungsbetrag und Gebühr KV 1210 vor/nach
     Anrechnung mit der Norm (Anmerkung Abs. 1 zu KV 1210 GKG),
   - **RVG und GKG werden nie automatisch addiert** —
     `meta.hinweis_getrennte_kostenarten` immer erwähnen,
   - den Zweitkontroll-Hinweis aus `haftung` (immer, bei jeder Antwort).
5. Bei Exit-Code 2 (Eingabefehler, u. a. Scope-Ablehnung bei
   Betragsrahmengebühren/PKH/Beratungshilfe, Teil-2-/Teil-3-Tatbestände in
   derselben Angelegenheit, Nr. 1008 kombiniert mit Wert über 30 Mio. €,
   Stichtag außerhalb der unterstützten Tabellenstände, unbekannter Key in
   `rvg`/`gkg` oder in einem Tatbestand/einer Position, angeforderte
   GKG-Anrechnung ohne KV 1100 bzw. KV 1210, Anrechnung bei verschiedenen
   Teilwerten, § 15 Abs. 3-Gruppe ohne Teilwerte, KV 1900 ohne
   `gegenstandswert`, Teilwert über 30 Mio. €) gibt Claude die
   Fehlermeldung wieder und korrigiert die Eingabe bzw. fragt nach — er rät
   kein Ergebnis.

## Output-Format

JSON-Report nach [`schema/README.md`](schema/README.md), Beispiel:
[`schema/beispiel-report.json`](schema/beispiel-report.json). Kernfelder im
`rvg`-Block: `tabellenstand`, `wertkappung`, `einfachgebuehr`,
`angelegenheiten` (je Angelegenheit `positionen` mit `satz`, `betrag`,
`mindestbetrag_gegriffen`, `quelle: "executor"` sowie eigenes `ergebnis` mit
Zwischensumme/7002/Netto/USt/Gesamt), `anrechnung`, `rechenkette`,
`ergebnis.gesamt_verguetung`. Im `gkg`-Block: `tabellenstand`,
`wertkappung`, `einfachgebuehr`, `positionen`, `anrechnung` (KV 1100 auf
KV 1210, sonst `null`), `rechenkette`, `ergebnis.gesamt`.

Jeder Geldbetrag im Report stammt aus dem jeweiligen `rechner.py`, nie vom
Modell (P3). Alle Beträge sind Dezimalstrings (z. B. `"847.60"`).

## Beispiele

### Beispiel 1 — Grundfall: Verfahren erster Instanz, RVG + GKG

Eingabe ([`schema/beispiel-eingabe.json`](schema/beispiel-eingabe.json)):
Streitwert 5.000 €, Stichtag 01.03.2026 (Tabellenstand KostBRÄG 2025),
Verfahrensgebühr (Nr. 3100), Terminsgebühr (Nr. 3104), Einigungsgebühr
(Nr. 1000) sowie GKG-Verfahrensgebühr 1. Instanz (KV 1210).

Von Claude präsentiertes Ergebnis (aus dem Report übernommen):

| Position | Satz | Betrag |
|---|---|---|
| 1,0-Gebühr (Streitwert 5.000 €, KostBRÄG 2025) | — | 354,50 € |
| Verfahrensgebühr (Nr. 3100 VV RVG) | 1,3 | 460,85 € |
| Terminsgebühr (Nr. 3104 VV RVG) | 1,2 | 425,40 € |
| Einigungsgebühr (Nr. 1000 VV RVG) | 1,5 | 531,75 € |
| Auslagenpauschale (Nr. 7002 VV RVG) | 20 %, gedeckelt | 20,00 € |
| **RVG gesamt (brutto, 19 % USt)** | | **1.711,22 €** |
| GKG Verfahrensgebühr 1. Instanz (KV 1210) | 3,0 | **511,50 €** |

**Zweitkontrolle durch die Kanzlei bleibt zwingend** — insbesondere Prüfung,
ob alle Voraussetzungen der einzelnen Gebührentatbestände (z. B. tatsächlich
stattgefundener Termin für Nr. 3104) im konkreten Fall vorliegen; das prüft
der Rechner nicht.

### Beispiel 2 — Zwei Angelegenheiten, Anrechnung, Erhöhung

Eingabe ([`schema/beispiel-eingabe-anrechnung.json`](schema/beispiel-eingabe-anrechnung.json)):
Streitwert 10.000 €, **zwei Angelegenheiten** — „Außergerichtliche
Vertretung" (Geschäftsgebühr Nr. 2300, Satz 1,3) und „Rechtsstreit erster
Instanz" (Verfahrensgebühr Nr. 3100 plus Erhöhungsgebühr Nr. 1008 für einen
weiteren Auftraggeber) — mit angeforderter Anrechnung.

Von Claude präsentiertes Ergebnis (aus dem Report übernommen; 1,0-Gebühr
652,00 €):

| Angelegenheit „Außergerichtliche Vertretung" | Satz | Betrag |
|---|---|---|
| Geschäftsgebühr (Nr. 2300 VV RVG) | 1,3 | 847,60 € |
| Auslagenpauschale (Nr. 7002 VV RVG, **je Angelegenheit**) | 20 %, gedeckelt | 20,00 € |
| USt (Nr. 7008 VV RVG) | 19 % | 164,84 € |
| **Gesamt Angelegenheit 1** | | **1.032,44 €** |

| Angelegenheit „Rechtsstreit erster Instanz" | Satz | Betrag |
|---|---|---|
| Verfahrensgebühr (Nr. 3100 VV RVG), nach Anrechnung | 1,3 | 423,80 € |
| Erhöhung (Nr. 1008 VV RVG, 1 weiterer Auftraggeber) | 0,3 | 195,60 € |
| Auslagenpauschale (Nr. 7002 VV RVG, **je Angelegenheit**) | 20 %, gedeckelt | 20,00 € |
| USt (Nr. 7008 VV RVG) | 19 % | 121,49 € |
| **Gesamt Angelegenheit 2** | | **760,89 €** |

**Gesamtvergütung (Summe über die Angelegenheiten, gleicher Gläubiger):
1.793,33 €.** Die Anrechnung steht als eigener Rechenschritt im Report:
Anrechnungssatz `min(1,3 × 0,5; 0,75) = 0,65`, Anrechnungsbetrag 423,80 €,
Verfahrensgebühr vor Anrechnung 847,60 € → nach Anrechnung 423,80 €. Claude
zeigt jede Angelegenheit getrennt (je eigene 7002-Pauschale und USt-Basis)
und benennt die Gesamtvergütung ausdrücklich als Summe über getrennte
Angelegenheiten.

### Beispiel 3 — Instanzenzug: erste Instanz + Berufung (RVG + GKG)

Eingabe ([`schema/beispiel-eingabe-berufung.json`](schema/beispiel-eingabe-berufung.json)):
Streitwert 10.000 €, Stichtag 01.03.2026 (KostBRÄG 2025), **zwei
Angelegenheiten** — „Rechtsstreit erster Instanz" (Verfahrensgebühr Nr. 3100,
Terminsgebühr Nr. 3104) und „Berufungsverfahren" (Verfahrensgebühr Nr. 3200,
Terminsgebühr Nr. 3202); dazu GKG-Berufung KV 1220. Report:
[`schema/beispiel-report-berufung.json`](schema/beispiel-report-berufung.json).

Von Claude präsentiertes Ergebnis (aus dem Report übernommen; 1,0-Gebühr RVG
652,00 €):

| Angelegenheit „Rechtsstreit erster Instanz" | Satz | Betrag |
|---|---|---|
| Verfahrensgebühr (Nr. 3100 VV RVG) | 1,3 | 847,60 € |
| Terminsgebühr (Nr. 3104 VV RVG) | 1,2 | 782,40 € |
| Auslagenpauschale (Nr. 7002 VV RVG) | 20 %, gedeckelt | 20,00 € |
| **Gesamt erste Instanz (brutto, 19 % USt)** | | **1.963,50 €** |

| Angelegenheit „Berufungsverfahren" | Satz | Betrag |
|---|---|---|
| Verfahrensgebühr (Nr. 3200 VV RVG) | 1,6 | 1.043,20 € |
| Terminsgebühr (Nr. 3202 VV RVG) | 1,2 | 782,40 € |
| Auslagenpauschale (Nr. 7002 VV RVG, **je Angelegenheit**) | 20 %, gedeckelt | 20,00 € |
| **Gesamt Berufung (brutto, 19 % USt)** | | **2.196,26 €** |

**Gesamtvergütung (Summe über beide Instanzen, gleicher Gläubiger):
4.159,76 €.** Getrennt davon GKG-Berufung KV 1220 (4,0): **1.132,00 €**
(1,0-Gebühr GKG 283,00 €). Jeder Rechtszug ist eine eigene Angelegenheit
(§ 17 Nr. 1 RVG) mit eigener Auslagenpauschale und eigener USt-Basis; erste
und zweite Instanz dürfen deshalb **nicht** in dieselbe Angelegenheit gelegt
werden — der Executor lehnt das ab (Instanz-Kollisionsregel). RVG-Vergütung
und GKG-Gerichtskosten bleiben getrennt.

### Beispiel 4 — Inkasso: Mahnbescheid → Widerspruch → streitiges Verfahren (GKG)

Anfrage im `gkg`-Block: Streitwert 10.000 €, Verfahrenseinleitung 01.03.2026
(KostBRÄG 2025), Positionen KV 1100 und KV 1210, `anrechnung_1100_auf_1210:
true`.

| Position | Satz | Betrag |
|---|---|---|
| 1,0-Gebühr GKG (Streitwert 10.000 €, KostBRÄG 2025) | — | 283,00 € |
| Mahnverfahren (KV 1100 GKG) | 0,5 | 141,50 € |
| Verfahren im Allgemeinen, 1. Rechtszug (KV 1210 GKG), vor Anrechnung | 3,0 | 849,00 € |
| ./. Anrechnung KV 1100 (Anmerkung Abs. 1 zu KV 1210 GKG) | — | − 141,50 € |
| **Gerichtskosten gesamt** | | **849,00 €** |

Der Gebührensatz von KV 1210 bleibt 3,0 — angerechnet wird der **Betrag** der
Gebühr KV 1100 (bei kleinen Werten inklusive deren Mindestbetrag, z. B.
38,00 € statt rechnerischer 30,50 €). Claude weist den `anrechnung`-Block des
Reports mit aus (Anrechnungsbetrag, KV 1210 vor/nach Anrechnung) und nennt die
Norm. Ist nur ein Teil des Streitgegenstands übergegangen, rechnet der
Executor die Anrechnung nicht (bewusste Grenze, siehe oben) — Claude weist
das als Lücke aus und schätzt keinen Anrechnungsbetrag.

### Beispiel 5 — Scope-Ablehnung: Betragsrahmengebühr

Anfrage mit `{"nr": "3102"}` (Verfahrensgebühr Sozialgericht,
Betragsrahmengebühr) liefert Exit 2: „Nr. 3102 VV RVG ist nicht unterstützt
— dieser Rechner deckt nur Wertgebühren in Zivilsachen ab … Betragsrahmen-
gebühren (Straf-/Sozialrecht), PKH-Vergütung (§ 49 RVG) und Beratungshilfe
sind außerhalb des Scopes — keine automatische Berechnung möglich." Claude
gibt diese Meldung wieder und schätzt keinen Ersatzbetrag.
