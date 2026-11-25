# Skill: agent-session-debug

How to inspect and recover a stuck or runaway agent session.

## Problem Patterns

1. Session stuck in RUNNING state indefinitely
2. Session exceeded maxBudgetUsd but didn't stop
3. Worktree left in corrupted state
4. PR created but session never completed

## Debug Workflow

### Step 1: Inspect Session State

```bash
# Get session details
curl -s http://localhost:3003/v1/sessions/<sessionId> | jq .
# Check session events
curl -s http://localhost:3003/v1/sessions/<sessionId>/events -H "Accept: text/event-stream"
```

### Step 2: Check Worktree Health

```bash
# List active worktrees
git worktree list
# Check for corrupted worktrees
ls -la /tmp/agent-worktrees/<sessionId>/ 2>&1
```

### Step 3: Kill Switch Procedure

```bash
# Cancel the session via API
curl -s -X DELETE http://localhost:3003/v1/sessions/<sessionId>
# Manually clean up worktree if needed
git worktree remove /tmp/agent-worktrees/<sessionId> --force
```

### Step 4: Langfuse Trace Correlation

```bash
# Find trace ID from session events
# Check Langfuse dashboard for trace <sessionId>
# Compare token usage and tool calls
```

## Prevention

- Monitor sessions exceeding 80% of maxBudgetUsd
- Set up alerting on RUNNING sessions > 30 minutes
- Validate worktree path exists before each turn
