# Skill fuer die Ausfuehrung der Bookly CLI erstellen

## Ziel
Erstelle einen wiederverwendbaren Skill, der die standardisierte Ausfuehrung der Bookly CLI in diesem Repository beschreibt, inklusive Preconditions, Befehlen, Validierung und Fehlerbehandlung.

## Kontext
- Repository basiert auf .NET und enthaelt ein CLI-Projekt unter `src/Bookly.Cli`.
- Agenten sollen CLI-Befehle reproduzierbar, sicher und ohne implizites Wissen ausfuehren koennen.
- Der Skill soll als operative Anleitung fuer Implementierung, Verifikation und Troubleshooting dienen.

## Aufgabe
Erstelle einen neuen Skill namens `bookly-cli-execution` mit einer `SKILL.md` Datei (inkl. sauberer Frontmatter), der mindestens folgende Punkte abdeckt:

1. **Use when / Trigger-Phrasen**
- Eindeutige Trigger fuer CLI-Ausfuehrung, z. B. "bookly cli ausfuehren", "cli command testen", "bookly command run", "cli smoke test".

2. **Voraussetzungen**
- Benoetigte Pfade, z. B. `src/Bookly.Cli`.
- Erforderliche Runtime/Tools (dotnet SDK, ggf. Aspire-Kontext falls relevant).
- Hinweise zu Konfiguration (`appsettings*.json`, Secrets niemals hardcoden).

3. **Standard-Workflow fuer Ausfuehrung**
- Build-Schritt.
- Beispielhafte Ausfuehrung von Commands (CRUD-Szenarien).
- Umgang mit Exit-Codes (0/1/2) entsprechend CLI-Konvention.
- Saubere Struktur fuer Parameter und Output-Formate (`table`, `json`, `csv`).

4. **Verifikation**
- Welche Tests bei CLI-Aenderungen mindestens auszufuehren sind.
- Wie Erfolg/Misserfolg eindeutig beurteilt wird.
- Welche Logs/Artefakte bei Fehlern zu pruefen sind.

5. **Troubleshooting**
- Typische Fehlerbilder (Konfiguration, DB-Verbindung, Validierung, Timeout).
- Konkrete, sichere Recovery-Schritte.

6. **Qualitaetskriterien**
- ASCII-only, klare Struktur, kurze und praezise Handlungsanweisungen.
- Keine widerspruechlichen oder projektspezifisch falschen Annahmen.
- Konsistent mit `AGENTS.MD` (Security, Testing, Aspire/Podman-Regeln).

## Definition of Done
- Skill ist an einem gueltigen Skill-Pfad erstellt.
- Frontmatter ist valide und Discovery-tauglich (`name`, `description` mit klaren Triggern).
- Workflow ist sofort ausfuehrbar und deckt Build, Run, Verify, Troubleshoot ab.
- Inhalt ist auf die reale Bookly-CLI zugeschnitten und nicht generisch gehalten.
