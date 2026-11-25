---
name: service-health-monitoring
domain: devops
description: service-health-monitoring lets the user keep services running automatically by setting up cron jobs that watch for failures and send Telegram alerts, with auto-healing actions like restarting containers or processes so nothing stays down unattended even when no one is watching.
---

## What This Skill Does

This skill service-health-monitoring lets the user keep services running automatically by setting up cron jobs that watch for failures and send Telegram alerts, with auto-healing actions like restarting containers or processes so nothing stays down unattended even when no one is watching.

## Use When
- You need to monitor critical processes/services and auto-restart them if they fail
- You want automatic recovery without manual intervention
- You need periodic health checks with alerting on failures

## Overview
Creates an automated health monitoring system that:
1. Checks service health at regular intervals (default: every 5 minutes)
2. Detects zombie processes, connection losses, memory leaks
3. Auto-restarts failed services
4. Sends Telegram notifications when restarts occur
5. Logs all events for audit trail

## Setup Steps

### 1. Create the health check script
Template: `~/.hermes/bin/service-health-check.sh`
Key checks:
- Process running check: `pgrep -f "service_name" | head -1`
- Zombie detection: `kill -0 $PID 2>/dev/null`
- Recent activity: `stat -c %Y logfile` vs `date +%s`
- Connection status: `grep "Connected\|Disconnected" logfile`
- Memory usage: `ps -p $PID -o %mem=`

### 2. Create the alert script (optional)
Template: `~/.hermes/bin/service-restart-alert.sh`
- Sends Telegram message on restart
- Requires `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID` env vars

### 3. Set up cron job with Hermes
```
cronjob action=create name="service-health-check" schedule="*/5 * * * *" prompt="..."
```
This runs every 5 minutes automatically.

## Key Commands

**Check if service is running:**
```bash
pgrep -f "service_name"
```

**Restart service:**
```bash
pkill -f "old_process"
sleep 2
nohup /path/to/service &
```

**View health logs:**
```bash
tail -f ~/.hermes/logs/health-check.log
```

**Test health check manually:**
```bash
bash ~/.hermes/bin/gateway-health-check.sh
echo $?  # 0 = healthy, 1 = restarted/failed
```

## Pitfalls
- **False positives on idle services:** Don't restart just because there's no activity. Check actual connection status or process state.
- **Cascading restarts:** If restart fails repeatedly, add a cooldown timer or max restart count to prevent spam.
- **Missing credentials:** Telegram alerts require `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID` in environment. Export them in cron or .env.
- **Permissions:** Scripts need executable permissions (`chmod +x script.sh`) and access to process management.
- **Duplicate poller trap (CRITICAL for Telegram):** If your gateway script spawns a new Telegram poller every time it sees a stale log, you will create multiple pollers fighting over the same bot token → 409 conflict loop. Always check if the primary daemon is already running before spawning a new one. Pattern: `find_gateway()` should prefer the long-running daemon PID over any freshly spawned `gateway run` process. If the daemon is alive, skip restart even if the log hasn't moved.

## Real-World Example: Hermes Gateway
See: `/root/.hermes/bin/gateway-health-check.sh` (health check) and
`/root/.hermes/bin/gateway-restart-alert.sh` (alert notification)

Monitors the Hermes Telegram gateway:
- Detects if process is zombie
- Checks for recent Telegram activity
- Verifies application initialization
- Monitors memory usage
- Auto-restarts with logging
- Sends Telegram alerts with diagnostics (uptime, memory, process count, system load, recent errors)
- **Duplicate poller prevention:** `find_gateway()` prioritizes the long-running daemon (`python3 /root/.local/bin/hermes`) over freshly spawned `gateway run` processes. `check_logs()` treats stale logs as a warning (not failure) when the daemon is alive. `restart_gateway()` skips if the daemon is already running. This prevents the 409 Telegram conflict loop caused by multiple pollers on the same bot token.

Runs every 5 minutes via cron job `hermes-gateway-health-check`.
A separate daily digest (`gateway-daily-summary.sh`) runs at 9 AM EST to produce a 24h summary.

## Docker-Contained Service Variant

Use this pattern when the monitored process lives **inside a Docker container**.
Key constraint: NO host-level `pkill`, `pgrep`, or process management allowed.
All checks and restarts go through `docker exec`.

