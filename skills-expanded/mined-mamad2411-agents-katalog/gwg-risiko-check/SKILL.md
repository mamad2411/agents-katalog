---
name: gwg-risiko-check
description: "GwG-Risikoscoring eines Mandats anhand der Katalogfaktoren der Anlagen 1 und 2 GwG mit Dokumentations-Output für die interne Akte — offline, deterministisch, regelbasierter Klassifikationsvorschlag mit Fundstellen. Triggert bei Geldwäsche-Risiko, GwG-Prüfung, Risikoklassifizierung Mandat, Sorgfaltspflichten, § 10 GwG, Hochrisikoländer, FATF-Grauliste/Schwarzliste, EU-Hochrisiko-Drittstaaten. Die Bewertung bleibt beim Verpflichteten."
status: beta
welle: 2
bereich: compliance
rdg_einordnung: "Strukturierte Dokumentationshilfe zu gesetzlichen Katalogfaktoren (Anlagen 1/2 GwG) mit regelbasiertem Klassifikationsvorschlag; keine Rechtsdienstleistung — die Risikobewertung und die Maßnahmenentscheidung trifft der Verpflichtete (§ 10 Abs. 2 GwG)."
daten_hinweis: "KYC-/Mandatsdaten im Input — pseudonymisieren oder DSGVO-/BRAO-konformen Modellzugang nutzen (AWS-Bedrock-Pfad, § 203 StGB). Der Executor arbeitet rein lokal, ohne Netzwerkzugriff."
haftung: "Ersetzt keine GwG-Pflichtenprüfung; das Scoring ist ein Vorschlag zur Aktendokumentation, kein Verwaltungsakt-sicherer Nachweis. Zweitkontrolle und Bewertung bleiben Kanzleisache. Die Anlagen-1/2-Fundstellen sind Platzhalter und vor produktiver Nutzung gegen gesetze-im-internet.de zu prüfen. Die Hochrisiko-Länderliste ist am 2026-07-13 browser-verifiziert (EU-VO (EU) 2016/1675 + BaFin-Rundschreiben 07/2026 zu den FATF-Listen), ändert sich aber laufend (FATF-Plenum ca. Feb/Jun/Okt) — Quartals-Review erforderlich."
---

# gwg-risiko-check

