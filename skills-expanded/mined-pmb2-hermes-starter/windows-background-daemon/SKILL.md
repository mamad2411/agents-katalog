---
name: windows-background-daemon
description: "Run arbitrary Python scripts as persistent background daemons on Windows (Git Bash / MSYS) with auto-restart, PID file, and log management — including MSYS path pitfalls and stale-instance cleanup."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [windows, daemon, background, process, python, msys, git-bash, auto-restart]
    triggers:
      - run as background daemon
      - persistent process
      - auto-restart script
      - daemonize python
      - background service windows
      - keep running script
    related_skills:
      - guardian-angel
      - windows-cron-msys-path-fix
      - subprocess-hang-diagnostics
---

# Windows Background Daemon — Persistent Python Process on Git Bash / MSYS

Run a Python script as a persistent background daemon on Windows with auto-restart, exponential backoff, PID file management, and log rotation. Handles the MSYS path translation gotchas that break naive `nohup` + `&` patterns.

## When To Use

- Launching a long-lived Python script (WebSocket listener, relay bridge, watcher daemon) that must survive the current shell session
- Script needs auto-restart on crash with backoff
- You need a single clean instance (not the 5 accumulated stale ones that build up over time)
- Previous attempt failed because the wrapper or path format was wrong

## Workflow

### 1. Identify and Kill Stale Instances

Multiple `terminal(background=true)` launches accumulate PIDs. Check what's actually running before relaunching:

```bash
# Identify what each Python PID is doing (essential — ps doesn't show full cmdline on MSYS)
for pid in $(cd /proc && ls -d [0-9]* 2>/dev/null); do
  cmd=$(cat /proc/$pid/cmdline 2>/dev/null | tr '\0' ' ' 2>/dev/null)
  if echo "$cmd" | grep -q "my_target_script.py"; then
    echo "STALE: PID $pid: $cmd"
  fi
done

# Kill them all
for pid in $(for p in $(cd /proc && ls -d [0-9]*); do
  cat /proc/$p/cmdline 2>/dev/null | tr '\0' ' ' | grep -q "my_script.py" && echo $p
done); do
  kill $pid 2>/dev/null
done
sleep 2  # settle
```

**Important:** Use `/proc/$pid/cmdline` (MSYS maps it from Win32). Translate NUL separators with `tr '\0' ' '`.

### 2. Write the Wrapper Script

Standard pattern — saves in `scripts/` alongside the daemon:

```bash
#!/usr/bin/env bash
PYTHON="${USER_HOME}/AppData/Local/Programs/Python/Python311/python.exe"
SCRIPT="C:/path/to/my_daemon.py"
LOG="C:/path/to/logs/my_daemon.log"
PIDFILE="C:/path/to/logs/my_daemon.pid"

mkdir -p "$(dirname "$LOG")"
echo "=== Started $(date -Iseconds) ===" >> "$LOG"

MAX_RESTARTS=999; RESTART=0; DELAY=2

while [ $RESTART -lt $MAX_RESTARTS ]; do
    echo "[$(date -Iseconds)] Launch #$((RESTART+1))" >> "$LOG"
    echo $$ > "$PIDFILE"
    "$PYTHON" -u "$SCRIPT" >> "$LOG" 2>&1
    EXIT=$?
    echo "[$(date -Iseconds)] Exited with code $EXIT" >> "$LOG"
    [ $EXIT -eq 0 ] && break
    RESTART=$((RESTART + 1))
    echo "[$(date -Iseconds)] Restart #$RESTART in ${DELAY}s" >> "$LOG"
    sleep $DELAY
    [ $DELAY -lt 30 ] && DELAY=$((DELAY * 2))
done
```

**Key flags:**
- **`-u`**: Unbuffered Python — real-time log visibility without needing `flush=True` on every `print()`.
- **`C:/path` format**: Forward slashes, capital drive letter. `/c/path` doubles to `C:\c\path` for native Windows executables.

### 3. Launch via Hermes Terminal

```bash
bash "C:/path/to/run_wrapper.sh"
```

Use `background=true, notify_on_complete=false` — daemons never intentionally exit.

### 4. Verify It's Running

```bash
# Check the wrapper PID
cat "/path/to/daemon.pid"
ps aux | grep $(cat "/path/to/daemon.pid") | grep -v grep

# Check the child Python PID
cat /proc/<child_pid>/cmdline | tr '\0' ' '

# Check logs for heartbeats
tail -f "/path/to/logs/daemon.log"
```

## MSYS Path Translation Pitfall (Critical)

When a Git Bash script invokes a native Windows binary (any `.exe`), MSYS translates paths in arguments. The translation is WRONG for `/c/...` style paths:

| Input | MSYS Output | Result |
|---|---|---|
| `"C:/path/script.py"` | `C:\path\script.py` | ✅ Works |
| `"/c/path/script.py"` | `C:\c\path\script.py` | ❌ Fails |

**Always use `C:/` (not `/c/`) for script paths when passing to a Windows `.exe` from Git Bash.**

## Monitoring After Launch

- **PID file stores wrapper's PID** (bash process), not the Python child. Kill the wrapper to cascade-kill the child.
- **Log freshness:** If the log stops growing but the PID is alive, the daemon may be in a long-blocking I/O call (WebSocket recv timeout, etc.) — this is normal.
- **`read_file` is safer than `tail -f`** for checking logs from Hermes tool context — long cat/tail pipelines on MSYS can receive SIGTERM (exit code 15) before completing.

## Pitfalls

- **`os.kill(pid, 0)` does NOT work on Windows** — it raises `OSError`/`PermissionError` or silently fails; it is not a liveness probe. Use `tasklist` (or `Get-Process`) instead.
- **`tasklist /FI "PID eq N"` output is column-formatted** — checking `f"PID {pid}" in stdout` is a false-negative (the header row says `PID` but rows are `python.exe  68572 Console ...`). Match with a regex on the row start: `bool(re.search(rf"^\S+\s+{pid}\s", r.stdout, re.MULTILINE))` and exclude `"No tasks" in stdout`. Verified 2026-08-11: the naive substring check reported a live bridge as dead.
- **An auto-resuming watchdog + a manual spawn = two daemons (double-reply storm).** If a watchdog cron (auto-spawn on dead PID) AND an operator both spawn the same daemon, you get two instances both consuming the same relay/queue. Kill the orphan whose PID does NOT match the PID file; verify with a full process scan for the script name (CIM: `Get-CimInstance Win32_Process -Filter "Name='python.exe'" | Where-Object { $_.CommandLine -like '*script.py*' }`) before trusting `tasklist`-based liveness.
- **`tasklist` liveness can disagree with `Get-CimInstance`** — `tasklist` may report a process as absent while CIM still lists it. When they disagree, trust CIM for existence and re-check the PID file.
- **Kill ALL stale instances before launching:** Daemons from prior Hermes sessions (including crashed ones) accumulate as orphaned children of PID 1. They compete for ports, relays, and lock files silently.
- **`ps aux` truncates command args on MSYS.** Always fall back to `/proc/$pid/cmdline` for accurate identification.
- **`terminal(background=true)` processes don't survive Hermes restart.** If Hermes restarts, background children become orphaned. They keep running but you lose the handle — restart them on boot.
- **Use system Python, not Git Bash's bundled `python3.exe`** at `/usr/local/bin/python3`. The bundled one has worse path compatibility with Windows-native operations. System Python at `${USER_HOME}/AppData/Local/Programs/Python/Python311/python.exe` is more reliable.
