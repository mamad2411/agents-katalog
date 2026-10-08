---
name: honorar-mahnwesen
description: "Wertet offene Posten (OPOS-CSV oder EXTF-Buchungsstapel) deterministisch aus — offener Restbetrag, Tage seit Fälligkeit, konfigurierbare Mahnstufen, Priorisierung (Betrag × Alter) — und draftet daraus interne Zahlungserinnerungen/Mahnungen der Kanzlei an eigene Mandanten. Triggert bei Mahnwesen, offene Rechnungen, Zahlungserinnerung, überfällige Forderungen, offene Posten, OPOS."
status: beta
welle: 4
bereich: zeit-abrechnung
rdg_einordnung: "Internes Forderungsmanagement der Kanzlei in eigener Sache (eigene Honorarforderungen gegen eigene Mandanten) — keine Inkasso-Dienstleistung für Dritte und keine Rechtsdienstleistung i. S. d. § 2 RDG. Der Skill trifft keine rechtliche Verzugsentscheidung (§ 286 BGB) und berechnet keine Verzugszinsen (§ 288 BGB); er ordnet nur kalendarisch nach Tagen seit Fälligkeit ein. Ob, wann und wie gemahnt wird, entscheidet die Kanzlei."
daten_hinweis: "Zahlungsdaten von Mandanten (Rechnungsnummern, Beträge, ggf. Namen/Aktenzeichen, § 203 StGB / DSGVO). Verarbeitung nur innerhalb des dokumentierten Speicher-Perimeters (D10: Kanzleisoftware, lokal verschlüsseltes Kanzlei-Gerät oder der ohnehin die Mandantendaten hostende/das Modell betreibende Server, z. B. AWS Bedrock Frankfurt) — kein neuer Speicherort. Der Executor arbeitet rein lokal, ohne Netzwerkzugriff."
haftung: "Zweitkontrolle, zwingend: Beträge, offene Restbeträge, Fälligkeitstage und Mahnstufen stammen aus dem Executor; jeder Entwurf ist vor Versand durch die Kanzlei zu prüfen (insb. ob die Forderung besteht, Fälligkeit/Verzug rechtlich vorliegen und der richtige Mandant adressiert ist). Verzugszinsen (§ 288 BGB) und die rechtliche Verzugsfeststellung (§ 286 BGB) sind bewusst NICHT enthalten und bleiben Kanzleisache. Versand entscheidet ausschließlich die Kanzlei."
---

# honorar-mahnwesen

> **Status: `beta`** — automatisierte Tests (Parser-Round-Trip gegen den
> EXTF-Writer, OPOS-Auswertung, CLI-Reject-Matrix) laufen grün in CI. Noch
> **nicht** händisch abgenommen; `status: getestet` vergibt allein der
> Maintainer nach einer Live-Abnahme (Reifegrad-Leiter, CONVENTIONS.md).

## Zweck

Wertet offene Honorarforderungen der Kanzlei aus und bereitet interne
Mahn-/Erinnerungsschreiben vor. Der deterministische Kern
[`core/calc/opos/`](../../core/calc/opos/README.md) berechnet je Posten:

- **offener Restbetrag** = Rechnungsbetrag − bereits gezahlt (`Decimal`, nie `float`),
- **Tage seit Fälligkeit** = Stichtag − Fälligkeitsdatum (reine Kalenderdifferenz),
- **Mahnstufe** aus konfigurierbaren Tagesschwellen (Default: Erinnerung ab
  Fälligkeit, 1. Mahnung ab 14 Tagen, 2. Mahnung ab 30 Tagen),
- **Priorität** = offener Restbetrag × Tage seit Fälligkeit (Sortierung der Arbeitsliste).

**Berufsrechts-Grenze (RDG):** internes Forderungsmanagement **in eigener
Sache** — kein Inkasso für Dritte, keine Rechtsdienstleistung. Der Skill sagt
nicht, ob rechtlich Verzug eingetreten ist; „Tage seit Fälligkeit" ist eine
kalendarische Größe, keine Verzugsfeststellung (§ 286 BGB).

