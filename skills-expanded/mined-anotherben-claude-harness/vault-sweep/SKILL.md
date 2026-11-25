---
name: vault-sweep
description: Weekly accountability check for the Obsidian vault. Detects stale inbox, context-needed active work, ghost work, verification debt, dead branches, missing metadata, and portfolio load. Use when the user says "sweep the vault", "what's stale", "clean up", or invokes /vault-sweep.
---

# Vault Sweep

The sweep now follows the controller model. It is primarily a detection and triage routine, not an automatic mutation pass.

Control-board policy:

- Show at least 5 active slices per project before collapsing. This is a display floor, not a work-in-progress cap.
- Do not cap active projects. Report portfolio load without treating breadth as failure by itself.
- Quiet active work is resumable context debt first. Do not archive, close, or shame it just because Ben has been away for a week or two.

## Controller Rules

Canonical statuses:

- `open`
- `claimed`
- `in-progress`
- `blocked`
- `done`
- `wont-do`

Normalize:

- `active` => `in-progress`
- `closed` => `done`
- `completed` => `done`

## Procedure

### 1. Load active items

Fetch:

- `status="open"`
- `status="claimed"`
- `status="in-progress"`
- `status="blocked"`

Also load:

- `folder="00-Inbox"`
- `folder="04-In-Progress"`

### 2. Classify controller debt

Flag:

- `STALE-INBOX`
  - inbox item older than 48 hours
- `CONTEXT-NEEDED`
  - claimed or in-progress item quiet for 7-14 days; surface resume anchors
- `STALE-ACTIVE`
  - claimed or in-progress item quiet for 15+ days or missing branch/worktree/owner/next-action anchors; advisory risk, not failure
- `GHOST`
  - completion evidence exists but status is not `done`
- `MISSING-NEXT`
  - governed item missing `next_action`
- `MISSING-ID`
  - item missing `id`
- `PROOF-GAP`
  - item has `proof_state`

### 3. Check branches and blockers

For `04-In-Progress` items with a branch:

- verify the branch still exists in the mapped repo
- flag dead branches

For items with `blocked_by`:

- inspect blocker state through vault-index
- flag blocks that are resolved in practice but still linked

### 4. Compute portfolio load

Report:

- distinct open projects
- distinct recently active projects
- active-slice counts by project
- highest-load projects
- blocked counts
- missing resume anchors

Do not cap active projects or call many projects a failure. If the board is broad, recommend better resume anchors and project homes rather than reducing the number of projects.

### 5. Present the report

Render these sections:

- `Immediate Cleanup`
- `Ghost Work`
- `Resume Context Needed`
- `Stale Active Work`
- `Inbox Debt`
- `Verification Debt`
- `Dead Branches`
- `Resolved Blockers`
- `Project Load`

Use concise tables or flat lists.

### 6. Offer actions

Offer guided operations, not automatic ones:

- normalize statuses
- add missing `next_action`
- refresh resume anchors on context-needed active work
- close or archive ghost work
- remove resolved blockers
- create missing project homes

Do not auto-escalate priorities unless the user explicitly asks for it.

### 7. Re-index after changes

After any updates:

```text
mcp__vault-index__index_vault(incremental=true)
```

### 8. Record the sweep timestamp

```bash
date -u +"%Y-%m-%dT%H:%M:%SZ" > /tmp/claude-vault-last-sweep
```
