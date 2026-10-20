---
name: multi-session
description: "Multi-session coordination for parallel AI sessions. Provides heartbeat, stale session detection, merge queue, and conflict management. Loaded conditionally when session-setup reports multiple active sessions."
---

# Multi-Session Coordination Skill

> This skill is loaded **only when `session-setup` reports `sessions > 1`**.
> Session initialization (ID generation, lock entry, branch creation) is handled by the `session-setup` skill.

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

This skill provides coordination helpers for multiple parallel AI sessions working on the same codebase. It handles heartbeat updates, stale session detection, merge queue, and conflict resolution.

## Overview

When multiple sessions are active (detected by `session-setup`), this skill provides:

1. Heartbeat updates to signal liveness
2. Stale session detection and resolution
3. Conflict risk analysis between active sessions
4. Merge queue coordination
5. Lock release and branch cleanup on completion
6. Abandon flow for cancelled PRDs

## File Locations

| File | Purpose |
|------|---------|
| `docs/session-locks.json` | Tracks active sessions and their claimed PRDs |
| `docs/prd-registry.json` | Master registry of all PRDs with conflict analysis |
| `docs/prds/` | Active PRDs ready for implementation |
| `docs/completed/` | Archived completed PRDs |
| `docs/abandoned/` | Archived abandoned PRDs |

## Operations

### Check for Stale Sessions

A session is stale if its heartbeat is older than 10 minutes:

```javascript
const isStale = (lock) => {
  const heartbeat = new Date(lock.heartbeat);
  const now = new Date();
  const minutesAgo = (now - heartbeat) / 1000 / 60;
  return minutesAgo > 10;
};
```

### Update Heartbeat

After completing each story, choose the path based on active session count:

#### Lazy heartbeat (solo — `sessions.length === 1`)

When you are the only active session, skip the expensive git round-trip:

1. Read `docs/session-locks.json` from the working tree (no checkout)
2. Update your lock entry in-place:
   ```json
   {
     "heartbeat": "<current ISO8601>",
     "currentStory": "US-XXX"
   }
   ```
3. Write the file back — **do NOT commit or push** (stays as a local-only change)
4. Continue working on your feature branch

> This avoids the stash → checkout main → pull → commit → push → checkout branch → pop cycle,
> saving 2-10 seconds per story for solo developers.

#### Full heartbeat (multi — `sessions.length > 1`)

When multiple sessions are active, perform the full git round-trip:

1. Checkout main: `git checkout main && git pull origin main`
2. Update lock entry:
   ```json
   {
     "heartbeat": "<current ISO8601>",
     "currentStory": "US-XXX"
   }
   ```
3. Update registry: increment `stories.completed`
4. Commit: `chore: heartbeat [sessionId] - completed [storyId]`
5. Push to main
6. Return to feature branch

### Release Lock (PRD Complete)

1. Merge branch to main
2. Archive PRD to `docs/completed/YYYY-MM-DD/`
3. Move PRD from registry `prds` to `completed`
4. Remove lock from `session-locks.json`
5. Delete branch (local and remote)
6. Commit: `chore: archive [prdId], release [sessionId]`

### Abandon PRD

1. Create archive folder: `docs/abandoned/YYYY-MM-DD-[prdId]/`
2. Move PRD file to archive
3. Create `reason.md` with abandonment details
4. Update registry: move to abandoned with status
5. Delete branch (local and remote)
6. Remove lock
7. Commit: `chore: abandon [prdId]`

## Conflict Risk Levels

| Level | Meaning | Behavior |
|-------|---------|----------|
| `none` | No overlapping files | ✅ Safe to run in parallel |
| `low` | Minor overlap (shared types) | ⚠️ Warn, allow with caution |
| `medium` | Some shared components | ⚠️ Warn strongly, suggest waiting |
| `high` | Major overlap (same features) | 🛑 Block unless explicitly overridden |

## Branch Naming

PRD ID → Branch name:

```
prd-print-templates → feature/print-templates
prd-permissions → feature/permissions
```

The `branchName` field in each PRD specifies the exact branch name.

## Error Handling

### Merge Conflict During Rebase

1. Log conflicting files
2. Update lock: `status: "blocked"`, add `blockedReason`
3. Push lock update to main
4. Stop session

### Push Rejection (Race Condition)

1. `git fetch origin`
2. `git rebase origin/main`
3. Retry push (up to 3 times)
4. If still failing: mark blocked

### Quality Check Failure

1. Log failure details
2. Attempt auto-fix
3. If failing after 3 attempts: mark blocked

## Stale Session Resolution

When user encounters stale session:

| Action | Steps |
|--------|-------|
| **Resume** | Update lock with new sessionId → checkout branch → continue |
| **Abandon** | Delete branch → move to abandoned/ → remove lock |
| **Skip** | Leave stale alone → claim different PRD |

## Example: Heartbeat Update

### Solo session (lazy)

```bash
# Read session-locks.json from working tree
# Update your heartbeat timestamp in-place
# Write back — no commit, no push, no branch switching
jq --arg ts "$(date -u +%Y-%m-%dT%H:%M:%SZ)" \
   '.sessions[] | select(.sessionId == "developer-abc123") .heartbeat = $ts' \
   docs/session-locks.json > docs/session-locks.json.tmp && \
   mv docs/session-locks.json.tmp docs/session-locks.json
# Continue working on feature branch — zero git overhead
```

### Multiple sessions (full round-trip)

```bash
# Save current work
git stash

# Switch to main
git checkout main
git pull origin main

# Update heartbeat (edit session-locks.json and prd-registry.json)
# ...

# Commit and push
git add docs/session-locks.json docs/prd-registry.json
git commit -m "chore: heartbeat developer-abc123 - completed US-003"
git push origin main

# Return to work
git checkout feature/print-templates
git stash pop
```

## Invoking Status Dashboard

To see current session status, invoke the session-status agent:

```
@session-status
```

This displays:
- Active sessions and their current work
- Stale sessions requiring attention
- Available PRDs with conflict analysis
- Completed PRDs
