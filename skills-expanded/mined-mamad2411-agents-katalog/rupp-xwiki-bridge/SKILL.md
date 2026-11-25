---
name: rupp-xwiki-bridge
description: PowerShell-basierte Bridge zum SPL Tele XWiki (http://10.13.18.141:8080). Generiert New-XWikiPage/Get-XWikiPage/Search-XWiki/Update-Befehle, die Dimitri direkt in PowerShell ausführt. Trigger-Phrasen Deutsch und Englisch, Beispiele Wiki-Seite erstellen, Page ins Wiki schreiben, Wiki durchsuchen, KEDB-Lookup, Wiki-Doku anlegen, SPL Tele Wiki, XWiki-Inhalt, neue Wiki-Page, Wiki erweitern, Wiki aktualisieren, lies aus dem Wiki, schreibe ins Wiki, dokumentiere im Wiki, Wiki-Eintrag, Anleitung im Wiki, Knowledge Base, KEDB. Nutze diesen Skill immer wenn Dimitri Wiki-Inhalte erstellen, aktualisieren, durchsuchen oder lesen möchte — auch proaktiv wenn aus einem anderen Kontext (Ticket, Meeting, Troubleshooting) etwas im Wiki dokumentiert werden soll.
---

# Rupp XWiki Bridge

## Kontext und Zweck

Dimitri arbeitet bei SPL Tele und nutzt deren internes XWiki als zentrales
Wissens-Repository. Da das XWiki nur im internen SPL-Tele-Netz erreichbar ist
(`10.13.18.141`) und Claude Desktop auf seinem Arbeitsrechner nicht installiert
werden darf, läuft die Mensch-KI-Symbiose über ein PowerShell-Toolkit:

- **Claude generiert** vollständige PowerShell-Befehle mit Content
- **Dimitri kopiert und führt aus** — ein Klick, fertig
- **PowerShell-Toolkit** kapselt Form-Token-Handling, URL-Encoding,
  Credential-Speicherung

Dieser Skill enthält das gesamte operative Wissen, damit Claude sofort
produktive Befehle generieren kann ohne Rückfragen zu Tool-Pfad, Wiki-Struktur
oder Syntax.

## Technische Basis

| Aspekt | Wert |
|---|---|
| XWiki-Instanz | `http://10.13.18.141:8080` |
| XWiki-Version | 17.10.4 |
| Toolkit-Pfad | `C:\Users\ruppd\OneDrive - SPL TELE\UiPath\Tools\XWiki\XWiki-Toolkit.ps1` |
| Toolkit-Version | 1.0.0 (Stand 2026-05-21) |
| Auto-Load | Via PowerShell-Profile bei jedem Start geladen |
| Credentials | DPAPI-verschlüsselt in `C:\Users\ruppd\.xwiki-credentials.xml` |
| Service-User | `ruppd` |
| Content-Syntax | `xwiki/2.1` (Default) |

## Verfügbare Toolkit-Funktionen

### New-XWikiPage

Erstellt eine neue Page ODER aktualisiert eine bestehende (XWiki nutzt PUT für beides).

```powershell
New-XWikiPage `
    -Title       "Display-Titel der Page" `
    -ParentSpace "Pfad/zum/Parent" `
    -Content @"
== Heading ==
Content in XWiki-Syntax 2.1
"@
```

Optional: `-PageName "URL_safe_name"` (Default: Title mit Spaces zu Unterstrichen)

**Wichtig:** `ParentSpace` ist der Container, in dem die neue Page landen soll —
NICHT inklusive der neuen Page selbst.

### Get-XWikiPage

Liest Inhalt und Metadata einer Page.

```powershell
$page = Get-XWikiPage -ParentSpace "..." -PageName "..."
$page.title       # Display-Titel
$page.content     # Roh-Content in XWiki-Syntax
$page.modified    # Unix-Timestamp ms
$page.author      # z.B. "XWiki.ruppd"
$page.version     # z.B. "6.1"
```

PageName muss der technische Name sein (URL-Slug), nicht der Display-Titel.
Bei Unklarheit zuerst `Search-XWiki` nutzen.

### Search-XWiki

Solr-basierte Suche über alle Pages. Schnell und robust.

```powershell
Search-XWiki -Query "Suchbegriff" -MaxResults 20
```

Für Title-Search präzise: `-Query 'title:"Mein Begriff"'`

Output enthält pro Treffer: `title`, `space`, `pageName`, `wiki`, `type`,
`modified`, `version`. Aus `space` + `pageName` kann der vollständige Pfad
rekonstruiert werden.

### Test-XWikiConnection

Smoketest. Sollte Dimitri bei Verbindungsproblemen ausführen.

## Wiki-Struktur — Reale Reference-Namen

**KRITISCH:** Die Wiki-Struktur hat über Jahre gewachsene Namenskonventionen
mit teils problematischen Sonderzeichen. Verwende IMMER die hier dokumentierten
Reference-Namen, nicht die UI-Bezeichnungen.

### Top-Level-Spaces

```
xwiki:Archiv                    Veraltete Inhalte, read-only
xwiki:Help                      XWiki-eigene Hilfe (Standard)
xwiki:Main                      XWiki-Standard-Root
xwiki:Sandbox                   XWiki-Standard-Test
xwiki: - Wiki Neu -             Produktiver Haupt-Space (Anzeige: "SPL TELE WIKI")
xwiki:XWiki                     XWiki-Konfiguration
```

### Produktiver Haupt-Space " - Wiki Neu -"

Diese Sub-Spaces sind die "echten" Bereiche der SPL Tele Doku. Beachte
die Naming-Anomalien!

```
 - Wiki Neu -
├── 2. Prozesse                          (Punkt im Namen, wird zu "2\. Prozesse")
├── 3. Hardware
├── 5. Fremdfirmen
├── ABK
├── AI                                   (TRAILING SPACE "AI " — kritisch!)
│   ├── Fuhrpark
│   ├── KI Server
│   ├── UiPath
│   │   ├── Erste Einstellungen in UiPath Studio
│   │   ├── First Settings
│   │   ├── Kickoff Meeting Notes Part I
│   │   ├── NOC Use Case
│   │   ├── VPN Connection Forti Net
│   │   └── XWiki Connector fuer UiPath
│   └── Vibecoding  Lovable              (doppeltes Leerzeichen!)
├── Aufgaben Betriebsurlaub
├── BE
├── Besprechungsröume                    (Tippfehler: sollte "räume" sein)
├── FAQ  Troubleshooting                 (DOPPELTES LEERZEICHEN!)
│   ├── Entra
│   ├── Intune
│   ├── Microsoft Office
│   │   ├── Bookings
│   │   ├── Excel
│   │   ├── Outlook
│   │   ├── Teams
│   │   └── Word
│   ├── Microsoft Pureview (ehemals Compliance)
│   ├── Netzwerk  Infrastruktur          (DOPPELTES LEERZEICHEN!)
│   ├── Office
│   ├── Parkplatz Switch MassResponse
│   ├── Security Center + Endpoint Defender
│   ├── Server  Infrastruktur            (DOPPELTES LEERZEICHEN!)
│   │   └── Active Directory
│   ├── Smart Warehouse
│   ├── Software
│   │   ├── BMD
│   │   ├── CodeTwo
│   │   ├── ELBA
│   │   ├── Jira
│   │   └── (viele weitere)
│   ├── Telefonie
│   │   ├── Callflows (dokumentiert)
│   │   └── Smartphone
│   ├── Übersicht Shared Mailboxen
│   └── Windows
├── RiMo
│   └── Rimo DWH
├── test2                                (Test-Space, sicher für Experimente)
├── Wichtige Links
└── Wichtige Telefonnummern
```

### Naming-Anomalien (kritisch!)

Die folgenden Anomalien führen zu API-Fehlern, wenn man sie falsch tippt:

| Anomalie | Korrekte Schreibweise | Falsch |
|---|---|---|
| Trailing Space in AI | `"AI "` | `"AI"` |
| Doppelte Leerzeichen | `"FAQ  Troubleshooting"` | `"FAQ Troubleshooting"` |
| Doppelte Leerzeichen | `"Server  Infrastruktur"` | `"Server Infrastruktur"` |
| Doppelte Leerzeichen | `"Netzwerk  Infrastruktur"` | `"Netzwerk Infrastruktur"` |
| Führende/folgende Spaces | `" - Wiki Neu -"` | `"- Wiki Neu -"` oder `"Wiki Neu"` |
| Punkt im Namen | `"2. Prozesse"` | `"2 Prozesse"` |
| Umlaut-Tippfehler | `"Besprechungsröume"` (so existiert es) | `"Besprechungsräume"` |

Bei Unklarheit IMMER zuerst `Search-XWiki` aufrufen, um den exakten
Reference-Namen zu finden — niemals raten oder annehmen.

## Standard-Workflow-Patterns

### Pattern 1: Neue Page erstellen

Anwendungsfall: Dimitri möchte eine neue Wiki-Seite anlegen.

```powershell
New-XWikiPage `
    -Title       "Mein neuer Titel" `
    -ParentSpace " - Wiki Neu -/FAQ  Troubleshooting/Software" `
    -Content @"
== Übersicht ==
[Kurze Einleitung]

== Problem ==
[Symptom-Beschreibung]

== Lösung ==
[Schritte]

== Verwandte Themen ==
* [[link>>doc: - Wiki Neu -.FAQ  Troubleshooting.Software.BMD.WebHome]]
"@
```

### Pattern 2: Bestehende Page lesen und aktualisieren (Read-Modify-Write)

Anwendungsfall: Dimitri will eine existierende Seite erweitern.

**Schritt 1 (Claude generiert):**
```powershell
$page = Get-XWikiPage -ParentSpace "..." -PageName "..."
$page.content
```

**Schritt 2:** Dimitri führt aus, kopiert Output in nächste Claude-Nachricht.

**Schritt 3 (Claude generiert):** Kompletten neuen Content (alt + neu zusammengeführt)
als `New-XWikiPage`-Aufruf mit gleichem Title/Pfad → führt zu Update.

### Pattern 3: KEDB-Lookup für aktuelles Problem

Anwendungsfall: Dimitri löst gerade ein Problem und will wissen, ob schon
dokumentiert.

```powershell
Search-XWiki -Query "Suchbegriff" | Select-Object title, space, type | Format-Table -AutoSize
```

Bei vielen Treffern: zusätzlich nach Space filtern oder Title-Search nutzen:
```powershell
Search-XWiki -Query 'title:"Outlook"' -MaxResults 10
```

### Pattern 4: Page lesen für gemeinsame Diskussion

Anwendungsfall: Dimitri will mit Claude über existierenden Inhalt sprechen.

```powershell
$page = Get-XWikiPage -ParentSpace "..." -PageName "..."
$page.content
```

Output wird in Claude-Chat eingefügt, dann diskutiert.

## XWiki-Syntax 2.1 Cheatsheet

| Element | Syntax |
|---|---|
| Heading 1 | `= Heading =` |
| Heading 2 | `== Heading ==` |
| Heading 3 | `=== Heading ===` |
| Bold | `**text**` |
| Italic | `//text//` |
| Underline | `__text__` |
| Monospace | `##code##` |
| Bullet List | `* Item` (eingerückt mit ** für Sub-Level) |
| Numbered List | `1. Item` (oder `1.1.` für Sub) |
| Link extern | `[[Text>>https://url]]` |
| Link intern | `[[Text>>doc:Space.Page]]` |
| Code-Block | `{{code language="bash"}}...{{/code}}` |
| Info-Box | `{{info}}Text{{/info}}` |
| Warning-Box | `{{warning}}Text{{/warning}}` |
| TOC | `{{toc/}}` |
| Datum (auto) | `{{date/}}` |
| Tabelle | `\|=Header\|=Header2\|<br>\|Cell1\|Cell2\|` |
| Page-Include | `{{include reference="Space.Page" /}}` |
| Horizontale Linie | `----` |
| Bild | `[[image:filename.png]]` (Anhang an Page) |

## Best Practices für Content-Generierung

Wenn Claude Wiki-Content generiert, gelten diese Qualitätsstandards
(abgeleitet aus Dimitri's KI-Mentoring-Charta):

1. **Klare Struktur** — Übersicht, Hauptteil, Verwandtes/Referenzen
2. **TOC bei längeren Pages** — `{{toc/}}` am Anfang
3. **Faktenbasis** — keine Spekulation, klare Quellenangabe bei externen Infos
4. **Reputations-Mandat** — jede Page repräsentiert Qualitätsstandard von SPL Tele
5. **Verlinkung** — wo sinnvoll auf verwandte Pages verweisen
6. **Maintainer-Footer** — bei Doku-Pages am Ende: Autor, Datum, Version
7. **Code in Code-Blöcken** — niemals als Plaintext-Befehl, immer `{{code}}...{{/code}}`
8. **Keine englischen Anglizismen** wenn deutsche Begriffe verfügbar
9. **Umlaute korrekt** — nicht ä/ö/ü vermeiden, im Content sind sie OK
   (NUR im PowerShell-Heredoc vorsichtig sein wegen Encoding)

## Verhalten in der Session

### Wenn Dimitri sagt "Erstelle eine Wiki-Page..."

1. **Klärung der Verortung** — falls ParentSpace nicht explizit genannt:
   bei klarem Thema vorschlagen, bei Unklarheit nachfragen
2. **Content vollständig generieren** — kein „...weitere Inhalte hier"
3. **PowerShell-Befehl als geschlossener Code-Block** — copy-paste-ready
4. **KEINE Erklärung wie der Befehl funktioniert** unless asked — Dimitri kennt das

### Wenn Dimitri sagt "Was haben wir zu X im Wiki?"

1. `Search-XWiki`-Befehl generieren
2. Nach Output: Treffer analysieren, gezielt zur relevanten Page hinleiten
3. Auf Wunsch: vollständigen Content via `Get-XWikiPage` lesen

### Wenn Dimitri sagt "Aktualisiere Seite X um Y"

1. Erst `Get-XWikiPage`-Befehl generieren
2. Auf Output warten (Dimitri kopiert ihn rein)
3. Vollständigen neuen Content generieren (alt + neu sauber integriert)
4. `New-XWikiPage`-Befehl mit identischem Title/ParentSpace generieren
   → bewirkt Update (HTTP 202)

### Wenn ein Befehl fehlschlägt

| HTTP | Wahrscheinliche Ursache | Vorgehen |
|---|---|---|
| 401 | Credentials abgelaufen | `Initialize-XWikiCredential` empfehlen |
| 403 | Form-Token-Cache abgelaufen | Befehl einfach erneut ausführen |
| 404 | Pfad oder PageName falsch | `Search-XWiki` zur Verifikation |
| 500 | Server-Fehler XWiki | Nochmals, ansonsten Admin kontaktieren |

## Sicherheits- und Compliance-Hinweise

- Toolkit nutzt Service-User `ruppd` mit Passwort in DPAPI-Store. Nicht in Outputs erwähnen.
- Bei Schreib-Operationen prüfen, ob Content sensitive Informationen enthält
  (Kennwörter, PIDs, persönliche Daten) — falls ja: Dimitri vorab warnen,
  Verschleierung vorschlagen.
- Bei kritischen Pages (Org-Diagramme, Compliance-Docs): vor Update-PUT
  Bestätigung einholen, nicht stillschweigend überschreiben.

## Verbundene Assets

| Asset | Bezug |
|---|---|
| UiPath Custom Connector "XWiki" v1.1.0 | Active im SPL Tele Tenant, für künftige Bot-Workflows |
| UiPath Connection "XWiki SPL Tele Prod" | Connected, Service-User ruppd |
| UiPath Folder "XWiki Automations" | Tool Automations Subfolder, leer aktuell |
| UiPath PAT "claude-desktop-mcp-xwiki" | 90-Tage-Ablauf 2026-08-19, Rotation-Reminder 2026-08-04 |
| Wiki-Page "XWiki Connector fuer UiPath" | Doku der Connector-Konfiguration, erstellt 2026-05-21 |

## Versionierung dieses Skills

- **v1.0.0** (2026-05-21) — Initiale Version. Erfasst Toolkit v1.0.0,
  vollständige Wiki-Struktur, Naming-Anomalien, alle vier Standard-Patterns.
  Erstellt nach erster erfolgreicher End-to-End-Validierung.
