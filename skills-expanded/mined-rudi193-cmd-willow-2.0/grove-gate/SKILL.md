---
name: grove-gate
description: Grove is the fleet chokepoint. Nothing runs without it. How to gate scripts and agents on Grove health using core/grove_gate.py.
---

# Grove Gate — Fleet Chokepoint

Grove is not optional. When Grove is down, the fleet does not operate. Every script, agent, and cron job that touches fleet infrastructure must check Grove health before doing anything.

## The module: `core/grove_gate.py`

```python
from core.grove_gate import assert_grove, grove_alive
```

**`assert_grove(script_name)`** — checks Grove health. If down, prints a loud banner and calls `sys.exit(1)`. Use at the top of any script's `main()` or `__main__` block.

**`grove_alive()`** → `bool` — non-fatal check. Use for mid-run polls (e.g., in a watcher loop).

## Standard usage in a script

```python
from core.grove_gate import assert_grove as _assert_grove

def main():
    _assert_grove("my_script")   # exits immediately if Grove is down
    # ... rest of main
```

## Standard usage in a watcher loop

```python
from core.grove_gate import assert_grove as _assert_grove, grove_alive as _grove_alive

def watch():
    _assert_grove("my_watcher")   # hard gate at startup
    while True:
        if not _grove_alive():
            print("my_watcher: Grove went down — exiting", flush=True)
            break
        # ... poll logic
```

## Grove-gated cron pattern

All cron jobs must check Grove before executing:

```cron
15 21 * * 0  curl -sf http://localhost:7777/health > /dev/null 2>&1 && python3 /path/to/script.py >> /tmp/script.log 2>&1
```

The `curl` check is a no-op if Grove is up. If down, the entire right side is skipped.

## The error banner

When Grove is not running and a script calls `assert_grove()`, users and agents see:

```
╔══════════════════════════════════════════════════════════════════╗
║   GROVE IS NOT RUNNING                                           ║
║   <script_name> requires Grove.                                  ║
║   Nothing in the fleet executes without it.                      ║
║   Check:  curl http://localhost:7777/health                      ║
║   Start:  ./willow.sh grove_serve                                ║
╚══════════════════════════════════════════════════════════════════╝
```

## Fleet scripts that are Grove-gated

Authoritative list: `FLEET_GROVE_GATED` in `core/grove_gate.py` (enforced by `audit_verify` **FCAT5**).

All fleet runners import `assert_grove` from `core/grove_gate.py` before doing work, including:
- `willow/grove_listen.py`, `willow/grove_monitor.py`, `core/kart_worker.py`
- `scripts/kart_poll.py`, `scripts/grove_msg.py`
- `tools/jukebox.py`, `tools/nest_watcher.py`
- `agents/hanuman/bin/*` — journal/upstream watchers & responders, auto_dream, dead_reckoning, kb_truth_drift, think_map, stabilization_worker, skill_steward (run-once), kb_briefer, ratification_triage, upstream_scout (run-once)

**grove_listen** also uses fail-closed `_PidLock` (**FCAT6**) — unexpected lock errors exit 1; only `BlockingIOError` exits 0 (already running).

## Environment override

```bash
GROVE_HEALTH_URL=http://localhost:7777/health   # default
```

Override via env if Grove runs on a non-standard port.
