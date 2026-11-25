---
name: email-akten-zuordnung
description: "Ordnet eingehende E-Mails (EML-Dateien oder M365-Metadaten via kontext-sync) Akten zu, priorisiert (inkl. Fristverdacht) und schlägt Ablage in der e-Akte vor. Triggert bei E-Mail-Triage, Posteingang zuordnen, e-Akte-Ablage, Mail-Priorisierung."
status: beta
welle: 3
bereich: post-akte
rdg_einordnung: "Organisatorische Posteingangs-Sortierung als Vorschlag (Aktenzeichen-/Parteiname-Abgleich, Prioritäts-Regel); keine inhaltliche Bearbeitung der Korrespondenz, keine Fristberechnung."
daten_hinweis: "E-Mail-Metadaten und -Auszüge sind Mandatsdaten — § 203 StGB / DSGVO beachten, DSGVO-/BRAO-konformer Modellzugang. PII-Minimierung: der Report enthält nie den vollen Mail-Text, nur Metadaten (Absender, Betreff, Datum) plus einen Textauszug von max. 500 Zeichen; Mail-Volltexte bleiben im Ursprungssystem (Mailserver/EML-Archiv/M365)."
haftung: "Zuordnungs-, Prioritäts- und Ablage-Vorschläge sind zu bestätigen und werden nie automatisch ausgeführt. Fristverdacht ist ein Hinweis, keine Fristberechnung — fristauslösende Post ist zwingend gesondert der Fristenkontrolle (Skill `fristenrechner`) zuzuführen. Mehrdeutige/widersprüchliche Zuordnungen gehen immer als Rückfrage an die Kanzlei, nie als automatische Entscheidung."
kontext_reads:
  - mandate/*.md
  - kontakte.md
kontext_writes:
  - posteingang/*
  - mandate/*.md
---

# email-akten-zuordnung

> **Status: `beta`** — automatisierte Tests laufen grün in CI (`tests/`):
> EML-Parsing (RFC-2047-Umlaut-Header, fehlende Felder), Az-Stufe Z0,
> Parteien-Stufen Z1–Z4 inkl. eines echten False-Positive-/Mehrdeutigkeits-
> Grenzfalls, Nachname-Stufe Z2N (Korroboration, Enthaltung bei
> Mehrdeutigkeit), `kein_treffer`-Lücke, Fristverdacht-Wortliste, Slug-/
> Dateinamen-Regel, Kommunikations-Zeilen-Format, PII-Grenze
> (Body-Truncation), CLI-Fehler (Exit 2), Beispiel-Sync. Noch **nicht**
> händisch abgenommen — `status: getestet` vergibt erst der Maintainer nach
> eigener Prüfung (Reifegrad-Leiter, CONVENTIONS.md).

## Zweck

Ordnet eingehende E-Mails (EML-Dateien oder gleichwertige Metadaten aus dem
kontext-sync/M365-Weg) den Mandaten aus `kontext/mandate/*.md` zu,
priorisiert sie (inkl. regelbasiertem Fristverdacht) und schlägt eine
Ablage in `posteingang/` samt der fertigen Kommunikations-Zeile fürs Mandat
vor — Datei/Metadaten rein, Vorschlags-Report raus, **keine automatische
Ablage**. Dies ist der erste Skill, der den Kontext-Layer
([`core/context/`](../../core/context/README.md), D11/D19) tatsächlich
konsumiert (`lese_mandate()`).

Die zugrundeliegende Zuordnungs-Bibliothek
[`core/calc/zuordnung/`](../../core/calc/zuordnung/) ist bewusst klein und
wiederverwendbar gehalten — Skill #14 `posteingang-ocr-verteilung`
(Welle 4) nutzt sie später für den Abgleich von gescannter Papierpost.

## Eingaben (Datei-Kontrakt, P2)

| Eingabe | Pflicht | Format | Beschreibung |
|---|---|---|---|
| E-Mail(s) | ja, genau ein Weg | `--eml <datei-oder-verzeichnis>` (`.eml`, Python-stdlib `email`-Parsing) **oder** `--input <metadaten.json>` (JSON-Array, kontext-sync/M365-Weg) | Vollständiger Kontrakt: [`schema/README.md`](schema/README.md). |
| `kontext/`-Verzeichnis | ja (`--kontext`) | Verzeichnis nach [`core/context/README.md`](../../core/context/README.md) | Mandate (`az`, `mandant`, `gegenseite`) werden über `lese_mandate()` eingelesen. |
| Fuzzy-Schwelle | nein (`--schwelle-moeglich`) | Float, Default `0.85` | Wie `interessenkollision-check`, dort begründet. |

Alle Eingaben werden nur **gelesen** — keine Kopie, kein Netzwerkzugriff, keine
Persistierung durch den Executor selbst.

## Ablauf

1. **Claude beschafft die E-Mail(s)** — entweder als `.eml`-Datei(en) oder,
   wenn Kanzlei-Post bereits über [`kontext-sync`](../kontext-sync/SKILL.md)
   (M365-MCP-Konnektor) angebunden ist, als Metadaten-JSON nach dem Kontrakt
   in [`schema/README.md`](schema/README.md). Es wird nie ein Absender,
   Betreff oder Textinhalt erfunden — fehlt ein Feld im Quellmaterial, bleibt
   es leer/`null`.
2. **Claude ruft den Executor auf** (kein eigenes Namens-/Az-Abgleichen durch
   das Modell):

   ```bash
   python3 ${CLAUDE_PLUGIN_ROOT}/skills/email-akten-zuordnung/executor.py \
     --eml <datei-oder-verzeichnis> \
     --kontext <kontext-verzeichnis> \
     [--output <report.json>] \
     [--schwelle-moeglich <float, Default 0.85>]

   # oder, für den kontext-sync/M365-Weg:
   python3 ${CLAUDE_PLUGIN_ROOT}/skills/email-akten-zuordnung/executor.py \
     --input <metadaten.json> --kontext <kontext-verzeichnis>
   ```

3. **Der Executor entscheidet deterministisch** (P3, Deterministik-Grenze):
   Zuordnungs-Kandidaten je Mandat (Stufen Z0–Z4 sowie Z2N, Nachname +
   Korroboration), `fristverdacht`,
   `prioritaet` und den `ablage_vorschlag` (Dateiname + Kommunikations-Zeile)
   — vollständige Definition in [`schema/README.md`](schema/README.md). Claude
   liest ausschließlich den JSON-Report und übernimmt alle Felder
   unverändert; es vergibt selbst nie eine Stufe, Priorität oder einen
   Dateinamen.
4. **Claude präsentiert je E-Mail eine Tabelle** (nie automatisch ablegen):
   - Absender, Betreff, Datum;
   - Zuordnungs-Kandidat(en) — Az, Stufe/Kategorie (✅ `treffer` /
     ⚠️ `moeglicher_treffer`), Begründung; bei **mehr als einem Kandidaten**
     oder ausschließlich `moeglicher_treffer`-Kandidaten: **immer** als
     Rückfrage an die Kanzlei formulieren, welches Mandat zutrifft — nie
     automatisch das erste/beste wählen (siehe das dokumentierte
     Mehrdeutigkeits-Beispiel in [`schema/README.md`](schema/README.md#beispiel-emls-in-diesem-ordner-fiktiv-exampledomains));
   - bei `kein_treffer`: explizit als Lücke ausweisen und nach dem
     zuständigen Mandat fragen — nie raten;
   - jeden Eintrag aus `zuordnung_hinweise[]` wiedergeben: dort steht, dass
     ein Nachname-Signal (Stufe Z2N) auf mehrere Mandate passte und deshalb
     bewusst **keine** Zuordnung erfolgt ist — das ist eine Rückfrage an die
     Kanzlei ("welches der genannten Mandate ist gemeint?"), keine Lücke im
     Material;
   - `prioritaet` (hoch/normal); bei `fristverdacht: true` **immer** den
     Hinweis wiedergeben, dass diese Post gesondert der Fristenkontrolle
     (`fristenrechner`, Zweitkontrolle) zuzuführen ist — ohne selbst eine
     Frist zu berechnen oder ein Normzitat anzubringen;
   - den `ablage_vorschlag` (Ziel-Dateiname, Kommunikations-Zeile); fehlt ein
     auswertbares Datum (`ablage_vorschlag.moeglich: false`), das als Lücke
     benennen und um das Datum bitten.
5. **Erst nach ausdrücklicher Bestätigung durch die Kanzlei** legt Claude ab:
   - die E-Mail-Datei nach `kontext/posteingang/<dateiname>` (aus
     `ablage_vorschlag.dateiname`);
   - die `kommunikations_zeile` an den `## Kommunikation`-Abschnitt des
     bestätigten `kontext/mandate/<az>.md` anhängen (Format siehe
     [`core/context/README.md`](../../core/context/README.md)).
   Ohne Bestätigung passiert nichts — der Report ist ein Vorschlag, keine
   Ausführung.
6. Bei Exit-Code 2 (Eingabefehler: Datei/Verzeichnis fehlt, kein `.eml` im
   Verzeichnis, kaputtes JSON, ungültiges Datum im `--input`-JSON, `kontext/`
   fehlt, Schwelle außerhalb `[0.0, 1.0]`) gibt Claude die Fehlermeldung
   wieder und fragt nach bzw. korrigiert die Eingabe — es rät kein Ergebnis.

## Output-Format

JSON-Report nach [`schema/README.md`](schema/README.md#ausgabe-json-report),
Beispiel: [`schema/beispiel-report.json`](schema/beispiel-report.json)
(tatsächlich vom Executor erzeugt aus den vier Beispiel-EMLs in `schema/`
gegen [`core/context/beispiel-kontext/`](../../core/context/beispiel-kontext/)).
Jede Stufe/Priorität/jeder Dateiname im Report stammt aus `executor.py`, nie
vom Modell (P3).

## Beispiel

Eingabe: [`schema/beispiel-az-im-betreff.eml`](schema/beispiel-az-im-betreff.eml)
gegen [`core/context/beispiel-kontext/`](../../core/context/beispiel-kontext/)
(Mandat `2026-001`, Az im Betreff erwähnt).

Von Claude präsentiertes Ergebnis (aus dem Report übernommen):

| Absender | Betreff | Datum | Kandidat | Priorität | Ablage-Vorschlag |
|---|---|---|---|---|---|
| Kanzlei Beispiel | Fristsetzung in unserer Sache, Az. 2026-001 | 2026-06-20 | ✅ **2026-001** (Z0, Az wörtlich im Betreff) | **hoch** (Fristverdacht: "Frist") | `posteingang/2026-06-20-fristsetzung-in-unserer-sache-az-2026-001.eml` |

**Hinweis zum Fristverdacht:** Signalwort "Frist" erkannt — diese Post ist
gesondert der Fristenkontrolle (`fristenrechner`, Zweitkontrolle)
zuzuführen. Dies ist **keine** Fristberechnung.

**Mehrdeutigkeits-Beispiel** (siehe
[`beispiel-fristverdacht.eml`](schema/beispiel-fristverdacht.eml)): Der
Absender "Zweite Beispiel KG" trifft sowohl auf Mandat `2026-002` (eigener
Mandantenname) als auch — über das gemeinsame Wort "Beispiel" — auf Mandat
`2026-001` (`mandant: "Beispiel GmbH"`). In diesem Fall stellt Claude die
Frage "Az. 2026-001 oder 2026-002 — welches Mandat ist gemeint?" statt
automatisch eines der beiden zu wählen.

## Bewusste Grenzen (Kurzfassung, vollständig in schema/README.md)

- Z1/Z2 (Parteiname als Phrase/Token-Menge) können bei kurzen/häufigen
  Namensbestandteilen mehrdeutig treffen (siehe Mehrdeutigkeits-Beispiel
  oben) — deshalb ist **mehr als ein Kandidat immer eine Rückfrage**, nie
  eine automatische Wahl.
- **Z1/Z2 brauchen den vollständigen Parteinamen** (inkl. Vorname). Eigene
  ausgehende Post mit der Anrede "Sehr geehrte/r Herr/Frau <Nachname>"
  erfüllt das nicht — bis zur Pilot-Abnahme 2026-08 war das eine
  undokumentierte Falsch-Negativ-Klasse. Stufe **Z2N** fängt sie ab, aber
  nur mit Korroboration: der Nachname der `gegenseite` desselben Mandats
  muss ebenfalls wörtlich und in Personen-Position vorkommen — entweder mit
  Anrede davor ("Herrn Köhn") oder über einen expliziten Rubrum-Trenner aus
  einer geschlossenen Menge ("./.", " gegen ") unmittelbar neben dem
  Nachnamen der anderen Partei ("Merkel ./. Köhn"). Bloße Wort-Nachbarschaft
  ohne einen der beiden Belege korroboriert NICHT (D12-Nachreview: sonst
  träfe "Rechtsanwalt Frank, Köln" fälschlich gegen ein Mandat "Frank" ./.
  "Köln") — ebenso wenig das letzte Token einer Organisations-Gegenseite
  ("Stadtwerke Berlin" → `berlin`). Ein Nachname allein bleibt `kein_treffer`,
  ebenso Mandate ohne `gegenseite`; Z2N ist immer nur `moeglicher_treffer`
  (nie so stark wie Z0/Z1/Z2). Details:
  [`schema/README.md`](schema/README.md#z2n--nachname--korroboration-warum-und-wie-eng).
- Kein Abgleich gegen die Absender-**Adresse** (nur Namensfelder), kein
  Az-Abgleich im Absendernamen (nur Betreff/Textauszug).
- Kölner Phonetik ist für deutsche Lautung entwickelt.
- `kein_treffer` ist kein Freibrief: Schreibweisen-/Bezugslücken jenseits
  der Stufen Z0–Z4/Z2N bleiben möglich.
- `kontakte.md` fließt aktuell nicht in die Zuordnung ein — nur
  `mandant`/`gegenseite` aus den Mandats-Frontmatters.
