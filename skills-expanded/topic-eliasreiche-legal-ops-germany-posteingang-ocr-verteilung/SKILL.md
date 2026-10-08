---
name: posteingang-ocr-verteilung
description: "Strukturiert bereits texterkannten (OCR-)Papier-Posteingang je Eingang zu Absender/Datum/Aktenzeichen/Fristindikatoren, ordnet ihn per core/calc/zuordnung einem Mandat zu und erzeugt einen Routing-Plan in die Hotfolder-Ablagekonvention kontext/posteingang/ — ein Provenienz-Validator erzwingt maschinell, dass jeder kritische Wert wörtlich im Scan-Text belegt ist; Ablage standardmäßig als Dry-Run, echtes Kopieren nur mit --ausfuehren. Triggert bei Posteingang scannen, OCR Papierpost, Post routen, Scan-Ablage."
status: beta
welle: 4
bereich: post-akte
rdg_einordnung: "Organisatorische Postverarbeitung (Extraktion, Mandats-Zuordnungsvorschlag, Ablage-Plan) als Vorschlag; keine inhaltliche Bearbeitung der Korrespondenz, keine rechtliche Einschätzung, keine Fristberechnung."
daten_hinweis: "Scans tragen Mandatsbezug (§ 203 StGB / DSGVO) — lokale Texterkennung bevorzugen (z. B. macOS-Texterkennung/Vision-Framework, pdftotext, markitdown), sonst ausschließlich über DSGVO-/BRAO-konformen Modellzugang (AWS-Bedrock-Pfad) verarbeiten. Dieser Skill enthält selbst kein OCR und keinen Netzwerkzugriff — der Executor liest nur die übergebenen Text- und kontext/-Dateien."
haftung: "Fristindikatoren sind ein regelbasiertes Hinweis-Flag (fristrelevant), keine Fristberechnung und keine Fristenkontrolle — fristauslösende Eingänge sind zwingend gesondert dem Skill fristenrechner (Zweitkontrolle) zuzuführen. OCR-Fehler und unvollständige Indikator-Erkennung sind möglich; die Vollständigkeit bleibt anwaltlich zu prüfen. Mandats-Zuordnungsvorschläge werden nie automatisch übernommen — Mehrdeutigkeit ist immer eine Rückfrage an die Kanzlei. Der Routing-Plan ist standardmäßig ein Dry-Run; tatsächliches Kopieren erfolgt nur nach explizitem --ausfuehren und kopiert (löscht/überschreibt nie)."
kontext_reads:
  - mandate/*.md
kontext_writes:
  - posteingang/
---

# posteingang-ocr-verteilung

> **Status: `beta`** — automatisierte Tests laufen grün in CI (`tests/`).
> Noch **nicht** händisch abgenommen — `status: getestet` vergibt erst der
> Maintainer nach eigener Prüfung (siehe
> [CONVENTIONS.md](https://github.com/eliasreiche/legal-ops-germany/blob/main/CONVENTIONS.md), Reifegrad-Leiter).

## Zweck

Strukturiert gescannten Papier-Posteingang, für den bereits eine
Texterkennung vorliegt, zu einem maschinenlesbaren **Eingang**: Absender,
Datum des Schreibens, fremdes/eigenes Aktenzeichen, Betreff/Mandatsbezug und
**Frist-Indikatoren** (Schlüsselwörter wie „Frist", „binnen", „spätestens",
Zustellungsvermerke) — samt einem deterministisch abgeleiteten
`fristrelevant`-Flag. Anschließend ordnet er den Eingang über die
wiederverwendbare Bibliothek
[`core/calc/zuordnung/`](../../core/calc/zuordnung/) (dieselbe wie
[`email-akten-zuordnung`](../email-akten-zuordnung/SKILL.md)) einem Mandat
aus `kontext/mandate/*.md` zu und erzeugt einen **Routing-Plan** in die
Ablagekonvention `kontext/posteingang/JJJJ-MM-TT_<az|unzugeordnet>_<absender-slug>/`.

Die inhaltliche Extraktion macht **das Modell (Claude)** — es liest den
Scan-Text und füllt das Schema. Damit dabei nichts erfunden wird, prüft ein
deterministischer Executor die Ausgabe (P3 / Anti-Halluzination maschinell
erzwungen):

- **Schema-Konformität** des `eingang.json` (Pflichtstruktur, ISO-Datum,
  Lücken-Disziplin, Konsistenz von Schlüsselwort zu Zitat),
- **Provenienz**: Datum des Schreibens, fremdes/eigenes Aktenzeichen und
  jedes Frist-Indikator-Zitat müssen — nach definierter Normalisierung —
  **wörtlich in mindestens einer Quelldatei** vorkommen; nicht belegte Werte
  werden als `nicht_belegt` ausgewiesen,
- **Fristrelevanz**: `fristrelevant` ist niemals eine Modell-Behauptung,
  sondern `true` nur, wenn mindestens ein Frist-Indikator provenienzgeprüft
  belegt ist,
- **Mandats-Zuordnung**: Kandidaten (Stufen Z0–Z4 sowie Z2N, Nachname +
  Korroboration) gegen
  `kontext/mandate/*.md`; Mehrdeutigkeit oder kein Treffer ⇒ `unzugeordnet`,
  nie geraten,
- **Routing-Plan**: Ziel-Pfad nach der dokumentierten Konvention; Default ist
  ein Dry-Run, tatsächliches Kopieren nur mit `--ausfuehren` (kopiert nie
  löscht, nie überschreibt — Kollision ist ein Fehler).

> ⚠️ **Keine Fristberechnung.** `fristrelevant` ist ein Hinweis-Flag, kein
> Fristende. Jede tatsächliche Fristberechnung läuft ausschließlich über den
> Skill [`fristenrechner`](../fristenrechner/SKILL.md) als deterministische
> Zweitkontrolle.

**Kein OCR-Code in diesem Repo.** Voraussetzung ist je Scan bereits
extrahierter Text (`<scan>.txt`/`.md` neben der Scan-Datei), erzeugt durch
ein externes, lokales Werkzeug — lokale Verarbeitung bevorzugt (§ 203 StGB):

- macOS-Texterkennung (Vision-Framework, z. B. per Vorschau/Automator),
- `pdftotext` (Poppler) für digital erzeugte PDFs mit Textebene,
- `markitdown` (bereits im Vault-Werkzeugkasten vorhanden) für gemischte
  Formate.

Alternativ liest Claude den Scan direkt (z. B. ein Bild/PDF multimodal) und
schreibt den erkannten Text selbst in eine Textdatei — dann gilt **derselbe
Provenienz-Kontrakt**: der Executor sieht in beiden Fällen nur Text, nie das
Bild/PDF. Eine Repo-weite Konvertierungs-Standard-Entscheidung ist beim
Maintainer offen; dieser Skill bindet keine bestimmte Lösung ein.

## Eingaben (Datei-Kontrakt, P2)

| Eingabe | Pflicht | Format | Beschreibung |
|---|---|---|---|
| Eingangs-Entwurf | ja (`--eingang`) | `.json` | Vom Modell nach Schema erzeugt. Struktur: [`schema/README.md`](schema/README.md), Beispiel: [`schema/beispiel-eingang.json`](schema/beispiel-eingang.json). |
| Scan-Text(e) | ja (`--quelle`) | `.txt` / `.md`, UTF-8 | Bereits extrahierter Text. Mehrfach angebbar. Beispiel: [`schema/beispiel-scan.txt`](schema/beispiel-scan.txt). |
| `kontext/`-Verzeichnis | ja (`--kontext`) | Verzeichnis nach [`core/context/README.md`](../../core/context/README.md) | Mandate (`az`, `mandant`, `gegenseite`) für die Zuordnung. |
| Scan-Datei(en) fürs Routing | nein (`--scan-datei`) | beliebig, mehrfach | Datei(en), die der Routing-Plan kopiert (Scan-Original und/oder Textauszug). Ohne diese Option enthält der Plan nur den berechneten Zielordner-Namen, keine Dateien. |
| Fuzzy-Schwelle | nein (`--schwelle-moeglich`) | Float, Default `0.85` | Wie `email-akten-zuordnung`, dort begründet. |
| Ausführen | nein (`--ausfuehren`) | Flag | Ohne diese Option: reiner Dry-Run-Plan. Mit dieser Option: tatsächliches Kopieren. |

Der Executor liest die Eingaben nur — keine OCR, kein Netzwerkzugriff. Nur
bei `--ausfuehren` schreibt er (kopierend) nach `kontext/posteingang/`.

## Ablauf

1. **Claude beschafft den Scan-Text** — entweder aus einer bereits
   vorhandenen `<scan>.txt`/`.md`-Datei (extern per OCR erzeugt) oder, wenn
   kein Werkzeug verfügbar ist, indem es den Scan selbst liest (multimodal)
   und den erkannten Text in eine `.txt`-Datei schreibt. Es wird nie ein
   Absender, Datum oder Aktenzeichen erfunden — fehlt eine Angabe im Text,
   bleibt sie leer/`null` bzw. wird als Lücke ausgewiesen.
2. **Claude kopiert [`schema/beispiel-eingang.json`](schema/beispiel-eingang.json)
   als Vorlage** und füllt sie aus dem Scan-Text — ein `eingang.json` wird
   **nie** frei aus dem Gedächtnis aufgebaut. Beim Absuchen nach
   Frist-Indikatoren orientiert sich Claude an dieser Wortliste (Beispiele,
   keine abschließende Aufzählung — anwaltliche Durchsicht bleibt nötig):
   „Frist", „binnen", „spätestens", „Zustellung"/„zugestellt"/
   „Zustellungsurkunde"/„PZU", „Mahnung", „Kündigung", „Bescheid", „Urteil",
   „Beschluss", „Klage", „einstweilige". Jeder gefundene Indikator bekommt
   ein wörtliches `quelle_zitat`, das das Schlüsselwort selbst enthält. Was
   nicht im Text steht, wird nicht ergänzt, sondern — soweit lücken-fähig
   (`absender`, `datum_schreiben`, `betreff`) — als `luecken`-Eintrag
   ausgewiesen.
3. **Claude ruft den Executor auf** (kein eigenes Prüfen/Zuordnen/Routen
   durch das Modell):

   ```bash
   python3 ${CLAUDE_PLUGIN_ROOT}/skills/posteingang-ocr-verteilung/executor.py \
     --eingang <eingang.json> \
     --quelle <scan.txt> [--quelle <weitere.txt> ...] \
     --kontext <kontext-verzeichnis> \
     [--scan-datei <scan-original-oder-textdatei> ...] \
     [--schwelle-moeglich <float, Default 0.85>] \
     [--output <report.json>]
   ```

4. **Der Executor prüft/entscheidet deterministisch** (P3): Schema,
   Provenienz jedes kritischen Werts, das `fristrelevant`-Flag, die
   Mandats-Zuordnung (Kandidaten Z0–Z4 sowie Z2N) und den Zielordner-Namen des
   Routing-Plans — vollständige Definition in
   [`schema/README.md`](schema/README.md). Claude liest ausschließlich den
   JSON-Report und übernimmt alle Felder unverändert.
5. **Bei `nicht_belegt` oder Schema-Fehler korrigiert Claude** den Eingang —
   einen nicht belegten Wert streichen (bzw. bei lücken-fähigen Feldern als
   Lücke ausweisen) oder das `quelle_zitat` korrigieren — nie erfinden — und
   ruft den Executor erneut auf. Kein One-Shot: Schritte 2–5 sind eine
   Korrekturschleife, bis Exit-Code `0` erreicht ist (siehe die verbindliche
   Korrekturschleife in [`aktenkopf-extraktor`](../aktenkopf-extraktor/SKILL.md),
   analog hier anzuwenden).
6. **Claude stellt das Ergebnis in Markdown dar**: Eingang (Absender, Datum,
   Az fremd/eigen, Betreff), Lückenliste, und — bei `fristrelevant: true` —
   einen **prominenten Abschnitt „Der Fristenkontrolle zuführen"** mit
   Verweis auf den Skill `fristenrechner` (Zweitkontrolle; keine eigene
   Fristberechnung oder Normzitat). Bei `zuordnung.erfordert_rueckfrage:
   true` formuliert Claude **immer** eine Rückfrage an die Kanzlei
   (Kandidatenliste zeigen, nie automatisch wählen) statt den Eingang
   automatisch als zugeordnet zu behandeln; bei `kein_treffer` entsprechend
   nach dem zuständigen Mandat fragen.
7. **Claude zeigt den Routing-Plan** (Zielordner, zu kopierende Dateien) und
   führt ihn **nur nach ausdrücklicher Bestätigung durch die Kanzlei** aus,
   indem der Executor erneut mit `--ausfuehren` aufgerufen wird. Ohne
   Bestätigung passiert nichts — der Plan ist ein Vorschlag, keine
   Ausführung. Meldet der Executor `routing_plan.fehler` (Kollision:
   Zielordner existiert bereits), gibt Claude die Fehlermeldung wieder und
   schlägt vor, den bestehenden Ordner zu prüfen — es wird nie
   überschrieben oder ein neuer Name geraten.
8. Bei Exit-Code 2 (Eingabefehler: Datei/Verzeichnis fehlt, kaputtes JSON,
   Schwelle außerhalb `[0.0, 1.0]`) gibt Claude die Fehlermeldung wieder und
   fragt nach bzw. korrigiert die Eingabe.

## Output-Format

JSON-Report nach [`schema/README.md`](schema/README.md), Beispiel:
[`schema/beispiel-report.json`](schema/beispiel-report.json) (tatsächlich
erzeugt aus [`schema/beispiel-eingang.json`](schema/beispiel-eingang.json) +
[`schema/beispiel-scan.txt`](schema/beispiel-scan.txt) gegen
[`core/context/beispiel-kontext/`](../../core/context/beispiel-kontext/)).
Kernfelder: `schema_ok`, `schema_fehler[]`, `provenienz[]`, `luecken[]`,
`fristrelevant`, `fristrelevant_hinweis`, `zuordnung` (`kandidaten[]`,
`eindeutig`, `az_fuer_routing`, `erfordert_rueckfrage`), `routing_plan`
(`ziel_ordner`, `dateien[]`, `ausgefuehrt`, `fehler`), `zusammenfassung`.

Jeder Beleg-Zustand, jedes Zuordnungs-Ergebnis und jeder Zielordner-Name im
Report stammt aus `executor.py`, nie vom Modell (P3).

## Beispiele

### Beispiel 1 — Mahnschreiben mit eindeutiger Zuordnung (alles belegt)

Eingabe: [`schema/beispiel-scan.txt`](schema/beispiel-scan.txt) (fiktives
Mahnschreiben der „Muster AG" mit eigenem und fremdem Aktenzeichen sowie
mehreren Frist-Indikatoren). Claude erzeugt daraus
[`schema/beispiel-eingang.json`](schema/beispiel-eingang.json); der Executor
belegt alle 6 kritischen Werte (Exit 0). Von Claude präsentiert:

**Eingang** — Muster AG, Schreiben vom 01.07.2026, Az. (eigen) 2026-001,
Az. (fremd) VB-2026-77, Betreff „Mahnung und Fristsetzung".

**Der Fristenkontrolle zuführen** ⚠️ — Frist-Indikatoren gefunden
(„Mahnung", „binnen", „spätestens") — dieser Eingang ist gesondert der
Fristenkontrolle zuzuführen (Skill `fristenrechner`, Zweitkontrolle). Dies
ist **keine** Fristberechnung.

**Mandats-Zuordnung** — ✅ eindeutig **2026-001** (Z0, eigenes Aktenzeichen
"2026-001" wörtlich im Text gefunden).

**Routing-Plan (Dry-Run)** — Ziel: `posteingang/2026-07-01_2026-001_muster-ag/`.
Erst nach Bestätigung durch die Kanzlei mit `--ausfuehren` tatsächlich
kopieren.

### Beispiel 2 — erfundener Wert wird abgefangen

Trägt der Eingang ein Datum oder Aktenzeichen, das **nicht** im Scan-Text
steht, meldet der Executor es als `nicht_belegt` (Exit 1) mit dem Hinweis
„Wert streichen oder als Lücke ausweisen". Claude übernimmt einen solchen
Wert nie, sondern streicht ihn oder führt ihn (soweit lücken-fähig) als
Lücke — so wird die Anti-Halluzinations-Regel maschinell erzwungen.

### Beispiel 3 — Mehrdeutige Zuordnung

Trifft der Eingang auf mehr als ein Mandat (oder nur auf einen
`moeglicher_treffer`), setzt der Executor `erfordert_rueckfrage: true` und
`az_fuer_routing: null`. Claude wählt **nie** automatisch eines der Mandate,
sondern stellt die Rückfrage „Az. X oder Az. Y — welches Mandat ist
gemeint?" (identisches Prinzip wie das dokumentierte
Mehrdeutigkeits-Beispiel in
[`email-akten-zuordnung`](../email-akten-zuordnung/SKILL.md#beispiel)). Der
Routing-Plan zeigt in diesem Fall vorläufig `unzugeordnet` als Zielordner.

## Grenzen

- **Kein OCR/Bildverarbeitung** — Voraussetzung ist bereits extrahierter
  Text; Qualität/Vollständigkeit der Texterkennung liegt außerhalb dieses
  Skills.
- **Keine Fristberechnung / kein Fristende** — nur ein deterministisch
  abgeleitetes `fristrelevant`-Flag; Fristen ausschließlich über
  [`fristenrechner`](../fristenrechner/SKILL.md).
- **Fristindikator-Vollständigkeit ist nicht maschinell erzwingbar** — ein
  vom Modell übersehenes Schlüsselwort führt zu `fristrelevant: false`,
  obwohl das Schreiben tatsächlich fristauslösend sein kann. Ersetzt keine
  anwaltliche Durchsicht.
- **Provenienz ist ein Beleg-, kein Richtigkeitsnachweis**: `belegt` heißt
  nur, dass der Wert (nach Normalisierung) im Text vorkommt — nicht, dass er
  rechtlich zutrifft.
- **Mandats-Zuordnung erbt die Grenzen von `core/calc/zuordnung/`** (Z1–Z4
  sowie Z2N können bei kurzen/häufigen Namens-Token mehrdeutig treffen) —
  deshalb ist mehr als ein Kandidat immer eine Rückfrage, nie eine
  automatische Wahl.
- **Routing kopiert, löscht nie** — das Original bleibt an seinem Ort;
  Kollision (Zielordner existiert bereits) ist ein Fehler, kein
  automatisches Zusammenführen oder Überschreiben. Ein nachträgliches
  Entfernen des Originals ist eine bewusste, separate Kanzlei-Entscheidung.
