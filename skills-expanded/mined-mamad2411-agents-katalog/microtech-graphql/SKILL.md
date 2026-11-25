---
name: microtech-graphql
description: >-
  Erstellt und optimiert GraphQL-Queries und Mutations fuer die microtech ERP
  microtech ERP. Deckt den gesamten ERP-Datenbestand ab: Artikel, Warengruppen, Stuecklisten,
  Adressen mit Anschriften und Ansprechpartnern, Vorgaenge (Angebote, Auftragsbestaetigungen,
  Lieferscheine, Rechnungen, Gutschriften, Bestellungen), Vorgangspositionen, offene Posten,
  Lagerbestaende, Projekte, Dokumente (DMS), Kalender, Kontakte, Kontenplan, Zahlungsverkehr
  und SEPA-Mandate. Unterstuetzt Lesen, Anlegen, Aendern, Loeschen, Buchen (fnPost),
  Stornieren (fnReverse), Wandeln (fnConvert), Archivieren sowie ERP-Parametertabellen
  (Vorgangsarten, Steuerschluessel, Zahlungsbedingungen, Einheiten, Versandarten, Waehrungen,
  Mahnstufen, Adressstatus, Projektstatus, Dokumentenarten, Kommunikationsarten u.v.m.).
  Verwende diesen Skill wenn der Nutzer mit microtech ERP oder microtech ERP arbeiten will,
  ERP-Daten abfragen, Belege erstellen oder verarbeiten will, oder microtech-spezifische
  Begriffe wie tbl, fld, fnPost, fnConvert, rowRead, rowNew, rowSave, acoGPreis,
  lnkPostalAddresses, @acquireLocks erwaehnt. NICHT verwenden fuer andere ERP-Systeme
  (SAP, Shopify, Odoo, Dynamics), allgemeine SQL/Datenbank-Fragen oder generische
  GraphQL-Schemas ohne microtech-Bezug.
license: MIT
compatibility: >-
  Erfordert einen MCP-Server mit GraphQL-Zugriff auf eine microtech ERP-Instanz.
  WICHTIG: Niemals das vollstaendige GraphQL-Schema per __schema-Introspection
  abrufen -- die Antwort ist zu gross und fuehrt zu Timeout oder Token-Limit.
  Stattdessen gezielt einzelne Typen per __type(name: "TypeName") abfragen.
metadata:
  author: microtech GmbH
  version: 1.0.0
  mcp-server: mcp-graphql
---

# microtech GraphQL - Skill-Referenz

Kompakte Referenz fuer die GraphQL-Schnittstelle des microtech ERP.
Optimiert fuer Query-Generierung ueber einen MCP-Server mit `graphql_query`-Tool.

> **ASCII:** Dieses Dokument verwendet `ae/oe/ue/ss` statt Umlaute.

> **WICHTIG - Introspection:** NIEMALS das vollstaendige Schema abrufen (`__schema`). Stattdessen gezielt einzelne Typen abfragen. Siehe `references/introspection-guide.md`.

> **Feldkataloge:** Fuer detaillierte Feldlisten pro Tabelle siehe `references/feldkatalog-*.md`.

> **Erweiterte Themen:** Fuer Archiv-Funktionen, externe Bearbeitung, Berechtigungen, Cross-Table-Patterns siehe `references/vorgaenge-erweitert.md`.

> **Mutation-Patterns:** Fuer Optimistic Locking, rowCopy, ifNotExists, Deep Nesting, Massenoperationen siehe `references/mutation-patterns.md`.

> **Query-Patterns:** Fuer keyFilter-Details, Arithmetik, skip-Wert, erweitertes @onNull, Schema-Metadaten siehe `references/erweiterte-query-patterns.md`.

> **Adressen-Verwaltung:** Praxisbeispiele fuer Adressen, Anschriften und Ansprechpartner (lesen, anlegen, aendern, loeschen) mit verschachtelten Links, Optimistic Locking, rowCopy, Massenoperationen und assign-Parametern in `references/adressen-verwaltung.md`. **Bei Adress-Aufgaben dort zuerst nachschlagen!**

> **Parametertabellen:** Konfigurations- und Parametertabellen auslesen (Vorgangsarten, Zahlungsbedingungen, Steuerschluessel, Einheiten, Versandarten, Waehrungen, Mahnstufen, Projektstatus u.v.m.) in `references/parametertabellen.md`. **Bei Fragen zur mandantenspezifischen Konfiguration dort nachschlagen!**

> **Workflow-Beispiele:** 17 vollstaendige Szenarien (Rechnung erstellen, Vorgang wandeln, Storno, Lagerbestand u.v.m.) in `references/workflow-beispiele.md`. **Bei komplexen Aufgaben dort zuerst nachschlagen!**

---

## Kritische Regeln (Top 9)

1. **keyFilter-First:** Bei JEDEM Filter zuerst pruefen, ob ein passender `by...`-Index existiert und `keyFilter` verwenden. Erst wenn kein passender Index vorhanden ist, auf `fastFilter` oder `slowFilter` zurueckfallen. Siehe Abschnitt 5 fuer den verbindlichen Workflow.
2. **@oneOf-Regel:** Pro Filterobjekt nur EIN Operator. Mehrere Bedingungen mit `and`/`or` kombinieren.
3. **`fnPost`/`fnReverse`/`fnConvert` nur in `rowRead`-Kontext** (nicht `rowModify`!), immer in `mutation`.
4. **`rowSave` vor `fnPost`** - ohne `rowSave` sind Positionen nicht gespeichert und werden nicht gebucht.
5. **Nach `rowSave` nicht mehr schreiben** im selben Block - fuehrt zu Laufzeitfehler und Rollback.
6. **Leere Belegnummer = Operation fehlgeschlagen** - immer `fldBelegNr` in `fn...`-Rueckgaben pruefen.
7. **Prozessketten-Integritaet - NIEMALS fn-Funktionen durch manuelle Operationen ersetzen!**
   ERP-Prozessfunktionen (`fnPost`, `fnReverse`, `fnConvert`, `fnMoveToArchive`) sind die EINZIGE korrekte Art, den Belegstatus zu veraendern. Sie sichern die Prozesskette (z.B. Angebot → AB → Lieferschein → Rechnung), verknuepfen Belege, aktualisieren Lagerbestaende, erzeugen Buchungssaetze und fuehren Plausibilitaetspruefungen durch. Wenn eine fn-Funktion fehlschlaegt, STOPPEN und den Nutzer informieren - KEINEN Workaround versuchen.
