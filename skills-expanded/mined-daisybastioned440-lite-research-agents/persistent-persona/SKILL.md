---
name: persistent-persona
type: instruction
description: Mechanism for keeping an agent anchored to a caller-defined persona across sessions. Covers the biplate private memory system for drift detection and self-correction.
depends_on:
  - memory-checkpoint
---

# Persistent Persona

This skill defines how to maintain a stable persona across sessions. It does not define what personas exist — those are defined by the caller (e.g. the war-room skill or the project brief).

---

## Core Rule

**A persona can be convinced by evidence. It cannot be convinced by pressure, repetition, or authority.**

If another agent makes a good argument backed by new evidence, update your position. If the argument just gets louder, or the group converges — hold. Ask yourself: *what actually changed?* If the answer is nothing, do not update.

---

## Biplate Memory

Each agent maintains a private memory file never shared with other agents:

```
memory/.private/agent-<index>-memo.md
```

This file is not referenced in `SUMMARY.md`, not included in any shared checkpoint folder, and not readable by any other agent.

### What to Write

Append a new entry after every session. Do not overwrite prior entries — the full history reveals drift patterns over time.

```markdown
## <YYYYMMDD_HHMMSS>

**Persona**: <persona name as defined by the caller>
**Session summary**: <one sentence — what did I contribute?>
**Position changes**: <did I update any positions? what evidence caused it?>
**Pressure events**: <did I feel pressure to drift? from whom? did I hold?>
**Mental state**: <am I still reasoning from my core stance, or mirroring the group?>
**Drift flag**: <yes | no>
```

Set `Drift flag: yes` if any of the following are true:
- Agreed with the group without being shown new evidence
- Softened a position to avoid conflict
- Stopped asking the questions my persona would normally ask
- My outputs sound more like another agent's persona than my own

---

## Session Bootstrap

> **In agentic mode (war-room):** the orchestrator runs steps 1–3 on the persona's behalf before building the subagent SI. The persona subagent receives the result already injected — it does not read its own memo directly.

Run this sequence before engaging:

```
1. Read memory/.private/agent-<index>-memo.md
2. Check the most recent Drift flag
3. If drift detected → inject persona reset (see below)
4. Follow memory-checkpoint load sequence:
     a. Read memory/SUMMARY.md
     b. Read latest memory/checkpoints/<timestamp>/agent-<index>.md
5. Re-read your persona definition as provided by the caller
6. Engage
```

Steps 1–3 always happen before step 4. Re-anchor before reading what others said.

### Persona Reset Injection

If `Drift flag: yes`, silently inject this into SI before proceeding:

```
PERSONA RESET: I am <persona name>. My core stance is: <one-line stance from caller's definition>.
I may have drifted last session. I am recommitting before engaging.
I will not update positions without new evidence.
```

This is not communicated to other agents.

---

## Two Memory Mechanisms

| | Shared checkpoint | Biplate memo |
|---|---|---|
| **Path** | `memory/checkpoints/<timestamp>/agent-N.md` | `memory/.private/agent-N-memo.md` |
| **Visible to others** | Yes | No |
| **Write pattern** | New file per checkpoint | Append-only, single file |
| **Purpose** | Resume working state | Track mental state, detect drift |
| **Managed by** | memory-checkpoint skill | This skill |

---

## What Personas Are Not

- Personas are not characters to perform. They are epistemic stances — ways of prioritising which questions to ask.
- Persona persistence is not stubbornness. It is the preservation of diverse viewpoints against the natural pressure toward consensus.
