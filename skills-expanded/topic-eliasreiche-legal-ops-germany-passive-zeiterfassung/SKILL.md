---
name: passive-zeiterfassung
description: "Rekonstruiert aus Kalender- und Mail-Metadaten Zeiterfassungs-Vorschläge je Akte zum Bestätigen oder Verwerfen und übergibt bestätigte Einträge an taetigkeitstext-rvg. Triggert bei Zeiterfassung, Stunden rekonstruieren, Timesheet-Vorschlag, erfasste Zeiten je Akte."
status: beta
welle: 3
bereich: zeit-abrechnung
kontext_reads:
  - mandate/*.md
rdg_einordnung: "Interner Verwaltungsvorschlag zur Zeiterfassung; keine Rechtsdienstleistung. Der Output ordnet Metadaten Akten zu und schlägt Zeitwerte vor — keine rechtliche Bewertung, keine Abrechnungsentscheidung."
daten_hinweis: "Wertet ausschließlich Kalender-/Mail-METADATEN des Kanzlei-Tenants aus (Betreff, Zeiten, Teilnehmer/Absender, Richtung) — bewusst KEINE Mail-Inhalte (§ 203 StGB / DSGVO-Minimierung). Die Betroffenen-Transparenz (Mitarbeitende, deren Termine/Mails ausgewertet werden) ist im Kanzlei-Team herzustellen; BRAO-konformer Modellzugang vorausgesetzt."
haftung: "Vorschläge sind Schätzungen aus Metadaten (Termin-Dauer aus start/ende, Mail-Zeit aus der Kanzlei-Pauschale) — nie eine erfundene Zeit. Abrechnungsrelevante Zeiten und die Akten-Zuordnung bestätigt die Kanzlei vor jeder Weiterverarbeitung (Zweitkontrolle). Der Skill ersetzt keine Zeiterfassungs-Sorgfalt der Kanzlei."
---

# passive-zeiterfassung

## Zweck

Rekonstruiert aus **Kalender- und Mail-Metadaten** je Akte
Zeiterfassungs-Vorschläge, die die Kanzlei bestätigt oder verwirft. Jeder
eindeutig zugeordnete Vorschlag ist bereits ein fertiger Leistungseintrag im
Format des Abnehmers [`taetigkeitstext-rvg`](../taetigkeitstext-rvg/SKILL.md) —
bestätigte Einträge laufen ohne Umbau in dessen Executor.

Der Skill erfindet nichts: Termin-Dauern kommen aus `start`/`ende`
([`core/calc/zeit`](../../core/calc/zeit/)), Mail-Zeitwerte ausschließlich aus
der Kanzlei-Konvention `config.mail_pauschale_minuten`, die Akten-Zuordnung
aus [`core/calc/zuordnung`](../../core/calc/zuordnung/) gegen
`kontext/mandate/*.md`. Fehlt eine Zuordnung oder ein Zeitwert, wird das als
Lücke ausgewiesen, nie geraten (P3, Anti-Halluzination).

## Eingaben (Datei-Kontrakt, P2)

Vollständige Feldtabellen und das M365-Mapping: [`schema/README.md`](schema/README.md).

| Flag | Pflicht | Inhalt |
|---|---|---|
| `--termine` | eines von beiden Pflicht | Kalender-Metadaten `{"termine": [...]}` (Betreff, start/ende, Teilnehmer, Ort). |
| `--mails` | eines von beiden Pflicht | Mail-Metadaten `{"mails": [...]}` (Zeitstempel, Betreff, Absender, Empfänger, Richtung) — **keine Bodies**. |
| `--kontext` | ja | `kontext/`-Verzeichnis mit `mandate/*.md`. |
| `--config` | nein | `{"mail_pauschale_minuten": int>0 \| null}` — Zeitansatz je Mail (Kanzlei-Konvention). Ohne Config → Mails ohne Zeitwert. |
| `--output` | nein | Zieldatei für den Report (Default: stdout). |

Die Metadaten-Dateien entstehen über [`kontext-sync`](../kontext-sync/SKILL.md)
(Microsoft-365-MCP-Konnektor) oder als manueller Export.

## Ablauf

1. **Metadaten-Dateien liegen vor** — Kalender-/Mail-Metadaten als
   `termine.json`/`mails.json` (via [`kontext-sync`](../kontext-sync/SKILL.md)
   oder Export). Keine Mail-Inhalte, nur Metadaten.
2. **Executor läuft** (deterministisch):

   ```bash
   python3 ${CLAUDE_PLUGIN_ROOT}/skills/passive-zeiterfassung/executor.py \
     --termine termine.json --mails mails.json --config config.json \
     --kontext <kontext-dir> --output report.json
   ```

   Er berechnet Termin-Dauern, ordnet jeden Termin/jede Mail einer Akte zu
   (Z0–Z4 sowie Z2N) und verteilt die Ergebnisse auf `vorschlaege`, `mehrdeutig`,
   `nicht_zuordenbar`, `ohne_zeitwert` und `warnungen` (Termin-Überlappungen).
3. **Claude präsentiert die Vorschläge je Akte tabellarisch** zum
   **Bestätigen / Verwerfen** — je Vorschlag: Datum, Akte (`az`), Dauer,
   Betreff/Stichworte, Zuordnungs-Beleg (Stufe + Begründung). `mehrdeutig`,
   `nicht_zuordenbar` und `ohne_zeitwert` werden **immer als offene Fragen**
   gestellt (welche Akte? welcher Zeitwert?), nie automatisch entschieden.
4. **Bestätigte Einträge → `leistungen.json` → Übergabe an
   [`taetigkeitstext-rvg`](../taetigkeitstext-rvg/SKILL.md)**: Claude schreibt
   die von der Kanzlei bestätigten `leistung`-Objekte als `leistungen.json`
   (Format identisch, siehe `schema/README.md`) und übergibt sie an dessen
   Executor zur Formulierung/Taktung. Die Taktung passiert dort, nicht hier.

## Output-Format

Der Report (`report.json`) enthält:

- **`vorschlaege[]`** — je Eintrag den fertigen `taetigkeitstext-rvg`-Eintrag
  (`leistung`), den Zuordnungs-Beleg (`zuordnung`: Stufe, Kategorie,
  Begründung) und `status: "zu_bestaetigen"`.
- **`mehrdeutig[]`** — mehrere Treffer oder nur mögliche Treffer; die Kanzlei
  wählt die Akte.
- **`nicht_zuordenbar[]`** — kein Kandidat (Lücke).
- **`ohne_zeitwert[]`** — Mails ohne konfigurierte Pauschale (Lücke; Minuten
  manuell nachtragen).
- **`warnungen[]`** — zeitlich überlappende Termine (beide Betreffs).
- **`summen.je_az`** — Minuten je Akte, nur über die eindeutigen Vorschläge
  (via `core/calc/zeit`).

Deterministik-Grenze (P3): Jeder Zahlen-/Datums-/Zuordnungswert im Report
stammt aus dem Executor und ist als solcher markiert — nie modellgeneriert.

## Beispiele

`schema/beispiel-termine.json` (5 Termine: eindeutig, mehrdeutig, nicht
zuordenbar, Überlappungspaar), `schema/beispiel-mails.json` (3 Mails) und
`schema/beispiel-config.json` erzeugen `schema/beispiel-report.json`.
`schema/beispiel-leistungen.json` sind die bestätigten Vorschläge im
`taetigkeitstext-rvg`-Format. Alle Beispieldateien werden per Executor erzeugt
und von den Tests synchron gehalten; der Round-Trip-Test lässt die bestätigten
Einträge durch den echten `taetigkeitstext-rvg`-Executor laufen.

## Grenzen

- **Zuordnung ist eine Heuristik** (Z0–Z4 sowie Z2N, siehe
  [`core/calc/zuordnung`](../../core/calc/zuordnung/)): Az-Treffer (Z0) sind
  sicher, Parteiname-Treffer (Z1–Z4) können bei kurzen/ähnlichen Namen falsch
  anschlagen — deshalb landet jede Unsicherheit in `mehrdeutig`/
  `nicht_zuordenbar`, nie in einem stillen Vorschlag. **Z2N** (Nachname beider
  Beteiligter + Korroboration) ist immer nur `moeglicher_treffer` und wird
  deshalb hier nie zu einem Vorschlag — ein Z2N-Kandidat landet in
  `mehrdeutig[]`, sofern er der einzige Kandidat für sein Mandat bleibt.
  Steht daneben aber genau ein `treffer` eines anderen Mandats (Status
  `eindeutig`), schreibt der Report für diesen nur `zuordnung: <treffer>` —
  der Z2N-Kandidat erscheint dort nirgends (Details:
  [`schema/README.md`](schema/README.md)).
- **Mail-Zeitwerte sind eine Pauschale**, kein gemessener Aufwand — die
  Kanzlei setzt sie als Konvention und korrigiert je Mail bei Bedarf.
- **Der Skill entscheidet nie über Abrechnung** — er liefert Vorschläge; jede
  abrechnungsrelevante Zeit bestätigt die Kanzlei.
