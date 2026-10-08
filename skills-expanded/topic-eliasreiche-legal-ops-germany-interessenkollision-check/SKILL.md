---
name: interessenkollision-check
description: "Fuzzy-Matching neuer Mandats-Parteien gegen die Mandanten-/Gegnerliste der Kanzlei (Kölner Phonetik, Matching-Stufen S1–S4) — Datei rein, Treffer-Report raus, vollständig offline. Triggert bei Kollisionsprüfung, Interessenkonflikt, Konflikt-Check vor Mandatsannahme, § 43a BRAO / § 3 BORA, Parteien abgleichen. Die anwaltliche Kollisionsentscheidung bleibt Kanzleisache."
status: beta
welle: 2
bereich: compliance
rdg_einordnung: "Organisatorische Kollisionsprüfung als Rechercheunterstützung; die berufsrechtliche Bewertung (§ 43a BRAO, § 3 BORA) trifft der Anwalt."
daten_hinweis: "Mandanten-/Gegnerlisten sind hochsensibel — lokal verarbeiten, nicht persistieren; § 203 StGB beachten."
haftung: "Kein Treffer ist kein Freibrief: Schreibweisen-Lücken möglich, abschließende Kollisionsprüfung bleibt Kanzleipflicht."
---

# interessenkollision-check

