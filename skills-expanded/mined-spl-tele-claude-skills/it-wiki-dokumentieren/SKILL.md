---
name: it-wiki-dokumentieren
description: >-
  Bringt Wissen aus beliebigen Quellen (Transkripte, Webseiten,
  Word-Dokumente, Markdown, Notizen, eingefuegter Text) als
  governance-konforme Seite ins produktive IT-Wiki (xwiki.spl-tele.com) -
  findet den richtigen Ort in der 00-99-Struktur, entscheidet neu-anlegen
  vs. bestehende Seite erweitern, waehlt das passende Template, vergibt
  Tags und verifiziert das Ergebnis. Jeder Nutzer authentifiziert sich mit
  seinem eigenen XWiki-Benutzer. Anwenden bei "dokumentiere das im Wiki",
  "ins IT-Wiki uebernehmen", "Doku erstellen aus", "Meeting-Notizen ins
  Wiki", "Anleitung ins Wiki schreiben", "Wiki-Seite ergaenzen",
  /it-wiki-doku.
---

# IT-Wiki dokumentieren (Quelle → richtige Wiki-Seite)

## Zweck

Das Team ist ausgelastet — Dokumentieren muss ein Ein-Kommando-Vorgang
sein: Quelle angeben, kompakten Vorschlag bestaetigen, fertig. Dieser
Skill uebernimmt Extraktion, Ortswahl, Governance und Verifikation.
Genau EIN Bestaetigungs-Gate vor dem Schreiben — nie null (produktives
KM-System), nie mehr als eins (Reibung).

## Vorgehen

### Schritt 1 — Quelle einlesen

| Quelle | Methode |
|--------|---------|
| .md / .txt / Notizen / eingefuegter Text | direkt lesen |
| Webseite (URL) | WebFetch; bei Bot-Schutz: Browser oder Nutzer um Kopie bitten |
| .docx | Word-Extraktion (docx-Skill oder `pandoc -t markdown`); eingebettete Bilder fuer Schritt 5 extrahieren |
| Meeting-/Video-Transkript (Text) | direkt lesen; bei Rohtranskript zuerst inhaltlich verdichten (Entscheidungen, Anleitungsschritte, Fakten — kein Wortprotokoll ins Wiki) |
| Audio/Video ohne Transkript | NICHT direkt verarbeitbar — zuerst Transkript erstellen lassen |

Aus der Quelle extrahieren: Was ist das dokumentationswuerdige Wissen?
(Anleitung? Prozess? Systembeschreibung? Bekannter Fehler? Begriff?)
Eine Quelle kann MEHRERE Wiki-Seiten ergeben — Governance-Grundregel
"eine Frage pro Seite" schlaegt "alles auf eine Seite".

### Schritt 2 — Ort finden (Pflicht: erst suchen, dann entscheiden)

1. **Duplikat-/Anknuepfungssuche** (immer, vor jeder Neuanlage):
   ```
   GET {WIKI}/rest/wikis/xwiki/query?q=<kernbegriffe>&type=solr&number=15
   ```
   Treffer lesen (mind. Titel + Kurzkontext). Existiert eine Seite zum
   Thema → **erweitern statt neu anlegen**.
2. **Bereich nach Strukturlandkarte** bestimmen:

| Inhalt | Bereich |
|--------|---------|
| Eskalation, Wiederanlauf, Backup/Restore, Runbooks | `IT-Wiki.00-Notfall` |
| Datenlebenszyklus: Quellsysteme, Ingestion/Lakehouse, ETL, Reporting/PowerBI-Arbeitsbereiche, Datenaustausch/Schnittstellen, Daten-Governance, KI-Use-Cases auf Datenebene | `IT-Wiki.01-Data.<Creation|Ingestion|Processing|Reporting|Exchange-und-Movement|Governance|AI>` |
| Ein Tool/eine Software: Zweck, Zugang, Konfiguration, Anleitungen | `IT-Wiki.02-Tools.<Toolname>` (grosse Tools haben eigenen Space: Rimo, Odoo, Jira, Fabric, PowerBI, Microsoft-365, Intune, Azure, Board...; sonstige Software unter `02-Tools.Software.<Name>`) |
| Server, Netzwerk, Hardware, Telefonie, Standorte | `IT-Wiki.03-Infrastruktur.<Server|Netzwerk|Hardware|Telefonie>` |
| Abteilungsprozesse, Organisation, Onboarding, Fremdfirmen | `IT-Wiki.04-Abteilung-IT.<Prozesse|Organisation|Admin|Fremdfirmen>` |
| Bekannter Fehler: Symptom → Ursache → Loesung | `IT-Wiki.05-KEDB` (Name: `KE-XXXX-<Kurzname>`, naechste freie Nummer per Suche ermitteln) |
| Zugaenge, Berechtigungskonzepte, Security-Themen | `IT-Wiki.06-Security-und-Compliance` |
| Begriff/Abkuerzung | `IT-Wiki.07-Glossar.<Begriff>` |
| Veraltetes | `IT-Wiki.99-Archiv` (nur auf ausdrueckliche Anweisung) |

