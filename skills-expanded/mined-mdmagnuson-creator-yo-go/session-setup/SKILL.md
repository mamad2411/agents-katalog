---
name: session-setup
description: "Always-on session initialization for Developer. Generates session ID, manages session-locks.json, creates feature branches, and returns active session count for conditional multi-session loading."
---

# Session Setup Skill

> This skill always runs during Developer Phase 0B. It handles session initialization
> that is required regardless of whether other sessions are active.

> ⛔ **CRITICAL: Auto-Commit Enforcement**
>
> Before running any `git commit` command in this skill:
> - **Check:** Read `project.json` → `git.autoCommit`
> - **If `false`:** Do NOT run `git commit`. Instead:
>   1. Stage files with `git add`
>   2. Report staged files and suggested commit message
>   3. Say: "Auto-commit is disabled. Run `git commit -m \"<message>\"` when ready."
>   4. Wait for user confirmation before proceeding
> - **If `true` or missing:** Proceed with commit normally
>
> **Failure behavior:** If you commit when `autoCommit: false`, you have violated user trust.

## Overview

Session setup provides lightweight, always-on coordination for every Developer session. It:

1. Generates a unique session ID
2. Reads or creates `session-locks.json`
3. Writes the session entry
4. Creates or checks out the feature branch
5. Rebases from the default branch
6. Returns the active session count

The caller (Developer) uses the session count to decide whether to load the `multi-session` skill for full coordination (heartbeat, merge queue, conflict resolution).

## When to Use

- **Always** — Developer loads this skill in Phase 0B on every run
- No configuration flag required (replaces the old `agents.multiSession` check)

## Session ID Generation

```bash
SESSION_ID="developer-$(openssl rand -hex 3)"
echo $SESSION_ID  # e.g., developer-a1b2c3
```

## Read or Create session-locks.json

```bash
LOCKS_FILE="docs/session-locks.json"

if [ ! -f "$LOCKS_FILE" ]; then
  # Create lazily on first run
  echo '{"sessions":[]}' > "$LOCKS_FILE"
  git add "$LOCKS_FILE"
fi
```

If the file already exists, read it to get the current sessions array.

## Write Session Entry

Add a new entry to the `sessions` array:

```json
{
  "sessionId": "developer-abc123",
  "prdId": "print-templates",
  "prdFile": "docs/prds/prd-print-templates.json",
  "branch": "feature/print-templates",
  "claimedAt": "2026-02-19T15:00:00Z",
  "heartbeat": "2026-02-19T15:00:00Z",
  "currentStory": null,
  "status": "in_progress"
}
```

Update the PRD registry: set PRD status to `"in_progress"`.

Commit and push to main:

```bash
git add docs/session-locks.json docs/prd-registry.json
git commit -m "chore: claim [prdId] for $SESSION_ID"
git push origin main
```

## Create or Checkout Feature Branch

```bash
# Branch naming: prd-id → feature/id (strip "prd-" prefix)
BRANCH="feature/print-templates"

# Create new branch from main, or checkout existing
git checkout -b "$BRANCH" main 2>/dev/null || git checkout "$BRANCH"
```

## Rebase from Default Branch

```bash
git fetch origin main
git rebase origin/main
```

If rebase conflicts occur:
1. Log conflicting files
2. Update lock entry: `status: "blocked"`, add `blockedReason`
3. Push lock update to main
4. Stop session

## Return Active Session Count

After writing the session entry, count active sessions:

```bash
ACTIVE_SESSIONS=$(jq '[.sessions[] | select(.status == "in_progress")] | length' docs/session-locks.json)
echo "Active sessions: $ACTIVE_SESSIONS"
```

### Caller Decision

The caller (Developer) uses this count:

| Count | Action |
|-------|--------|
| `1` (only this session) | Proceed without loading `multi-session` skill — no coordination overhead |
| `> 1` (other sessions active) | Load `multi-session` skill for heartbeat, merge queue, and conflict coordination |

## File Locations

| File | Purpose |
|------|---------|
| `docs/session-locks.json` | Tracks active sessions and their claimed PRDs |
| `docs/prd-registry.json` | Master registry of all PRDs with conflict analysis |
| `docs/prds/` | Active PRDs ready for implementation |

## Error Handling

### Push Rejection (Race Condition)

If another session claimed between your read and push:

1. `git fetch origin`
2. `git rebase origin/main`
3. Re-read `session-locks.json` — check if PRD was claimed by another session
4. If claimed: pick a different PRD
5. If available: retry push (up to 3 times)
6. If still failing: mark blocked