8. **NIEMALS `rowNew` als Ersatz fuer `fnConvert`** - ein manuell angelegter Folgebeleg hat KEINE Verknuepfung zum Vorgaenger. Die Prozesskette ist unterbrochen, Mengen werden nicht korrekt gefuehrt, Lieferstatus wird nicht aktualisiert. Stattdessen: Fehlerursache klaeren (Wandlungspfad nicht konfiguriert, Beleg bereits archiviert, etc.) und Nutzer fragen.
9. **NIEMALS `rowDelete` als Ersatz fuer `fnReverse`** - eine Loesung per `rowDelete` umgeht die Storno-Logik: keine Storno-Belegnummer, keine Gegenbuchungen, keine Lagerkorrektur, kein Audit-Trail. Stattdessen: `fnReverse` verwenden, bei Fehler Nutzer informieren.

---

## Arbeitsweise: So bearbeitest du Nutzeranfragen

### Schritt 1: Anfrage klassifizieren
- **Lesen/Suchen** → `query` (Daten anzeigen, suchen, auflisten, zaehlen)
- **Schreiben/Aendern** → `mutation` (anlegen, aendern, loeschen, buchen, wandeln)
- **Unbekannte Felder/Tabelle** → Erst Introspection (`references/introspection-guide.md`)

> **Source of Truth:** Bei Unsicherheit ueber Feldnamen, Schreibbarkeit oder verfuegbare Operationen IMMER die Live-API per Introspection pruefen. Dokumentierte Feldlisten koennen veraltet sein - die API ist die einzig zuverlaessige Quelle.

### Schritt 2: Tabelle identifizieren
- Nutze die Tabelle aus "Schnellreferenz" unten
- Bei Unsicherheit: Introspection oder Nutzer fragen

### Schritt 3: Reference-Dateien konsultieren

**BEVOR du eine Query oder Mutation baust:** Pruefe ob ein passendes Beispiel oder Detail-Wissen existiert.

- **Komplexe Aufgabe?** → Zuerst `references/workflow-beispiele.md` durchsuchen (17 Szenarien)
- **Feldnamen unklar?** → Passenden `references/feldkatalog-*.md` lesen
- **Filter-Logik?** → `references/erweiterte-query-patterns.md` (keyFilter, Arithmetik, Datums-Filter)
- **Adressen/Anschriften/Ansprechpartner?** → `references/adressen-verwaltung.md` (verschachtelte Links, rowReAnsNr, assign-Parameter, Massenoperationen)
- **Mutation-Pattern?** → `references/mutation-patterns.md` (Optimistic Locking, rowCopy, Deep Nesting)
- **Vorgangsfunktionen?** → `references/vorgaenge-erweitert.md` (Archiv, externe Bearbeitung)
- **Parametertabellen/Konfiguration?** → `references/parametertabellen.md` (Vorgangsarten, Steuerschluessel, Zahlungsbedingungen, Einheiten, Versandarten, Waehrungen, Mahnstufen, Projektstatus, Dokumentenarten u.v.m.)
- **Introspection noetig?** → `references/introspection-guide.md` (Typ-Namenskonventionen)

> **Nicht raten - nachschlagen!** Die Reference-Dateien enthalten getestete, korrekte Beispiele. Lieber 30 Sekunden lesen als eine fehlerhafte Query bauen.

### Schritt 4a: Query bauen (Lesen)
1. **Filter-Strategie (keyFilter-First!):**
   - Gibt es einen `by...`-Index fuer das Suchfeld? → `keyFilter` verwenden
   - Kein Index? → `fastFilter` (einfache Gleichheit auf `fld...`)
   - Komplex? → `slowFilter` (Arithmetik, `in`, `fn...`)
2. Query mit `graphql_query`-Tool ausfuehren
3. Ergebnis dem Nutzer verstaendlich praesentieren

### Schritt 4b: Mutation bauen (Schreiben)
1. **Operation waehlen:**
   - Neuer Datensatz → `rowNew` (ggf. mit `assignAddress`/`assignProduct`)
   - Aendern → `rowModify`
   - Buchen/Stornieren/Wandeln → `rowRead` + `fnPost`/`fnReverse`/`fnConvert`
   - Loeschen → `rowDelete` (aber NICHT als Ersatz fuer `fnReverse`!)
2. **`@acquireLocks` pruefen:** Bei Multi-Tabellen-Mutations immer angeben
3. **Speicher-Strategie:** `rowSave` vs. `rowSaveAndModify` - bei Vorgaengen mit Positionen immer `rowSaveAndModify` + inneres `rowSave` vor `fnPost`
4. Mutation ausfuehren und **Ergebnis pruefen** (leere Belegnummer = fehlgeschlagen!)

### Schritt 5: Ergebnis verifizieren
- **Query:** Kamen Daten zurueck? Paginierung noetig (`hasNextPage`)?
- **Mutation:** `fldBelegNr` pruefen - leer bedeutet die Operation ist fehlgeschlagen
- **Fehler:** Abschnitt "Troubleshooting" pruefen, Nutzer informieren
- **Nie stillschweigend Fehler ignorieren** - immer dem Nutzer mitteilen was passiert ist

### Typische Nutzer-Szenarien

