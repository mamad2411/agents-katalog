---
name: laminar-mcp
description: Use when working on Laminar demands via the remote Laminar MCP and you see wrong or empty client/product scope, plans from source-context lists without per-id loads, needless raw transcripts, same-step or same-release story-map peers, anchored ADR conflicts, MCP transitions/assignments, broken or silent MCP, or mentions of Laminar MCP, demands, TAL-* ids, story map, anchored or source context, or Laminar handoff.
---

# Laminar MCP

## Overview

**Laminar** is the product behind this MCP. **Server `tools/list` (or equivalent)** wins on names and args over this file. No assumption of a local Laminar checkout. Prefer **signals** from `load_source_context`; stop loading when the next step is clear.

## For the developer (human)

- Attach **`@laminar-mcp`** when starting demand work so the agent reads this playbook.
- Give **demand id** (`TAL-*` or Convex id) and **client/product** if scope must not be guessed; say if you want **anchored handoff** at session end.
- If MCP fails: confirm Laminar MCP enabled + auth; retry or paste **`tools/list`** for the agent.

## Agent: session scope

`get_current_context` → if needed `list_clients` / `list_products` → `set_context` (`clientId`, then `productId`). Lists need **client**; story map and releases need **product**. `clear_context` only to drop product on purpose.

## Agent: demand context (order)

Demand record → anchored ADR → evidence → map → peers.

| Goal | Tool | Notes |
|------|------|--------|
| Demand fields | `get_work_item` | `query` = id. `descriptionFormat: "plain"` to read; `json`/`both` only if editing description. |
| Handoff doc | `get_work_item_anchored_context` | Version + markdown. |
| Pick docs | `list_source_contexts` | IDs + short lines only—not a planning basis. |
| Evidence | `load_source_context` | Per relevant id before substantive answers. Signals default; `includeRawText: true` only if signals missing or insufficient. |
| Map | `get_story_map` | Then `list_story_map_activities` / `list_story_map_steps` (`storyMapId`), `list_story_map_work_items`, `list_releases`, `list_work_items`. |

Synthesize intent from `get_work_item` + `get_work_item_anchored_context`; ground details in loaded source contexts.

## Agent: handoff

Use **`put_work_item_anchored_context`**: `get_work_item_anchored_context` → merge sections per **live server schema** (`decisions`, `constraints`, `openQuestions`, `stateItems`, `outOfScope`, `scenarios` + coverage enum, optional `documentTitle`) → put with `expectedVersion` (`0` if new) → on conflict, refetch and retry. Optional: `update_work_item` via TipTap JSON from `get_work_item` (`descriptionFormat: "json"`); preview with `confirmed: false` on writes (`update_work_item`, `transition_work_item`, `assign_work_item`, `unassign_work_item`).

## Agent: story-map peers

With product in `set_context`: `get_story_map` → `list_story_map_work_items` → find row → filter others by same `userStepId`, `userActivityName`, or `releaseId`/`releaseName` → selectively `get_work_item` / anchored / `load_source_context`.

## Supporting reads

`list_statuses`, `list_team_members`, `list_blocker_types`. Prefer reads first; `confirmed: false` to preview mutations.

## Common mistakes

| Symptom | Fix |
|--------|-----|
| Plans from list lines only | `load_source_context` each id. |
| Raw dumps by default | Signals first; raw only if insufficient. |
| Story map / releases errors | Set `clientId` + `productId`. |
| Chat-only “done” | `put_work_item_anchored_context` + version. |
| Tool errors | Human fixes MCP or pastes `tools/list`; no invented args. |

## When MCP is down or unclear

Ask the human to restore connectivity or paste **`tools/list`**. Do not invent parameters.