### Why it matters
- `pkill -f "gateway run"` on the host cannot see container processes
- A host-level watchdog with `pkill` will never accidentally kill a containerized process
- Conversely, a Docker watchdog cannot interfere with host processes -- isolation is structural

### Port check inside container
```bash
# /proc/net/tcp uses little-endian hex for ports
# e.g. port 18789 = 0x4965
docker exec "$CONTAINER" grep -qi "4965" /proc/net/tcp /proc/net/tcp6 2>/dev/null
```

### Restart inside container
```bash
docker exec -d "$CONTAINER" sh -c "myservice run --port 18789 >> /tmp/service.log 2>&1"
```

### Container-down detection (escalate immediately, don't retry)
```bash
RUNNING=$(docker inspect --format '{{.State.Running}}' "$CONTAINER" 2>/dev/null)
if [ "$RUNNING" != "true" ]; then
    # Can't help -- send alert and exit
    send_telegram "Container is DOWN. Run: docker start $CONTAINER"
    exit 1
fi
```

### Retry loop pattern (3 attempts, verify after each)
```bash
attempt=1
while [ $attempt -le 3 ]; do
    docker exec -d "$CONTAINER" sh -c "service run >> /tmp/service.log 2>&1"
    sleep 8  # wait for startup
    if port_is_up; then
        send_telegram "Service recovered on attempt $attempt"
        exit 0
    fi
    attempt=$((attempt + 1))
    [ $attempt -le 3 ] && sleep 10
done
send_telegram "All 3 restart attempts failed -- manual intervention required"
exit 1
```

### Telegram alerts -- reuse Hermes credentials
```bash
token=$(grep '^TELEGRAM_BOT_TOKEN=' "$HOME/.hermes/.env" | cut -d= -f2-)
chat_id=$(grep '^TELEGRAM_CHAT_ID=' "$HOME/.hermes/.env" | cut -d= -f2-)
curl -s -X POST "https://api.telegram.org/bot${token}/sendMessage" \
    -d "chat_id=${chat_id}" -d "text=${msg}" -d "parse_mode=Markdown" > /dev/null 2>&1
```

### Real-world example
`/root/openclawcharles/ops/openclaw-gateway-watchdog.sh`
Monitors OpenClaw gateway (port 18789) inside container `openclaw-mm3f-openclaw-1`.
Runs every 2 minutes via root crontab.

### Pitfalls
- **Silent failure trap:** `docker exec -d` fires and forgets. Always re-check the port after sleeping -- don't assume the restart worked.
- **Container vs process:** Two separate failure modes. If the container is down, `docker exec` will fail -- detect this first and escalate rather than retry.
- **Port hex conversion:** `/proc/net/tcp` stores port in little-endian hex. Convert: `printf '%04X\n' 18789` gives `4965`. Always verify the hex matches your port.
- **POST_RESTART_WAIT:** Give the process 8-10 seconds to bind the port before checking. Too short = false failure detection.

## Anti-Pattern: The Duplicate-Telegram-Poller Death Spiral

A misconfigured health check can cause a Telegram 409 conflict loop. Here's how:

1. Health check sees gateway log is stale (no new entries in >5 min)
2. Health check kills the gateway process
3. Health check spawns a *new* gateway process
4. But the primary Hermes daemon was already running and polling Telegram
5. Now two processes share the same Telegram bot token → Telegram returns 409 Conflict
6. Both processes retry on loop, hammering Telegram

**Symptoms:**
- `docker logs` shows repeated `getUpdates conflict: 409` errors
- Telegram bot becomes unresponsive
- Health check keeps restarting the gateway but the log stays stale

**The fix has three parts** (applied to `gateway-health-check.sh`):