3. Tool-Doku, die einen Fehler beschreibt → KEDB-Eintrag PLUS Verweis
   von der Tool-Seite ("Bekannte Fehler").

### Schritt 3 — Neu vs. Erweitern

- **Erweitern**, wenn eine Seite dieselbe Frage behandelt: Content per
  GET holen, neuen Inhalt an der logisch richtigen Stelle integrieren
  (nicht anhaengen!), Widersprueche zugunsten der neuen Quelle
  aufloesen und ALT-Angaben korrigieren, Status-Footer-Datum
  aktualisieren.
- **Neu**, wenn keine Seite die Frage behandelt: Template waehlen —
  Tool-Seite → `Template-Tool`, Ablauf/Prozess → `Template-Prozess`,
  Datenfluss zwischen Systemen → `Template-Schnittstelle`,
  Fehler+Loesung → `Template-KnownError`, Glossarbegriff → Muster der
  bestehenden `07-Glossar`-Seiten. Template-Inhalt zur Laufzeit aus dem
  Wiki holen (nie aus dem Gedaechtnis):
  ```
  GET {WIKI}/rest/wikis/xwiki/spaces/IT-Wiki/spaces/Vorlagen/spaces/<Template>/pages/WebHome
  ```
  Alle `_(Platzhalter)_` befuellen oder Zeile entfernen — keine leeren
  Platzhalter veroeffentlichen. Prozesse als Mermaid-Diagramm mit einem
  Satz Kontext davor. Status-Footer: `Status: Entwurf · Owner: <Autor
  bzw. Quelle> · Letzter Review: <heutiges Datum>`.

### Schritt 4 — Governance anwenden (verbindlich)

- **Page-Name**: keine Leerzeichen-Fehler, keine Umlaute, sprechend,
  Bindestriche (`Gateway-neu-starten`). Nummern-Praefix nur Top-Level.
