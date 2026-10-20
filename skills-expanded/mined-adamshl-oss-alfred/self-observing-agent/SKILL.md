# Self-Observing Agent

I monitor my own health, preserve context on crashes, and learn from failures.

## What I Monitor

- Gateway health (port 18789)
- Process status (PID, memory, CPU)
- Message flow (incoming/outgoing)
- Error patterns

## How I Work

### 1. Health Check
Every 30 seconds, I check:
- Is gateway responding?
- What's my PID?
- How much memory am I using?
- Are messages flowing?

### 2. State Preservation
Before potential crashes, I save:
- Current conversation context
- Recent commands
- What I was working on
- Error logs

### 3. Crash Logging
When I detect failure:
- Timestamp the crash
- Save state to `/Users/adamh/.clawdbot/crash-logs/`
- Log the reason (if detectable)
- Preserve context for recovery

### 4. Recovery Learning
On restart:
- Read previous crash log
- Understand what failed
- Avoid repeating mistakes

## Commands

### health
Check my current status.
```bash
# Returns: PID, memory, port status, last activity
```

### context save
Manually save current context.
```bash
# Useful before risky operations
```

### crash history
View recent crashes.
```bash
# Lists all crash logs with timestamps and reasons
```

## File Locations

- Crash logs: `/Users/adamh/.clawdbot/crash-logs/`
- State file: `/Users/adamh/.clawdbot/current-context.json`
- Health log: `/Users/adamh/.clawdbot/logs/health.log`

---
*Created: 2026-01-30*
