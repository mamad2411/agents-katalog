---
name: autonomous-system-supervision
description: Build self-healing watchdogs that stay silent when healthy.
version: 1.1.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [supervision, watchdog, cron, autonomous, mutual-health, recovery]
    triggers:
      - coding buddy
      - autonomous supervisor
      - mutual health monitoring
      - cron wrapper pattern
      - silent when healthy
      - self-contained cron
      - watchdog that fixes
      - separate llm supervisor
    related_skills:
      - cron-watchdog
      - guardian-angel
      - complete-implementation-cycle
      - opencode
      - windows-cron-msys-path-fix
---

# Autonomous System Supervision

Patterns for building autonomous supervisor/watchdog systems that use a separate LLM provider, monitor each other's health, stay silent when healthy, and self-heal via subprocess-to-repo invocation.

## When to Use

- Building a watchdog that fixes the main agent when it breaks itself
- Creating cron jobs that must never spam chat
- Two autonomous systems need to know about each other
- A cron script needs to call code in a git repo without import issues

## Architecture Pattern

```
┌──────────────────────────────────────────────────────────┐
│              SUPERVISOR (separate LLM)                    │
│                                                           │
│  1. WATCH    ──→ Monitor logs, session DB, API health     │
│  2. DETECT   ──→ Pattern-match errors (provider/system)   │
│  3. BRIEF    ──→ Build context of what broke              │
│  4. INVOKE   ──→ Spawn coding agent with backup LLM       │
│  5. FIX      ──→ Agent diagnoses and repairs              │
│  6. VERIFY   ──→ Confirm main agent is healthy            │
│  7. CLEANUP  ──→ Erase error messages from chat           │
│  8. RESUME   ──→ Main agent continues where it left off   │
└──────────────────────────────────────────────────────────┘
```

## Pattern 1: Self-Contained Cron Wrapper

**Problem:** Cron scripts at `~/AppData/Local/hermes/scripts/` cannot import from project repos — the repo is not on `sys.path`, the working directory differs, and MSYS mangling breaks relative paths.

**Solution:** Make cron scripts fully self-contained. Use `subprocess` to call the actual implementation in the repo:

```python
"""Cron wrapper — self-contained, no repo imports."""
import sys, os, subprocess, json
from pathlib import Path

REPO_ROOT = Path(r"${MY_REPOS}\Documents\github\project-name")
IMPLEMENTATION = REPO_ROOT / "src" / "main.py"

def run():
    result = subprocess.run(
        [sys.executable, str(IMPLEMENTATION), "--once", "--json"],
        capture_output=True, text=True, timeout=120,
        cwd=str(REPO_ROOT),
        env={**os.environ, "PYTHONPATH": str(REPO_ROOT / "src")}
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr)
    return json.loads(result.stdout)
```

**Rules:**
1. Never use relative imports from cron scripts
2. Use absolute Windows paths (`E:\...`) NOT MSYS paths (`/e/...`)
3. Set `PYTHONPATH` in the subprocess environment
4. Pass `sys.executable` — don't assume `python` resolves
5. Copy the script to `~/AppData/Local/hermes/scripts/` for cron resolution

## Pattern 2: Silent-When-Healthy Delivery

**the operator's rule:** No cron spam in chat. Scripts must produce zero output when everything is healthy.

```python
def main():
    errors = run_check()
    if errors == 0:
        return   # No stdout → Hermes suppresses delivery entirely
    print(f"Found {errors} issue(s)")
    sys.exit(1)
```

**How it works:** Hermes' no_agent scheduler automatically suppresses delivery when stdout is empty.

**Delivery classification for new jobs:**

| Category | Deliver | Pattern |
|----------|---------|---------|
| Revenue/actionable | `origin` | Always report |
| Watchdog/monitor | `origin` | Silent healthy, report on action |
| Pulse/status check | `local` | Save to disk only |
| Background collector | `local` | Never deliver to chat |

## Pattern 3: Mutual Health Monitoring

When two autonomous systems coexist, each checks the other's cron health:

```python
def check_sibling():
    result = subprocess.run(
        ['hermes', 'cron', 'list'], capture_output=True, text=True, timeout=10
    )
    exists = '<sibling-job-id>' in result.stdout and 'enabled' in result.stdout
    errored = '<sibling-name>' in result.stdout and 'error:' in result.stdout.lower()
    return exists and not errored
```

**Heuristics:** Check job ID presence → cron exists. Scan for `error:` in sibling's block → last run failed. Never take action based on sibling alone — only report. Non-blocking: if check fails, assume healthy.

## Pattern 4: Per-Line Timestamp Log Filtering

Parse timestamps on each line rather than relying on file mtime:

```python
import re
from datetime import datetime, timedelta

cutoff = datetime.now() - timedelta(minutes=5)
for line in lines[-300:]:
    ts_match = re.search(r'(\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2})', line)
    if ts_match:
        line_ts = datetime.fromisoformat(ts_match.group(1).replace(' ', 'T'))
        if line_ts < cutoff:
            continue
```