| Nutzer sagt... | Du machst... |
|----------------|-------------|
| "Zeig mir Artikel X" | `query` → `tblProducts` → `rowRead` mit keyFilter |
| "Alle Kunden aus PLZ 5xxxx" | `query` → `tblAddresses` → `lnkPostalAddresses` → slowFilter auf fldPLZ |
| "Erstell eine Rechnung fuer Kunde 10000" | `mutation` mit `@acquireLocks` → `tblTransactions` → `rowNew` + `rowSave` + `fnPost` |
| "Wandle Angebot 12345 in AB" | `mutation` → `tblTransactions` → `rowRead` + `fnConvert` |
| "Wieviele Artikel haben wir?" | `query` → `tblProducts` → `conRead(first: 100)` → paginieren + `hasNextPage` |
| "Storniere Rechnung 67890" | `mutation` → `tblTransactions` → `rowRead` + `fnReverse` |
| "Zeig mir Adresse 10000 mit Anschriften und Ansprechpartnern" | `query` → `tblAddresses` → `lnkPostalAddresses` → `lnkContactPeople` → siehe `references/adressen-verwaltung.md` |
| "Leg einen neuen Kunden / Lieferanten / Interesenten an mit Anschrift und Ansprechpartner" | `mutation` → verschachtelt: `rowNew` + `rowSave` + `lnkPostalAddresses` + `lnkContactPeople` → siehe `references/adressen-verwaltung.md` |
| "Welche Vorgangsarten gibt es?" | `query` → `tblTransactionTypes` → `rowsRead` → siehe `references/parametertabellen.md` |
| "Welche Zahlungsbedingungen sind konfiguriert?" | `query` → `tblPaymentTerms` → `rowsRead` → siehe `references/parametertabellen.md` |
| "Zeig mir die Steuerschluessel" | `query` → `tblValueAddedTaxTypes` → `rowsRead` → siehe `references/parametertabellen.md` |
| "Welche Einheiten/Waehrungen gibt es?" | `query` → `tblUnitsOfMeasure`/`tblCurrencies` → siehe `references/parametertabellen.md` |

---

## Schnellreferenz

### Wichtigste Tabellen

| GraphQL-Tabelle | Beschreibung | Schreibbar |
|----------------|-------------|------------|
| `tblAddresses` | Adressen | ja |
| `tblPostalAddresses` | Anschriften | ja |
| `tblContactPeople` | Ansprechpartner | ja |
| `tblContacts` | Kontakte | ja |
| `tblProducts` | Artikel | ja |
| `tblProductGroups` | Warengruppen | ja |
| `tblSuppliers` | Artikel-Lieferanten | ja |
| `tblTransactions` | Vorgaenge | ja |
| `tblTransactionItems` | Vorgangspositionen | ja (verschachtelt in tblTransactions) |
| `tblTransactionsArchive` | Archiv Vorgaenge | ja |
| `tblProjects` | Projekte | ja |
| `tblDocuments` | Dokumente | ja |
| `tblCalendar` | Kalender | ja |
| `tblWarehouses` | Lager | ja |
| `tblClient` | Mandant (Einzeldatensatz) | ja |
| `tblOpenItems` | Offene Posten | nein |
| `tblInventory` | Lagerbestaende | nein |
| `tblUsers` | Benutzer | nein |
| **Parametertabellen** | | |
| `tblTransactionTypes` | Vorgangsarten (Wandlungskette, Buchungsparameter) | nein |
| `tblPostingParameters` | Buchungsparameter | nein |
| `tblUnitsOfMeasure` | Mengeneinheiten (UN/ECE-Codes fuer E-Rechnung) | nein |
| `tblValueAddedTaxTypes` | Steuerschluessel mit Saetzen und DATEV-Zuordnung | nein |
| `tblPaymentTerms` | Zahlungsbedingungen | nein |
| `tblCurrencies` | Fremdwaehrungen mit Wechselkursen | nein |
| `tblShippingTypes` | Versandarten | nein |
| `tblAddressStatuses` | Adressstatus mit Nummernkreisen | nein |
| `tblSalutations` | Anreden | nein |
| `tblDunningLevels` | Mahnstufen | nein |
| `tblPaymentMethods` | Zahlungsarten | nein |
| `tblProjectTypes` | Projektarten | nein |
| `tblProjectStates` | Projektstatus (Workflow) | nein |
| `tblDocumentTypes` | Dokumentenarten (DMS) | nein |
| `tblDocumentStates` | Dokumentenstatus (Workflow) | nein |
| `tblCommunicationTypes` | Kommunikationsarten | nein |

### Haeufigste Patterns (Copy-Paste-fertig)

```graphql
# LESEN - Einzelner Datensatz
query { tblProducts { rowRead(kf1ArtNr: { string: "LUTSCHER" }) { fldArtNr fldSuchBeg fldBez1(as: DISPLAY_TEXT) } } }

# LESEN - Liste mit Filter
query { tblProducts { rowsRead(slowFilter: { gt: [{field: fldVk0_Preis}, {value: 0}] }) { fldArtNr fldVk0_Preis(as: TEXT) } } }

# LESEN - Paginiert
query ($after: String) { tblProducts { conRead(first: 10, after: $after) { edges { node { fldArtNr } cursor } pageInfo { hasNextPage endCursor } } } }

# SCHREIBEN - Neuer Datensatz
mutation { tblProducts { rowNew { fldArtNr(set: { string: "NEU-001" }) fldBez1(set: { text: "Bezeichnung" } as: DISPLAY_TEXT) } } }

# SCHREIBEN - Datensatz aendern
mutation { tblProducts { rowModify(kf1ArtNr: { string: "LUTSCHER" }) { fldBez1(set: { text: "Neuer Name" } as: DISPLAY_TEXT) } } }

# SCHREIBEN - Vorgang anlegen + buchen
mutation @acquireLocks(forWriting: [tblTransactions, tblTransactionItems], forReading: [tblAddresses, tblProducts]) {
  tblTransactions {
    rowNew(assignAddress: { kf1AdrNr: { text: "10000" } }) {
      fldArt(set: { text: "Rechnung I" })
      rowSaveAndModify {
        fldBelegNr
        tblTransactionItems {
          rowNew(assignProduct: { kf1ArtNr: { text: "LUTSCHER" } }) { fldMge(set: { float: 10 }) }
        }
        rowSave { fnPost { fldBelegNr } }   # rowSave VOR fnPost!
      }
    }
  }
}
```

---

## 1. Grundstruktur

### Tabellenzugriff

Alle Operationen beginnen mit `tbl...` auf oberster Ebene:

```graphql
query {
  tblProducts { ... }       # Artikel
  tblAddresses { ... }      # Adressen
  tblTransactions { ... }   # Vorgaenge
}
```

### Leseoperationen

| Feld | Beschreibung | Rueckgabe |
|------|-------------|-----------|
| `rowRead(...)` | Einzelnen Datensatz lesen | `Row` oder `null` |
| `rowsRead(...)` | Liste lesen | `[Row]` |
| `conRead(...)` | Paginierte Liste (Relay Connection) | `Connection` |

### Einzeldatensatz-Tabellen

