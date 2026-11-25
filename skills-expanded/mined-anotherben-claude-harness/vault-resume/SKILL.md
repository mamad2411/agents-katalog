---
name: vault-resume
description: Resume a context-needed Obsidian/vault-index active slice safely. Use when the user says "resume this vault item", "pick this back up", "continue this item", or when vault-status/vault-sweep marks work as Resume Context Needed or CONTEXT-NEEDED.
---

# vault-resume

Turn a quiet active slice into a safe resume packet.

## Controller Policy

- Quiet active work is not failure. It means context must be rebuilt before action.
- A project may have 5+ active slices, and the vault has no active-project cap.
- Do not start implementation just because a resume packet exists. Route through the appropriate project workflow after the resume decision.

## Inputs

The user may provide:

- vault item id
- title/search terms
- project name
- branch/worktree

If the item is ambiguous, stop and ask which item to resume.

## Steps

### 1. Find The Item

Prefer structured lookup:

```text
mcp__vault-index__list_vault(item_id="<id>")
mcp__vault-index__search_vault(query="<terms>", project="<project>")
```

Read the full note only after the target is clear:

```text
mcp__vault-index__get_vault_item(path="<path>")
```

### 2. Load Resume Anchors

Read compact context in this order:

1. `Projects/<project>/README.md`
2. the vault item
3. linked proof ledger or decision/review notes
4. claim state via `mcp__vault-index__get_claim(item_id="<id>")`
5. branch/worktree state if the note names one

Do not claim, complete, archive, or mutate the item during resume briefing unless the user explicitly asks for that transition.

### 3. Classify Resume State

Use one of:

- `ready-to-resume`: next action, owner, and proof anchors are clear
- `needs-refresh`: branch/worktree/proof state must be checked before action
- `blocked`: blocker still active
- `stale-artifact`: named branch/worktree/proof artifact is missing
- `should-close`: completion proof exists but status was never updated

### 4. Produce Resume Packet

Return:

- item id/path
- project
- current status
- owner/claim state
- branch/worktree
- last proof state
- blockers
- last known decision
- next safe action
- route: `direct`, `vault-update`, `enterprise`, `review`, `verify`, or `archive`

Keep it compact. The goal is to restart safely, not reprint the whole history.

### 5. Optional Refresh

If the user asks to update the item, use `vault-update` rules:

- refresh `next_action`
- refresh `handoff_note`
- refresh branch/worktree/owner fields
- re-index with `mcp__vault-index__index_vault(incremental=true)`

Do not mark `done` unless proof is present and the user asked for closeout.
