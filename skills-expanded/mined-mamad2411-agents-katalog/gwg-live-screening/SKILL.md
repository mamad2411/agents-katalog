---
name: gwg-live-screening
description: "Screent Parteinamen gegen offizielle EU-/UN-Sanktionslisten (lokale XML-Dateien, Matching-Stufen S1–S4) und dokumentiert Treffer, mögliche Treffer UND Nicht-Treffer (negative clearance). Triggert bei Sanktionslisten-Abgleich, Embargo-Prüfung, GwG-Screening, Sanktionsprüfung vor Mandatsannahme. Maßnahmen bei Treffern entscheidet der Verpflichtete."
status: beta
welle: 4
bereich: compliance
rdg_einordnung: "Organisatorischer Abgleich gegen öffentliche Pflichtlisten als Rechercheunterstützung; keine Rechtsdienstleistung. Die Bewertung eines Treffers und jede Maßnahme (z. B. Verdachtsmeldung § 43 GwG, Bereitstellungsverbot nach EU-Sanktionsrecht) trifft der Verpflichtete."
daten_hinweis: "Nur Parteinamen (ggf. Typ) gehen in den Abgleich; die Listen sind öffentlich. Namen sind personenbezogene Daten — lokal verarbeiten, nicht persistieren, § 203 StGB / DSGVO beachten. Der Executor arbeitet rein offline, kein Netzwerkzugriff."
haftung: "Listenstand ist datiert zu dokumentieren (Frische-Gate erzwingt Generierungs- + Abrufdatum je Liste). Kein Treffer ist kein Freibrief; falsch-negative Treffer durch Transliteration nicht-lateinischer Schreibweisen sind möglich — kein abschließender Nachweis. Zweitkontrolle und Maßnahmenentscheidung bleiben Kanzleisache."
---

# gwg-live-screening