`tblClient` braucht keine Suchparameter:
```graphql
query { tblClient { rowRead { fldMandNr fldMandTyp } } }
```

---

## 2. Datensatzauswahl

### `exactMatch` - Exakte Suche

```graphql
rowRead(exactMatch: { byNr: { kf1ArtNr: { string: "PROD-001" } } })
```

### Verschachtelte Schluesselfelder

```graphql
rowRead(exactMatch: {
  byArtNrLagNr: {
    kf1ArtNr: { string: "LUTSCHER"
      kf2LagNr: { string: "HAUPT" }
    }
  }
})
```

### Verkuerzte Schreibweisen

```graphql
# Statt:
rowRead(exactMatch: { byNr: { kf1ArtNr: { string: "LUTSCHER" } } })
# Kurz (impliziert exactMatch + byNr):
rowRead(kf1ArtNr: { string: "LUTSCHER" })

# Bereich:
rowsRead(kf1ArtNr: { from: { string: "0" }, to: { string: "12000" } })
```

### Weitere Sucharten

```graphql
# Naechster Treffer
rowRead(nearestMatch: { byNr: { kf1ArtNr: { string: "PROD-000" } } })

# Aktueller Benutzer
tblUsers { rowRead(using: current) { fldAnmNa } }

# Bereich mit exklusiver Obergrenze
rowsRead(allBetween: { byNr: { kf1ArtNr: { from: { string: "A" }, to: { string: "Z" }, toExclusive: true } } })
```

---

## 3. Datenfelder und Ausgabeformate

### Praefix-System

| Praefix | Bedeutung | Beispiel |
|---------|-----------|---------|
| `tbl...` | Tabelle | `tblProducts` |
| `fld...` | Datenfeld | `fldArtNr`, `fldPreis` |
| `kf...` | Schluesselfeld | `kf1ArtNr`, `kf2LagNr` |
| `by...` | Sortierfolge | `byNr`, `bySuchBeg` |
| `row...` | Verweis auf verknuepften Datensatz | `rowWgrNr` |
| `lnk...` | Verlinkung zu Datentabelle | `lnkInventory` |
| `aco...` | Betragsgruppe | `acoEPr`, `acoGPreis` |
| `img...` | Bildfeld | `imgBild` |
| `fn...` | Funktion | `fnPost`, `fnIsCustomer` |
| `_...` | System-Feld | `_if`, `_string` |

### `as`-Parameter - Ausgabeformat

```graphql
fldPreis                    # Standardformat
fldPreis(as: TEXT)          # "99,95 EUR" (lokalisiert)
fldPreis(as: FLOAT)         # 99.95
fldPreis(as: STRING)        # Roher String
fldPreis(as: INT)           # Ganzzahl
fldPreis(as: DISPLAY_TEXT)  # Anzeigeformat (auch fuer RTF-Felder → Klartext)
fldGueltigAb(as: TEXT)      # "24.12.2023" (lokalisiert)
fldGspKz(as: BOOLEAN)       # true/false
```

### Gemeinsame Felder (in fast allen Tabellen)

```
# Identifikation
fldID                       # Automatische ID
fldModifyLSN / fldInsertLSN # Versionierung (BigInt)

# Audit-Trail
fldErstDat / fldErstBzr     # Erstellungsdatum / -benutzer
fldAendDat / fldAendBzr     # Aenderungsdatum / -benutzer

# Sperren
fldGspKz                    # Gesperrt-Kennzeichen (Boolean)
fldGspDat / fldGspInfo      # Sperrdatum / -information
fldGspGrp                   # Gesperrtgruppe

# Freitext
fldInfo                     # Informationsfeld
fldMemo                     # Memo-Feld
fldQuickInfo                # QuickInfo
```

---

## 4. Verknuepfungen

### Verweise (`row...`) - Einzelner verknuepfter Datensatz

```graphql
tblProducts {
  rowsRead {
    fldArtNr
    fldWgrNr                  # Fremdschluessel-Wert
    rowWgrNr { fldBez }       # Verknuepfte Warengruppe
    rowEinh { fldKuBez }      # Verknuepfte Einheit
  }
}
```

### Verlinkungen (`lnk...`) - Liste verknuepfter Datensaetze

**WICHTIG:** `by.../using...` gehoeren auf `rowsRead` INNERHALB des Links, NICHT auf `lnk...`:

```graphql
# RICHTIG:
lnkInventory {
  rowsRead(byArtNrLagNrArtBDat: { usingArtNr: {} }) { fldLagNr fldMge }
}

# FALSCH:
lnkInventory(byArtNrLagNrArtBDat: { usingArtNr: {} }) {
  rowsRead { ... }
}
```

### Verschachtelte Tabellen (`tbl...` innerhalb Row)

```graphql
tblClient {
  rowRead {
    fldMandNr
    tblBnkVb { rowsRead { fldNr fldIBAN } }
  }
}
```

---

## 5. Filter

### VERBINDLICHER WORKFLOW: keyFilter-First

**BEVOR du einen Filter schreibst, fuehre IMMER diese Schritte aus:**

1. **Sortierfolgen ermitteln:** Pruefe per Introspection, welche `by...`-Sortierfolgen die Tabelle hat:
   ```graphql
   { __type(name: "{SingularName}SlowAnyFields") { enumValues { name } } }
   ```
   **WICHTIG:** Der Enum-Name verwendet den **Singular-Namen** der Entitaet, NICHT den Tabellennamen!
   Beispiele: `ProductSlowAnyFields`, `TransactionSlowAnyFields`, `AddressSlowAnyFields`.
   Sonderfaelle: `CalendarEntrySlowAnyFields`, `AccountSlowAnyFields`, `BillOfMaterialsEntrySlowAnyFields`, `InventoryEntrySlowAnyFields`.
   Gleiches Muster gilt fuer `{SingularName}FastAnyFields`.
   Die `by...`-Parameter findest du auf den `rowsRead`/`conRead`-Argumenten. Alternativ: Probiere `rowsRead(allBetween: { by` und schau welche Vorschlaege die API akzeptiert.

2. **keyFilter pruefen:** Gibt es eine `by...`-Sortierfolge, die das gewuenschte Filterfeld als `kf...`-Schluessel enthaelt? → **keyFilter verwenden!**
   ```graphql
   # Beispiel: Laender ohne Staatsangehoerigkeitsnummer
   # byStaatsNr existiert mit kf1StaatsNr → keyFilter nutzen!
   rowsRead(allBetween: {
     byStaatsNr: { keyFilter: { isNull: { field: kf1StaatsNr } } }
   })
   ```

