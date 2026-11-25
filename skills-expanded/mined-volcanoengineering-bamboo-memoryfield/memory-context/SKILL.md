---
name: memory-context
description: repository memory-context retrieval and handoff skill for AI agents working across Knobs, context windows, ADM/RAG memory, hot/warm/cold storage, project state reconstruction, and long-running AI-assisted development.
---

# Memory Context

This Skill is for keeping the project memory usable.

The goal is not to remember everything. The goal is to retrieve the right slice, keep it findable, and preserve what matters before the context window collapses.

Use this Skill when:
- reconstructing project state after a cold start or hiatus
- deciding what memory to load and what to leave cold
- preparing a handoff between agents
- aligning ADM, RAG, Watchdog, and ctx-orientation
- deciding what belongs in hot, warm, or cold memory
- preventing a Knob from losing its thread

## Operating Rules

- Read the active Knob first. In this repo that usually means `docs/memory-ctx/ctx-orientation.md`. In downstream repos it usually means `docs/ctx-orientation.md`.
- Load `behavior/` when the question is about rules, context windows, entropy, or Token budget.
- Load `architecture/memory/` when the question is about ADM, RAG, Watchdog, drift, CRUD, or memory structure.
- Do not pull the whole repo into context just because it is available.
- Keep current work hot, recent handoffs warm, and old history cold until it is named by reference.
- If the repo map and the files disagree, treat that as memory drift and flag it.
- If the user is asking from a half-remembered state, rebuild the path instead of guessing.

## Memory Shape

Memory is not one bucket.

- ADM is episodic memory. Knobs, chapters, sessions, handoffs, cool-down periods.
- RAG is semantic and procedural memory. Terms, stable rules, retrieval paths, architecture patterns.
- Watchdog is the auditor. It checks drift, rot, missing updates, and bad memory hygiene.
- `ctx-orientation.md` is the temporal source of truth. In this repo it lives under `docs/memory-ctx/`. In downstream repos it normally lives directly under `docs/`. It tells the next agent what changed and why.

If these disagree, do not smooth it over. Name the conflict and repair the map.

## Canonical References

Read only what the current task needs:
- `docs/memory-ctx/ctx-orientation.md`
- `docs/repo-organization.md`
- `behavior/ctx-rules.md`
- `behavior/ctx-entropy.md`
- `behavior/ctx-window.md`
- `behavior/ctx-token-limits.md`
- `architecture/memory/memory.md`
- `architecture/memory/memory-adm.md`
- `architecture/memory/memory-rag.md`
- `architecture/memory/memory-crud.md`
- `architecture/memory/memory-drift.md`
- `architecture/memory/memory-watchdog.md`

## Handoff Standard

When handing memory forward:
- say what Knob is active
- say what files were changed or are relevant
- say what memory should stay hot
- say what can go cold
- say what still needs audit

Do not create ceremonial memory. If it does not help the next agent retrieve, preserve, or act, it is probably bloat.
