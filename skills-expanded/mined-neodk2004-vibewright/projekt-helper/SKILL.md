---
name: projekt-helper
description: Macht aus einer einzeiligen Projektidee eine fertige Laufkarte in Obsidian (Interview → Bedarfsanalyse → Plan → Werkzeug-Check → Dashboard, Punkte, Kanban). Der User entscheidet nur an den Gates. Trigger: /projekt-helper <Name> | <Idee in einer Zeile>
---

# Projekt-Helper (Etappe 0)

Der User ist **nur Entscheider**. Du stellst Fragen als Multiple-Choice (AskUserQuestion), schreibst alles selbst und fragst an jedem 🚦-Gate nach Freigabe. Keine langen Chat-Texte: Die Ergebnisse stehen in den Dateien, im Chat nur eine Zeile plus Link.

**Ablage:** siehe Schritt 1 (Obsidian-Vault oder lokaler Ordner) · Alle Texte auf Deutsch mit korrekten Umlauten.
**Dateinamen:** keine Zeichen `: / \ ? * " < > |` (Windows). Doppelpunkte im Titel durch Klammern oder „ – “ ersetzen.
**Fragen bündeln:** Wo es geht, mehrere Fragen in *einem* AskUserQuestion-Aufruf stellen (z. B. Kollision + erste Interviewfragen).

## 1 · Start
- **Ablage bestimmen:** `%APPDATA%/obsidian/obsidian.json` lesen.
  - Genau 1 Vault → diesen nehmen. Mehrere → per AskUserQuestion wählen lassen.
  - **Kein Obsidian** → AskUserQuestion: „Obsidian installieren“ (`winget install Obsidian.Obsidian`, danach Vault `~/Documents/Obsidian/Projekte` anlegen und den User bitten, ihn einmal in Obsidian als Vault zu öffnen) / „Lokal als .md + .html speichern“ (Ablage `~/Documents/KI-ProjektHelper`).
  - Im Folgenden heißt die gewählte Ablage `<Ablage>`.
- **Dataview vorhanden?** `<Ablage>/.obsidian/plugins/dataview/` existiert → Dataview-Tabellen. Sonst (neuer Vault oder lokal) → **statische Tabellen**, die bei jeder Änderung neu geschrieben werden.
- Name und Idee aus den Argumenten lesen (`Name | Idee`). Fehlt etwas → per AskUserQuestion bzw. Freitext nachfragen.
- **Kollision prüfen:** Gibt es `<Ablage>/<Name>/` schon (Groß-/Kleinschreibung egal), wird **nichts überschrieben**. Frage per AskUserQuestion: „Neuen Namen vergeben“ / „Als `<Name> (Test)` anlegen“ / „Abbrechen“.
- Ordner `<Ablage>/<Name>/Punkte/` anlegen.

## 2 · Interview 🚦
- 1–2 Runden mit AskUserQuestion, je Runde höchstens 4 Fragen mit je 2–4 Optionen. Bei Fragen mit mehreren passenden Antworten `multiSelect` setzen.
- Pflicht-Themen: Zielgruppe, Kernnutzen/Muss-Umfang, Plattform/Technik, Erfahrungsstand, Zeitbudget pro Woche, Abgrenzung (was ausdrücklich **nicht**).
- Schon Klares nicht noch einmal fragen. Eine 2. Runde nur, wenn Antworten neue Lücken öffnen.
- **Projekttyp** aus Idee und Antworten ableiten: `code` (es entsteht Software/Firmware) oder `sonstiges` (Video, Hardware-Bau, Event, Lernen …). Bei Unklarheit mitfragen.
- Ergebnis: `<Name>/<Name> – Interview.md` (Frage → Antwort-Tabelle, ganz oben `Projekttyp: code|sonstiges`).

## 3 · Bedarfsanalyse 🚦
Datei `<Name>/<Name> – Bedarfsanalyse.md` mit: **Ziel** (2–3 Sätze), **Rahmen** (Tabelle aus dem Interview), **Muss**, **Kann (später)**, **Nicht-Ziele**, **Risiken** (Tabelle Risiko/Auswirkung/Gegenmaßnahme), **Machbarkeit** (Ampel + 1 Satz).
→ Gate per AskUserQuestion: „Passt so“ / „Ändern (ich sage was)“ / „Abbrechen“. Bei „Ändern“ anpassen und erneut fragen.

## 4 · Plan 🚦
Datei `<Name>/<Name> – Plan.md`: 3–6 Phasen. Pro Phase: Ziel, Ergebnis („fertig, wenn …“), grober Aufwand (klein/mittel/groß). Phase 1 = kleinster lauffähiger Stand.
→ Gate wie oben.