3. **Fallback:** Nur wenn KEIN passender `by...`-Index existiert:
   - `fastFilter` fuer einfache Vergleiche auf `fld...`-Felder
   - `slowFilter` NUR fuer Arithmetik, `in`-Operator, `fn...`-Funktionen

**NIEMALS direkt `slowFilter` verwenden, ohne vorher `keyFilter` geprueft zu haben!**

### Drei Filtertypen

| Filter | Performance | Besonderheiten |
|--------|------------|----------------|
| `keyFilter` | **Am schnellsten** | Filter auf `kf...`-Felder innerhalb `by...` - IMMER bevorzugen! |
| `fastFilter` | Schnell (DB-seitig) | Nur einfache Vergleiche auf `fld...` |
| `slowFilter` | Langsam (App-seitig) | Arithmetik, `in`-Operator, `fn...` - nur als letzter Ausweg |

### Vergleichsoperatoren

```graphql
{ eq: [{field: fldStatus}, {value: 1}] }       # gleich
{ ne: [{field: fldStatus}, {value: 0}] }       # ungleich
{ gt: [{field: fldMge}, {value: 0}] }          # groesser
{ lt: [{field: fldMge}, {value: 100}] }        # kleiner
{ ge: [{field: fldMge}, {value: 1}] }          # groesser-gleich
{ le: [{field: fldMge}, {value: 99}] }         # kleiner-gleich
{ isNull: { field: fldAuftrNr } }              # NULL-Pruefung
{ isNotNull: { field: fldAuftrNr } }
```

### Boolesche Kombinationen

```graphql
{ and: [Ausdruck1, Ausdruck2] }
{ or:  [Ausdruck1, Ausdruck2] }
{ not: Ausdruck }
```

### WICHTIG: @oneOf-Regel

Pro Filterobjekt nur EIN Operator:

```graphql
# FALSCH:
fastFilter: { eq: [...], gt: [...] }

# RICHTIG:
fastFilter: { and: [ { eq: [...] }, { gt: [...] } ] }
```

### IN-Operator (nur slowFilter)

```graphql
{ in: { left: { field: fldLagBestArt }, list: [1, 7] } }
```
Alle Werte muessen denselben Typ haben (@sametype-Regel).

### keyFilter - Performantester Filter

Filtert auf `kf...`-Felder INNERHALB des `by...`-Parameters. Schneller als fast/slowFilter.

```graphql
# Alle Artikel ab Nummer "10"
rowsRead(
  allBetween: {
    byNr: {
      keyFilter: { ge: [{ field: kf1ArtNr }, { value: "10" }] }
      kf1ArtNr: { from: { string: "0" }, to: { string: "ZZZZZ" } }
    }
  }
)

# Mehrere Werte per OR
keyFilter: {
  or: [
    { eq: [{ field: kf1AdrNr }, { value: "10000" }] }
    { eq: [{ field: kf1AdrNr }, { value: "70000" }] }
  ]
}
```

**Prioritaet:** `keyFilter` > `fastFilter` > `slowFilter` (immer schnellsten moegl. Typ waehlen).

Detaillierte keyFilter-Patterns siehe `references/erweiterte-query-patterns.md`.

### Funktionen in Filtern (nur slowFilter)

```graphql
{ fnPos: [{ value: "Suchtext" }, { field: fldSuchBeg }] }   # Textsuche (>0 = gefunden, NUR String-Felder!)
{ fnGetAktDate: [] }                                      # Aktuelles Datum
{ fnIncDate: [{ fnGetAktDate: [] }, { value: 0 }, { value: -12 }] }  # Datum +/- Monate
```

### Arithmetik in slowFilter

```graphql
# Brutto > 100 pruefen
slowFilter: { gt: [{ mul: [{ field: fldVk0_Preis }, { value: 1.19 }] }, { value: 100 }] }
```

Operatoren: `add`, `sub`, `mul`, `div`, `mod`, `neg`. Details in `references/erweiterte-query-patterns.md`.

---

## 6. Direktiven

### `@store` - Wert in Variable speichern

Variable muss in der Operations-Signatur deklariert werden:

```graphql
query ($storedValue: Any = null) {
  tblProducts {
    rowsRead {
      fldSuchBeg @store(in: $storedValue)
      echo: _any(value: $storedValue)
    }
  }
}
```

`@store` funktioniert ueber Verschachtelungsebenen hinweg (aeussere Tabelle → verschachtelte tbl/lnk).

### `@onNull` - Null-Behandlung

```graphql
fldSuchBeg @onNull(returnValue: "Nicht gefunden")     # Alternativwert
fldPreis @onNull(returnValue: skip)                    # Feld ueberspringen
fldArtNr @onNull(errorMessage: "ArtNr fehlt")          # Fehler ausloesen
```

### `@acquireLocks` - Praventive Sperren (nur mutation)

```graphql
mutation @acquireLocks(
  forWriting: [tblTransactions, tblTransactionItems],
  forReading: [tblAddresses, tblProducts]
) { ... }
```

Verhindert Deadlocks bei Multi-Tabellen-Mutationen.

### `@skip` / `@include`

```graphql
fldPreis @include(if: $includePrice)
```

---

## 7. System-Felder

```graphql
# Wertausgabe
_any(value: $variable)
_string(expr: { add: [{field: fldArtNr}, {value: " - "}, {field: fldSuchBeg}] })
_boolean(expr: { gt: [{field: fldLagMge}, {value: 0}] })
_localDate(expr: { fnGetAktDate: [] })

# Bedingte Ausfuehrung
details: _if(expr: { gt: [{field: fldLagMge}, {value: 0}] }) {
  fldStdPreis
  fldLagMge
}

# Bedingter Skalarwert
status: _ifThenElse(
  expr: { gt: [{field: fldLagMge}, {value: 0}] },
  then: "Verfuegbar",
  else: "Nicht auf Lager"
)

# Fehler ausloesen
_raise(message: "Negative Lagermenge!")
```

---

## 8. Mutationen

### query vs. mutation

- `query`: Snapshot-Transaktion, keine Sperren, null bei Fehler
- `mutation`: Normale Transaktion, Alles-oder-Nichts (Fehler = Rollback)