> **Status: `beta`** — automatisierte Tests laufen grün in CI
> (`tests/test_gwg_rechner.py` + `tests/test_gwg_executor_cli.py`). Noch
> **nicht** händisch abgenommen: Die Katalog-Fundstellen der Anlagen 1/2 GwG
> sind Platzhalter und vor produktiver Nutzung gegen die aktuelle
> Gesetzesfassung zu prüfen. `status: getestet` wird erst nach dieser Prüfung
> durch den Maintainer gesetzt (siehe
> [CONVENTIONS.md](https://github.com/eliasreiche/legal-ops-germany/blob/main/CONVENTIONS.md), Reifegrad-Leiter).

**Hochrisiko-Länderliste — Quellen (✅ browser-verifiziert am 2026-07-13):**
Die Datei [`core/calc/gwg/hochrisiko_drittstaaten.json`](../../core/calc/gwg/hochrisiko_drittstaaten.json)
führt drei Listen zusammen:

- **EU-Hochrisiko-Drittstaaten** — Delegierte Verordnung (EU) 2016/1675 der
  Kommission, konsolidierte Fassung CELEX 02016R1675-20260129 (EUR-Lex,
  Anhang Abschnitte I–IV), Stand 2026-01-29. Rechtsanker § 15 Abs. 3 Nr. 2
  GwG — ein Treffer ist ein **gesetzlicher** Trigger für verstärkte
  Sorgfaltspflichten (mindestens § 15 Abs. 5 GwG).
- **FATF-Schwarzliste** („High-Risk Jurisdictions subject to a Call for
  Action") und **FATF-Grauliste** („Jurisdictions under Increased
  Monitoring") — FATF-Erklärungen/-Bericht vom 19.06.2026, referenziert über
  BaFin-Rundschreiben 07/2026 (GW) vom 13.07.2026 (die FATF-Primärseite
  fatf-gafi.org blockt automatisierte Zugriffe, daher die amtliche deutsche
  Sekundärquelle). Ein reiner FATF-Treffer **ohne** EU-Listung ist **keine**
  Gesetzespflicht nach § 15 Abs. 3 Nr. 2 GwG (der nur auf die EU-Liste
  verweist) — siehe Gewichtungs-Entscheidung unten.

**Pflege-Hinweis:** Quartals-Review nach jedem FATF-Plenum (ca.
Februar/Juni/Oktober) sowie bei neuen EU-Änderungsverordnungen zu
2016/1675. Das Alter der Liste (`abgerufen_am`) wird **bei jedem Lauf** gegen
die Schwellen geprüft und als `warnungen`-Eintrag in den Report geschrieben
(ab 4 Monaten; ab 12 Monaten als „überfällig") — zusätzlich auf stderr. Der
CI-Test schlägt ab 12 Monaten hart fehl
(`tests/test_gwg_rechner.py::test_gwg_hochrisiko_liste_ist_nicht_ueberfaellig`).

## Zweck

GwG-Risikoscoring eines Mandats anhand der Katalogfaktoren nach den Anlagen 1
und 2 GwG mit einem Dokumentations-Output für die interne Akte — vollständig
offline und deterministisch. Das Ergebnis ist ein **regelbasierter
Klassifikationsvorschlag** (keine numerischen Gewichts-Scores), der die
angewandten Faktoren mit exakter Fundstelle und die anwendbaren
Sorgfaltspflichten benennt. Die **Bewertung selbst trifft der Verpflichtete**
(risikobasierter Ansatz, § 10 Abs. 2 GwG).

## Eingaben (Datei-Kontrakt, P2)

| Eingabe | Pflicht | Format | Beschreibung |
|---|---|---|---|
| Mandats-Fragebogen | ja | `.json` | Strukturierter Fragebogen zum Mandat — siehe [`schema/README.md`](schema/README.md) und [`schema/beispiel-mandat.json`](schema/beispiel-mandat.json). Fehlende Felder = `unklar` (nie geraten). |

Die Katalogfaktoren (Fundstelle + Paraphrase) liegen als Daten in
[`core/calc/gwg/anlage1.json`](../../core/calc/gwg/anlage1.json),
[`core/calc/gwg/anlage2.json`](../../core/calc/gwg/anlage2.json) und
[`core/calc/gwg/hochrisiko_drittstaaten.json`](../../core/calc/gwg/hochrisiko_drittstaaten.json).

> ⚠️ **Anti-Halluzination.** Die Faktoren sind **Paraphrasen** mit exakter
> Fundstelle (z. B. „Anlage 2 Nr. 1 Buchst. e GwG"), **kein** Wortlaut-Zitat.
> Die Buchstaben-Zuordnung der Anlagen und die Zusammensetzung der
> Hochrisiko-Länderliste (Delegierte Verordnung (EU) 2016/1675) ändern sich und
> sind vor produktiver Nutzung gegen gesetze-im-internet.de bzw. die aktuelle
> EU-Fassung zu prüfen. Jede Norm-Fundstelle im Output trägt einen
> 3-Zustands-Marker.

## Ablauf

1. **Claude füllt den Fragebogen** ausschließlich aus dem, was Nutzer oder Akte
   hergeben. Was nicht belegt ist, bleibt `unklar` — **nie raten** (P-Anti-
   Halluzination). Ergebnis: eine Mandatsdatei nach
   [`schema/README.md`](schema/README.md). Bei juristischen Personen und
   trust-ähnlichen Strukturen gehört dazu die Frage nach Sitz/Wohnsitz **und
   Staatsangehörigkeit der wirtschaftlich Berechtigten**
   (`wirtschaftlich_berechtigte_laender`, Mehrzahl möglich) — ohne sie prüft
   das Länder-Gate nur den Mandantensitz, und der Report weist das als Lücke
   aus.

2. **Der Executor rechnet und klassifiziert** (kein eigenes Scoring durch das
   Modell, P3):

   ```bash
   python3 ${CLAUDE_PLUGIN_ROOT}/skills/gwg-risiko-check/executor.py \
     --mandat <mandat.json> \
     [--output <report.json>] \
     [--heute <JJJJ-MM-TT>]
   ```

   Der regelbasierte Rechner ([`core/calc/gwg/rechner.py`](../../core/calc/gwg/rechner.py))
   entscheidet über die erste greifende Regel: Anwendbarkeits-Gate
   (§ 2 Abs. 1 Nr. 10 GwG) → kritische Lücken → § 15 (PEP/Hochrisiko-Drittstaat)
   → nur Anlage-1-Faktoren → sonst. Das Länder-Gate wertet dabei
   Mandantensitz **und** alle angegebenen Länder der wirtschaftlich
   Berechtigten aus; das risikoreichste Land entscheidet. Claude liest **nur**
   den erzeugten Report und übernimmt Status, Faktoren und Fundstellen
   unverändert.

   **Frische-Gate (Muster gwg-live-screening):** `--heute` ist das Bezugsdatum
   (Default: Systemdatum, nur für Tests zu setzen). Ist die hinterlegte
   Hochrisiko-Länderliste älter als 4 bzw. 12 Monate, steht das im Report unter
   `warnungen` und auf stderr; der Report wird trotzdem erzeugt (Exit 0).
   Claude gibt jede `warnungen`-Zeile in der Akten-Dokumentation wieder.

3. **Claude rendert den Report als Akten-Dokumentation** (Markdown):
   Anwendbarkeit, Faktoren-Tabelle mit Fundstellen (jede mit ihrem
   3-Zustands-Marker), Klassifikationsvorschlag mit Begründung, Pflichten-
   Hinweise (§§ 10/14/15/43 GwG), Lücken und `warnungen`. Bei geografischen
   Faktoren immer die `herkunft` mitschreiben (Mandantensitz vs. wirtschaftlich
   Berechtigter). Jeder Zahlen-/Status-/Fundstellenwert stammt aus dem Report,
   nicht aus dem Modell.

4. **Zitat-Kontrolle** als letzter Schritt: Die §-Zitate der gerenderten
   Markdown-Doku sind gegen die mitgelieferte Registry
   [`schema/quellen-registry.json`](schema/quellen-registry.json) abzugleichen,
   damit sie nicht unmarkiert bleiben. Die Anlagen-Fundstellen sind kein
   §-Zitat; sie behalten ihren ⚠️-Marker und gehören zur händischen Abnahme.

## Output-Format

JSON-Report nach [`schema/README.md`](schema/README.md), Beispiel:
[`schema/beispiel-report.json`](schema/beispiel-report.json) (erzeugt aus
[`schema/beispiel-mandat.json`](schema/beispiel-mandat.json)).

Der Klassifikationsvorschlag ist einer von:
`nicht_verpflichtet`, `unvollstaendig`, `niedrig`, `mittel`, `hoch`. Bei
`nicht_verpflichtet`/`unvollstaendig` wird **bewusst keine Risikoklasse**
vergeben. Jeder Wert trägt `quelle: "executor"` (P3).

## Beispiele

### Beispiel 1 — mittleres Risiko (allgemeine Sorgfaltspflichten)

Ein Immobilienkauf-Mandat einer deutschen GmbH, wirtschaftlich Berechtigter
geklärt, kein PEP, aber bargeldintensiv. Der Executor liefert
`klassifikationsvorschlag: "mittel"` mit dem Faktor „Anlage 2 Nr. 1 Buchst. e
GwG" (bargeldintensiv) und dem Hinweis auf § 10 GwG
([`schema/beispiel-report.json`](schema/beispiel-report.json)).

### Beispiel 2 — hohes Risiko (PEP)

Ist im Fragebogen `pep: "ja"` gesetzt, greift Regel 2: Ergebnis `hoch` mit dem
Faktor „§ 15 Abs. 3 Nr. 1 GwG" und dem Pflichten-Hinweis auf die verstärkten
Sorgfaltspflichten (§ 15 GwG). Bei `sitz_land` in der EU-Hochrisiko-Liste greift
dieselbe Regel über „Anlage 2 Nr. 3 Buchst. a GwG" / § 15 Abs. 3 Nr. 2 GwG
(gesetzlicher Trigger); bei Nordkorea/Iran zusätzlich der Hinweis auf die
BaFin-Allgemeinverfügung. Der Länder-Treffer wird immer mit dem Vorbehalt
„Listen ändern sich laufend — Stand prüfen" gekennzeichnet, und der Report
weist im Feld `laender_listen_treffer` aus, welche der drei Listen (EU,
FATF-schwarz, FATF-grau) im Detail getroffen haben.

### Beispiel 3 — nicht verpflichtet

Ist `kataloggeschaeft: "keins"`, ist der Rechtsanwalt insoweit kein
Verpflichteter (§ 2 Abs. 1 Nr. 10 GwG): Ergebnis `nicht_verpflichtet`, keine
Risikoklasse, mit dem Vorbehalt „Einordnung prüfen".

### Beispiel 4 — hoch, aber Haus-Einstufung (nur FATF-Grauliste)

Ist `sitz_land` z. B. `KW` (Kuwait) — nur auf der FATF-Grauliste, nicht auf der
EU-Liste —, liefert der Rechner ebenfalls `hoch` (Gewichtungs-Entscheidung:
jeder Listen-Treffer löst `hoch` aus), aber **ohne** das Anlage-2-/§-15-Zitat.
Stattdessen trägt der Faktor die `id: "haus_fatf_listen_treffer"` mit
`fundstelle: "Hausrichtlinie (keine GwG-Norm)"` und der
Pflichten-Hinweis macht explizit klar: keine unmittelbare Gesetzespflicht,
konservative Haus-Einstufung nach BaFin-Rundschreiben 07/2026. Ist das Land
zugleich EU-Mitgliedstaat (z. B. Bulgarien), ergänzt ein Vorbehalt, dass es
begrifflich schon kein „Drittstaat" i. S. d. § 15 Abs. 3 Nr. 2 GwG sein kann.

### Beispiel 5 — EU-Holding mit Hochrisiko-UBO (Länder-Gate greift über den wirtschaftlich Berechtigten)

Eine Ltd. mit `sitz_land: "CY"` (EU-Mitgliedstaat) und
`wirtschaftlich_berechtigte_laender: ["RU"]` ergibt `hoch`: Russland steht auf
der EU-Hochrisiko-Liste, der Treffer ist ein gesetzlicher § 15-Abs.-3-Nr.-2-
Trigger, auch wenn der Mandantensitz in der EU liegt. `laender_listen_treffer`
weist `herkunft: "Sitz/Staatsangehörigkeit des wirtschaftlich Berechtigten"`
aus. Ohne das Feld bliebe es (wie vor der Ergänzung) bei `mittel` — der Report
führt die fehlende Angabe dann als Lücke.

## Gewichtungs-Entscheidung: alle drei Listen lösen `hoch` aus (Maintainer, konservativ)

Ein Treffer auf **jeder** der drei hinterlegten Listen (EU-Hochrisiko,
FATF-Schwarzliste, FATF-Grauliste) führt in diesem Skill zur Klassifikation
`hoch` — auch dann, wenn nur die FATF-Grauliste greift und **keine**
gesetzliche Pflicht nach § 15 Abs. 3 Nr. 2 GwG besteht (der ausschließlich auf
die EU-Liste verweist). Das ist eine bewusst konservative Haus-Praxis, keine
Behauptung einer Gesetzespflicht. Damit die Unterscheidung nicht verloren
geht, weist der Report bei jedem Länder-Treffer im Feld
`laender_listen_treffer` aus, welche Liste(n) getroffen haben, und die
Pflichten-Hinweise unterscheiden zwischen echtem § 15-GwG-Tatbestand (EU-
Listung oder PEP) und reiner Haus-Einstufung (nur FATF, keine EU-Listung) —
Details im Docstring von
[`core/calc/gwg/rechner.py`](../../core/calc/gwg/rechner.py).

## Grenzen (bewusst)

- **Kein Rechtsrat, keine Bewertung** — nur Dokumentationshilfe; die
  Risikobewertung trifft der Verpflichtete (§ 10 Abs. 2 GwG).
- **Anlagen-1/2-Fundstellen sind Platzhalter** — vor produktiver Nutzung
  gegen die aktuelle Gesetzesfassung zu prüfen (Reifegrad `getestet`). Die
  Hochrisiko-Länderliste ist am 2026-07-13 browser-verifiziert, ändert sich
  aber laufend — Quartals-Review nach FATF-Plenum Pflicht.
- **FATF-Grauliste-Treffer ohne EU-Listung sind keine Gesetzespflicht** —
  die Klassifikation `hoch` ist dort eine konservative Haus-Einstufung
  dieses Skills, kein Verwaltungsakt-sicherer Nachweis einer § 15-GwG-Pflicht.
- **Keine PEP-Ermittlung, kein Sanktionslisten-Abgleich, keine
  Identifizierung** — dafür ist der Live-Screening-Pfad bzw. eine eigene
  Prüfung nötig.
- **Der Länderbezug des wirtschaftlich Berechtigten wird nicht ermittelt,
  sondern eingegeben** — der Skill prüft nur die angegebenen Länder gegen die
  Listen; Beteiligungsketten, Kontrollverhältnisse und Zwischengesellschaften
  bleiben Sache der Identifizierung nach § 10 Abs. 1 Nr. 2 GwG. Fehlt die
  Angabe, ist das eine Lücke im Report, keine Entwarnung.