> **Status: `beta`** — automatisierte Tests laufen grün in CI (`tests/`,
> 91 Fälle: Normalisierung, Kölner Phonetik, Fuzzy-Maße, Matching-Stufen
> S1–S4 inkl. False-Positive-Grenzfälle, CSV-/JSON-Parsing, CLI). Noch
> **nicht** händisch abgenommen — `status: getestet` vergibt erst der
> Maintainer nach eigener Prüfung (siehe
> [CONVENTIONS.md](https://github.com/eliasreiche/legal-ops-germany/blob/main/CONVENTIONS.md), Reifegrad-Leiter).

## Zweck

Fuzzy-Matching neuer Mandats-Parteien gegen die Mandanten-/Gegnerliste der
Kanzlei — Datei rein, Treffer-Report raus, vollständig offline, keine
Persistierung. Unterstützt die organisatorische Kollisionsprüfung vor
Mandatsannahme (§ 43a Abs. 4 BRAO, § 3 BORA), ersetzt sie aber nicht: der
Executor liefert Kandidaten, die **anwaltliche Kollisionsentscheidung**
bleibt immer Kanzleisache.

Die zugrundeliegende Matching-Bibliothek
[`core/calc/matching/`](../../core/calc/matching/) ist bewusst
wiederverwendbar angelegt — Skill #13 `gwg-live-screening` (Welle 3) nutzt
sie später für den Abgleich gegen Sanktionslisten.

## Eingaben (Datei-Kontrakt, P2)

| Eingabe | Pflicht | Format | Beschreibung |
|---|---|---|---|
| Mandanten-/Gegnerliste | ja (`--liste`) | `.csv`, `;`-getrennt, UTF-8 (BOM toleriert) | Pflichtspalten `name;rolle;typ`, optional `az;notiz`. Vollständiger Kontrakt: [`schema/README.md`](schema/README.md), Beispiel: [`schema/beispiel-mandantenliste.csv`](schema/beispiel-mandantenliste.csv). |
| Neue Parteien | ja (`--parteien`) | `.csv` (gleicher Kontrakt, nur `name` Pflicht) oder `.json` (Liste von Objekten mit mindestens `name`) | Beispiel: [`schema/beispiel-neue-parteien.json`](schema/beispiel-neue-parteien.json). |

Beide Dateien werden vom Executor nur **gelesen** — keine Kopie, keine
Persistierung, kein Netzwerkzugriff. Die Verarbeitung findet vollständig
lokal statt.

## Ablauf

1. **Claude beschafft/erstellt die beiden Eingabedateien** (Mandanten-/
   Gegnerliste und neue Parteien) nach dem Kontrakt in
   [`schema/README.md`](schema/README.md). Fehlt eine der Dateien oder eine
   Pflichtangabe, fragt Claude nach — es ergänzt nie Namen, Aktenzeichen
   oder Rollen selbst (Anti-Halluzination).
2. **Claude ruft den Executor auf** (kein eigenes Namensvergleichen durch
   das Modell):

   ```bash
   python3 ${CLAUDE_PLUGIN_ROOT}/skills/interessenkollision-check/executor.py \
     --liste <mandantenliste.csv> \
     --parteien <neue_parteien.csv|.json> \
     [--output <report.json>] \
     [--schwelle-moeglich <float, Default 0.85>]
   ```

3. **Der Executor entscheidet Stufe und Score jedes Kandidaten-Paars
   deterministisch** (P3, Deterministik-Grenze): S1 exakt nach
   Normalisierung, S2 Token-Mengen-Gleichheit/-Teilmenge, S3 Kölner
   Phonetik je Token, S4 Fuzzy-Ratio ≥ Schwelle — siehe
   [`schema/README.md`](schema/README.md#match-stufen) für die vollständige
   Definition. Claude liest ausschließlich den JSON-Report und übernimmt
   `stufe`, `score` und `begruendung` unverändert — es vergibt selbst nie
   eine Stufe oder einen Score.
4. **Claude stellt den Report als Markdown-Tabelle dar**: je Kandidaten-Paar
   neue Partei, Listeneintrag (mit Rolle und Aktenzeichen), Stufe/Regel,
   Score, Begründung. Dabei immer:
   - `treffer` und `moeglicher_treffer` optisch unterscheiden (z. B. ✅ /
     ⚠️), sortiert wie im Report (Treffer vor möglichen Treffern);
   - bei **jedem** `moeglicher_treffer` **und** bei **jedem Treffer mit
     Gegner-Rolle** (Listeneintrag oder neue Partei mit `rolle: gegner`)
     ausdrücklich darauf hinweisen, dass die Kollisionsentscheidung
     (§ 43a Abs. 4 BRAO, § 3 BORA) beim Anwalt liegt — der Report liefert
     Kandidaten, keine Entscheidung;
   - die Zusammenfassung nennen (Anzahl neuer Parteien, Listeneinträge,
     geprüfter Paare, Treffer, möglicher Treffer);
   - **immer** den Hinweis "kein Treffer ist kein Freibrief" anbringen,
     wenn eine oder mehrere neue Parteien in **keinem** Kandidaten-Paar
     auftauchen (siehe `haftung`-Feld oben und die bewussten Grenzen in
     [`schema/README.md`](schema/README.md#bewusste-grenzen));
   - erwähnen, dass die Verarbeitung vollständig lokal/offline erfolgte und
     keine der beiden Listen durch den Skill gespeichert wurde.
5. Bei Exit-Code 2 (Eingabefehler: Datei fehlt, Pflichtspalte fehlt,
   ungültiger `rolle`/`typ`-Wert, kaputtes JSON, nicht unterstützte
   Dateiendung, Schwelle außerhalb `[0.0, 1.0]`) gibt Claude die
   Fehlermeldung wieder und korrigiert die Eingabe bzw. fragt nach — es
   rät kein Ergebnis.

## Output-Format

JSON-Report nach [`schema/README.md`](schema/README.md#ausgabe-json-report),
Beispiel: [`schema/beispiel-report.json`](schema/beispiel-report.json)
(tatsächlich vom Executor erzeugt aus den beiden Beispieldateien, mit je
einem Treffer auf jeder der vier Stufen sowie einer echten
Nichttreffer-Partei). Jeder Score/jede Zahl im Report stammt aus
`executor.py`, nie vom Modell (P3).

## Beispiel

Eingabe: [`schema/beispiel-mandantenliste.csv`](schema/beispiel-mandantenliste.csv)
(5 Einträge) + [`schema/beispiel-neue-parteien.json`](schema/beispiel-neue-parteien.json)
(5 neue Parteien).

Von Claude präsentiertes Ergebnis (aus dem Report übernommen):

| Neue Partei | Listeneintrag (Rolle, Az.) | Stufe | Score | Begründung |
|---|---|---|---|---|
| Bau Mustermann GmbH | Mustermann Bau GmbH (mandant, 12/2024) | ✅ treffer (S2) | 1.0 | Token-Mengen-Gleichheit nach Normalisierung: {bau, mustermann} |
| Erika Mustermann | Erika Mustermann (mandant, 34/2023) | ✅ treffer (S1) | 1.0 | exakter Treffer nach Normalisierung |
| Schmitt | Schmidt (gegner, —) | ⚠️ moeglicher_treffer (S3) | 1.0 | phonetisch identisch nach Kölner Phonetik: 862 = 862 |
| Beispiel Handels GmbH | Beispiel Handel GmbH & Co. KG (gegner, —) | ⚠️ moeglicher_treffer (S4) | 0.97 | Ähnlichkeit 0.97 ≥ Schwelle 0.85 |

**Nicht getroffen:** "Voellig Unbeteiligte Partei GmbH" erscheint in keinem
Kandidaten-Paar — das ist **kein Freibrief**, sondern bedeutet nur: keine
der implementierten Match-Stufen hat einen Zusammenhang mit der
Mandanten-/Gegnerliste gefunden (siehe bewusste Grenzen in
[`schema/README.md`](schema/README.md#bewusste-grenzen)).

**Hinweis zur Kollisionsprüfung:** Bei "Schmitt"/"Schmidt" und
"Beispiel Handels GmbH"/"Beispiel Handel GmbH & Co. KG" handelt es sich um
`moeglicher_treffer` — die Kollisionsentscheidung (§ 43a Abs. 4 BRAO, § 3
BORA) trifft der Anwalt. "Beispiel Handel GmbH & Co. KG" trägt zudem die
Rolle `gegner` — auch bei einem eindeutigen `treffer` mit Gegner-Rolle wäre
dieser Hinweis zwingend.

## Bewusste Grenzen (Kurzfassung, vollständig in schema/README.md)

- Rechtsform-Gleichheit allein ist nie ein Treffer ("Müller GmbH" vs.
  "Schulze GmbH" matcht nicht).
- Kölner Phonetik ist für deutsche Lautung entwickelt.
- Kurze Namen bergen ein erhöhtes Fuzzy-False-Positive-Risiko trotz der
  hoch angesetzten Default-Schwelle (0.85).
- Kein Abgleich über Aktenzeichen/Notiz-Text — nur `name`-Felder werden
  verglichen.
- Ein `kein_treffer` ist **kein Freibrief**: Spitznamen, Umfirmierungen
  oder Transliterationen aus anderen Schriftsystemen bleiben ggf.
  unentdeckt. Die abschließende Kollisionsprüfung bleibt Kanzleipflicht.
