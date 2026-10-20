---
name: watchdog-transient-tolerance
description: >-
  Transient-failure tolerance for watchdog/self-healing cron scripts that take
  destructive actions (fleet pause, process restart). Classify transient vs
  persistent errors, retry in-cycle, require N consecutive failures before
  acting — so a single DNS blip never darkens a whole fleet.
version: 1.0.0
author: Hermes Agent (Forge)
license: MIT
metadata:
  hermes:
    tags: [watchdog, transient, tolerance, self-healing, cron, pause, retry, resilience]
    triggers:
      - watchdog paused everything
      - false pause
      - transient failure
      - getaddrinfo failed
      - don't pause on one failure
      - fleet dark
      - destructive action on health check
      - pause tolerance
      - retry before pausing
    related_skills: [cron-watchdog, guardian-angel, model-health-watchdog, python-import-debugging, windows-cross-platform-debugging]
---

# Watchdog Transient-Failure Tolerance

Design pattern for any cron watchdog / self-healing script whose health check
triggers a DESTRUCTIVE action (pause all jobs, restart a process, kill a
service). The cardinal rule: **never take the destructive action on a single
failed health check** — transient errors (DNS, timeouts, connection resets)
self-heal within seconds, and a false pause/restart costs far more than the
blip itself.

## The Incident That Proved It (2026-07-31)

The Cron Guardian paused **54 of 61 cron jobs for ~15 min of fleet-wide
dark** because ONE transient DNS blip (`getaddrinfo failed` on the Tier-1
`/models` check) hit a zero-retry, zero-tolerance pause path. The API was
never down; the resolver hiccuped for seconds. Auto-recovery next cycle
fixed it, but the fleet still went dark for a full cycle for nothing.

## The Pattern

1. **In-cycle retry** — on a transient failure, sleep ~5s and re-check once.
   Retry success → log "self-healed on retry", reset the streak, no action.
2. **N-cycle tolerance window** — still failing → increment a persisted
   `transient_streak` counter in the state file; act only when
   `streak >= TRANSIENT_TOLERANCE_CYCLES` (2 cycles ≈ 30 min at a 15-min
   cadence). One-off blips never accumulate to an action.
3. **Non-transient still acts immediately** — HTTP 4xx/5xx, auth failure,
   credit exhaustion (429) are real, non-self-healing conditions. Never
   classify them as transient, or you delay response to genuine outages.
4. **Reset discipline** — zero the streak on every healthy cycle AND on
   recovery. Steady-state state file has no streak field.
5. **Exit-code semantics** — `exit(0 if (healthy and has_credits) else 1)`.
   The naive `return 0 if healthy else 1` reports "ok" on the very cycle
   that paused/restarted everything.

### Transient classification

```python
TRANSIENT_MARKERS = [
    "getaddrinfo", "name resolution", "temporary failure",
    "timeout", "timed out", "connection reset", "connection aborted",
    "connection refused", "network is unreachable", "no route to host",
]

def is_transient(detail):
    d = detail.lower()
    return any(m in d for m in TRANSIENT_MARKERS)
```

Only Tier-1 (reachability) failures get the tolerance treatment. If Tier-1
passed and Tier-2 (credits/chat) failed, that's a real condition — act
immediately.

### Exemption lists stay mandatory

Tolerance does NOT replace the NEVER_PAUSE / infrastructure-exemption list.
Watchdogs that pause jobs must never pause themselves, other watchdogs, or
infrastructure jobs (backup, rotation, ingestion). Keep both mechanisms.

## Verification (behavioral test, not unit mocks)

Redirect the module's I/O globals (`JOBS_FILE`, `STATE_FILE`, `JOBS_LOCK`,
`REPORT_DIR`) to a temp dir, monkeypatch `check_model_health` + report
collectors, no-op `time.sleep`, then drive 4 phases:

1. Single transient blip → streak 1, fleet stays up (THE regression case)
2. 2nd consecutive transient → action taken, exempt jobs untouched
3. Recovery → resume + streak reset
4. Non-transient (HTTP 401 / credits) → immediate action

Runnable harness: `scripts/guardian-transient-tolerance-test.py`
(run it after any change to a pause-decision path).

## Gotchas

