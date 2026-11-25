---
name: kontext-sync
description: "Synchronisiert Kanzlei-Daten (Mandate, Kontakte, Kanzlei-Profil) zwischen der Kanzleisoftware/M365 und dem lokalen kontext/-Ordner — per vorhandenem MCP-Konnektor oder per filesystem-Referenzadapter, danach immer Schema-Validierung. Triggert bei kontext/ synchronisieren, Kanzlei-Daten abgleichen, Mandat aktualisieren, kontext-sync, Kontext-Layer befüllen, Mandatsakte nach kontext/ holen, M365 nach kontext/ übernehmen. Konflikte werden nie automatisch aufgelöst."
status: beta
welle: 3
bereich: querschnitt
rdg_einordnung: "Reine Datei-/Datensynchronisation zwischen Systemen nach dokumentiertem Schema (kein inhaltliches Verfassen, keine rechtliche Bewertung); keine Rechtsdienstleistung."
daten_hinweis: "kontext/ enthält Mandatsdaten (Az., Mandant, Gegenseite, Streitwert) — Datenperimeter und Klassifizierung nach D10 (Datenklassifizierung des Vaults/der Kanzlei-Datenhaltung, kod-decisions) beachten: nur in regulatorisch/technisch sicheren Tools verarbeiten, DSGVO-/BRAO-konformen Modellzugang nutzen (AWS-Bedrock-Pfad, § 203 StGB). Der filesystem-Adapter arbeitet rein lokal, ohne Netzwerkzugriff; ein MCP-Konnektor (z. B. M365) überträgt Daten an einen externen Dienst — dessen Freigabe ist Sache der Kanzlei."
haftung: "Der Validator und der filesystem-Adapter sind deterministische Executors (P3) — Schema-Konformität und Konflikterkennung sind automatisiert getestet. Der MCP-Sync-Schritt selbst (welcher Konnektor, welche Felder wie gemappt werden) ist nicht automatisiert testbar und bleibt manuelle Prüfung. Ein gemeldeter Konflikt wird NIE automatisch aufgelöst — Zweitkontrolle und Merge-Entscheidung bleiben Kanzleisache."
kontext_reads:
  - kanzlei.md
  - mandate/*.md
  - kontakte.md
kontext_writes:
  - mandate/*.md
  - kontakte.md
  - posteingang/*
  - export/*
---

# kontext-sync

> **Status: `beta`** — der Validierungspfad (Schema-Prüfung nach jedem Sync)
> und der `filesystem`-Referenzadapter (Pull/Push, Idempotenz,
> Konflikt-Handling) sind end-to-end durch automatisierte Tests abgedeckt
> (`tests/`). **Nicht** automatisiert abgedeckt: der eigentliche MCP-Sync
> gegen ein reales System (z. B. M365) — dafür gibt es keinen deterministisch
> testbaren Endpunkt in CI. `status: getestet` setzt zusätzlich eine
> händische Abnahme des kompletten Sync-Laufs (inkl. echtem MCP-Konnektor)
> durch den Maintainer voraus (Reifegrad-Leiter, CONVENTIONS.md).

## Zweck

Der Kontext-Layer (`kontext/`, siehe
[`core/context/README.md`](../../core/context/README.md)) ist die **einzige**
Schnittstelle der Skills zu Kanzlei-Wissen (D11). Dieser Querschnitts-Skill
hält `kontext/` mit der tatsächlichen Kanzlei-Software synchron — nie liest
oder schreibt ein anderer Skill die Kanzleisoftware direkt. Zwei Wege
dorthin, je nachdem was verfügbar ist:

1. **Vorhandener MCP-Konnektor** (z. B. der offizielle M365-MCP-Server für
   Mail/Kalender/Kontakte, D11a) — Claude ruft die Konnektor-Tools auf und
   schreibt das Ergebnis in `kontext/` nach dem dokumentierten Schema.
2. **`filesystem`-Referenzadapter** — wenn Kanzlei-Daten bereits als Dateien
   vorliegen (Export aus DATEV/Advoware/RA-MICRO o. ä.), siehe
   [`core/adapters/filesystem/README.md`](../../core/adapters/README.md).

Bewusst **ohne** „mcp" im Namen (D17: Funktion statt Implementierung) — der
Skill befüllt `kontext/`, unabhängig davon, welcher Anbindungsweg gerade
verfügbar ist.

## Eingaben (Datei-Kontrakt, P2)

| Eingabe | Pflicht | Format | Beschreibung |
|---|---|---|---|
| `kontext/`-Zielverzeichnis | ja | Verzeichnis | Nach dem Schema in [`core/context/README.md`](../../core/context/README.md). |
| Mapping (nur beim filesystem-Adapter) | ja, wenn Adapter genutzt | `.json` | Quelle-/Kontext-Dateipaare, siehe [`core/adapters/filesystem/README.md`](../../core/adapters/filesystem/README.md). |
| Manifest (nur beim filesystem-Adapter) | wird erzeugt/aktualisiert | `.json` | Hash-Verlauf für Idempotenz/Konflikterkennung. |

Vollständiges Schema-Kontrakt-Verzeichnis: [`schema/README.md`](schema/README.md).

## Ablauf

1. **Kanzlei-Daten nach `kontext/` holen (oder zurückschreiben)** — je nach
   verfügbarem Weg:

   - **MCP-Konnektor:** Claude ruft die verfügbaren Konnektor-Tools auf
     (z. B. Kalender-/Kontakt-/Mail-Abfragen des M365-MCP-Servers), bildet
     die Ergebnisse auf das `kontext/`-Schema ab (Mandats-Frontmatter,
     Abschnitte) und schreibt die Datei(en).
   - **filesystem-Adapter:**

     ```bash
     python3 ${CLAUDE_PLUGIN_ROOT}/core/adapters/filesystem/adapter.py pull \
       --quelle <externer-export-ordner> --kontext <kontext-verzeichnis> \
       --manifest <manifest.json> --mapping <mapping.json>
     ```

     (bzw. `push` für die Gegenrichtung). Der Adapter entscheidet
     Kopieren/Überspringen/Konflikt deterministisch (P3) — Claude liest nur
     den JSON-Report.

2. **Immer im Anschluss: Schema-Validierung** (kein Sync gilt als
   abgeschlossen, ohne dass dieser Schritt gelaufen ist):

   ```bash
   python3 ${CLAUDE_PLUGIN_ROOT}/core/context/validator.py --kontext <kontext-verzeichnis>
   ```

   Claude liest ausschließlich den erzeugten Report (`fehler[]`,
   `warnungen[]`) und übernimmt ihn unverändert — kein eigenes Ermessen über
   Schema-Konformität (P3).

3. **Bei Konflikt (Adapter-Exit 3) nie raten**: Claude präsentiert die
   gemeldeten `.conflict`-Dateien und den Report-Auszug und fragt die
   Kanzlei, welche Version gilt. Keine automatische Zusammenführung, keine
   Bevorzugung einer Seite.

4. **Optional als Folgeschritt**: Retention-Hinweis nach einem Sync, der
   Mandats-Beendigungen aktualisiert hat:

   ```bash
   python3 ${CLAUDE_PLUGIN_ROOT}/core/calc/retention/executor.py --kontext <kontext-verzeichnis>
   ```

## Output-Format

Zwei JSON-Reports, beide `quelle: "executor"` (P3):

- Adapter-Report (`ergebnisse[]`, `anzahl_konflikte`, `konflikte[]`) — siehe
  [`core/adapters/filesystem/README.md`](../../core/adapters/README.md).
- Validator-Report (`ok`, `fehler[]`, `warnungen[]`) — siehe
  [`core/context/README.md`](../../core/context/README.md).

Claude fasst beide für die Kanzlei in Klartext zusammen: was wurde
übernommen, was übersprungen (unverändert), was ist ein Konflikt, was meldet
der Validator als Schema-Fehler oder Warnung.

## Beispiele

### Beispiel 1 — sauberer Pull ohne Konflikt

Ein DATEV-Export liegt als Ordner vor, Mapping zeigt auf drei Mandate. Der
Adapter meldet drei `synchronisiert`-Einträge, keine Konflikte (Exit 0). Der
anschließende Validator-Lauf meldet `ok: true` — Claude bestätigt der
Kanzlei, dass `kontext/` aktuell ist.

### Beispiel 2 — Konflikt

Ein Mandats-File wurde sowohl in der Kanzleisoftware als auch händisch in
`kontext/mandate/2026-001.md` geändert. Der Adapter erkennt: beide Seiten
haben sich seit dem letzten Sync geändert → schreibt
`mandate/2026-001.md.conflict`, meldet den Konflikt, Exit 3. Claude zeigt
beide Versionen (Original + `.conflict`) an und fragt, welche gilt — **keine
automatische Entscheidung**.

### Beispiel 3 — Schema-Fehler nach Sync

Nach einem MCP-Sync fehlt in einem neu angelegten Mandats-File der
Abschnitt `## Nächste Frist`. Der Validator meldet den Fehler mit
`datei:zeile` (Exit 1) — Claude ergänzt den Abschnitt (Verweis auf die
offene Frist oder „Keine offene Frist") und lässt den Validator erneut
laufen, bis `ok: true`.

## Grenzen (bewusst)

- **Kein eigenes Merge-Werkzeug** — Konflikte werden erkannt, nie
  automatisch aufgelöst.
- **MCP-Konnektor-Mapping ist nicht in diesem Skill kodifiziert** — welche
  Konnektor-Felder auf welches `kontext/`-Feld abgebildet werden, entscheidet
  Claude je nach verfügbarem Konnektor; das ist der nicht automatisiert
  testbare Teil (siehe Status oben).
- **Keine Bewertung der Mandatsinhalte** — reine Synchronisation und
  Schema-Prüfung, keine inhaltliche Analyse.
