---
name: port-process
description: Find what's using a port, kill stuck processes, and manage system resources. Use when user mentions "port in use", "what's on port", "kill process", "lsof", "address already in use", "EADDRINUSE", "zombie process", "process management", "find PID", "free up port", "htop", "resource usage", or debugging port/process issues.
---

# Port and Process Management

## Find What's Using a Port

```bash
# macOS and Linux
lsof -i :3000

# Linux only (faster)
ss -tlnp | grep :3000

# Older Linux systems
netstat -tlnp | grep :3000

# Show all listening ports
lsof -i -P -n | grep LISTEN
ss -tlnp
```

`lsof -i :PORT` works on both macOS and Linux and is the most reliable first choice. On Linux, `ss` is faster and preferred over the deprecated `netstat`.

## Kill a Process

```bash
# By PID
kill 12345          # SIGTERM (graceful)
kill -9 12345       # SIGKILL (forced, last resort)

# By port — kill whatever is on port 3000
lsof -ti :3000 | xargs kill
lsof -ti :3000 | xargs kill -9   # forced

# By name
pkill node
pkill -f "next dev"
killall node        # macOS/Linux, kills all matching by exact name
```

The `-t` flag in `lsof -ti` outputs only PIDs, making it pipeable to `kill`.

## macOS vs Linux Differences

| Task | macOS | Linux |
|---|---|---|
| Port lookup | `lsof -i :PORT` | `lsof -i :PORT` or `ss -tlnp` |
| Kill by port | `lsof -ti :PORT \| xargs kill` | `fuser -k PORT/tcp` |
| Process tree | `pstree PID` (install via brew) | `pstree -p PID` or `ps --forest` |
| Network stats | `netstat -an` (no `-p` flag) | `ss -tlnp` or `netstat -tlnp` |
| File descriptors | `lsof -p PID` | `ls /proc/PID/fd` or `lsof -p PID` |

On macOS, `ss` and `fuser` are not available. Stick with `lsof`.

## "Address Already in Use" Diagnostic Flow

When you hit `EADDRINUSE` or "address already in use":

```bash
# 1. Find what owns the port
lsof -i :3000

# 2. Check if it's your own stale process
lsof -i :3000 -sTCP:LISTEN

# 3. Get details on the PID
ps -p <PID> -o pid,ppid,user,command

# 4. Graceful kill first
kill <PID>

# 5. Verify it released
lsof -i :3000

# 6. If still stuck, force kill
kill -9 <PID>

# 7. If port is in TIME_WAIT (Linux), you can reuse it
# Add SO_REUSEADDR in code, or wait ~60 seconds
ss -tlnp | grep :3000
```

If the port is held by a process with PPID 1, it is orphaned. Kill it directly.

## Find Processes by Name

```bash
# Search running processes
ps aux | grep node
ps aux | grep -v grep | grep node   # exclude the grep itself

# Better alternatives
pgrep -la node        # list PIDs and command lines
pgrep -f "next dev"   # match full command string
pidof node            # Linux only, returns PIDs

# Detailed info for a known PID
ps -p 12345 -o pid,ppid,user,%cpu,%mem,etime,command
```

## Process Tree

```bash
# Linux
pstree -p 12345       # show tree rooted at PID
ps -ejH               # tree view of all processes
ps --forest -eo pid,ppid,cmd

# macOS (install pstree via: brew install pstree)
pstree 12345

# Find parent of a process
ps -o ppid= -p 12345
```

Useful for finding which shell or supervisor spawned a runaway process.

## Background and Foreground

```bash
# Run in background
node server.js &

# List background jobs in current shell
jobs

# Bring job #1 to foreground
fg %1

# Send foreground job to background
# Press Ctrl-Z first (suspends it), then:
bg %1

# Detach from terminal (survives logout)
nohup node server.js > output.log 2>&1 &

# Disown an already-running background job
node server.js &
disown %1

# disown makes the shell forget about the job so it won't get SIGHUP on exit
```