### Schreiboperationen

| Operation | Zweck |
|-----------|-------|
| `rowNew` | Neuen Datensatz erstellen |
| `rowNew(ifNotExists: ...)` | Nur erstellen wenn nicht vorhanden (gibt `null` statt Fehler) |
| `rowCopy(exactMatch: ...)` | Datensatz kopieren (nicht-gesetzte Felder vom Original) |
| `rowModify(exactMatch: ...)` | Datensatz aendern |
| `rowDelete(exactMatch: ...)` | Datensatz loeschen |
| `rowsModify/rowsCopy/rowsDelete` | Massenoperationen (Fehler bei einem → Rollback aller) |

### Row-Kontexte

| Kontext | Schreiben | `lnk...` | `tbl...` schreibbar |
|---------|-----------|----------|---------------------|
| `RowMutationNew/Copy/Modify` | ja | nein | ja |
| `RowMutationRead` (nach rowSave) | nein | ja (mit Schreiben) | nein |
| `RowMutationDelete` | nein | nein | nein |

### Datensatz erstellen

```graphql
mutation {
  tblProducts {
    rowNew {
      fldArtNr(set: { string: "PROD-001" })
      fldBez1(set: { text: "Neuer Artikel" } as: DISPLAY_TEXT)
      fldVk0_Preis(set: { float: 99.95 })
    }   # Automatisch gespeichert am Block-Ende
  }
}
```

Bedingt (kein Fehler wenn vorhanden, gibt `null` zurueck):
```graphql
rowNew(ifNotExists: { exactMatch: { byNr: { kf1ArtNr: { string: "PROD-001" } } } })
```

### Datensatz kopieren

```graphql
mutation {
  tblProducts {
    rowCopy(kf1ArtNr: { string: "LUTSCHER" }) {
      fldArtNr(set: { string: "LUTSCHER-V2" })
      # Alle anderen Felder (Preis, Bez., etc.) vom Original uebernommen
      fldBez1(as: DISPLAY_TEXT)
      fldVk0_Preis(as: FLOAT)
    }
  }
}
```

Details zu rowCopy, ifNotExists und Optimistic Locking in `references/mutation-patterns.md`.

### Datensatz aendern

```graphql
mutation {
  tblProducts {
    rowModify(kf1ArtNr: { string: "PROD-001" }) {
      fldVk0_Preis(set: { float: 129.95 })
      fldBez1(as: DISPLAY_TEXT)       # Nur lesen
    }
  }
}
```

### Datensatz loeschen

```graphql
mutation {
  tblProducts {
    rowDelete(kf1ArtNr: { string: "PROD-001" }, ignoreWarnings: true) {
      fldArtNr                         # Noch lesbar vor Loeschung
    }
  }
}
```

### Speicheroperationen

```graphql
# rowSave - Speichern, dann Read-Kontext (lnk... verfuegbar)
rowNew {
  fldArtNr(set: { string: "X" })
  rowSave { fldID fldModifyLSN }     # Ab hier nur lesen + lnk...
}

# rowSaveAndModify - Speichern, weiter schreiben
rowNew {
  fldArtNr(set: { string: "X" })
  rowSaveAndModify {
    fldBez1(set: { text: "Name" } as: DISPLAY_TEXT)
    tblTransactionItems { ... }       # Verschachtelte Tabelle schreibbar
  }
}
```

**WICHTIG:** Nach `rowSave`/`rowSaveAndModify` NICHT mehr im aeusseren Block schreiben!

### Feldmanipulation (`set`-Parameter)

```graphql
fldArtNr(set: { string: "PROD-005" })           # String
fldVk0_Preis(set: { float: 99.95 })             # Float
fldVk0_Preis(set: { text: "99,95" })            # Lokalisierter Text
fldGspAbDat(set: { text: "2023-12-24" })          # Datum (ISO-Format YYYY-MM-DD, auch localdate moeglich)
fldGspKz(set: { boolean: true })                 # Boolean
fldArt(set: { text: "Rechnung I" })              # Vorgangsart (immer Text, Nummern koennen abweichen!)
fldMge(set: { int: 5 })                         # Integer
fldGspAbDat(set: {})                             # NULL setzen

# Auto-Nummerierung (naechste freie Nr wenn vergeben)
fldAdrNr(set: { text: "10000", allowAutoNrOnSave: true })

# Kaskadierende Updates unterdruecken
fldZahlBed(set: { text: "30 Tage netto", suppressRelatedUpdates: true })
```

### Assign-Parameter

```graphql
# Row-Assign: Felder aus anderem Datensatz befuellen
rowNew(assignAddress: { kf1AdrNr: { text: "10000" } }) { ... }
rowNew(assignUser: { using: current }) { ... }

# Feld-Assign: Einzelnes Feld per Suche zuweisen
fldWgrNr(assignProductGroup: { exactMatch: { byBez: { kf1Bez: { text: "Elektronik" } } } })
fldSBzrNr(assignUser: { using: current })

# using: context in Verlinkungen (nimmt aeusseren Datensatz)
lnkProjects { rowNew(assignAddress: { using: context }) { ... } }
```

### Verlinkungen in Mutationen (nur in RowMutationRead)

```graphql
mutation {
  tblAddresses {
    rowRead(kf1AdrNr: { string: "10000" }) {
      lnkPostalAddresses {
        rowNew(setAdrNrAnsNr: usingAdrNr) {
          fldNa2(set: { text: "Lieferanschrift" })
          rowSave { fldAnsNr }
        }
      }
    }
  }
}
```

`set...`-Parameter bei `rowNew` in Verlinkungen: befuellt Schluesselfelder automatisch aus Kontext.

---

## 9. Vorgaenge - Kern-Workflow

### Vorgangsarten

**WICHTIG:** Immer `text` statt `int` verwenden - Nummern koennen pro Installation abweichen!

```graphql
fldArt(set: { text: "Rechnung I" })     # RICHTIG - Bezeichnung
fldArt(set: { int: 70 })                # VERMEIDEN - Nummer kann abweichen
```

