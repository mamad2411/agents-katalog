---
name: aktenkopf-extraktor
description: "Strukturiert eingehende Mandats-Dokumente (Anspruchsschreiben, Kündigung, Behördenpost) zu einem maschinenlesbaren Aktenkopf — Rubrum, Parteien, Datumsnennungen, Geldbeträge, Aktenzeichen — samt Lückenliste fehlender Pflichtangaben; ein Executor erzwingt Provenienz gegen Halluzination. Triggert bei Aktenanlage, Mandats-Intake, Dokument/Schreiben strukturieren, Aktenkopf erstellen."
status: beta
welle: 2
bereich: intake
rdg_einordnung: "Organisatorische Strukturierung und Extraktion eingehender Mandats-Dokumente in einen Aktenkopf; keine rechtliche Ersteinschätzung, keine Subsumtion, keine Fristberechnung. Erkannte Datumsnennungen sind Rohmaterial für die Aktenanlage, keine Rechtsdienstleistung."
daten_hinweis: "Mandantendaten im Input — nur über DSGVO-/BRAO-konformen Modellzugang (AWS-Bedrock-Pfad) verarbeiten; § 203 StGB beachten. Der Executor arbeitet rein lokal, ohne Netzwerkzugriff, und liest nur die übergebenen Dateien."
haftung: "Erkannte Fristen/Datumsnennungen sind bloße Hinweise, keine Fristenkontrolle und keine Fristberechnung — dafür ist ausschließlich der Skill fristenrechner als Zweitkontrolle zuständig. Die Vollständigkeit der Extraktion (insb. der Lückenliste) bleibt anwaltlich zu prüfen."
---

# aktenkopf-extraktor