**Bewusst zurückgestellt (v1):**
- **Verzugszinsen (§ 288 BGB)** — bräuchten gepflegte Basiszinssatz-Stammdaten
  (Halbjahres-Sätze der Deutschen Bundesbank); erscheinen im Report als
  **Hinweis-Lücke**, nie als Zahl.
- **Rechtliche Verzugsfeststellung (§ 286 BGB)** — u. a. verbraucherabhängig
  (Verzug ohne Mahnung erst 30 Tage nach Fälligkeit *und* Hinweis bei
  Verbrauchern, § 286 Abs. 3 BGB); bleibt ausdrücklich Kanzleisache.

## Eingaben (Datei-Kontrakt, P2)

Genau **eine** Quelle je Lauf (vollständiges Schema: [`schema/README.md`](schema/README.md)):

| Quelle | Flag | Format | Charakter |
|---|---|---|---|
| OPOS-Liste | `--opos-csv` | `.csv` (Semikolon, Komma-Dezimal, Kopfzeile) | **Normalweg und präzise Primärquelle** — je Zeile ein Posten mit Fälligkeitsdatum |
| Buchungsstapel | `--extf` | DATEV-EXTF (Format 700, Kategorie 21) | **Sonderweg, nur bei DATEV-Anbindung** — vereinfachte Belegfeld-1-Aggregation, kein Fälligkeitsdatum im EXTF |

> **EXTF ist der Sonderweg, keine gleichwertige Zweitquelle.** EXTF-Buchungs-
> stapel entstehen nur dort, wo eine DATEV-Anbindung besteht (Export aus DATEV
> bzw. vom Steuerberater). Kleine Kanzleien ohne DATEV haben so eine Datei
> schlicht nicht — für sie ist die OPOS-/Debitorenliste als CSV der reguläre
> Weg. Liegt kein echtes EXTF vor: keins nachbauen, sondern `--opos-csv`
> nutzen.

Zusätzlich immer `--stichtag JJJJ-MM-TT` (Bezugstag für „Tage seit
Fälligkeit" — aus der Eingabe, **nie** aus der Wall-Clock, damit gleiche
Eingabe denselben Report liefert). Optional `--mahnstufen-config <config.json>`
(Tagesschwellen überschreiben) und `--zahlungsziel-tage <N>` (nur `--extf`,
Default 14).

Die EXTF-Quelle liest der strikte Parser
[`core/calc/extf/parser.py`](../../core/calc/extf/parser.py) (das getestete
Gegenstück zum `datev-export`-Writer). Fehlende Angaben (Mandant/Fälligkeit
im EXTF, Buchungen ohne Belegfeld 1) werden als **Lücke** bzw. unter
`nicht_zuordenbar` ausgewiesen — nie geraten.

## Ablauf

1. **Claude ruft den Executor auf** (kein eigenes Rechnen/Formatieren):

   ```bash
   # Präzise Quelle (OPOS-CSV):
   python3 ${CLAUDE_PLUGIN_ROOT}/skills/honorar-mahnwesen/executor.py \
     --opos-csv <posten.csv> --stichtag 2026-07-16 \
     --output <report.json>

   # Ergänzende Quelle (EXTF-Buchungsstapel):
   python3 ${CLAUDE_PLUGIN_ROOT}/skills/honorar-mahnwesen/executor.py \
     --extf <stapel.csv> --stichtag 2026-07-16 --zahlungsziel-tage 14 \
     --output <report.json>
   ```

2. **Bei Exit 0**: Claude liest den JSON-Report und stellt die nach Priorität
   sortierte Arbeitsliste zusammen (Rechnungsnummer, Mandant, offener Rest,
   Tage seit Fälligkeit, Mahnstufe) — und weist **immer** auf die
   Zurückstellungen hin: keine Verzugszinsen (§ 288 BGB), keine
   Verzugsfeststellung (§ 286 BGB), Versand ist Kanzlei-Entscheidung.