**Hinweis: `fnConvert`** akzeptiert den Parameter `transactionTypeNo` sowohl als Integer als auch als Text:
```graphql
fnConvert(transactionTypeNo: 50, ...)              # Integer - Standard-Nummer (50 = Lieferschein)
fnConvert(transactionTypeNo: "Lieferschein", ...)  # Text - Bezeichnung
```
Standard-Nummern und Bezeichnungen finden sich in `references/vorgangsarten.md`.

Vollstaendige Liste aller Vorgangsarten mit Standard-Nummern und Buchungsparametern: `references/vorgangsarten.md`

### Funktionsuebersicht

| Funktion | Beschreibung | Kontext | Rueckgabe |
|----------|-------------|---------|-----------|
| `fnPost` | Buchen | `rowRead` | Einzelwert |
| `fnReverse` | Stornieren | `rowRead` | Einzelwert |
| `fnConvert` | Wandeln | `rowRead` | **Array** |
| `fnMoveToArchive` | Archivieren | `rowRead` | Einzelwert |

**Alle erfordern:** `mutation` + `rowRead`-Kontext. Leere Belegnummer = fehlgeschlagen.

### Vorgang anlegen mit Positionen

```graphql
mutation @acquireLocks(
  forWriting: [tblTransactions, tblTransactionItems]
  forReading: [tblAddresses, tblProducts]
) {
  tblTransactions {
    rowNew(assignAddress: { kf1AdrNr: { text: "10000" } }) {
      fldArt(set: { text: "Rechnung I" })

      rowSaveAndModify {
        fldBelegNr

        tblTransactionItems {
          pos1: rowNew(assignProduct: { kf1ArtNr: { text: "LUTSCHER" } }) {
            fldMge(set: { float: 10 })
          }
          pos2: rowNew(assignProduct: { kf1ArtNr: { text: "MYSTERYBOX" } }) {
            fldMge(set: { float: 2 })
          }
        }
      }
    }
  }
}
```

**Hinweise:**
- `fldArtNr` akzeptiert Artikelnummern UND Barcodes (Auto-Resolve)
- `fldArt` kann als Nummer (`int: 50`) oder Text (`text: "Rechnung I"`) gesetzt werden
- `fldZeilenNr(set: { int: 0 })` fuegt Position an den Anfang

### Vorgang buchen (`fnPost`)

```graphql
# Bestehenden Vorgang buchen
mutation {
  tblTransactions {
    rowRead(exactMatch: { byBelegNr: { kf1BelegNr: { string: "RE12500005" } } }) {
      fnPost { fldBelegNr }     # Leer = nicht gebucht!
    }
  }
}
```

### Anlegen + Buchen in einer Mutation

```graphql
mutation @acquireLocks(
  forWriting: [tblTransactions, tblTransactionItems]
  forReading: [tblAddresses, tblProducts]
) {
  tblTransactions {
    rowNew(assignAddress: { kf1AdrNr: { text: "10000" } }) {
      fldArt(set: { text: "Rechnung I" })
      rowSaveAndModify {
        fldBelegNr
        tblTransactionItems {
          pos1: rowNew(assignProduct: { kf1ArtNr: { text: "LUTSCHER" } }) {
            fldMge(set: { float: 10 })
          }
        }
        rowSave {                    # WICHTIG: Erst speichern!
          fnPost { fldBelegNr }      # Dann buchen
        }
      }
    }
  }
}
```

### Vorgang stornieren (`fnReverse`)

```graphql
mutation {
  tblTransactions {
    rowRead(exactMatch: { byBelegNr: { kf1BelegNr: { string: "RE12500002" } } }) {
      fnReverse { fldBelegNr }
    }
  }
}
```

### Vorgang wandeln (`fnConvert`)

Gibt ein **Array** zurueck (kann mehrere Vorgaenge erzeugen):

```graphql
mutation {
  tblTransactions {
    rowRead(exactMatch: { byBelegNr: { kf1BelegNr: { string: "AN2500001" } } }) {
      fnConvert(transactionTypeNo: 50, deliveryQuantityHandling: IGNORE) {
        fldBelegNr
      }
    }
  }
}
```

`deliveryQuantityHandling`: `IGNORE` | `KEEP_UNCHANGED` | `RECALCULATE` | `RECALCULATE_IF_ZERO`

### Preisberechnung nach Speichern

```graphql
rowSave {
  acoGPreis {
    totalGrossAmount          # Brutto
    totalNetAmount            # Netto
    totalTaxAmount            # Steuer
  }
}
```

---

## 10. Betragsgruppen (`aco...`)

Kurzbeispiel Lesen: `acoEPr { totalGrossAmount totalNetAmount totalTaxAmount }`

Details (Lesen, Schreiben, Preisberechnung nach Speichern): `references/betragsgruppen.md`

---

## 11. Paginierung (Relay Connection)

```graphql
query ($pageSize: Int = 10, $after: String) {
  tblProducts {
    conRead(first: $pageSize, after: $after) {
      edges {
        cursor
        node { fldArtNr fldSuchBeg }
      }
      pageInfo { hasNextPage endCursor startCursor edgeCount }
    }
  }
}
```

**WICHTIG:** `edgeCount` gibt nur die Anzahl der zurueckgegebenen Edges zurueck, NICHT die Gesamtanzahl der Datensaetze. Es gibt kein `totalCount`-Feld. Zum Zaehlen: `first` mit ausreichend grossem Wert setzen und `hasNextPage` pruefen.

---

## 12. Haeufige Fehler vermeiden

