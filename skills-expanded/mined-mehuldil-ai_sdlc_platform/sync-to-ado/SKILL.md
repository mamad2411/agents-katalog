---
name: sync-to-ado
description: Atomic Azure Boards sync — compose with ask-first CRUD; use observer for inbound events
model: sonnet-4-6
token_budget: {input: 4000, output: 2000}
---

# Sync to ADO

**Purpose:** All **outbound** Azure DevOps work (create/update/comment/link state) goes through this skill’s flow; **agent files stay thin** and delegate here + `agents/shared/ado-integration.md`.

## When to invoke

- Push story content to a work item (`sdlc ado push-story`, etc.)
- Post gate or review comments
- Reconcile state after a merge (with **`rules/merge-and-source-of-truth.md`**)

## Steps

1. **Read** `agents/shared/ado-integration.md` — ask-first, previews, `--yes` / `SDLC_ADO_CONFIRM` for non-TTY.
2. **CLI** — Prefer `sdlc ado …` from `cli/sdlc.sh` over ad-hoc REST in agent prose.
3. **Inbound** — If Boards changed first, ensure **`orchestrator/ado-observer/`** is deployed so events can drive the next stage (two-way posture).

## Do not

- Embed raw REST payloads in agent markdown — keep them in CLI libraries or scripts.
- Create duplicate work items for the same scope; query existing items first.
