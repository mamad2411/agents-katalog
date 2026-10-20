---
description: "Use when: du hast einen Session-Ordnerpfad und willst verstehen, was in diesem Durchlauf schiefgelaufen ist — oder ob alles sauber lief. Analysiert logs, Metriken und Artefakte einer Rotaris-Session auf Fehler, Engpässe und Auffälligkeiten."
agent: Ask
name: "Session-Analyse"
argument-hint: "Pfad zum Session-Ordner (z. B. .rotaris/sessions/a1b2c3d4e5f6) [optional: Symptom oder Verdacht]"
---

Analysiere den Rotaris-Session-Durchlauf im angegebenen Ordner. Dein Ziel: Finde heraus, **was schiefgelaufen ist** — oder bestätige, dass der Lauf sauber war. Wenn der Nutzer ein Symptom oder einen Verdacht mitgibt, nutze das als Einstiegspunkt; andernfalls analysiere das gesamte Protokoll auf Auffälligkeiten.

## Session-Verzeichnisstruktur

Jeder Session-Ordner unter `<workspace>/.rotaris/sessions/<session_id>/` enthält:

```
<session_id>/
├── metadata.json              ← Einstieg: execution_status, Timestamps
├── summary.md                 ← Maschinen-generierte Zusammenfassung
├── issues.json                ← Strukturierte Issues (tool_error, timeout, …)
├── metrics.json               ← Detaillierte Metriken (Tokens, Tool-Calls, …)
├── timeline.jsonl             ← Chronologische Ereignisse
├── lock                       ← PID-Lock (ignorieren)
├── snapshot.json              ← nur in Sessions vor 2026-08-23 (ignorieren, state/ nutzen)
├── state/
│   ├── resume.json            ← SessionState (child_states, exhausted_models, run_type, …)
│   ├── ui_transcript.json     ← Chat-Verlauf (User/Agent-Nachrichten)
│   ├── ui_edit_diffs.json     ← UI-Edit-Diffs
│   └── run_config.json        ← Config-Snapshot (Personas, Models, Tools)
├── evidence/
│   ├── debug.log              ← Python-Logging (DEBUG-Level, rotaris_core + openhands SDK)
│   ├── tool-calls.jsonl       ← Jeder Tool-Call: agent_name, tool_name, status, elapsed_ms, is_error
│   ├── model-input.jsonl      ← Model-Input-Sanitization (stale drops, Kompression)
│   ├── context-selection.jsonl← Context-Injection/Elision-Entscheidungen
│   ├── report-validation.jsonl← Report-Validierungsergebnisse
│   ├── memory.jsonl           ← Memory-Snapshots
│   └── conversations/
│       ├── index.json         ← Alle Conversations (agent_name, persona, model, status, event_count)
│       └── event_logs/<id>/events/*.json  ← Roh-Events des OpenHands SDK
└── artifacts/                 ← Generierte Artefakte (Code, Pläne, Reports)
```

## Analyse-Workflow

### Schritt 1: Schnelldiagnose

Lies zuerst diese drei Dateien — sie geben in unter 30 Sekunden ein Lagebild:

1. **`metadata.json`** → `execution_status`: `succeeded`, `failed`, `running`, `idle`?
2. **`summary.md`** → Enthält der Abschnitt `## Warnings` Einträge? Welche?
3. **`issues.json`** → Wie viele Issues? Welche `kind`-Werte tauchen auf? Sortiere nach `severity`.

### Schritt 2: Tiefenanalyse nach Befund

Je nachdem, was Schritt 1 ergibt, grabe tiefer:

| Signal                                 | Wo weitersuchen                                                                                                                                      |
| -------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------- |
| `execution_status: failed`             | `timeline.jsonl` nach letzten Events vor Abbruch → `evidence/debug.log` nach `ERROR`/`CRITICAL` → `state/resume.json` → `ralph_progress.stop_reason` |
| `tool_error` in issues                 | `evidence/tool-calls.jsonl` nach `is_error: true` → `evidence/debug.log` nach Tool-Namen + Exception                                                 |
| `timeout` in issues                    | `evidence/debug.log` nach `timeout` + `CancelledError` → `state/resume.json` → `child_states` nach Kind mit Status `FAILED`                          |
| `model_input_sanitized` in issues      | `evidence/model-input.jsonl` → viele `dropped_stale_system_messages` / `dropped_stale_tool_descriptions` deuten auf Context-Window-Überlauf          |
| Kind im Status `BLOCKED`               | `state/resume.json` → `child_states` → Abhängigkeitskette prüfen (welcher Parent ist `FAILED`/`CANCELLED`?)                                          |
| `exhausted_provider_models` nicht leer | `state/resume.json` → Quota-Problem: Provider/Modell hat 429 mit `insufficient_quota` geliefert                                                      |
| `WAITING_ON_MODEL_SLOT`                | `state/resume.json` → `child_states` → Modell-Parallelitätslimit (`max_parallel`) erreicht                                                           |