## Resource Usage

```bash
# Interactive process monitor
top                   # built-in everywhere
htop                  # better UI (install separately)

# One-shot: top processes by CPU
ps aux --sort=-%cpu | head -20        # Linux
ps aux -r | head -20                  # macOS (sorted by CPU)

# One-shot: top processes by memory
ps aux --sort=-%mem | head -20        # Linux
ps aux -m | head -20                  # macOS (sorted by memory)

# Memory summary
free -h               # Linux only
vm_stat               # macOS (pages, divide by 4096 for bytes)
```

## Disk Usage

```bash
# Filesystem overview
df -h

# Size of a directory
du -sh /path/to/dir

# Find large directories (top 10)
du -h /path | sort -rh | head -10

# Interactive disk usage explorer
ncdu /path            # install separately, very useful

# Find files over 100MB
find / -type f -size +100M -exec ls -lh {} \; 2>/dev/null

# Docker disk usage (common space hog)
docker system df
docker system prune -a   # reclaim space, removes unused images/containers
```

## File Descriptors

```bash
# Check current limits
ulimit -n             # soft limit for open files
ulimit -Hn            # hard limit

# Raise soft limit for current session
ulimit -n 65536

# List open files for a process
lsof -p 12345
lsof -p 12345 | wc -l   # count them

# Linux: inspect directly
ls /proc/12345/fd | wc -l

# Find processes with many open files (Linux)
for pid in /proc/[0-9]*; do
  echo "$(ls $pid/fd 2>/dev/null | wc -l) $pid"
done | sort -rn | head -10
```

If a process hits the file descriptor limit, it logs errors like "too many open files." Raise `ulimit -n` or fix the file/socket leak.

## Signals

| Signal | Number | Behavior | When to use |
|---|---|---|---|
| SIGTERM | 15 | Graceful shutdown, process can catch and clean up | Default. Always try first. |
| SIGINT | 2 | Same as Ctrl-C | Interactive stop |
| SIGHUP | 1 | Hangup. Some daemons reload config on SIGHUP. | Reload config (nginx, Apache) |
| SIGKILL | 9 | Immediate termination, cannot be caught | Process ignores SIGTERM |
| SIGSTOP | 19 | Pause process (like Ctrl-Z) | Temporarily freeze a process |
| SIGCONT | 18 | Resume stopped process | Unpause after SIGSTOP |

Always send SIGTERM first. Give it a few seconds. Only use SIGKILL (`kill -9`) when the process refuses to exit. SIGKILL skips all cleanup -- temp files, lock files, and sockets will be left behind.

```bash
kill PID              # SIGTERM
kill -HUP PID         # SIGHUP (reload)
kill -9 PID           # SIGKILL (last resort)
```

## Common Scenarios

### Dev server won't start (port taken)

```bash
lsof -ti :3000 | xargs kill
# then restart your server
```

### Orphaned Node.js process eating CPU

```bash
pgrep -la node
# identify the stale one by its command line
kill <PID>
```

### Multiple stale dev servers

```bash
# Kill all node processes (careful in production)
pkill -f "next dev"
pkill -f "vite"
pkill -f "react-scripts"
```

### Out of disk space

```bash
df -h                           # confirm which volume is full
du -h /home --max-depth=2 | sort -rh | head -20   # find biggest dirs
# Common culprits:
docker system prune -a          # unused Docker data
rm -rf node_modules/.cache      # build caches
npm cache clean --force         # npm cache
```

### Zombie processes

```bash
# Find zombies
ps aux | awk '$8=="Z"'

# Zombies can't be killed directly -- kill their parent instead
ps -o ppid= -p <ZOMBIE_PID>
kill <PARENT_PID>
```

A zombie is a process that finished but whose parent hasn't read its exit status. Killing the parent lets init/systemd reap it.