3. **Schreiben-Entwürfe (optional):** Auf Wunsch draftet Claude je Posten eine
   **Zahlungserinnerung/Mahnung** — ausschließlich aus Executor-Werten. Jeder
   Betrag, jedes Datum und jede „Tage seit Fälligkeit"-Angabe im Entwurf ist
   ein Executor-Ergebnis; Claude erfindet keine Beträge/Fristen und trägt
   keine Verzugszinsen ein. Bausteine siehe unten. Der Entwurf geht nie ohne
   Kanzlei-Freigabe hinaus.
4. **Bei Exit 2** (Eingabe-/Formatfehler): Claude gibt die Fehlermeldung
   unverändert wieder und korrigiert die Eingabe bzw. fragt nach — er rät
   keinen Ersatz-Betrag, kein Ersatz-Datum und erzeugt keine Teil-Datei.

## Output-Format

Ein JSON-Report aus [`executor.py`](executor.py) / [`core/calc/opos/rechner.py`](../../core/calc/opos/rechner.py) (P3):

- `zusammenfassung` (Anzahl offen, Summe offen, ausgeglichen, nicht zuordenbar),
- `offene_posten` — nach Priorität absteigend; je Posten offener Rest, Tage
  seit Fälligkeit, Mahnstufe, Priorität, `verzugszins_hinweis` (immer Lücke,
  nie Zahl), `hinweise[]`,
- `ausgeglichene_posten`, `nicht_zuordenbar` (EXTF-Buchungen ohne Belegfeld 1),
- alle Zahlen als Decimal-Strings (keine float-Rundung).

Beispiel-Eingabe: [`schema/beispiel-opos.csv`](schema/beispiel-opos.csv).
Deterministik-Grenze (P3): jeder Zahlen-/Datums-/Geldwert stammt aus dem
Executor und ist als solcher markiert (`meta.deterministik`).

## Schreiben-Bausteine (Entwurf, kein Template-Engine)

Claude setzt den Entwurf aus diesen Bausteinen zusammen und füllt **nur**
Executor-Werte ein (Platzhalter in `{}`):

- **Zahlungserinnerung** (freundlich): „Sehr geehrte/r {mandant}, zu unserer
  Rechnung {rechnungsnummer} vom {rechnungsdatum} ist ein Betrag von
  {offener_rest} € offen (fällig seit {faelligkeitsdatum}, {tage} Tage). Wir
  bitten um Ausgleich bis {…, von der Kanzlei zu setzen}."
- **1./2. Mahnung** (bestimmter): zusätzlich Verweis auf die vorherige
  Erinnerung; **keine** Zinsforderung durch den Skill (§ 288 BGB bleibt
  Kanzleisache), **keine** Verzugsbehauptung.

Jeder Norm-Verweis im Entwurf trägt einen 3-Zustands-Marker
(CONVENTIONS.md): § 286 BGB ⚠️ (nicht prüfbar — der Executor prüft keinen
Verzug), § 288 BGB ⚠️ (bewusst nicht berechnet).

## Grenzen (bewusst)

- **Keine Verzugszinsen** (§ 288 BGB ⚠️) und **keine** rechtliche
  Verzugsfeststellung (§ 286 BGB ⚠️) — nur „Tage seit Fälligkeit".
- **EXTF ist Sonderweg und vereinfacht** — er setzt eine DATEV-Anbindung
  voraus (ohne die es keinen Buchungsstapel gibt) und rechnet mit
  Belegfeld-1-Saldo und Zahlungsziel-Annahme statt echtem Fälligkeitsdatum.
  Normalweg und präzise Quelle ist die OPOS-CSV.
- **Kein Inkasso, keine Rechtsdienstleistung** — nur eigenes
  Forderungsmanagement der Kanzlei.
- **Kein Versand** — der Skill erzeugt Entwürfe; Mahnung/Versand entscheidet
  die Kanzlei.
- **`status: getestet` erst nach Live-Abnahme** durch den Maintainer — nie
  durch automatisierte Tests allein.
