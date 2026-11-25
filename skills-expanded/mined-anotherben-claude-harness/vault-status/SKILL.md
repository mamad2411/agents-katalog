---
name: vault-status
description: >-
  Cross-project controller summary for the Obsidian vault. Use when the user
  says "what's open", "vault status", "show my dashboard", "what am I working
  on", or invokes /vault-status. Also use when the user seems unsure what to
  work on next or needs a project overview. Mirrors the Obsidian-first
  controller: project load, immediate attention, ghost work, verification
  gaps, and inbox debt.
---

# Vault Status Controller

This skill is the terminal summary of the same model rendered in Obsidian by `Master Dashboard.md`.

## Controller Contract

Use these canonical statuses:

- `open`
- `claimed`
- `in-progress`
- `blocked`
- `done`
- `wont-do`

Normalize legacy values before reasoning:

- `active` => `in-progress`
- `closed` => `done`
- `completed` => `done`

High-signal controller fields:

- `id`
- `project`
- `status`
- `next_action`
- `proof_state`
- `owner_family`
- `owner_instance`
- `branch`
- `worktree_path`
- `claimed_at`
- `completed_at`

Control-board policy:

- Show at least 5 active slices per project before collapsing. This is a display floor, not a work-in-progress cap.
- Do not cap active projects. Many active projects is portfolio load to summarize, not a failure by itself.
- Quiet active work is `CONTEXT-NEEDED` first: keep it resumable by surfacing owner, branch, worktree, `next_action`, handoff, and proof anchors.

## Steps

### 1. Fetch active vault state

Use `mcp__vault-index__list_vault` with these filters:

- all active work: `status="open"`, `status="claimed"`, `status="in-progress"`, `status="blocked"`
- `folder="00-Inbox"` for inbox debt
- `folder="04-In-Progress"` for active-lane drift

Do not read full files unless the user asks for a specific item.

### 2. Apply optional project filter

If the user names a project, filter every result to that `project`. State clearly: `Filtered to project: <name>`.

### 3. Compute controller views

Compute these views from the compact JSON:

- `Needs Attention Today`
  - all `critical` items
  - all `blocked` items
- `Project Load`
  - per project: open count, inbox count, active count, blocked count, critical count, resume-needed count
- `Active Slices`
  - at least 5 claimed/in-progress/blocked slices per project when available
  - no penalty for projects with more than 5 active slices
- `Ghost Work`
  - items not `done`/`wont-do` but with `completed_at` set or `handoff_note` present
- `Verification Gaps`
  - items with `proof_state`
  - items with obvious completion signals but still open
- `Inbox Debt`
  - inbox items older than 48 hours

### 4. Compute staleness and integrity flags

Use these controller flags:

- `STALE-INBOX`: inbox item older than 48 hours
- `CONTEXT-NEEDED`: claimed or in-progress item quiet for 7-14 days; resume it by reading project home, owner, branch/worktree, `next_action`, handoff, and proof anchors
- `STALE-ACTIVE`: quiet for 15+ days or missing resume anchors; advisory risk, not failure
- `MISSING-NEXT`: governed item missing `next_action`
- `MISSING-ID`: item missing `id`
- `GHOST`: completion evidence exists but status is not `done`

### 5. Render the summary

Present:

1. A project-load table
2. A short `Needs Attention Today` list
3. An `Active Slices` list grouped by project, showing at least 5 per project when available
4. A short `Resume Context Needed` list
5. A short `Ghost Work` list
6. A short `Verification Gaps` list
7. A short `Inbox Debt` list

Prefer project/action language over queue dumps. Example:

```markdown
## Project Load
| Project | Open | Inbox | Active | Blocked | Critical |
|---------|------|-------|--------|---------|----------|

## Needs Attention Today
- [critical] my-project — Shopify Order Ingress Completeness Watchdog
- [blocked] my-project — Bundle Deals MVP Remaining

## Ghost Work
- my-project — Supplier portal phase5 rbac users 006
```

### 6. Close with one recommendation

Choose the highest-signal next move:

- critical items first
- then blocked items
- then context-needed active work
- then ghost work cleanup
- then inbox triage
- otherwise highest-load project

## Obsidian Note

If the user wants the actual dashboard surface, direct them to:

- `[[Master Dashboard]]`
- `[[06-Portfolio/00 Portfolio Control Tower]]`
- `[[06-Portfolio/05 Verification Gap Register]]`
- `[[Projects/<project>/README]]`