> **Status: `beta`** — automatisierte Tests laufen grün in CI
> (`tests/test_aktenkopf_extraktor_executor.py`, 34 Fälle). Noch **nicht** händisch
> abgenommen —
> `status: getestet` vergibt erst der Maintainer nach eigener Prüfung (siehe
> [CONVENTIONS.md](https://github.com/eliasreiche/legal-ops-germany/blob/main/CONVENTIONS.md), Reifegrad-Leiter).

## Zweck

Strukturiert eingehende Mandats-Dokumente (Anspruchsschreiben, Kündigung,
behördliches Schreiben u. Ä.) zu einem maschinenlesbaren **Aktenkopf**:
Kurzrubrum, Sachverhalt, Parteien, erkannte **Datumsnennungen**, Geldbeträge,
fremde Aktenzeichen und — zentral — einer **Lückenliste** der für die
Aktenanlage noch fehlenden Pflichtangaben.

Die inhaltliche Extraktion macht **das Modell (Claude)** — es liest das
Dokument und füllt das Schema. Damit dabei nichts erfunden wird, prüft ein
deterministischer Executor die Ausgabe (P3 / Anti-Halluzination maschinell
erzwungen):

- **Schema-Konformität** des `aktenkopf.json` (Pflichtstruktur, ISO-Datumsformate),
- **Provenienz**: jeder kritische Wert (Datum, Geldbetrag, Aktenzeichen, IBAN,
  E-Mail, Telefonnummer) muss — nach definierter Normalisierung — **wörtlich in
  mindestens einer Quelldatei** vorkommen; die Fundstelle (Datei + Zeile) steht
  im Report. Nicht belegte Werte werden als `nicht_belegt` ausgewiesen,
- **Lücken-Disziplin**: ein leeres Pflichtfeld ist nur zulässig, wenn es
  explizit im `luecken`-Array steht — sonst Schema-Fehler.

> ⚠️ **Keine Fristberechnung, keine Fristenkontrolle.** Die `fristen_hinweise`
> sind bloß *erkannte Datumsnennungen* aus dem Text (mit vermuteter Bedeutung),
> **kein** berechnetes Fristende und keine Notfrist-Bewertung. Jede tatsächliche
> Fristberechnung läuft ausschließlich über den Skill
> [`fristenrechner`](../fristenrechner/SKILL.md)
> als deterministische Zweitkontrolle. Dieser Skill ersetzt keinen
> Fristenkalender.

**PDF/Scan ist out of scope.** Der Skill verarbeitet Text-/Markdown-Quellen.
Die Aufbereitung eingescannter Post (OCR, Klassifikation) übernimmt der Skill
`posteingang-ocr-verteilung` (Welle 4).

## Eingaben (Datei-Kontrakt, P2)

| Eingabe | Pflicht | Format | Beschreibung |
|---|---|---|---|
| Aktenkopf | ja | `.json` | Vom Modell nach Schema erzeugter Aktenkopf. Struktur: [`schema/README.md`](schema/README.md), Beispiel: [`schema/beispiel-aktenkopf.json`](schema/beispiel-aktenkopf.json). |
| Quelldokument(e) | ja | `.txt` / `.md`, UTF-8 | Das/die zugrunde liegende(n) Dokument(e). Mehrfach angebbar (`--quelle` je Datei). Beispiel: [`schema/beispiel-eingabe.md`](schema/beispiel-eingabe.md). |

Der Executor liest nur diese Dateien, kein Netzwerk, keine Datenbank.

## Ablauf

**Verbindlicher Arbeitsablauf (Audit 2026-07-15).** Eine händische Abnahme hat
gezeigt: Ein freihändig aus dem Gedächtnis erstelltes Aktenkopf-JSON produziert
zuverlässig Schema-Fehler — u. a. falsche Wurzel-Schlüssel (statt des
Schema-Objekts `aktenkopf` ein flacher Aufbau, statt `betraege` ein erfundenes
`geldbetraege`, statt `aktenzeichen_fremd` ein erfundenes `fremde_aktenzeichen`),
Enum-Verstöße (`Mandant_aktuell` statt `mandant`, `natürlich` statt
`natuerlich`) und fehlende Pflichtfelder bei `fristen_hinweise` (`datum_im_text`,
`originalschreibweise`, `vermutete_bedeutung`) — insgesamt 35 Fehler in einem
Testlauf. Die Provenienz-Prüfung selbst fing dabei zuverlässig einen nicht
belegten Wert ab. Deshalb sind die folgenden Schritte **verbindlich, kein
Freihand-Entwurf und kein One-Shot**:

1. **Claude kopiert [`schema/beispiel-aktenkopf.json`](schema/beispiel-aktenkopf.json)
   als Vorlage** und füllt sie aus dem/den Quelldokument(en) — ein
   Aktenkopf-JSON wird **nie** frei aus dem Gedächtnis aufgebaut. Wurzel-Schlüssel
   (`aktenkopf`, `parteien`, `fristen_hinweise`, `betraege`, `aktenzeichen_fremd`,
   `luecken`) und Enum-Werte (`rolle`: `mandant`/`gegner`/`sonstige`; `typ`:
   `natuerlich`/`juristisch`) werden **wörtlich** aus der Vorlage bzw.
   [`schema/README.md`](schema/README.md) übernommen — nie umformulieren, nie mit
   Umlauten oder abweichender Groß-/Kleinschreibung schreiben. Was nicht im Text
   steht, wird nicht ergänzt, sondern als Eintrag in `luecken` ausgewiesen (mit
   Begründung, warum die Angabe für die Aktenanlage nötig ist). Datumsnennungen
   kommen als `fristen_hinweise` mit wörtlichem `quelle_zitat` in den Aktenkopf,
   nie als berechnete Frist.

   **Verfahrensverlauf (Audit 2026-09-02, 200-Seiten-Akte):** Angaben, die
   sich im Lauf eines Verfahrens ändern können — Gericht, Aktenzeichen,
   Prozessbevollmächtigte, Anschriften — werden **nie aus der ersten Nennung**
   übernommen. Es gilt der **zeitlich letzte dokumentierte Stand** als
   aktuell; frühere Stände bleiben als Historie erhalten. Zeitlich heißt
   **nach Datum des jeweiligen Schriftsatzes/Beschlusses**, nicht nach
   Position im Dokument — Akten sind häufig rückwärts chronologisch sortiert.
   Dafür das gesamte Dokument nach Wechsel-Signalen durchsuchen, mindestens:
   „verwiesen", „Verweisung", „abgegeben", „Abgabe", „nunmehr zuständig",
   „neues Aktenzeichen", „bisheriges Aktenzeichen", „bestelle ich mich",
   „zeige ich an, dass", „Prozessbevollmächtigte", „Mandat niedergelegt",
   „Vertretung beendet", „neue Anschrift".
   - **Gericht und Aktenzeichen**: Jedes gerichtliche Aktenzeichen, das der
     Akte je zugeordnet war, wird ein eigener Eintrag in `aktenzeichen_fremd[]`
     — bei Verweisung an ein anderes Gericht **und** bei Az-Wechsel innerhalb
     derselben Instanz (Abgabe an andere Abteilung/Kammer, Trennung,
     Wiederaufnahme). `stelle` nennt Gericht **und** Status, genau **ein**
     Eintrag trägt „(aktuell)": z. B. „Amtsgericht Neubrandenburg (bis
     Verweisung an AG Neukölln)" / „Amtsgericht Neukölln (aktuell)". Der
     Eintrag mit „(aktuell)" ist der geltende Gerichtsstand.
   - **Prozessbevollmächtigte** (`vertreten_durch`): der **zuletzt** bestellte
     Vertreter der Partei — auch wenn die Partei anfangs unvertreten war.
     Bei Anwaltswechsel: „RA Neu (seit Schriftsatz vom TT.MM.JJJJ; zuvor RA
     Alt)". Nach Niederlegung ohne Nachfolger: `null` und die Niederlegung in
     `sachverhalt_kurz` vermerken.
   - **Anschrift**: die zuletzt mitgeteilte.
2. **Claude ruft den Executor auf** (kein eigenes Prüfen durch das Modell):

   ```bash
   python3 ${CLAUDE_PLUGIN_ROOT}/skills/aktenkopf-extraktor/executor.py \
     --aktenkopf <aktenkopf.json> \
     --quelle <dokument.md> [--quelle <weitere.txt> ...] \
     --output <report.json>
   ```

3. **Der Executor prüft deterministisch** (P3): Schema, Provenienz jedes
   kritischen Werts (belegt/`nicht_belegt` mit Fundstelle) und die
   Lücken-Disziplin. Exit-Code `0` = sauber, `1` = mindestens ein
   `nicht_belegt`-Wert und/oder Schema-Fehler, `2` = Eingabefehler.
4. **Bei `nicht_belegt` oder Schema-Fehler korrigiert Claude** den Aktenkopf —
   einen nicht belegten Wert entweder **streichen** (er stand nicht im Dokument)
   oder als **Lücke** ausweisen — nie erfinden; ein leeres Pflichtfeld mit einem
   `luecken`-Eintrag versehen — und ruft den Executor erneut auf. **Kein
   One-Shot**: Schritte 1–4 bilden eine Korrekturschleife (erstellen → prüfen →
   korrigieren → erneut prüfen), keinen Einmal-Check. Wiederholen, bis der
   Executor mit Exit-Code `0` sauber durchläuft.
5. **Claude stellt das Ergebnis in Markdown dar**: Aktenkopf, Parteien-Tabelle,
   bei gerichtlichen Aktenzeichen eine Zeile **Gericht/Az (aktuell)** mit der
   Historie darunter (frühere Gerichte/Az aus `aktenzeichen_fremd[]`),
   Frist-Hinweise **mit deutlichem Haftungshinweis** (erkannte Datumsnennungen,
   keine Fristenkontrolle; Fristberechnung nur über `fristenrechner`) und die
   Lückenliste. Jeder als `nicht_belegt` gemeldete Wert wird nie stillschweigend
   übernommen.

## Output-Format

JSON-Report nach [`schema/README.md`](schema/README.md), Beispiel:
[`schema/beispiel-report.json`](schema/beispiel-report.json) (erzeugt aus
[`schema/beispiel-aktenkopf.json`](schema/beispiel-aktenkopf.json) +
[`schema/beispiel-eingabe.md`](schema/beispiel-eingabe.md)). Kernfelder:
`schema_ok`, `schema_fehler[]`, `provenienz[]` (je Wert `status`, `fundstelle`,
`begruendung`), `luecken[]`, `zusammenfassung`.

Jeder Beleg-Zustand im Report stammt aus `executor.py`, nie vom Modell (P3).

## Beispiele

### Beispiel 1 — Anspruchsschreiben nach Verkehrsunfall (alles belegt)

Eingabe: [`schema/beispiel-eingabe.md`](schema/beispiel-eingabe.md) (fiktives
gegnerisches Anspruchsschreiben, Verkehrsunfall, mit Zahlungsfrist, mehreren
Beträgen, fremdem Aktenzeichen und Bankverbindung). Claude erzeugt daraus
[`schema/beispiel-aktenkopf.json`](schema/beispiel-aktenkopf.json); der Executor
belegt alle 11 kritischen Werte (Exit 0). Von Claude präsentiert:

**Aktenkopf** — Mustermann ./. Beispiel (Verkehrsunfall), Eingang 05.03.2026.

| Rolle | Name | Typ | Anschrift | vertreten durch |
|---|---|---|---|---|
| Mandant | Max Mustermann | natürlich | Musterweg 3, 20099 Hamburg | — |
| Gegner | Erika Beispiel | natürlich | *(Lücke)* | Dr. Petra Gegner |
| Sonstige | Dr. Gegner & Kollegen | juristisch | Musterallee 100, 20095 Hamburg | — |

**Frist-Hinweise** (⚠️ erkannte Datumsnennungen — **keine Fristberechnung**,
Zweitkontrolle über `fristenrechner`):

| Datum (im Text) | Vermutete Bedeutung |
|---|---|
| 20.03.2026 | Von der Gegenseite gesetzte Zahlungsfrist (außergerichtlich), keine gesetzliche Notfrist |
| 12.02.2026 | Unfalltag — möglicher Verjährungsbeginn, anwaltlich zu prüfen |

**Lücken für die Aktenanlage**: Anschrift der Gegnerin fehlt im Schreiben;
Telefon/E-Mail des Mandanten beim Erstkontakt zu erfragen.

### Beispiel 2 — erfundener Wert wird abgefangen

Trägt der Aktenkopf einen Betrag oder ein Datum, das **nicht** im Dokument
steht, meldet der Executor es als `nicht_belegt` (Exit 1) mit dem Hinweis „Wert
streichen oder als Lücke ausweisen". Claude übernimmt einen solchen Wert nie,
sondern streicht ihn oder führt ihn als Lücke — so wird die Anti-Halluzinations-
Regel maschinell erzwungen.

## Grenzen

- **Keine Fristberechnung / kein Fristende** — nur erkannte Datumsnennungen
  (siehe Haftungshinweis oben); Fristen ausschließlich über `fristenrechner`.
- **PDF/Scan** out of scope → `posteingang-ocr-verteilung` (Welle 4).
- **Provenienz ist ein Beleg-, kein Richtigkeitsnachweis**: `belegt` heißt nur,
  dass der Wert (nach Normalisierung) im Text vorkommt — nicht, dass er
  rechtlich zutrifft oder das Modell ihn dem richtigen Feld zugeordnet hat. Die
  Zuordnung (welche Partei, welche Bedeutung) bleibt anwaltlich zu prüfen.
- **Normalisierungsgrenzen**: Telefonnummern werden nur um Trennzeichen bereinigt
  verglichen (keine Ländervorwahl-Äquivalenz `+49` ↔ `0`); Datums-/Geldformate
  sind in [`schema/README.md`](schema/README.md) abschließend dokumentiert.
