---
name: vault-context
description: Pre-session project briefing that loads targeted context from the Obsidian vault before starting work. Use when the user says "context for [project]", "brief me on [project]", or invokes /vault-context. Also auto-suggested before /enterprise runs (enforced by hook). Pulls controller state from the vault, claim ownership from vault-index, and code repo structure via cortex-engine.
---

# Vault Context Briefing

## Prerequisites

A project name is required. If the user does not provide one, ask which project they want a briefing on.

## Controller Contract

Normalize statuses before reasoning:

- `active` => `in-progress`
- `closed` => `done`
- `completed` => `done`

Prioritize these fields in the briefing:

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

- A project may have 5+ active slices; show at least 5 before collapsing, and do not treat more as a failure.
- There is no active-project cap.
- Quiet active work from the last week or two should be treated as `Resume Context Needed`, not abandoned or failed.

## Steps

### 0. Check for stale vault index

Before querying, check if evidence hooks have written to the vault since the last reindex:

```bash
cat ~/Documents/Product\ Ideas/_evidence/.needs-reindex 2>/dev/null
```

If the marker exists, call `mcp__vault-index__index_vault(incremental=true)` first, then remove the marker:

```bash
rm -f ~/Documents/Product\ Ideas/_evidence/.needs-reindex
```

### 1. Load the project home first

Attempt to read `Projects/<project>/README.md` from the vault. If it exists, treat it as the human-facing summary anchor for the rest of the briefing.

### 2. Fetch active items for the project

Use `mcp__vault-index__list_vault(project="<name>")`. Keep everything except `done` and `wont-do` items unless the user explicitly asks for history.

Group into:

- immediate attention: `critical` or `blocked`
- active delivery: `claimed` and `in-progress`
- resume context needed: claimed/in-progress items quiet for 7-14 days, with branch/worktree/owner/next_action/handoff/proof anchors
- open queue: `open`
- inbox debt: `00-Inbox`
- ideas: `03-Ideas`
- verification gaps: `proof_state` or ghost-work signals

### 3. Load live claim ownership state

Call:

- `mcp__vault-index__list_claims(project="<project>")`
- `mcp__vault-index__get_claim(item_id="<id>")` for the most important active items

Show claim owner and lease expiry for claimed work where available.

### 4. Record session identity

Create the session markers required by edit gates:

```bash
SESSION_ID=$(ls -t "$CLAUDE_PROJECT_DIR"/../*.jsonl 2>/dev/null | head -1 | xargs basename | sed 's/\.jsonl$//')
if [ -z "$SESSION_ID" ]; then
  PROJ_KEY=$(echo "$CLAUDE_PROJECT_DIR" | sed 's|/|_|g; s|^_||')
  SESSION_ID=$(ls -t ~/.claude/projects/-${PROJ_KEY}/*.jsonl 2>/dev/null | head -1 | xargs basename | sed 's/\.jsonl$//')
fi
touch "/tmp/claude-vault-context-${SESSION_ID}"
touch "/tmp/claude-plan-approved-${SESSION_ID}"
```

Do not claim any vault item inside `vault-context`.

### 5. Load code repo outline

Use cortex-engine:

- `mcp__cortex-engine__cortex_status()`
- `mcp__cortex-engine__cortex_tree(depth=2)`
- `mcp__cortex-engine__cortex_outline(file_path="...")` for key modules referenced by active items

### 6. Compile the briefing

Present sections in this order:

1. `Project Home`
   - mention whether `Projects/<project>/README.md` exists
2. `Immediate Attention`
   - critical and blocked items
3. `Active Delivery`
   - claimed and in-progress items with owner, lease, branch, and next action
4. `Resume Context Needed`
   - quiet active items with their resume anchors and the next safe read/action
5. `Ghost Work`
   - items with completion signals but not `done`
6. `Verification Gaps`
   - items with `proof_state`
7. `Inbox And Ideas`
   - inbox older than 48h first, then ideas
8. `Code Repo Structure`
   - top-level tree and key modules

### 7. Close with one actionable recommendation

Choose one:

- address critical work
- unblock blocked work
- resume context-needed active work
- clean ghost work
- triage stale inbox
- otherwise start highest-priority open task