**Rules:** Only scan last 300 lines of the 2 most recent files. Parse ISO timestamps per line. Cap at 20 errors per cycle. Deduplicate by hashing `{type}:{pattern}:{first_50_chars}`.

## Pattern 5: Cooldown-Based Error Dedup

```python
import hashlib

def hash_error(err):
    key = f"{err['type']}:{err['pattern']}:{err.get('line_text','')[:50]}"
    return hashlib.md5(key.encode()).hexdigest()[:12]

if error_hash in state['errors_seen']:
    last = datetime.fromisoformat(state['errors_seen'][error_hash])
    if datetime.now() - last < timedelta(minutes=10):
        continue   # In cooldown — skip
```

## Pattern 6: Ignore-Pattern Filter for External Service Noise

**Problem:** Generic regex patterns (`server.*error`, `connection.*refused`, `HTTP 5[0-9][0-9]`) match external service errors (Discord 503s, WebSocket disconnects, network resets) that are NOT Hermes model/provider issues and are unactionable by the supervisor.

**Solution:** Add a secondary `ignore_re` filter that runs AFTER the primary detection regex. If a line matches BOTH a detection pattern AND an ignore pattern, skip it:

```python
self.ignore_re = re.compile(
    '|'.join([
        r'discord\.errors\.', r'DiscordServerError',
        r'websocket.*close', r'heartbeat.*timeout',
        r'gateway.*reconnect', r'ConnectionResetError',
        r'ConnectionRefusedError', r'\[Errno 10054\]',
        r'\[Errno 10061\]', r'asyncio.*TimeoutError',
        r'Task exception was never retrieved',
    ]), re.IGNORECASE
)

# In the scan loop:
provider_match = self.provider_re.search(line)
system_match = self.system_re.search(line)

if (provider_match or system_match) and self.ignore_re.search(line):
    continue   # External service noise — skip

if provider_match or system_match:
    # Real error — record it
```

**Rules:**
- Apply ignore check AFTER detection, not before — you want to see what was filtered
- Discord errors (503, WebSocket, heartbeat) are NEVER Hermes model issues
- Windows errno 10054/10061 are socket resets from external services
- Async task cleanup messages are Python runtime noise

## Pattern 7: N-Consecutive-Failure Threshold Before Alerting

**Problem:** Even with ignore patterns and cooldowns, transient false positives occasionally slip through. Alerting on the first recovery attempt creates spam.

**Solution:** Track `consecutive_failures` in a persistent state file. Only deliver alerts after N consecutive failed cycles:

```python
STATE_FILE = repo_root / "data" / "buddy_state.json"
MAX_SILENT_FAILURES = 3

state = json.loads(STATE_FILE.read_text())  # {'consecutive_failures': 0, ...}

if recovery_attempted and not recovery_success:
    state['consecutive_failures'] += 1
else:
    state['consecutive_failures'] = 0

if state['consecutive_failures'] >= MAX_SILENT_FAILURES:
    print(f"PERSISTENT FAILURE: {state['consecutive_failures']} consecutive")
    sys.exit(1)
else:
    sys.exit(0)  # Silent — below threshold
```

**Rules:**
- Reset counter on ANY healthy cycle (`errors_found == 0`)
- Reset counter on successful recovery
- Reset counter on cooldown entries (stale/false positives)
- Default threshold: 3 consecutive failures before alerting
- Exit 0 while silent (Hermes suppresses delivery on empty stdout)

## Integration with OpenCode

```bash
opencode run "Fix the errors described in /path/to/brief.md" \
  --model deepseek/deepseek-chat \     # DIFFERENT provider from main agent
  -f /path/to/brief.md \
  --workdir ~/AppData/Local/hermes
```

The supervisor's LLM provider must be DIFFERENT from the main agent's.

## Pitfalls

- **`from typing import Dict` required** for type annotations in cron scripts. Python 3.11 supports `dict` natively but `Dict` needs the import.
- **MSYS path translation** — `python "/c/Users/..."` gets mangled to `E:\c\Users\...`. Use `C:\Users\...` with forward slashes.
- **Cron script is copied, not linked** — changes to the repo must be synced to `~/AppData/Local/hermes/scripts/`.
- **False positives from old log lines** — always use per-line timestamp filtering, not just file mtime.
- **Cooldown prevents thrashing** — same error won't retry within 10 min.
- **OpenCode timeout** — long recovery sessions need `timeout=300` or higher.
- **Session DB scanning produces unreliable stale data** — disable it in favor of log-only detection.
- **OpenCode corrupt DB** — `no such column: replacement_seq` requires killing stale processes, deleting the DB, and letting it regenerate. See `opencode` skill's troubleshooting reference.

## Reference Implementation

`pmb2/coding-buddy` — Full implementation of all patterns. Python stdlib only, OpenCode for recovery, MIT licensed.