| Fehler | Loesung |
|--------|---------|
| `fnPost` in `rowModify`-Kontext | Nur in `rowRead`-Kontext |
| `fnPost` ohne `rowSave` | Immer `rowSave` vor `fnPost` |
| Schreiben nach `rowSave` im selben Block | Nach `rowSave` nur lesen, oder `rowSaveAndModify` |
| `lnk...` in schreibendem Kontext | Erst `rowSave`, dann `lnk...` im Read-Kontext |
| Mehrere Operatoren in einem Filterobjekt | `and`/`or` verwenden (@oneOf-Regel) |
| `fnMoveToArchive` nach `fnPost` in einer Mutation | Getrennte Mutationen (Auto-Archivierung!) |
| Leere Belegnummer nicht geprueft | Immer `fldBelegNr` in `fn...`-Rueckgabe pruefen |
| `by.../using...` auf `lnk...` statt auf `rowsRead` | Gehoeren auf `rowsRead`/`rowsModify` innerhalb des Links |
| `@store(as: "name")` | Korrekt: `@store(in: $variable)` mit Deklaration in Signatur |
| `"Argument \"set\" is not defined"` | Fehlende Berechtigung - `set` wird ohne Recht nicht angeboten |
| Feldreihenfolge nicht beachtet | Felder werden sequentiell ausgefuehrt - Menge VOR Preis setzen |
| `rowCopy` ohne neuen Schluessel | Kopie braucht eigenen Primaerschluessel |
| `rowsDelete` bricht ab | Ein Fehler bei einem Datensatz → Rollback ALLER Loeschungen |
| `fnConvert` schlaegt fehl → `rowNew` als Workaround | **VERBOTEN!** Bricht die Prozesskette. Fehlerursache klaeren und Nutzer informieren |
| `fnReverse` schlaegt fehl → `rowDelete` als Workaround | **VERBOTEN!** Umgeht Storno-Logik (keine Gegenbuchungen, kein Audit-Trail). Nutzer informieren |
| `fnPost` schlaegt fehl → naechsten Schritt trotzdem ausfuehren | **VERBOTEN!** Folgeschritte (z.B. Wandlung) setzen erfolgreiche Buchung voraus. Nutzer informieren |
| `fnMoveToArchive` schlaegt fehl → manuell Daten kopieren/loeschen | **VERBOTEN!** Archivierung hat eigene Logik. Nutzer informieren |
| Prozessschritte ueberspringen (z.B. direkt RE statt AB→LI→RE) | Nur wenn Nutzer dies explizit bestaetigt. Auf moeglichen Kettenverlust hinweisen |
| `edgeCount` als Gesamtanzahl interpretiert | `edgeCount` zaehlt nur zurueckgegebene Edges, NICHT alle Datensaetze. `first: 0` ergibt immer `edgeCount: 0`. Zum Zaehlen: `first: 100+` und `hasNextPage` pruefen |
| `fldNa2`/`fldOrt`/`fldPLZ`/`fldStr` auf `tblAddresses` | Diese Felder leben in `tblPostalAddresses`, Zugriff ueber `lnkPostalAddresses` |

---

## 13. Troubleshooting

### Fehlermeldung: `"Argument \"set\" is not defined"`

**Ursache:** Fehlende Berechtigung. Der API-Nutzer hat kein Recht, dieses Feld zu setzen.
**Loesung:** Berechtigung im ERP pruefen. Berechtigungs-pflichtige Felder: `fldDat`, `fldVerk`, `fldKredLimit`, `fldInExtBeaKz`, `fldGspKz`, `fldEPreis`.

### Fehlermeldung: `"Address \"10002\" is blocked."`

**Ursache:** Adresse hat `fldGspKz = true` (Gesperrt-Kennzeichen).
**Loesung:** Andere Adresse verwenden oder Sperrung im ERP aufheben.

### Leere Belegnummer nach `fnPost`/`fnReverse`/`fnConvert`

**Ursache:** Funktion konnte nicht ausgefuehrt werden (Voraussetzungen nicht erfuellt).
**Loesung:** Immer Belegnummer pruefen: `fnPost { fldBelegNr }`. Leer = fehlgeschlagen.

### Rollback nach `fnPost` trotz erfolgreicher Buchung

**Ursache:** Eine NACHFOLGENDE Operation in derselben Mutation ist fehlgeschlagen. Alles-oder-Nichts.
**Loesung:** `fnPost` und Folgeoperationen in getrennte Mutationen aufteilen, oder Fehlerquelle beheben.

### `fnPost` hat keine Wirkung (Positionen fehlen)

**Ursache:** `rowSave` vor `fnPost` vergessen. `fnPost` arbeitet nur auf gespeicherten Daten.
**Loesung:** Immer `rowSave { fnPost { fldBelegNr } }` - `rowSave` VOR `fnPost`.

### `lnk...`-Felder nicht verfuegbar

**Ursache:** Datensatz ist noch in schreibendem Kontext (`RowMutationNew/Copy/Modify`).
**Loesung:** Erst `rowSave` aufrufen → wechselt zu `RowMutationRead` → `lnk...` wird verfuegbar.

### Laufzeitfehler nach `rowSave`

**Ursache:** Versuch im selben Block nach `rowSave` noch Felder zu schreiben.
**Loesung:** `rowSaveAndModify` verwenden wenn danach noch geschrieben werden soll, oder alle Schreiboperationen VOR `rowSave` platzieren.

### Deadlock bei parallelen Mutationen

**Ursache:** `@acquireLocks` fehlt oder unvollstaendig.
**Loesung:** `@acquireLocks(forWriting: [...], forReading: [...])` mit ALLEN beteiligten Tabellen.

### fn-Funktion schlaegt fehl (fnConvert/fnPost/fnReverse/fnMoveToArchive)

**Ursache:** Vielfaeltig - fehlende Konfiguration (Wandlungspfad), Beleg bereits archiviert, fehlende Berechtigung, Geschaeftsregel verletzt, Beleg gesperrt.
**Loesung:** STOPP - KEINEN Workaround versuchen! Insbesondere:
- **NICHT** per `rowNew` einen Ersatzbeleg anlegen (bricht Prozesskette)
- **NICHT** per `rowDelete` einen Beleg loeschen statt zu stornieren (umgeht Audit-Trail)
- **NICHT** den naechsten Prozessschritt ausfuehren wenn der aktuelle fehlschlug
Stattdessen: Fehlermeldung dem Nutzer zeigen und gemeinsam klaeren. Moegliche Ursachen:
- Wandlungspfad im ERP nicht konfiguriert → ERP-Administrator muss Pfad freischalten
- Beleg bereits im Archiv → `fnConvert` nur auf aktive Vorgaenge moeglich
- Fehlende Berechtigung → API-Nutzer-Rechte pruefen
- Geschaeftsregel verletzt → Beleg-Daten pruefen (z.B. fehlende Pflichtfelder)

### Query gibt `null` zurueck obwohl Datensatz existiert

**Ursache (in mutation):** `modifyLSN` stimmt nicht ueberein (Optimistic Locking Konflikt).
**Ursache (in query):** Schluessel falsch oder Sortierfolge stimmt nicht.
**Loesung:** `@onNull`-Pattern verwenden um Konflikte abzufangen. Siehe `references/mutation-patterns.md`.
