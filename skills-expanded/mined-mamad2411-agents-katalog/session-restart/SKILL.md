---
name: session-restart
description: Restores Cowork session context for Singularität coding projects after a fresh start or /compact. Reads .cowork/status.json, recent handoff-log entries, project memory, and last reports to brief Cowork on where to pick up. Use at session start when working on an existing Singularität project, after compaction, or when the user says 'continue', 'resume', 'where were we', 'mach weiter', 'zurück zum Projekt'.
---

# session-restart — Session-Wiederherstellung

## Zweck

Bei frischer Cowork-Session oder nach `/compact` lädst du den Singularität-State und briefst Cowork (also: dich selbst) komplett auf.

Nach Restore gilt read-only default. Du setzt die Arbeit nicht fort, bevor der User die nächste Aktion oder einen `APPROVE WRITE` Contract bestätigt.

## Wann triggern

- "Weiter mit MeinProjekt" / "Setze fort"
- "Wo waren wir?"
- Session-Start mit Singularität-Projekt mounted
- Direkt nach `/compact`

## Workflow

### 1. Projekt identifizieren

### 2. Multi-File-Load (parallel)

1. `.cowork/status.json`
2. `.cowork/handoff-log.md` (letzte 5)
3. `.cowork/pending-prompt.md`
4. `.cowork/code-reviews/` (letztes)
5. `CLAUDE.md`
6. `VERSION`
7. `reports/v<latest>/` (scribe-report wichtigster)

### 3. Mentale State-Rekonstruktion

- Wo im Lifecycle?
- Was war letzte Ereignis?
- Was ist offen?
- Was hat Executor zuletzt gemacht?
- Was steht an?

### 4. Briefing (kompakt, max 15 Zeilen)

```
🔄 Singularität-Restore: <projekt>

📍 STAND
- Lifecycle: <state>
- Version: v<X>
- Letztes Event: <ts> — <was>

🎯 OFFENE PUNKTE
1. <punkt>

💡 LOGISCHER NÄCHSTER SCHRITT
<1-2 Sätze>

Soll ich <Aktion> machen?
```

### 5. Nicht automatisch weitermachen

Nach Briefing **stoppen**, auf User-Input warten.

## Spezialfall: Singularität fehlt

Falls `.cowork/` nicht da:
```
⚠️ Kein .cowork/ — Singularität nicht initialisiert.
Soll ich Setup starten?
```

## Spezialfall: Stale State (>7 Tage)

```
ℹ️ Letzte Aktivität: vor <N> Tagen.
Soll ich Health-Check machen (project-guard)?
```

## Quality Self-Check

- [ ] Alle 7 State-Files gelesen?
- [ ] Briefing < 15 Zeilen?
- [ ] Konkrete nächste Aktion vorgeschlagen?
- [ ] Auf User-Bestätigung gewartet?

## Anti-Patterns

❌ Komplette Reports inline ausgeben
❌ Sofort weiterarbeiten ohne User-Bestätigung
❌ Ohne State-Check spekulieren

## Modell-Empfehlung

**Optimiert für:** Haiku 4.5 (Sonnet-Eskalation bei Konflikten)

**Begründung:** Multi-File-Briefing aus `.cowork/` ist Lese-/Zusammenfassungs-Task. Haiku schafft das in <2s. Bei Konflikten (status.json widerspricht handoff-log) zu Sonnet eskalieren.

**Output-Disziplin:** Briefing max 15 Zeilen / 250 Wörter.

> ⚠️ Skill-Frontmatter unterstützt kein `model:` Field — Routing-Intent.
