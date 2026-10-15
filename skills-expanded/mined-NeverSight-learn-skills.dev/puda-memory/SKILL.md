---
name: puda-memory
description: Maintains project.md as the single source of truth for a project. Use after creating or updating protocols, or after running protocols, to record logs, protocol links, and history with timestamps.
---

# Puda Memory

## Goal

Maintain **project.md** as the source of truth for each project: logs, protocol links, and a chronological history so runs are reproducible and auditable.

**CRITICAL**: Persist all project-related state so runs are reproducible and auditable.

Each project folder has **project.md** as the single place to record everything about that project for long-term memory. Paths below are relative to the project folder (which contains `protocols/` and `logs/`).

## When to Update

- After **creating** a protocol file
- After **updating** or deriving a new protocol
- After **every** protocol run and log file is generated (append the run entry and the new log path)

## What to Record in project.md

- **Logs**: Use explicit markdown links to log files under `logs/`, e.g. `[<run_id>](logs/<run_id>.log)`. Add a new log link each time a protocol is run.
- **Protocols**: Use explicit markdown links to protocol files under `protocols/`. In the "Protocols" section, list each as `[<protocol_id>](protocols/<protocol_id>.json)` with an optional short description after the link (e.g. `[<protocol_id>](protocols/<protocol_id>.json) — changed dispense amount to 100ul in step 10`).
- **History**: A chronological log of actions with ISO 8601 timestamps. **MUST** use a real timestamp—never guess or use a placeholder. Get the timestamp from the relevant file: for "ran" entries use the first line of the log file; for "created"/"updated" entries use the `timestamp` key in the protocol JSON file. Use explicit markdown links for all file paths. Append one line per action in this form:
  - `<timestamp> created [<protocol_id>](protocols/<protocol_id>.json)`
  - `<timestamp> updated [<old_protocol_id>](protocols/<old_protocol_id>.json) to [<new_protocol_id>](protocols/<new_protocol_id>.json)`
  - `<timestamp> ran [<protocol_id>](protocols/<protocol_id>.json) — logs: [<log_id>](logs/<log_id>.log)`
