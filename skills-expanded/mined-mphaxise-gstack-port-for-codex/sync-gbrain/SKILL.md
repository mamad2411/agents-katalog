---
name: sync-gbrain
description: Re-index this repo into the local GBrain-style substrate and refresh the Codex port's memory/search guidance.
---

# Sync GBrain

Use this skill when the user asks to sync, refresh, re-index, or update GBrain for this repo.

This is the Codex adaptation of upstream GStack's `sync-gbrain`. It prefers the local `brain/` helpers in this repo and uses the real `gbrain` CLI only when it is already installed.

## Workflow

1. Preserve local changes:
   - run `git status --short`
   - identify untracked or modified `brain/` files before any write
2. Refresh repo knowledge:
   - run `python3 scripts/brain_doctor.py` if present
   - run `python3 scripts/brain_search.py "gstack"` and `python3 scripts/brain_search.py "gbrain"` to verify search still sees the corpus
3. Sync new repo guidance:
   - update tracked docs or skill registries only when the task explicitly requires it
   - leave untracked `brain/` pages alone unless the user asked to capture new knowledge
4. If the upstream `gbrain` CLI exists, use read-only status commands first, then summarize any stronger sync path it offers.
5. If the machine is a configured remote MCP thin client, skip local indexing
   stages by design and report that remote reachability remains query-time
   evidence; do not route the missing local engine into repair steps.
6. If schema cleanup is requested, route to `schema-unify` before any bulk retyping or migration.
7. End with a verdict:
   - `local brain active`
   - `upstream gbrain available` or `upstream gbrain absent`
   - `actions taken`
   - `remaining gaps`

## Guardrails

- Do not bulk rewrite the `brain/` corpus during a sync.
- Do not silently convert file-backed pages into a different store.
- Do not treat upstream GBrain availability as required for the local Codex port to work.
- Do not treat a configured remote thin client as a broken local engine.
- Do not treat generated `brain/.raw` or `brain/sources` pages as publishable repo changes unless the user explicitly promotes them.
