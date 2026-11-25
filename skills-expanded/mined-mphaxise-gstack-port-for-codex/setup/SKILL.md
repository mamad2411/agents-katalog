---
name: setup
description: GBrain-inspired setup for Codex. Use when establishing the local package, file conventions, identity files, or a future substrate for the GBrain layer.
---

# Setup

Use this skill when the user wants to initialize or normalize the Codex-side GBrain package setup.

This port is adapted from `garrytan/gbrain` at commit `0b47afbf402a4e27a648bb9d131ce584461461ea`.

## Workflow

1. Inspect what already exists in the repo.
2. Decide which setup layer is needed:
   - docs and registries
   - identity files
   - task/report directories
   - future memory-substrate placeholders
3. Create only the minimal durable structure needed.
4. Verify the package still validates after setup changes.

## Current Upstream Coverage

Choose the topology explicitly: one local brain, a cross-machine thin client, or split engines per worktree. Prefer the repo's file-backed substrate by default; when the real GBrain runtime is requested and available, support Supabase, bring-your-own Postgres, live sync, health verification, and a brain-first lookup policy without silently changing storage engines.

## Guardrails

- Do not bootstrap a fake backend just to mimic upstream GBrain setup.
- Prefer explicit conventions over hidden magic.
- Keep setup reversible and easy to understand from the repo itself.
