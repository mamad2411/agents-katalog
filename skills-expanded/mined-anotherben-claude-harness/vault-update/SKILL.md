---
name: vault-update
description: Move vault items through the lifecycle — claim them, promote them, block them, complete them, archive them, or hand them off. Use when the user says "close that bug", "mark it done", "this is blocked", "archive that", or invokes /vault-update. Also required before enterprise-verify/enterprise-compound. Aligns updates with the Obsidian-first controller contract.
---

# vault-update

Update the status of a vault item and move it to the correct folder.

Vault path: `{{VAULT_PATH}}`

## Controller Contract

Canonical statuses:

- `open`
- `claimed`
- `in-progress`
- `blocked`
- `done`
- `wont-do`

Normalize legacy values when you encounter them:

- `active` => `in-progress`
- `closed` => `done`
- `completed` => `done`

Required governed fields:

- `id`
- `project`
- `status`
- `updated`
- `next_action`

Optional but high-value fields:

- `proof_state`
- `owner_family`
- `owner_instance`
- `branch`
- `worktree_path`
- `claimed_at`
- `completed_at`
- `handoff_from`
- `handoff_note`
- `blocked_by`
- `related`

Resume policy:

- Quiet active work is not terminal and not failure.
- For context-needed active slices, refresh `next_action`, `handoff_note`, branch/worktree, and ownership anchors instead of archiving or closing.
- A project may have 5+ active slices, and the vault has no active-project cap.

## Steps

### 1. Find the item

Use `mcp__vault-index__search_vault(query="<search term>")`. If ambiguous, stop and ask the user which item they mean.

### 2. Read the item when needed

Use `mcp__vault-index__get_vault_item(path="<path>")` when you need the full note before applying the transition.

### 3. Apply the frontmatter update

Always set `updated` to the current ISO timestamp.

When changing status, also ensure:

- `next_action` is present for every non-`done` and non-`wont-do` item
- `proof_state` is set if proof is the reason work remains open
- ownership fields match the coordination state
- `blocked_by` uses underscore form, not `blocked-by`

### 4. Call the matching coordination tool

After the note update, call the matching vault-index coordination tool:

| Transition | Coordination tool |
|---|---|
| `claimed` or `in-progress` | `mcp__vault-index__claim_item(...)` |
| `done` | `mcp__vault-index__complete_item(...)` |
| release / pause | `mcp__vault-index__release_item(...)` |
| handoff | `mcp__vault-index__reassign_item(...)` |

If the coordination call fails, stop and report the error. Do not continue with file moves that would leave note state and claim state inconsistent.

### 5. Move the file if needed

Use these folder rules:

| New status | Target folder |
|---|---|
| `claimed` | `04-In-Progress/` |
| `in-progress` | `04-In-Progress/` |
| `done` | `05-Archive/` |
| `wont-do` | `05-Archive/` |
| `blocked` | stay where it is unless it already belongs in `04-In-Progress/` |
| `open` | `01-Bugs/`, `02-Tasks/`, `03-Ideas/`, or `00-Inbox/` based on type and completeness |

For inbox promotion:

- bug => `01-Bugs/`
- task => `02-Tasks/`
- idea => `03-Ideas/`
- ambiguous feature or note => keep in `00-Inbox/`

### 6. Refresh the index

Call `mcp__vault-index__index_vault(incremental=true)` after the change.

### 7. Confirm

Print one line:

```text
<item>: <old status> -> <new status> | folder: <old> -> <new> | coordination: <claim/completed/released/reassigned>
```

## Fail-Closed Rule

If live claim state and note state disagree, repair that before doing anything else.
