---
name: restart-analyzer
description: Investigates why PM2 applications keep restarting. Correlates restart timestamps with error logs, system load, and memory usage to find root causes. Auto-triggers when PM2 restart counts are unusually high (>10), or when the user mentions crashes, restarts, instability, or "why does it keep restarting". Also useful when the user says "debug crashes", "app keeps dying", or "investigate restarts".
allowed-tools: [Bash, Read, Grep]
---

# Restart Analyzer

Investigate why PM2-managed applications on newna.ai are restarting excessively.

## When to trigger

- PM2 restart count > 10 for any process
- User mentions crashes, restarts, or instability
- After a deploy when the app doesn't stay up

## Investigation Steps

### 1. Get restart counts and timing
```bash
pm2 jlist 2>/dev/null | jq '.[] | {name, pm2_env: {restart_time: .pm2_env.restart_time, created_at: .pm2_env.created_at, status: .pm2_env.status, pm_uptime: .pm2_env.pm_uptime}}'
```

### 2. Check for OOM kills
```bash
dmesg -T 2>/dev/null | grep -i "out of memory\|oom\|killed process" | tail -10
journalctl -k --since "6 hours ago" --no-pager 2>/dev/null | grep -i "oom\|killed" | tail -10
```

### 3. Check error logs around restart times
```bash
# Get timestamps of recent restarts from PM2
pm2 describe newna-admin 2>/dev/null | grep -E "restart time|uptime"

# Check error logs
tail -100 /home/sabro/projects/newna-admin/logs/error.log 2>/dev/null
tail -100 /home/sabro/projects/NewNa.Ai-ChatApp/logs/error.log 2>/dev/null
```

### 4. Check memory usage
```bash
free -h
pm2 jlist 2>/dev/null | jq '.[] | {name, monit: .monit}'
```

### 5. Check for unhandled rejections
```bash
grep -i "unhandledRejection\|uncaughtException\|SIGTERM\|SIGKILL\|ECONNREFUSED\|SQLITE_BUSY" /home/sabro/projects/newna-admin/logs/error.log 2>/dev/null | tail -20
grep -i "unhandledRejection\|uncaughtException\|SIGTERM\|SIGKILL\|ECONNREFUSED\|SQLITE_BUSY" /home/sabro/projects/NewNa.Ai-ChatApp/logs/error.log 2>/dev/null | tail -20
```

### 6. Check system load at restart times
```bash
uptime
sar -u 1 3 2>/dev/null || mpstat 1 3 2>/dev/null || echo "No CPU history available"
```

### 7. Check for database locks
```bash
ls -la /home/sabro/projects/newna-admin/data/admin.db-wal 2>/dev/null
ls -la /home/sabro/projects/NewNa.Ai-ChatApp/chat.db-wal 2>/dev/null
```
Large WAL files can indicate long-running transactions or database contention.

## Common Root Causes

| Pattern | Likely Cause | Fix |
|---------|-------------|-----|
| OOM in dmesg | Memory leak or too many concurrent processes | Increase swap, add `max_old_space_size`, reduce concurrency |
| UnhandledRejection | Missing try/catch on async code | Find the failing promise and add error handling |
| SQLITE_BUSY | Database contention from concurrent writes | Add WAL mode, reduce write frequency, add retry logic |
| ECONNREFUSED | Downstream service unavailable | Check Docker containers, restart dependent services |
| SIGTERM without errors | External kill (systemd, manual, OOM) | Check systemd journals and dmesg |

## Output

Report:
- App name and restart count
- Identified root cause (or top 3 candidates)
- Supporting evidence (log lines, timestamps, metrics)
- Recommended fix
- Whether this is a recurring pattern or one-time event