### Schritt 3: Kind-Agent-Analyse

Prüfe in `state/resume.json` den `child_states`-Array. Jeder Eintrag hat:

- `state`: Der Zustand aus dem Child-State-Automaten (`QUEUED`, `RUNNING`, `SUCCEEDED`, `FAILED`, `CANCELLED`, `BLOCKED`, `WAITING_ON_DEPS`, `WAITING_ON_MODEL_SLOT`, `SUMMARIZING`)
- `persona`, `agent_name`, `task_id`
- `error`: Fehlermeldung falls `FAILED`

Auffälligkeiten:

- Kinder im Status `FAILED` mit leerem `error` → Exception ohne Fang
- Kinder im Status `SUMMARIZING` aber Session beendet → Abbruch während Summarization
- `BLOCKED`-Kinder → Kaskadenfehler, oft irrelevant (nur dokumentieren)
- Orchestrator-Kind (`persona: orchestrator`) im Status `FAILED` → Gesamtlauf gescheitert

### Schritt 4: Tool-Call-Analyse

`evidence/tool-calls.jsonl` auswerten:

- Fehlerhafte Calls (`is_error: true`) → welche Tools? Wiederholen sie sich?
- Langsamste Calls (nach `elapsed_ms` sortieren) → Engpässe?
- Tool-Namen, die nicht in `run_config.json` als verfügbar gelistet sind → Konfigurationsfehler
- `delegate` statt `delegate` → Prompt-Problem (alter Tool-Name)

### Schritt 5: Konversationsanalyse

`evidence/conversations/index.json` zeigt alle Kind-Konversationen:

- Konversationen mit `status != "completed"` → nicht sauber beendet
- `event_count` sehr niedrig (< 5) → Kind hat kaum gearbeitet (sofortiger Fehler?)
- `event_count` sehr hoch (> 200) → Endlosloop oder sehr komplexer Task?

Für verdächtige Konversationen: `evidence/conversations/event_logs/<id>/events/*.json` nach letzten Events durchsuchen (insbesondere `AgentFinishAction`, `AgentErrorAction`).

## Ausgabeformat

Erstelle einen strukturierten Analysebericht:

```markdown
# Session-Analyse: `<session_id>`

## Zusammenfassung

- Status: succeeded/failed/running
- Laufzeit: X Minuten
- Aufgabe: [aus ui_transcript.json oder summary.md]
- Stop-Grund: [aus ralph_progress.stop_reason]

## Kritische Befunde

1. **[...]** – [konkreter Fehler mit Dateiverweis + Zeilennummer]
2. ...

## Warnungen

- [aus summary.md + issues.json + eigener Analyse]

## Kind-Agenten

| Agent | Persona | Status    | Fehler                 |
| ----- | ------- | --------- | ---------------------- |
| ...   | ...     | SUCCEEDED |                        |
| ...   | ...     | FAILED    | Unknown persona: coder |

## Metriken

- Tool-Calls gesamt: N (davon X Fehler)
- Token-Verbrauch: N
- Kompressionen: N
- Auffälligkeiten: [Stale-Drops, Quota-Exhaustion, …]

## Empfehlungen

1. ...
2. ...
```

## Wichtige Hinweise

- Alle Pfade in Befunden **relativ zum Session-Ordner** angeben, mit Zeilennummern wo möglich.
- `BLOCKED`-Kinder sind **Kaskadenopfer** — nicht als eigenständige Fehler werten, sondern beim auslösenden Kind dokumentieren.
- Das Session-Logging-Level ist `WARNING` (mit `DEBUG` für bestimmte Subsysteme). Nicht wundern, wenn `debug.log` nicht jedes Detail enthält.
- `snapshot.json` war bis 2026-08-23 eine Kompatibilitätskopie von `state/resume.json` und wird seitdem nicht mehr geschrieben. Wo sie noch liegt, ist sie veraltet — `state/resume.json` hat Vorrang.
- Bei `execution_status: running` (abgestürzt ohne Cleanup) ist die Analyse der letzten Timeline-Events + debug.log-Einträge entscheidend.
- Der Orchestrator (`persona: orchestrator`) steuert den gesamten Lauf. Sein Status und seine Fehler sind der wichtigste Einzelindikator.
