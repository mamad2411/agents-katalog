---
name: bkd
description: Operate a BKD kanban board over its REST API. Use when the user wants to manage BKD projects, issue execution workflows, cron jobs, or execution capacity through a reachable BKD server.
---

# BKD

Operate BKD by sending HTTP requests to `$BKD_URL`, which must point at the BKD
API root such as `http://host:port/api`.

Keep this entry file small. Load only the references needed for the current turn.

## Always-On Rules

1. Confirm `$BKD_URL` before making any request. If it is missing, ask for it.
2. Prefer `curl -s` piped to `jq` so results are easy to inspect.
3. Use the safe issue execution flow: create in `todo` -> follow-up -> move to `working`.
4. Check `/processes/capacity` before starting any execution.
6. Move finished work to `review`, not `done`. Use `done` only after human confirmation.
7. Use follow-up for all inter-issue communication.
8. Treat project and issue deletions as soft-delete unless the API says otherwise.
9. Expect all responses to use `{ success, data }` or `{ success, error }`.
10. Never use `sleep` to wait for subtasks or long-running operations. Create a cron job (`issue-follow-up`) to callback the coordinator issue on a schedule, then let the current turn end.

## Core Workflow

### Single Issue Execution

```bash
# 1. Create issue
ISSUE=$(curl -s -X POST "$BKD_URL/projects/{projectId}/issues" \
  -H 'Content-Type: application/json' \
  -d '{"title":"short title","statusId":"todo"}')
ISSUE_ID=$(echo "$ISSUE" | jq -r '.data.id')

# 2. Send details
curl -s -X POST "$BKD_URL/projects/{projectId}/issues/$ISSUE_ID/follow-up" \
  -H 'Content-Type: application/json' \
  -d '{"prompt":"full implementation details"}' | jq

# 3. Start execution
curl -s -X PATCH "$BKD_URL/projects/{projectId}/issues/$ISSUE_ID" \
  -H 'Content-Type: application/json' \
  -d '{"statusId":"working"}' | jq
```

### Quick Operations

```bash
# Health check
curl -s "$BKD_URL/health" | jq

# Execution capacity
curl -s "$BKD_URL/processes/capacity" | jq

# Monitor logs (last 3 turns, assistant messages only)
curl -s "$BKD_URL/projects/{projectId}/issues/{issueId}/logs/filter/types/assistant-message/turn/last3" | jq

# Cron jobs
curl -s "$BKD_URL/cron/actions" | jq
curl -s "$BKD_URL/cron" | jq
```

## Reference Packs

Load only what the current task needs:

- `references/rest-api.md`
  Use for exact BKD routes, payload shapes, query params, and field lists.
- `references/orchestration.md`
  Use for multi-subtask dispatch workflows, mode selection (worktree vs simple), subtask creation and monitoring, and follow-up communication patterns.
- `references/quality-review.md`
  Use for subtask self-review responsibilities, coordinator logs filter assessment, and signal classification.
- `references/merge-strategy.md`
  Use for worktree branch merging, conflict resolution, post-merge verification, and cleanup after subtasks complete in worktree mode.

## Quick Routing

Choose references by intent:

- Single issue CRUD, cron jobs, or API details: load `references/rest-api.md`.
- Multi-subtask dispatch or orchestration: load `references/orchestration.md`.
- Subtask quality assessment or code review: load `references/quality-review.md`.
- Branch merging after worktree subtasks: load `references/merge-strategy.md`.
- Full orchestration pipeline: load `references/orchestration.md`, then `references/quality-review.md`, then `references/merge-strategy.md` as each phase is reached.
