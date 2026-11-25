---
name: handoff
description: Compact the current conversation into a handoff document for another agent to pick up.
argument-hint: "What will the next session be used for?"
disable-model-invocation: true
---

Write a handoff so a fresh agent can continue.

## Before writing

1. Update `.scratch/<slug>/flow.state.yaml` — set `current_phase_id`, `current_issue`, `phases_done`, `gates_satisfied` as appropriate.
2. Then write handoff to the **OS temp directory** (not the workspace).

## Handoff body

- **Goal** — what the next session should accomplish
- **Decisions** — what is settled
- **Open questions** — what is not
- **Artifacts** — paths to PRDs, issues, ADRs, `flow.state.yaml` (reference, don't duplicate)
- **Suggested next** — `/aiops` or `/aiops 继续` with slug; or specific phase skill from journey

Redact secrets. If the user passed arguments, treat them as the next-session focus.
