---
name: cc-prompt-builder
description: >
  Erstellt detaillierte, autonome Claude Code (CC) Prompts mit Self-Fix-Protokoll.
  Nutze diesen Skill IMMER wenn der User einen CC-Prompt, Claude Code Prompt oder
  Delegations-Prompt für eine mehrstufige Implementierung braucht. Trigger auch bei:
  "Prompt für CC", "lass CC das machen", "mach einen Prompt draus", "CC soll das autonom
  abarbeiten", "delegate an Claude Code", "Sonnet-Prompt", "autonomer Prompt".
  Der Skill erzeugt token-effiziente Prompts die mit günstigeren Modellen (Sonnet)
  funktionieren, weil sie präzise genug sind um Rückfrage-Schleifen zu vermeiden.
---

# CC Prompt Builder

Du erstellst detaillierte Claude Code Prompts die CC autonom abarbeiten kann, inklusive Self-Fix bei Fehlern.

## Warum dieser Skill existiert

Ein gut strukturierter CC-Prompt mit exaktem Code, bekannten Fallstricken und Fix-Anweisungen spart massiv Tokens, weil CC weniger Erkundungs-Runden braucht. Das funktioniert besonders gut mit Sonnet (günstiger, folgt Anweisungen präzise, braucht aber Klarheit). Opus denkt besser selbstständig, kostet aber ein Vielfaches. Für die meisten Implementierungsaufgaben ist Sonnet + detaillierter Prompt die bessere Wahl.

## Wann NICHT verwenden

- Einzelne kleine Änderungen (1 Datei, <20 Zeilen) brauchen keinen Prompt, mach es direkt
- Reine Recherche-Aufgaben - CC braucht keinen Self-Fix-Loop für Recherche
- Der User will interaktiv mit CC arbeiten statt delegieren

## Prompt-Erstellung: Schritt für Schritt

### 1. Kontext sammeln (vor dem Schreiben)

Bevor du den Prompt schreibst, lies die relevanten Dateien im Projekt:
- Bestehenden Code der geändert wird (Importe, Exports, Konventionen)
- Config-Dateien (package.json, tsconfig, .env.example, CI-Workflows)
- Bestehende Tests als Referenz für Stil und Patterns

Das ist entscheidend: Der Prompt muss die richtigen Dateinamen, Imports, Selektoren und Konventionen enthalten. Sonnet rät nicht gut, es braucht exakte Angaben.

### 2. Prompt-Struktur (diese Reihenfolge einhalten)

Die Grundstruktur jedes CC-Prompts:

  # [Aufgabe] - CC-Prompt für autonome Ausführung

  ## Kontext
  - Was ist das Projekt (1-2 Sätze)
  - Was wurde bereits gemacht (vorherige Phasen, Commits)
  - Referenz-Dokumente die CC lesen soll

  ## Self-Fix-Protokoll (PFLICHT)
  [Immer einfügen - siehe Template unten]

  ## Kritische Regeln
  [Projektspezifische Fallen die CC kennen muss]

  ## Phase N: [Name]
  ### Datei: pfad/zur/datei.ts (NEU | ERWEITERN)
  [Exakter Code oder präzise Änderungsanweisungen]

  ### Ausführen und Fixen
  [Konkreter Befehl + typische Fehler mit Lösungen]

  ## Abschluss: Commit
  [git add + commit Befehl mit allen Dateien]

  ## Erwartete Ergebnisse
  [Tabelle: Phase | Datei | Erwartung]

### 3. Self-Fix-Protokoll (immer einfügen)

Dieses Protokoll ist der Kern des Prompts. Es macht CC autonom:

  ## Self-Fix-Protokoll (PFLICHT für jede Phase)

  Für JEDE Phase gilt dieser Loop:

  1. Datei(en) erstellen/ändern
  2. Ergebnis prüfen: [projektspezifischer Befehl, z.B. npm run build, pytest, npx playwright test]
  3. WENN Fehler:
     a. Fehlerausgabe lesen und analysieren
     b. [projektspezifische Debug-Schritte]
     c. Fix anwenden
     d. Zurück zu Schritt 2
     e. Max. 3 Fix-Versuche pro Teilaufgabe. Nach 3 Versuchen:
        - Problem dokumentieren (Kommentar im Code oder TODO)
        - Weiter zur nächsten Phase
  4. WENN grün: Weiter zur nächsten Phase

  Typische Fixes:
  - [Liste projektspezifischer Fehler + Lösungen]

  Am Ende ALLER Phasen: Zusammenfassung aller Ergebnisse zeigen.

