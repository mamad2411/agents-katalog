---
name: manage-system
description: >
  Manage ScreenHand system services — supervisor daemon, memory health, session diagnostics.
  Start/stop/pause supervisor, install as launchd service, check memory stats, query verified
  learnings, clear memory, snapshot state. Use when: "start supervisor", "stop supervisor",
  "pause automation", "resume automation", "install service", "memory stats", "clear memory",
  "check system health", "what has screenhand learned", "system status", "diagnostics".
disable-model-invocation: true
allowed-tools:
  - mcp__sh__supervisor_start
  - mcp__sh__supervisor_stop
  - mcp__sh__supervisor_pause
  - mcp__sh__supervisor_resume
  - mcp__sh__supervisor_status
  - mcp__sh__supervisor_install
  - mcp__sh__supervisor_uninstall
  - mcp__sh__memory_snapshot
  - mcp__sh__memory_stats
  - mcp__sh__memory_clear
  - mcp__sh__memory_query_patterns
  - mcp__sh__memory_recall
  - mcp__sh__memory_errors
  - mcp__sh__recovery_queue_add
  - mcp__sh__recovery_queue_list
  - mcp__sh__session_claim
  - mcp__sh__session_heartbeat
  - mcp__sh__session_release
---

# ScreenHand System Management

You are managing ScreenHand's background services, memory system, and session infrastructure.

## Supervisor Daemon

The supervisor monitors active automation sessions for stalls, expired leases, and blockers (CAPTCHA, 2FA, rate limits). It runs as a detached background process.

### Lifecycle
```
supervisor_start()              → spawn daemon (detached, survives Claude Code restart)
supervisor_status()             → active sessions, health, stall counts, log tail
supervisor_pause()              → signal ALL automation to stop (safety kill switch)
supervisor_resume()             → lift pause, automation resumes
supervisor_stop()               → graceful SIGTERM shutdown
```

### Install as macOS Service
```
supervisor_install()            → creates launchd plist, auto-starts on login
supervisor_uninstall()          → removes launchd service
```

After installing, the supervisor starts automatically on every login — no need to manually start it.

### Recovery Queue
When the supervisor detects a stalled session, it queues recovery actions:
```
recovery_queue_list(status="pending")       → see what needs attention
recovery_queue_add(sessionId, action, reason) → manually queue a recovery
```

Recovery actions: `nudge` (retry), `restart` (kill + relaunch), `escalate` (notify user).

## Memory System

ScreenHand maintains 4 memory stores at `~/.screenhand/memory/`:
- **actions.jsonl** — chronological log of every tool call (max 10MB, rotates)
- **strategies.jsonl** — successful tool sequences saved by `memory_save` (max 500)
- **errors.jsonl** — error patterns with resolutions (max 200)
- **learnings.jsonl** — verified selector/method patterns with confidence scores (max 1000)

### Diagnostics
```
memory_snapshot()               → full state: session info, mission, health, top patterns, policy
memory_stats()                  → aggregate: action count, strategy count, error count, success rate, disk usage
```

### Query Verified Learnings
Learnings are the highest-quality knowledge — patterns verified through repeated success:
```
memory_query_patterns(scope="x-twitter")         → all verified patterns for X
memory_query_patterns(method="browser_click")     → all patterns using browser_click
memory_query_patterns(scope="figma", method="browser_js")  → Figma + Plugin API patterns
```

Each learning has: scope, method, pattern description, confidence (0-1), success/fail counts.

### Check Known Errors
```
memory_errors(tool="browser_click")    → known failure patterns for browser_click
memory_errors(tool="ui_press")         → known failure patterns for ui_press
```

Returns error patterns with context and resolutions — use this before attempting tools that have failed before.

### Clear Memory
```
memory_clear(category="errors")        → clear error patterns only
memory_clear(category="strategies")    → clear saved strategies
memory_clear(category="learnings")     → clear verified patterns
memory_clear(category="actions")       → clear action log
memory_clear()                         → clear everything (use with caution)
```

### Recall Strategies
```
memory_recall(task="post on twitter")  → fuzzy search past successful strategies
```

## Session Management

For long-running automations that need exclusive window control:
```
session_claim(app="Chrome", windowId="...") → lock window (prevents other agents)
session_heartbeat(sessionId="...")           → keep alive (every 60s, expires after 5 min)
session_release(sessionId="...")             → release lock + flush learnings
```

## Health Check Workflow

Run this to assess overall system health:
1. `supervisor_status()` — daemon running? any stalled sessions?
2. `memory_stats()` — how much has been learned? error rate? disk usage?
3. `memory_snapshot()` — detailed state, active patterns, policy
4. `recovery_queue_list()` — any pending recovery actions?
5. `memory_query_patterns()` — review verified learnings

## Intelligence Wrapper Reminder

Every tool call through ScreenHand goes through an intelligence pipeline that automatically:
- Warns about known errors for the tool being called
- Injects selector hints from reference files
- Suggests next steps based on past strategies
- Records outcomes for future learning

Check tool responses for `[HINT]`, `[WARNING]`, and `[STRATEGY]` lines — these are injected automatically by the server and contain actionable guidance.

$ARGUMENTS