- **Titel** = die Frage, die die Seite beantwortet ("PowerBI Gateway
  neu starten", nicht "PowerBI Wartung"). Umlaute im Titel erlaubt.
- **Tags**: 2–4 aus dem festen Vokabular — System: rimo odoo jira
  powerbi fabric sharepoint power-automate teams azure board ses uipath
  intune microsoft-365 windows telefonie · Typ: anleitung prozess
  architektur schnittstelle governance glossar referenz · Domaene:
  finanzen useradministration security reporting onboarding notfall.
  KEINE neuen Tags erfinden.
- **Sprache**: Deutsch oder Englisch, innerhalb der Seite nicht mischen.
- Text statt Screenshot, wo der Inhalt es erlaubt (KI-Tauglichkeit).

### Schritt 5 — Vorschlag zeigen (das eine Gate)

Kompakt an den Auftraggeber, dann auf Ok warten:

> **Vorschlag:** [NEU aus Template-X | ERWEITERN] `IT-Wiki.<voller.Pfad>`
> **Titel:** ... · **Tags:** a, b, c
> **Inhalt (Kurzfassung):** 3–5 Zeilen was auf die Seite kommt
> *(bei Erweiterung: was sich aendert; bei mehreren Seiten: Liste)*

### Schritt 6 — Schreiben (nach Ok)

**Grundsatz Authentifizierung (verbindlich fuer alle Modi):** Jeder
Nutzer schreibt mit seinem EIGENEN XWiki-Benutzer — nie mit einem
geteilten Admin- oder Service-Account. XWiki protokolliert den
authentifizierten Benutzer als Autor jeder Version; nur so bleibt der
Audit-Trail (wer hat was geaendert) korrekt. Voraussetzung: Der Nutzer
hat einen XWiki-Account mit Schreibrecht im IT-Wiki (legt der
XWiki-Admin an). Credential-Werte niemals im Chat erfragen, ausgeben
oder in Dateien schreiben.

**Ausfuehrungsmodus zuerst bestimmen:**

- **Claude Code** (Shell verfuegbar, Rechner im SPL-Netz): Befehle selbst
  ausfuehren. Credentials aus den User-Umgebungsvariablen `XWIKI_USER` /
  `XWIKI_PASSWORD` lesen (zur Laufzeit in der Shell, Fallback Registry
  `HKCU:\Environment`, falls der Prozess frisch gesetzte Vars noch nicht
  geerbt hat). Werte nie ausgeben. Sind die Variablen nicht gesetzt →
  Erstkonfiguration (siehe unten) durchfuehren lassen, dann fortsetzen.
- **Claude Desktop / claude.ai** (keine Shell bzw. Sandbox OHNE
  Intranet-Zugriff): NICHT versuchen, das Wiki direkt zu erreichen.
  Stattdessen fertige **PowerShell-Befehle generieren**, die der Nutzer
  lokal einfuegt, und ihn bitten, die Ausgabe zurueckzugeben. Login-Block
  einmal pro Sitzung — nutzt die persoenlichen Env-Vars, falls gesetzt,
  sonst interaktive Abfrage (Passwort bleibt beim Nutzer, nie im Chat):
  ```powershell
  if ($env:XWIKI_USER -and $env:XWIKI_PASSWORD) {
      $b = [Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes(
           "$($env:XWIKI_USER):$($env:XWIKI_PASSWORD)"))
  } else {
      $cred = Get-Credential   # eigenen XWiki-Login eingeben
      $b = [Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes(
           "$($cred.UserName):$($cred.GetNetworkCredential().Password)"))
  }
  $H = @{Authorization = "Basic $b"}
  ```
  Danach jeden REST-Aufruf als `Invoke-RestMethod -Headers $H ...`
  generieren (Suche → Nutzer liefert Treffer zurueck → Vorschlag →
  Schreiben → Verifikation). Ein Schritt pro Block, kopierfertig.

**Erstkonfiguration (einmal pro Kollege und Rechner):** Den folgenden
Block gibt der Nutzer SELBST in einem eigenen PowerShell-Fenster ein
(nicht Claude ausfuehren lassen — das Passwort soll nie durch den
Modell-Kontext laufen). In Claude Code geht das direkt in der Session
mit dem Prefix `!`:
  ```powershell
  $u = Read-Host "XWiki-Benutzername"
  $p = Read-Host "XWiki-Passwort" -AsSecureString
  $pp = [Runtime.InteropServices.Marshal]::PtrToStringAuto(
        [Runtime.InteropServices.Marshal]::SecureStringToBSTR($p))
  [Environment]::SetEnvironmentVariable("XWIKI_USER", $u, "User")
  [Environment]::SetEnvironmentVariable("XWIKI_PASSWORD", $pp, "User")
  Remove-Variable p, pp
  "Gespeichert. Claude Code/Desktop neu starten, damit die Variablen greifen."
  ```
  Danach Login-Test: `GET {WIKI}/rest/wikis/xwiki/spaces/IT-Wiki/pages/WebHome`
  mit Basic Auth muss HTTP 200 liefern (nur Statuscode berichten).

`{WIKI}` = `http://xwiki.spl-tele.com`.

```bash
# Seite anlegen/ersetzen (nested: je Ebene /spaces/<Name>, dann /pages/WebHome)
PUT {WIKI}/rest/wikis/xwiki/spaces/IT-Wiki/spaces/<...>/pages/WebHome
    Content-Type: application/xml, Basic Auth
    Body: <page xmlns="http://www.xwiki.org"><title>..</title>
          <syntax>xwiki/2.1</syntax><content>..</content></page>
# Tags setzen
PUT .../pages/WebHome/tags   Content-Type: application/x-www-form-urlencoded
    Body: tags=a,b,c
# Bilder/Dateien anhaengen
PUT .../pages/WebHome/attachments/<dateiname>  (Body = Binaerdaten)
```
Details, Fallstricke und Python-Rezepte: siehe Skill
[xwiki-instance-migration](../xwiki-instance-migration/SKILL.md).

### Schritt 7 — Verifizieren (nie ueberspringen)

1. `GET {WIKI}/bin/view/<Pfad>/` als **Gast** → HTTP 200, kein
   "unknown macro", Bilder laden (Stichprobe `<img src>` → HTTP 200).
2. Tags-GET → gesetzte Tags vorhanden (`name`-Attribut im XML!).
3. Bei Erweiterung: Versionsnummer erhoeht, kein Altinhalt verloren
   (Diff der Abschnitte).
4. **Autor-Check**: `GET {WIKI}/rest/wikis/xwiki/spaces/.../pages/WebHome`
   → `<author>` der neuen Version ist der EIGENE XWiki-Benutzer (nicht
   Admin/Service-Account). Weicht der Autor ab → Credentials pruefen,
   nicht weiterarbeiten.
5. Dem Auftraggeber den Link liefern: `{WIKI}/bin/view/<Pfad>/`.

## Faktenbasis

Faktenregister `.claude/research/2026-07-17-xwiki-migration-coolify.md`
(REST-Rezepte Fakten 29, 32; Tags-Handling; Auth 13). Governance,
Strukturlandkarte und Templates am 2026-07-17 direkt aus dem
Produktiv-Wiki gelesen (IT-Wiki.Wiki-Governance, IT-Wiki.Vorlagen.*,
Bereichs-Beschreibungen) — Stufe A.

## Prüfkriterien

- Duplikatsuche wurde VOR der Ortswahl ausgefuehrt (Solr-Query belegbar).
- Genau ein Bestaetigungs-Gate; Vorschlag enthielt Ort, Titel, Tags,
  Kurzinhalt.
- Ergebnis-Seite: Template-Struktur befuellt (keine leeren Platzhalter),
  Titel als Frage, 2–4 Vokabular-Tags, Status-Footer mit Datum.
- Gast-Render-Check + Tag-Check bestanden, Link geliefert.

## Bekannte Fallstricke

- **Nested Pages**: `IT-Wiki.X.Y` ist REST-seitig
  `/spaces/X/spaces/Y/pages/WebHome` — ein `/pages/Y` liefert 404
  (Templates sind z. B. verschachtelt!).
- **Rohtranskripte nie 1:1 uebernehmen** — verdichten; Wortprotokolle
  gehoeren nicht in die Knowledge Base.
- **Sammelseiten vermeiden**: lieber 3 kleine Seiten mit klaren Fragen
  als eine grosse ("eine Frage pro Seite").
- **Tags nur aus dem Vokabular** — neue Tags zerstoeren die
  Verwandte-Themen-Logik und die Tag-Cloud-Konsistenz.
- **Template-Platzhalter**: `_(...)_ ` stehen lassen sieht fertig aus,
  ist aber leer — befuellen oder Zeile streichen.
- **grep -c auf einzeiligem XML zaehlt Zeilen, nicht Treffer** — fuer
  Checks `grep -o | wc -l` oder XML-Parser.
- **Vertrauliches**: Passwoerter/Tokens aus Quellen NIEMALS ins Wiki —
  stattdessen "liegt im Keepass/Infisical" schreiben. Quelle mit
  Personendaten → nur das fachlich Noetige uebernehmen.
- Basic Auth funktioniert nur fuer `/rest/...`; `/bin/view` verifiziert
  man als Gast (Admin wird ggf. zum Distribution Wizard umgeleitet).

## Installation (pro Kollege)

1. **Claude Code** (empfohlen): Repo klonen und Skill-Ordner kopieren —
   ```powershell
   git clone https://github.com/spl-tele/Claude_Skills.git
   Copy-Item -Recurse "Claude_Skills\skills\it-wiki-dokumentieren" "$HOME\.claude\skills\"
   ```
   Claude Code laedt den Skill beim naechsten Start automatisch.
2. **Claude Desktop**: dasselbe Ziel `%USERPROFILE%\.claude\skills\`;
   alternativ das fertige Paket `dist\it-wiki-dokumentieren.zip` aus dem
   Repo in den Einstellungen unter Skills/Faehigkeiten hochladen (sofern
   die installierte Version den Zip-Upload anbietet).
3. Erstkonfiguration aus Schritt 6 ausfuehren (eigener XWiki-Account +
   Env-Vars), Login-Test bestehen — fertig.

## Versionshistorie

- v1.2 (2026-07-24): Frontmatter-YAML repariert (Doppelpunkt in
  unquotierter description brach strikte Parser, z. B. GitHub-Rendering;
  jetzt Folded Scalar). Authentifizierung auf persoenliche
  XWiki-Benutzer umgestellt: geteilte Admin-Credentials aus dem Skill
  entfernt, stattdessen `XWIKI_USER`/`XWIKI_PASSWORD` als
  User-Env-Vars je Kollege plus Get-Credential-Fallback; neue
  Erstkonfigurations-Anleitung und Autor-Check in der Verifikation
  (Audit-Trail: jede Aenderung laeuft unter dem echten Benutzer).
  Installations-Abschnitt fuer die Team-Verteilung ergaenzt.
- v1.1 (2026-07-17): Claude-Desktop-Modus ergaenzt (PowerShell-Bridge:
  Skill generiert kopierfertige Invoke-RestMethod-Bloecke, Nutzer fuehrt
  lokal aus — noetig, weil die Desktop-Sandbox keinen Intranet-Zugriff
  hat). Get-Credential-Login haelt das Passwort aus dem Chat.
- v1.0 (2026-07-17): Erstellt fuer Aufgabe "Doku-Zufuhr ins neue
  IT-Wiki so einfach wie moeglich"; End-to-End in Sandbox getestet.