## 5 · Werkzeug-Check 🚦
Prüfen, ob **du (Claude)** und **der Rechner** alles für den Plan haben. Nichts raten, sondern wirklich nachsehen:
- **Skills:** die Liste verfügbarer Skills in deinem Kontext + `~/.claude/skills/`, `.claude/skills/`
- **Plugins:** `~/.claude/plugins/installed_plugins.json`; Katalog: `~/.claude/plugins/marketplaces/claude-plugins-official/.claude-plugin/marketplace.json`
- **MCP:** `claude mcp list < /dev/null`
- **System:** SDKs, Compiler, Git, Laufzeiten, VMs, Windows-Edition usw., je nachdem, was der Plan voraussetzt (`command -v`, `--version`)

Datei `<Name>/<Name> – Werkzeug-Check.md`: Tabelle **Bedarf | Wofür (Phase) | Status ✅/❌/➖ | Quelle | Empfehlung**.
Regeln:
- **Nur offizielle bzw. geprüfte Quellen** (`claude-plugins-official`, Hersteller-Downloads). Alles andere als „ungeprüft“ markieren und nicht empfehlen.
- **Minimal:** nur empfehlen, was eine Phase wirklich braucht. Kein „nice to have“.
- Fehlendes Fachwissen ohne passenden offiziellen Skill/MCP → als „eigener Projekt-Skill (Etappe 2)“ vormerken, nicht erfinden.
- Widersprüche zum Plan (z. B. Werkzeug läuft auf diesem System nicht) **im Plan korrigieren**.
- **Nichts selbst installieren.** → Gate per AskUserQuestion (multiSelect): Welche Empfehlungen installieren/vormerken? Die Auswahl in der Datei abhaken. Installiert wird nur nach ausdrücklichem Ja, sonst landet die Installation als Checklistenpunkt in der passenden Phase.

## 6 · Obsidian-Spiegel
Erst nach Freigabe des Plans und des Werkzeug-Checks schreiben:

**a) Punkte**: eine Datei pro Phase: `<Name>/Punkte/Phase N – <Titel>.md`
```
---
typ: punkt
projekt: <Name>
status: offen            # Phase 1: in-arbeit
bereich: <Bereich>
aufwand: klein|mittel|groß
prio: <N = Phasennummer>
quelle: "<Name> – Plan.md"
erfasst: <heute>
commit: ""            # nur bei Projekttyp code
---
## Ziel
…
## Checkliste
- [ ] konkrete Schritte (3–8)
## Fertig, wenn
…
```

**b) Dashboard** `<Name>/<Name> – Dashboard.md`. Frontmatter:
```
---
typ: projekt
name: <Name>
status: "vorbereitung"
phase: "Phase 1 – <Titel>"
fortschritt: 0
naechster_schritt: "<erster Punkt der Phase-1-Checkliste>"
blocker:
letzte_aktivitaet: <heute>
projekttyp: code|sonstiges
repo: ""              # nur bei Projekttyp code
aktualisiert: <heute>
---
```
Body: `# <Name> – Dashboard`, `← [[Dashboard|Alle Projekte]]` (nur wenn `<Ablage>/Dashboard.md` existiert), ein `>`-Einzeiler, Links auf Interview/Bedarfsanalyse/Plan, `## ➡️ Nächster Schritt`, `## 🔁 Wiedereinstieg` (3 Zeilen: wo stehe ich, was zuletzt passiert ist, womit es weitergeht) und Dataview-Tabellen für `in-arbeit`, `offen` und `erledigt` aus `"<Name>/Punkte"` mit `WHERE typ = "punkt" AND projekt = "<Name>"` (Spalten wie in den anderen Projekt-Dashboards des Vaults: Punkt, Prio, Bereich, Aufwand). Ohne Dataview: dieselben drei Tabellen statisch. Bei `sonstiges` in „Erledigt“ keine Commit-Spalte.

**b2) Nur bei lokaler Ablage (ohne Obsidian):** zusätzlich `<Name>/<Name> – Dashboard.html`: eine eigenständige Seite ohne externe Abhängigkeiten, mit Stand, nächstem Schritt, Wiedereinstieg, Phasen inkl. Checklisten und relativen Links auf die .md-Dateien. Sie wird bei jeder Änderung neu geschrieben.

**c) Kanban** – nur wenn `<Ablage>/Projekte-Kanban.md` existiert: Unter `## Backlog / Rückstand` eine Zeile anhängen:
`- [ ] [[<Name> – Dashboard|<Name>]] – <Kurzbeschreibung> · Phase 1 geplant`
Nur diese Zeile einfügen, nichts anderes im Kanban ändern.

## 7 · Abschluss
Eine Zeile im Chat: was angelegt wurde, plus Pfad zum Dashboard. Danach nichts weiter.

## Nicht in Etappe 0
Harness (CLAUDE.md, Skills, Agents, MCP), Git und ein eigener Code-Ordner: Das kommt in Etappe 2/3.