> **Status: `beta`** — automatisierte Tests laufen grün in CI (`tests/`:
> Parser gegen fiktive EU-/UN-Fixtures, Match-Stufen S1–S4, Frische-Gate,
> CLI-Adversarialfälle, Abruf-URL-Format). Noch **nicht** händisch abgenommen
> und **nicht** gegen die echten Listen produktiv geprüft — `status: getestet`
> vergibt erst der Maintainer nach eigener Prüfung (siehe
> [CONVENTIONS.md](https://github.com/eliasreiche/legal-ops-germany/blob/main/CONVENTIONS.md),
> Reifegrad-Leiter). Die §-Zitate unten tragen den Marker ⚠️ (nicht gegen
> gesetze-im-internet.de geprüft).

## Zweck

Screent Parteinamen (natürliche und juristische Personen) gegen zwei
offizielle, öffentlich abrufbare Sanktionslisten und erzeugt einen
Dokumentations-Report für die Akte:

- **EU-Konsolidierte Finanzsanktionsliste** (FSF „full file", XML-Export,
  webgate.ec.europa.eu),
- **UN Security Council Consolidated List** (XML, scsanctions.un.org).

Der Abgleich unterstützt die organisatorische Sanktions-/Embargo-Prüfung
(u. a. im Rahmen der GwG-Sorgfaltspflichten, § 10 GwG ⚠️, und des
EU-Sanktionsrechts) — er **ersetzt sie nicht**: der Executor liefert
Kandidaten, die Bewertung und jede Maßnahme bleibt beim Verpflichteten.

**Abgrenzung zum Nachbar-Skill** [`gwg-risiko-check`](../gwg-risiko-check/SKILL.md):
jener klassifiziert das **Länderrisiko** eines Mandats anhand von Länderlisten
(EU-Hochrisiko/FATF); dieser Skill screent **konkrete Personen/Organisationen**
gegen **Sanktionslisten**. Zwei verschiedene Prüfungen.

## Eingaben (Datei-Kontrakt, P2)

| Eingabe | Pflicht | Format | Beschreibung |
|---|---|---|---|
| Parteien | ja (`--parteien`) | `.csv` (Pflichtspalte `name`) oder `.json` | Zu prüfende Personen/Organisationen. Vollständiger Kontrakt: [`schema/README.md`](schema/README.md), Beispiel: [`schema/beispiel-parteien.json`](schema/beispiel-parteien.json). |
| Listen-Verzeichnis | ja (`--listen-verzeichnis`) | Verzeichnis mit `*.xml` + `abruf-meta.json` | Lokale Listen-Dateien (EU-FSF/UN, Format automatisch erkannt) und die vom Abruf-Skript geschriebene Metadatei mit `abgerufen_am` je Liste. |

Der Executor **liest** nur — keine Persistierung, kein Netzwerkzugriff.

## Ablauf

1. **Listen beschaffen (getrennt vom Screening).** Der Abruf läuft über das
   klar abgetrennte Skript
   [`core/adapters/sanktionslisten/abruf.py`](../../core/adapters/sanktionslisten/abruf.py)
   (nur Stdlib `urllib`) — nie im Screening-Executor (P3-Deterministik). Es
   lädt die zwei offiziellen URLs in ein Zielverzeichnis und schreibt
   `abruf-meta.json` mit `abgerufen_am`. Alternativ manuell:

   ```bash
   # UN (frei abrufbar)
   curl -L -o listen/un-consolidated.xml \
     https://scsanctions.un.org/resources/xml/en/consolidated.xml
   # EU-FSF „full file" (öffentlicher Token-Parameter laut EU-Doku)
   curl -L -o listen/eu-fsf.xml \
     "https://webgate.ec.europa.eu/fsd/fsf/public/files/xmlFullSanctionsList_1_1/content?token=<oeffentlicher-token>"
   ```

   Bei manuellem Download muss `abruf-meta.json` von Hand das `abgerufen_am`
   je Datei tragen, sonst greift das Frische-Gate (Schritt 3).

2. **Claude erstellt die Parteien-Datei** nach dem Kontrakt in
   [`schema/README.md`](schema/README.md), ausschließlich aus dem, was Nutzer
   oder Akte hergeben — nie Namen erfinden (Anti-Halluzination).

3. **Claude ruft den Executor auf** (kein eigenes Namensvergleichen durch das
   Modell, P3):

   ```bash
   python3 ${CLAUDE_PLUGIN_ROOT}/skills/gwg-live-screening/executor.py \
     --parteien <parteien.csv|.json> \
     --listen-verzeichnis <listen-verzeichnis> \
     [--output <report.json>] \
     [--schwelle-moeglich <float, Default 0.80>]
   ```

   **Frische-Gate (D19-Muster):** Je Liste müssen Generierungsdatum (aus dem
   XML) UND `abgerufen_am` (aus `abruf-meta.json`) vorliegen; fehlt eines,
   bricht der Executor mit **Exit 3** ab und erzeugt **keinen** Report. Ist
   eine Liste älter als 7 Tage, trägt der Report eine Warnung.

4. **Der Executor entscheidet Stufe und Score deterministisch** (P3), über die
   wiederverwendbare Bibliothek [`core/calc/matching`](../../core/calc/matching/):
   S1 exakt / S2 Token / S3 Kölner Phonetik / S4 Fuzzy ≥ Schwelle — jeweils
   gegen Primärname UND alle Aliase jedes Listeneintrags. Kategorien
   `treffer` (S1/S2), `moeglicher_treffer` (S3/S4), `kein_treffer`. Claude
   liest ausschließlich den JSON-Report und übernimmt `stufe`, `score`,
   `listen_referenz` und `begruendung` unverändert.

5. **Claude rendert den Report als Akten-Dokumentation** (Markdown): je Partei
   das Ergebnis (Treffer/möglicher Treffer/kein Treffer), bei Treffern die
   Liste, Fundstelle (`listen_referenz`, `programm`), Match-Stufe, den
   getroffenen Namen (Primär oder Alias) und ggf. Geburtsdatum. Dabei immer:
   - die Listen-Frische ausweisen (Generierungs- + Abrufdatum je Liste) und
     jede `warnung_veraltet` sichtbar machen;
   - `treffer` und `moeglicher_treffer` optisch unterscheiden (z. B. ✅ / ⚠️);
   - bei **jedem** Treffer/möglichen Treffer klarstellen, dass die Bewertung
     und jede Maßnahme (Verdachtsmeldung § 43 GwG ⚠️, Bereitstellungsverbot
     nach EU-Sanktionsrecht ⚠️) beim Verpflichteten liegt — der Report liefert
     Kandidaten, keine Entscheidung;
   - **Nicht-Treffer ausdrücklich dokumentieren** (negative clearance ist der
     Hauptzweck der GwG-Dokumentation), aber „kein Treffer ist kein Freibrief"
     anbringen (Transliterations-/Schreibweisen-Grenze, siehe `haftung`);
   - erwähnen, dass der Abgleich vollständig lokal/offline erfolgte.

6. Bei **Exit 2** (Eingabefehler: Datei/Verzeichnis fehlt, Pflichtspalte
   fehlt, kaputtes XML/JSON, unbekannte XML-Wurzel, Schwelle außerhalb
   `[0,1]`) und **Exit 3** (Frische-Gate) gibt Claude die Fehlermeldung wieder
   und korrigiert die Eingabe bzw. löst einen frischen Abruf aus — es rät kein
   Ergebnis.

## Output-Format

JSON-Report nach [`schema/README.md`](schema/README.md#ausgabe-json-report),
Beispiel: [`schema/beispiel-report.json`](schema/beispiel-report.json)
(tatsächlich vom Executor erzeugt). Jeder Zahlen-/Datums-/Score-Wert stammt
aus dem Executor bzw. Parser (P3), nie vom Modell.

## Beispiel

Eingabe: [`schema/beispiel-parteien.json`](schema/beispiel-parteien.json)
(4 Parteien) gegen die Fixtures unter [`tests/fixtures/`](tests/fixtures/)
(fiktive EU-FSF- und UN-Ausschnitte). Von Claude präsentiertes Ergebnis (aus
dem Report übernommen):

| Partei | Ergebnis | Liste / Fundstelle | Stufe | Getroffener Name |
|---|---|---|---|---|
| Max Mustermann | ✅ treffer | EU-FSF / EU.9001.99 (MUSTER-PROG) | S1 | Max Mustermann (Primär) |
| Musterbau AG | ✅ treffer | UN / MUe.9101 (MUSTER) | S1 | Musterbau AG (Alias) |
| Maximilian Mustermann | ⚠️ moeglicher_treffer | EU-FSF / EU.9001.99 | S3 (Kölner Phonetik) | Maximilian Mustremann (Alias) |
| Johanna Sauber | — kein_treffer | — | — | — (negative clearance dokumentiert) |

**Hinweis:** „Max Mustermann" erzeugt zusätzlich einen `moeglicher_treffer`
(S4, Score 0.83) gegen den UN-Alias „Hans Mustermann" — ein bewusst in Kauf
genommener falsch-positiver Kandidat der konservativen Schwelle 0.80, der
händisch zu prüfen ist. Die Bewertung jedes Treffers und jede Maßnahme
(§ 43 GwG ⚠️ / EU-Bereitstellungsverbot ⚠️) trifft der Verpflichtete.

## Bewusst NICHT in v1 (Grenzen / Zurückstellungen)

- **Nur EU-FSF + UN.** **OFAC** (US) und **UK/OFSI**-Listen sind
  zurückgestellt (anderes Schema, Lizenz-/Pflegefragen).
- **Kein PEP-Screening** — belastbare PEP-Listen gibt es nur aus kommerziellen
  Quellen; kein offener Pflicht-Feed.
- **Kein Transparenzregister-Abgleich** — produktiv nur über Reseller
  zugänglich.
- **Nur lateinische Schreibweisen belastbar.** Nicht-lateinische
  Originalschreibweisen (arab./kyrill.) werden zwar geparst, aber das Matching
  (Kölner Phonetik/Fuzzy) ist dafür nicht ausgelegt — Transliterations-Grenze
  (steht auch im `haftung`-Feld).
- **Keine Maßnahmen-Automatik.** Verdachtsmeldung (§ 43 GwG ⚠️),
  Bereitstellungs-/Verfügungsverbot (EU-Sanktionsrecht ⚠️) und jede weitere
  Konsequenz entscheidet und dokumentiert der Verpflichtete.
- **Ein `kein_treffer` ist kein Freibrief** — Schreibvarianten jenseits der
  Stufen S1–S4 bleiben ggf. unentdeckt; die abschließende Prüfung bleibt
  Kanzleipflicht.