- **Hyphenated script names** — the live guardian is `cron-guardian.py`
  (HYPHEN): `import cron_guardian` fails with ModuleNotFoundError even with
  the dir on sys.path. Load via `importlib.util.spec_from_file_location()`
  (see `python-import-debugging`).
- **Stale sibling copies** — verify which script copy is live before
  patching (e.g. stale v1.0 `~/.hermes/scripts/cron-guardian.py` vs live
  `AppData/Local/hermes/scripts/cron-guardian.py`). Confirm via state-file
  location and `last_check_at` matching the cron job's last run.
- **`git -C <msys-path>` silently fails in git-bash** — use `cd` + plain
  git when checking repos (see `windows-cross-platform-debugging`).

## False Positive Filtering (ignore_re)

When your watchdog's error detection uses regex patterns, it WILL catch
false positives — especially from external services (Discord, WebSocket,
CDN) that produce log strings matching `server.*error` or `HTTP 5[0-9][0-9]`.

**Pattern:** Add an `ignore_re` alongside the detection `re.compile`:

```python
# Catch what you care about
DETECTION_PATTERNS = [
    r"provider.*error", r"model.*unavailable", r"api.*key.*invalid",
    r"connection.*refused", r"5[0-9][0-9].*server error",
    r"timeout.*provider", r"rate.?limit.*exceeded",
]

# Filter out false positives from external services
IGNORE_PATTERNS = [
    r"discord\.errors", r"discord\.websocket", r"discord\.gateway",
    r"WebSocket.*disconnect", r"ConnectionError.*Discord",
    r"503 Service Unavailable", r"upstream connect error",
    r"transport failure reason", r"remote connection failure",
    r"Task exception was never retrieved",  # asyncio noise
]

detection_re = re.compile('|'.join(DETECTION_PATTERNS), re.IGNORECASE)
ignore_re = re.compile('|'.join(IGNORE_PATTERNS), re.IGNORECASE)

for line in log_lines:
    if ignore_re.search(line):  # skip false positives first
        continue
    if detection_re.search(line):
        # This is a real error
```

**Where to place it:** In the detection loop, test the `ignore_re` BEFORE
the detection `re.search`. This prevents false positives from ever reaching
the error-counting or recovery code.

**Design principle:** Detection patterns are broad (catch everything that
looks like an error). Ignore patterns are narrow (exact strings from known
noisy services). Together they form a pass-through filter: ignore first,
then detect.

## N-Consecutive Failure Threshold

Even with ignore_re, some transient errors will slip through. The solution
is a **tolerance window** — act only after N consecutive failures:

```python
# Persistent state file
state = load_state()
if errors > 0:
    state['consecutive_failures'] = state.get('consecutive_failures', 0) + 1
    if state['consecutive_failures'] >= FAILURE_THRESHOLD:  # e.g. 3
        take_action(state)
else:
    state['consecutive_failures'] = 0  # reset on healthy run
save_state(state)
```

Standard thresholds:
- **Watchdog scripts** (no_agent, running every 5-15 min): threshold=3
  (15-45 min of tolerance before alerting)
- **Health checks** (every 1-2 min): threshold=5
- **Mutual health checks** (between two agents): threshold=3

**Reset discipline:** Zero the streak on EVERY healthy run. A single clean
cycle resets the count. This means a random transient error that happens
once every 24 hours never triggers an alert.

## State-file persistence for N-consecutive thresholds

The N-consecutive threshold requires state to survive between runs. For
no_agent cron scripts, use a JSON state file in the cron output directory
or `~/AppData/Local/hermes/cron/`:

```python
STATE_FILE = Path.home() / "AppData/Local/hermes/cron/coding_buddy_state.json"

def load_state():
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text())
    return {"consecutive_failures": 0, "last_alerted": None}

def save_state(state):
    STATE_FILE.write_text(json.dumps(state, indent=2))
```

## References

- `references/cron-guardian-v2.2-case-study.md` — full session detail: the
  incident timeline, the v2.2 diff structure, and the state-file evolution.
- Related (protected, read-only) skills with overlapping territory:
  `cron-watchdog` (NEVER_PAUSE blacklist, guardian state corruption),
  `model-health-watchdog` (two-tier health-check architecture),
  `guardian-angel` (consecutive-failure thresholds for restarts).
