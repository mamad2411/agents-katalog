---
name: fristenrechner
description: "Berechnet gerichtliche und prozessuale Fristen nach §§ 186–193 BGB und § 222 ZPO deterministisch mit nachvollziehbarer Rechenkette (Fristbeginn, Ende, Wochenend-/Feiertagsverschiebung je Bundesland). Triggert bei Fristberechnung, Einspruchsfrist, Berufungs-/Beschwerde-/Revisionsfrist, Notfrist, Fristende, Zustelldatum plus Fristart, Feiertagsverschiebung. Strikt Zweitkontrolle, ersetzt keine Fristenkontrolle der Kanzlei."
status: getestet
haendisch_getestet: 2026-07-15
welle: 1
bereich: fristen-termine
rdg_einordnung: "Rechnerische Fristermittlung nach §§ 186–193 BGB / § 222 ZPO ohne Subsumtion des Einzelfalls; die rechtliche Einordnung des fristauslösenden Ereignisses (wirksame Zustellung, richtige Fristart, Fristbeginn-Alternativen) bleibt beim Anwalt."
daten_hinweis: "Die Berechnung benötigt nur Datum, Fristart und Bundesland — keine Mandantendaten. Wird beim Export ein Aktenzeichen/eine Bezeichnung mitgegeben, kann die Export-Datei (.ics/.csv) diese tragen — dann wie eine Akte behandeln (Speicherperimeter D10). Beide Executors arbeiten rein lokal, ohne Netzwerkzugriff."
haftung: "Zweitkontrolle, zwingend: Der Rechner ist das zweite Augenpaar, nie das erste — er ersetzt keine Fristenkontrolle der Kanzlei (Fristenkalender, Vier-Augen-Prinzip, anwaltliche Endkontrolle bleiben unberührt). Bei Notfristen und teilgebietlichen Feiertagen gilt das doppelt. Der Kalender-Export ist ein technischer Übernahmehelfer; Import und Kontrolle im Zielsystem verantwortet die Kanzlei."
---

# fristenrechner