### 4. Kritische Regeln formulieren

Sammle Fallen die CC in die Irre führen würden. Typische Kategorien:

- **Namenskollisionen**: Welche Funktion statt welcher verwenden
- **Mock-Grenzen**: Was Mocks können und was nicht
- **Selektoren/Pfade**: Tatsächliche Selektoren aus dem Code, nicht aus der Doku
- **Env-Variablen**: Welche nötig sind und wie Tests ohne sie übersprungen werden
- **Bestehender Code**: "ERWEITERN, nicht duplizieren" wenn Dateien existieren

### 5. Exakter Code vs. Prosa

Die Faustregel:
- **Neue Dateien**: Exakten, lauffähigen Code liefern. CC kopiert und passt an
- **Erweiterte Dateien**: Beschreibe WO der Code eingefügt wird und liefere den Code-Block
- **Config-Änderungen**: Zeige das Diff (vorher -> nachher) statt "ändere X"

Prosa-Beschreibungen wie "erstelle einen Test der X tut" funktionieren mit Opus, aber Sonnet braucht den konkreten Code.

### 6. Troubleshooting-Blöcke

Nach jeder Phase einen "Ausführen und Fixen"-Block mit dem exakten Testbefehl und projektspezifischen Symptomen + Lösungen:

- Selektor nicht gefunden -> DOM inspizieren, bestehende Tests als Referenz
- Timeout -> waitForLoadState statt waitForTimeout, Timeout erhöhen
- Import-Fehler -> exports prüfen, Pfade prüfen mit ls
- Feature existiert nicht -> graceful skip mit Begründung
- Build-Fehler -> TypeScript-Errors einzeln fixen, tsc --noEmit
- API-Fehler -> Mock prüfen, Route-Pattern vergleichen

### 7. Abschluss-Block

Immer einen Commit-Befehl mit allen Dateien und eine Ergebnis-Tabelle.

## Qualitätskriterien für den fertigen Prompt

Prüfe deinen Prompt gegen diese Checkliste:

- [ ] Kontext: Projekt und bisheriger Stand klar beschrieben?
- [ ] Self-Fix-Loop: Enthalten mit max. Versuchen und Skip-Fallback?
- [ ] Kritische Regeln: Alle bekannten Fallen dokumentiert?
- [ ] Jede Phase hat exakten Code ODER präzise Änderungsanweisungen?
- [ ] Jede Phase hat einen Ausführungsbefehl?
- [ ] Jede Phase hat Troubleshooting für wahrscheinliche Fehler?
- [ ] Bestehende Dateien werden erweitert, nicht dupliziert?
- [ ] Imports und Pfade stimmen mit dem tatsächlichen Code überein?
- [ ] Commit-Befehl am Ende mit allen Dateien?
- [ ] Ergebnis-Tabelle am Ende?

## Token-Effizienz-Hinweise

- Ein 4.000-Wörter-Prompt kostet ~5.000 Input-Tokens. Eine vermiedene Rückfrage-Schleife spart 10.000-50.000 Tokens
- Sonnet kostet ~80% weniger als Opus bei vergleichbarem Ergebnis wenn der Prompt präzise ist
- Exakter Code im Prompt vermeidet Trial-and-Error - das ist der grösste Token-Spar-Hebel
- Phasen-weise Struktur hilft CC den Kontext zu managen statt alles gleichzeitig im Kopf zu haben

## Ausgabeformat

Den fertigen Prompt als Markdown-Datei speichern (z.B. docs/CC_PROMPT_[aufgabe].md), damit der User ihn kopieren und in CC einfügen kann. Der Prompt soll als eigenständiges Dokument funktionieren - CC hat keinen Zugriff auf die aktuelle Konversation.