```bash
# 1. find_gateway() — prefer the long-running daemon, not spawned gateway processes
find_gateway() {
    local daemon_pid
    daemon_pid=$(ps aux | grep 'python3.*hermes$' | grep -v grep | awk '{print $2}' | head -1)
    if [ -n "$daemon_pid" ] && kill -0 "$daemon_pid" 2>/dev/null; then
        echo "$daemon_pid"; return 0
    fi
    # Fallback: any hermes gateway
    ps aux | grep -E 'hermes.*gateway' | grep -v grep | awk '{print $2}' | head -1
}

# 2. check_logs() — stale log + alive daemon = warning, not failure
check_logs() {
    local age=$(($(date +%s) - $(stat -c %Y "$GATEWAY_LOG")))
    local pid="$1"
    if [ -n "$pid" ] && kill -0 "$pid" 2>/dev/null && [ "$age" -gt 3600 ]; then
        log "WARN: Log stale (${age}s) but daemon PID $pid alive — skipping restart"
        return 0  # NOT a failure
    fi
    [ "$age" -gt "$LOG_STALE_SECONDS" ] && return 1
    return 0
}

# 3. restart_gateway() — never spawn duplicate if daemon is already running
restart_gateway() {
    local old_pid=$(find_gateway)
    local daemon_pid=$(ps aux | grep 'python3.*hermes$' | grep -v grep | awk '{print $2}' | head -1)
    if [ "$old_pid" = "$daemon_pid" ] && kill -0 "$daemon_pid" 2>/dev/null; then
        log "SKIP: Primary Hermes daemon (PID $daemon_pid) already running"
        return 0  # Don't kill it, don't spawn a second one
    fi
    # ... normal kill and restart ...
}
```

**Rule:** A stale log on an alive daemon is not a restart trigger. Idle health ≠ dead health.

## OpenClaw-Specific Non-Fatal Errors (Do Not Restart)

When monitoring OpenClaw (container `openclaw-mm3f-openclaw-1`), the following log entries are **known false positives** — the system is fine, do NOT trigger a restart:

| Log pattern | Verdict | Why |
|---|---|---|
| `ERR_MODULE_NOT_FOUND: cleanup-kBh9Q3mQ.js` | Non-fatal | Telegram dispatch still succeeds (`sendMessage ok`) |
| `heartbeat failed: Cannot find module` (same path) | Non-fatal | Heartbeat fires every 30 min and fails; container keeps running |
| `[sessions/store] pruned stale session entries` | Cosmetic | Normal OpenClaw housekeeping, not an error |

**Correct health check for OpenClaw:**
```bash
# Check process list — two node processes = healthy
docker exec openclaw-mm3f-openclaw-1 ps aux | grep node | grep -v grep
# Expected: node server.mjs (PID 10) + openclaw (PID 22)

# Check update-offset files for recent polling activity
ls -la /root/.openclaw/.openclaw/telegram/update-offset-*.json

# Check Telegram sendMessage success rate in logs
docker logs openclaw-mm3f-openclaw-1 --since "10m" 2>&1 | grep "sendMessage ok" | wc -l
```

**The restart trigger should be:** `docker inspect --format '{{.State.Running}}' openclaw-mm3f-openclaw-1` returning anything other than `true` — not log error lines.

---

## Anti-Pattern: Docker Healthcheck Probing the Wrong Endpoint

When a containerized app requires authentication, the built-in Docker healthcheck may fail with 401 — even though the app is perfectly healthy. The health check fails, Docker marks the container unhealthy, and a restart loop begins.

**Symptoms:**
- `docker inspect <container>` shows `Health: unhealthy` with `401` in the log
- Container itself is actually running fine (logs show successful startup, migrations, etc.)
- Next.js apps often have this problem if the health check hits an API route requiring a session

**Fix:** Override the healthcheck in `docker-compose.yml` to probe a public endpoint that doesn't require auth:

```yaml
services:
  my-app:
    healthcheck:
      test: ["CMD", "curl", "-f", "http://127.0.0.1:3000/login"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 15s
```

Then `docker compose up -d` to recreate the container with the new probe.

**Debugging tip:** Use `docker exec <container> curl -s http://127.0.0.1:3000/<endpoint>` to find which URL returns 200 without auth before setting it in the healthcheck.

## Next Steps
- Monitor the health logs for a few days to ensure it's working
- Adjust thresholds (timeout, memory limits) based on your service
- Add more checks as needed (CPU, disk, port availability)
- Create similar health checks for other critical services

## Verification
After setup, confirm:
```bash
# Check cron job is scheduled
cronjob action=list

# Test the health check script manually
bash ~/.hermes/bin/gateway-health-check.sh

# Verify logs exist and are being written
ls -lh ~/.hermes/logs/health-check.log
tail ~/.hermes/logs/health-check.log
```