> **Status: `getestet`** — automatisierte Tests laufen grün in CI (`tests/`,
> inkl. Orakel-Fälle gegen borghei `legal_calc`); händische Live-Abnahme durch
> den Maintainer am 2026-07-15 (Real-World-Test: Berufungs- und
> Berufungsbegründungsfrist aus zugestelltem LG-Urteil, Rechenkette und
> iCal-/CSV-Export verifiziert). Keine Produktions-Garantie — Zweitkontrolle
> bleibt Pflicht (siehe [CONVENTIONS.md](https://github.com/eliasreiche/legal-ops-germany/blob/main/CONVENTIONS.md), Reifegrad-Leiter).

## Zweck

Berechnet Fristen nach §§ 186–193 BGB und § 222 ZPO deterministisch über den
Executor [`core/calc/fristen/`](../../core/calc/fristen/) — mit
vollständiger, nachvollziehbarer **Rechenkette**: Fristbeginn (§ 187 BGB),
rechnerisches Ende (§ 188 BGB, inkl. Monatsende-Fall des Abs. 3), jede
Verschiebung wegen Sonnabend/Sonntag/Feiertag (§ 193 BGB / § 222 Abs. 2 ZPO)
einzeln mit Grund und Norm. Die Feiertage des Fristende-Orts liefert
[`core/calc/feiertage/`](../../core/calc/feiertage/) (alle 16
Bundesländer, berechnet für beliebige Jahre, teilgebietliche Feiertage ehrlich
gekennzeichnet).

**Zwei Stufen in einem Skill: berechnen → exportieren.** Unmittelbar nach der
Berechnung erzeugt der Skill aus dem Report einen Kalender-/Docketing-Export
(iCal `.ics` / CSV) über den zweiten Executor
[`core/calc/fristen/kalender_executor.py`](../../core/calc/fristen/kalender_executor.py)
— zum Import in Fristenkalender oder Kanzleisoftware. Der Export ist
deterministisch aus dem Report abgeleitet und **idempotent**: dieselbe Frist
ergibt denselben Export (kein Duplikat beim Re-Import); erst eine **Korrektur**
der Frist erzeugt einen neuen Export (neue `UID`). Der Export wird also einmal
nach der Berechnung erstellt und nur bei einer Korrektur neu.

**Positionierung: strikt Zweitkontrolle.** Der Rechner ersetzt keine
Fristenkontrolle der Kanzlei — er ist das zweite Augenpaar neben
Fristenkalender und Vier-Augen-Prinzip. Ein abweichendes Ergebnis ist ein
Anlass zur Prüfung, nie eine Freigabe. Auch der Export ist ein technischer
Übernahmehelfer; Import und Fristenkontrolle im Zielsystem verantwortet die
Kanzlei.

**Deterministik-Grenze (P3):** Claude rechnet nie selbst — kein Kopfrechnen,
kein Datums-Schätzen, auch nicht bei „einfachen" Fristen. Jeder Datumswert in
der Antwort stammt unverändert aus dem Executor-Report.

## Eingaben (Datei-Kontrakt, P2)

| Eingabe | Pflicht | Format | Beschreibung |
|---|---|---|---|
| Fristanfrage | ja | `.json` | `ereignis_datum`, `fristart` (Katalog-id) **oder** `dauer`+`einheit`, optional `fristtyp` (`ereignis`/`beginn`), `bundesland` (Pflicht). Schema: [`schema/README.md`](schema/README.md), Beispiele: [`schema/beispiel-eingabe.json`](schema/beispiel-eingabe.json), [`schema/beispiel-eingabe-frei.json`](schema/beispiel-eingabe-frei.json). |

Vordefinierte Fristarten (Berufung § 517 ZPO, Berufungsbegründung § 520 Abs. 2
ZPO, Einspruch gegen Versäumnisurteil § 339 ZPO, Widerspruch gegen Mahnbescheid
§§ 692, 694 ZPO, Revision/Revisionsbegründung §§ 548, 551 ZPO, Anhörungsrüge
§ 321a ZPO, Wiedereinsetzung § 234 ZPO) liegen als Daten im
[Fristarten-Katalog](../../core/calc/fristen/fristarten.json) —
Übersicht in [`schema/README.md`](schema/README.md).

Das `bundesland` ist Pflicht, weil § 193 BGB auf die Feiertage am
**Fristende-Ort** abstellt (bei gerichtlichen Fristen: Sitz des Gerichts).
Nennt der Nutzer kein Bundesland, fragt Claude nach — nie ein Bundesland
annehmen oder „bundesweit" rechnen.

## Ablauf

1. **Claude schreibt die Fristanfrage als JSON-Datei** (nach
   [`schema/README.md`](schema/README.md)). Fehlende Pflichtangaben
   (Ereignisdatum, Fristart bzw. Dauer, Bundesland) werden beim Nutzer
   erfragt, nie ergänzt (Anti-Halluzination).
2. **Claude ruft den Executor auf** (kein eigenes Rechnen durch das Modell):

   ```bash
   python3 ${CLAUDE_PLUGIN_ROOT}/core/calc/fristen/executor.py \
     --input <anfrage.json> \
     --output <report.json>
   ```

3. **Der Executor entscheidet jedes Datum deterministisch** (P3). Claude
   liest ausschließlich den JSON-Report und übernimmt Fristbeginn,
   rechnerisches Ende, Verschiebungen und Fristende unverändert.
4. **Claude stellt den Report als Rechenkette dar**: jeder Schritt mit Norm
   und Zwischenergebnis, alle `warnungen` und `hinweise` sichtbar. Dabei
   immer ausweisen:
   - **Notfrist / verlängerbar** (aus dem Katalog übernommen),
   - **teilgebietliche Feiertage**: sind beide möglichen Enden im Report
     (`fristende_bei_teilgebietlichem_feiertag`), zeigt Claude **beide** und
     die Prüfpflicht für die konkrete Gemeinde — nie eines unterschlagen,
   - **kein technisches Fristende** beim Widerspruch gegen den Mahnbescheid,
   - den Zweitkontroll-Hinweis aus `haftung` (immer, bei jeder Antwort).
5. **Claude erzeugt sofort den Export** aus dem Report (zweiter Executor, kein
   erneutes Rechnen). Ein Aktenzeichen / eine Bezeichnung übernimmt Claude nur,
   wenn der Nutzer sie genannt hat (nie erfinden):

   ```bash
   python3 ${CLAUDE_PLUGIN_ROOT}/core/calc/fristen/kalender_executor.py \
     --report <report.json> --format beide --output-dir <ordner> \
     [--aktenzeichen <az>] [--vorlauftage <n>]
   ```

   Claude nennt die erzeugte(n) Datei(en) und weist die Vorfrist aus.
6. **Kein neuer Export ohne Korrektur.** Solange die Frist unverändert bleibt,
   ist der Export dieselbe Datei (stabile `UID`) — Claude erzeugt ihn nicht
   erneut, sondern verweist auf den bestehenden. Ändert der Nutzer eine
   fristbestimmende Angabe (Ereignisdatum, Fristart, Bundesland …), läuft der
   Ablauf ab Schritt 1 neu; der Export bekommt dann eine neue `UID` und ersetzt
   im Zielkalender das alte Ereignis.
7. Bei Exit-Code 2 (Eingabefehler) gibt Claude die Fehlermeldung wieder und
   korrigiert die Eingabe bzw. fragt nach — er rät kein Ergebnis. Der Export
   akzeptiert nur echte Executor-Reports (`ergebnis.quelle == "executor"`) und
   lehnt modellgenerierte Werte ab (P3).

## Output-Format

JSON-Report nach [`schema/README.md`](schema/README.md), Beispiel:
[`schema/beispiel-report.json`](schema/beispiel-report.json). Kernfelder:
`rechenkette` (Schritte mit `norm`, `beschreibung`, `ergebnis`,
`quelle: "executor"`), `ergebnis.fristende`,
`ergebnis.fristende_bei_teilgebietlichem_feiertag`, `warnungen`, `hinweise`.

Jeder Datumswert im Report stammt aus `executor.py`, nie vom Modell (P3).

**Kalender-Export** (zweiter Executor), Beispiele:
[`schema/beispiel-export.ics`](schema/beispiel-export.ics),
[`schema/beispiel-export.csv`](schema/beispiel-export.csv). Ganztags-`VEVENT`
auf das (frühere, sichere) Fristende mit `VALARM`-Vorfrist, Norm-, Notfrist-
und Verschiebungs-Kennzeichnung sowie der Zweitkontroll-Klausel; CSV mit einer
Zeile je Frist (`;`-getrennt). Format-, Feld- und UID-Details:
[`schema/README.md`](schema/README.md) → „Kalender-Export".

## Beispiele

### Beispiel 1 — Berufungsfrist (Katalog), Verschiebung nach § 193 BGB

Eingabe ([`schema/beispiel-eingabe.json`](schema/beispiel-eingabe.json)):
Zustellung des Urteils am 15.01.2026, Fristart `berufung`, Bundesland NW.

Von Claude präsentiertes Ergebnis (aus dem Report übernommen):

| Schritt | Norm | Ergebnis |
|---|---|---|
| Ereignistag 15.01.2026 (Do) zählt nicht mit | § 187 Abs. 1 BGB | Fristbeginn 16.01.2026 |
| 1 Monat: der Zahl nach entsprechender Tag | § 188 Abs. 2 Alt. 1 BGB | 15.02.2026 (So) |
| Sonntag → nächster Werktag | § 193 BGB / § 222 Abs. 2 ZPO | **16.02.2026 (Mo)** |

Hinweise (aus dem Report): Notfrist (✅ § 224 Abs. 1 Satz 2 ZPO), Fristbeginn
spätestens fünf Monate nach Verkündung (§ 517 ZPO). **Zweitkontrolle durch die
Kanzlei bleibt zwingend.**

### Beispiel 2 — freie Frist, teilgebietlicher Feiertag (beide Enden)

Eingabe ([`schema/beispiel-eingabe-frei.json`](schema/beispiel-eingabe-frei.json)):
2 Wochen ab 01.08.2025, Bundesland BY. Das rechnerische Ende 15.08.2025 (Fr)
ist Mariä Himmelfahrt — in Bayern nur in Gemeinden mit überwiegend
katholischer Bevölkerung Feiertag. Der Report weist **beide** Enden aus:

- Fristende **15.08.2025 (Fr)**, falls der Fristende-Ort keinen Feiertag hat,
- Fristende **18.08.2025 (Mo)**, falls Mariä Himmelfahrt dort gilt
  (`fristende_bei_teilgebietlichem_feiertag`),

mit Warnung: konkrete Gemeinde prüfen. Claude zeigt immer beide Daten und
empfiehlt, vorsorglich das frühere Ende zu notieren.

### Beispiel 3 — Widerspruch gegen Mahnbescheid (kein technisches Fristende)

Fristart `widerspruch_mahnbescheid`: Der Report berechnet den Ablauf der
Zwei-Wochen-Frist aus der Belehrung (§ 692 Abs. 1 Nr. 3 ZPO), kennzeichnet
aber `kein_technisches_fristende: true` — Widerspruch bleibt möglich, solange
der Vollstreckungsbescheid nicht verfügt ist; verspäteter Widerspruch gilt
als Einspruch (§ 694 ZPO). Claude gibt das Datum nie als „harte" Frist aus.
Auch im Export erscheint es als **„Kontrolltermin (kein technisches
Fristende)"**, nicht als Frist.

### Beispiel 4 — Export der Berufungsfrist (calc → iCal/CSV)

Aus dem Report von Beispiel 1 (Az. `12/2026`) erzeugt der Export-Executor ein
Ganztags-Ereignis auf **16.02.2026** mit Vorfrist am 13.02.2026 (Default 3
Tage). Kernzeilen der `.ics`
([`schema/beispiel-export.ics`](schema/beispiel-export.ics)):

```
SUMMARY:Frist: Berufungsfrist [NOTFRIST] — Az. 12/2026
DTSTART;VALUE=DATE:20260216
BEGIN:VALARM
TRIGGER:-P3D
```

Läuft der Export für dieselbe Frist erneut, ist die `UID` identisch — der
Re-Import aktualisiert dasselbe Ereignis. Korrigiert der Nutzer z. B. das
Zustelldatum, ändert sich die `UID` und der Kalender erhält ein neues Ereignis.
