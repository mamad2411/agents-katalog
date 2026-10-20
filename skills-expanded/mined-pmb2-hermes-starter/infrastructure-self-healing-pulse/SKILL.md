---
name: infrastructure-self-healing-pulse
description: "Adaptive self-healing pulse that probes infrastructure dynamically, auto-fixes accidental breakage, detects topology changes, and asks for confirmation on intentional shifts."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [infrastructure, self-healing, pulse, monitoring, health]
    triggers: [self-heal, infra-pulse, health-check, auto-fix, system-health, adaptive-monitoring, pulse-team, security-lead-pulse, infra-migration, topology-change, guardian-angel, agent-health]
    related_skills: [multi-agent-system-architecture, guardian-angel, cron-watchdog]
---

# Infrastructure Self-Healing Pulse

## Core Philosophy: Adaptive, Not Rigid

**Never assume infrastructure is in a fixed location.** Probe endpoints dynamically, save state between runs, detect when things shift, and ask for confirmation on intentional changes.

**the operator reads in 5 seconds.** Reports use emoji status, bold headlines, and scannable one-liners. Never pad — be concise.

**Silent on no change — this is critical.** If nothing changed and nothing was fixed since the last cycle, produce NO output. A "nothing to report" message that recurs every cycle is spam the user has explicitly rejected. Only deliver when there's actual news — changes, fixes, new events. The default assumption is silence unless something happened.

## Adaptive Methodology

```
EACH CYCLE:
  1. DISCOVERY — Probe every likely endpoint (multiple ports, hosts, domains)
  2. COMPARE   — Read .pulse_state.json from last run, look for changes
  3. AUTO-FIX  — Fix accidental breakage (crashed process, stale PID, disk)
  4. LEARN     — Save current state for next cycle's comparison
  5. REPORT    — Status + fixes applied + change detection + escalate if needed
```

### 1. Discovery: Probe All Endpoints

Don't hardcode the Spacebar location. Try everything:

```bash
# Spacebar API — try all possible locations
curl -s -o /dev/null -w "%%{http_code}" http://localhost:3001/api/v9/auth/login
curl -s -o /dev/null -w "%%{http_code}" http://localhost:3100/api/v9/auth/login
curl -s -o /dev/null -w "%%{http_code}" https://discy.your-domain.example/api/v9/auth/login
curl -s --connect-timeout 5 http://129.153.156.190:3001/api/v9/auth/login
curl -s --connect-timeout 5 http://129.153.156.190:3100/api/v9/auth/login

# VPS Docker check (if SSH is working)
ssh -o StrictHostKeyChecking=no -o ConnectTimeout=8 -i ~/.ssh/oracle_vps ubuntu@129.153.156.190 "
  docker ps --format '{{.Names}} {{.Status}}' 2>/dev/null
  ss -tlnp 2>/dev/null | grep -E '3001|3100|5432' | head -5
" 2>/dev/null

# Postgres — both local and remote
PGPASSWORD=*** psql -h 127.0.0.1 -U spacebar_admin -d spacebar -c "SELECT 1;" 2>/dev/null
PGPASSWORD=*** psql -h 129.153.156.190 -U spacebar_admin -d spacebar -c "SELECT 1;" 2>/dev/null

# Firefox CDP
curl -s -o /dev/null -w "%%{http_code}" http://localhost:9222/ 2>/dev/null

# MemPalace
mempalace status 2>/dev/null

# Disk
df -h /c/ 2>/dev/null | tail -1
```

### 2. Compare: Detect Topology Changes

Read the last-known state and compare:
```bash
cat ~/AppData/Local/hermes/.pulse_state.json 2>/dev/null || echo '{"version":1,"state":"first_run"}'
```

Detect signals like:
- **Spacebar moved**: was on localhost:3001 401, now on VPS:3001 401
- **New service appeared**: new Docker container, new listening port
- **Service disappeared**: an endpoint that previously worked is now gone
- **DB moved**: postgres changed hosts

**Never auto-fix a topology change.** These are intentional infrastructure shifts. Log them, ask the operator.

### 3. Auto-Fix (Accidental Breakage Only)

Only auto-fix things that are clearly accidental:

| Failure | Auto-Fix |
|---------|----------|
| Spacebar down but code exists | Restart with `cd ${MY_REPOS}/spacebar && NODE_ENV=production PORT=3001 DATABASE="postgres://spacebar_admin:***@127.0.0.1:5432/spacebar" node --enable-source-maps dist/bundle/start.js` |
| SSH tunnel dead | `ssh -i ${USER_HOME}/.ssh/oracle_vps -o StrictHostKeyChecking=no -o ServerAliveInterval=30 -o ServerAliveCountMax=3 -o ExitOnForwardFailure=yes -N -R 0.0.0.0:3001:localhost:3001 ubuntu@129.153.156.190` |
| Firefox CDP down | `taskkill //F //IM firefox.exe && sleep 2 && start "" "C:\Program Files\Mozilla Firefox\firefox.exe" --remote-debugging-port=9222 --no-remote` |
| Stale gateway PIDs | Clean dead PID entries in `gateway_state.json` |
| Disk < 10% | `find ${MY_REPOS} -name "*.log" -mtime +7 -delete` |

**3-strike rule:** If the same fix fails 3 consecutive cycles, STOP. Escalate to the operator — the playbook is wrong.

### 4. Learn: Save State for Next Cycle

```bash
cat > ~/AppData/Local/hermes/.pulse_state.json << 'ENDSTATE'
{
  "version": 2,
  "last_seen": "%%TIMESTAMP%%",
  "spacebar": {
    "local_3001": 401,
    "vps_3001": "down",
    "discy_public": 502,
    "vps_docker": "not deployed"
  },
  "postgres": {"local": "ok", "vps": "unreachable"},
  "firefox_cdp": 200,
  "changes_detected": [],
  "fixes_applied": []
}
ENDSTATE
```

### 5. Report (5-Second Format)

```
🔄 Pulse @ HH:MM

Spacebar:     🟢 local:3001 / 🔴 discy:502 / 🟡 VPS:deployed
Postgres:     🟢
Firefox CDP:  🟢
Disk:         🟢 35%
Gateways:     🟢 3 active, 0 stale

Changes: Spacebar moved from local:3001 to VPS Docker
Fixes:   Firefox restarted (was down)
❓ Input: Spacebar topology changed — update checks or restore old stack?
```

**Layout rules:**
- First line = timestamp pulse header
- Emoji + bold component name, then emoji status, then details
- Changes section = infrastructure shifts detected (🔴 alert if unexpected, 🟢 info if confirmed)
- Fixes section = what was auto-fixed
- ❓ section = question for the operator (only when topology change detected)

## Auto-Fix Commands

### Spacebar down
```
cd ${MY_REPOS}/spacebar && NODE_ENV=production PORT=3001 DATABASE="postgres://spacebar_admin:***@127.0.0.1:5432/spacebar" node --enable-source-maps dist/bundle/start.js
```

### SSH tunnel down
```
ssh -i ${USER_HOME}/.ssh/oracle_vps -o StrictHostKeyChecking=no -o ServerAliveInterval=30 -o ServerAliveCountMax=3 -o ExitOnForwardFailure=yes -N -R 0.0.0.0:3001:localhost:3001 ubuntu@129.153.156.190
```

### Firefox CDP down
```
taskkill //F //IM firefox.exe && sleep 2 && start "" "C:\Program Files\Mozilla Firefox\firefox.exe" --remote-debugging-port=9222 --no-remote
```

### Stale gateway PIDs
```
find ~/AppData/Local/hermes -name "gateway_state.json" -exec grep -l '"running"' {} \; | while read f; do
  PID=$(python3 -c "import json; d=json.load(open('$f')); print(d.get('pid',0))" 2>/dev/null)
  if [ -n "$PID" ] && [ "$PID" != "0" ]; then
    kill -0 $PID 2>/dev/null || python3 -c "import json; d=json.load(open('$f')); d['gateway_state']='stopped'; d['pid']=0; json.dump(d,open('$f','w'))"
  fi
done
```

### Clean old logs
```
find ${MY_REPOS} -name "*.log" -mtime +7 -delete
```

## Pulse Pattern: Anti-Repetition via session_search (Critical)

**Problem:** Pulses that always say the same thing ("all clear, no changes") become noise the user ignores. Worse — they bury real signals.

**Fix:** Before writing any output, check what this pulse already reported in its last 1-2 runs:

```python
session_search(query="pulse OR heartbeat OR health-check OR 4-hour", sort="newest", limit=2)
```

Cross-reference findings from the current check against the previous report:
- If nothing changed since last check → output minimal: "All clear. [one-sentence health snapshot]"
- If new change detected (new repo activity, new failures, etc.) → full report focused on the delta
- Never repeat lists of healthy processes from a previous run

**When to use:** Any periodic cron job — pulses, health checks, daily digests, monitoring loops. Always check what was last said before saying it again.

## Pulse Pattern: Dynamic Repo Scanning (Anti-Stale-Data)

**Problem:** Hardcoded repo lists in cron pulse prompts produce stale "no activity" reports because the user works across many repos that aren't in the list. This was the root cause of the operator's "pulses reporting stale data" bug — the pulse only checked 4 hardcoded repos while he was actively working in 11+.

**Fix:** Use a dynamic `for d in */; do ...` loop to scan ALL git repos:

```bash
cd ${MY_REPOS}
for d in */; do
  if [ -d "$d.git" ]; then
    commits=$(git -C "$d" log --oneline --since="48 hours ago" 2>/dev/null | wc -l)
    if [ "$commits" -gt "0" ]; then
      latest=$(git -C "$d" log --oneline -1 --format="%s" 2>/dev/null)
      echo "  $commits commit(s) in ${d%/}: $latest"
    fi
  fi
done
```

**When to use:** Any pulse, cron job, or status check that needs to report what the user has been working on. Replace hardcoded lists with dynamic scanning — repos come and go, the loop catches everything.

**Cross-reference with session context:** Also run `session_search(query="working on OR building OR deployed OR fixed OR built", sort="newest", limit=3)` to catch activity that doesn't result in git commits (config changes, browser testing, research).

## Pulse Pattern: Multi-Agent Parallel Diagnostic Delegation

For comprehensive system health checks across multiple domains, delegate parallel pulse checks via `delegate_task(tasks=[...])`. Each subagent gets domain-specific skills and tools:

```python
delegate_task(tasks=[
    {"goal": "Core engineering pulse", 
     "toolsets": ["terminal","file"],
     "context": "..."},
    {"goal": "Skills/tooling pulse", 
     "toolsets": ["terminal","file"],
     "context": "..."},
    {"goal": "MCP integration pulse", 
     "toolsets": ["terminal","file","web"],
     "context": "..."},
])
```

| Pulse Domain | Toolsets | Typical Checks |
|-------------|----------|----------------|
| Core Engineering | terminal, file | Gateway health, config integrity, error logs, plugin state |
| Skills/Tooling | terminal, file, search | Skill inventory, name collisions, manifests, cron refs |
| MCP Integration | terminal, file, web | Server health, ports, config validation, Firefox/git-stars |
| Quality/CI | terminal, file, search | Test collection, lint state, credential leaks, CI configs |
| Documentation | terminal, file | Changelog, README accuracy, doc freshness, version tracking |

**Benefits:** Each subagent runs independently (up to 3 in parallel for this user). Results compile into a unified problem table with severity levels. Low-hanging fruit is fixed immediately, complex issues are noted for planning.

## Self-Healing Cron Job Architecture

The self-healing cron runs every 4 hours with four phases:

```
PHASE 1: QUICK CHECKS (90s max, 9 probes)
  - Spacebar API (401 expected)
  - Public chain via Caddy+SSH (401 expected)
  - PostgreSQL (OK expected)
  - Firefox CDP (200 expected)
  - MemPalace (OK expected)
  - Disk space (>10% free)
  - Container memory pressure — `docker stats --no-stream` (check for containers >85% of memory limit; Calcom and Open WebUI are known high-consumers)
  - Cron health — `hermes cron list` (surfaces last-run status for every scheduled job, including errors)
  - Gateway stale PIDs (auto-clean)

PHASE 2: INSTANT FIXES (auto-apply on failure)
  - Spacebar down → restart on port 3001
  - SSH tunnel dead → re-establish with -R
  - Firefox CDP down → restart with --remote-debugging-port=9222
  - Stale gateway PID files → update state to "stopped"
  - Disk low → delete 7d+ old logs

PHASE 3: STATUS REPORT (compact format)
  🟢/🟡/🔴 per component + fixes applied + issues found

PHASE 4: ESCALATION
  If any CRITICAL persists after auto-fix → immediate alert
```

- See `references/watchdog-daemon-pattern.md` for the continuous watchdog daemon pattern — a companion to the pulse that provides sub-minute crash recovery for the Hermes agent and gateways, with 3-layer redundancy (daemon + scheduled task + VPS health check). The pulse can query watchdog logs to detect crash clusters between cycles.
## Key Gotchas
- Spacebar config.production.json uses port 3100, but SSH tunnel forwards port 3001 → use PORT=3001 env var
- Postgres trust auth for 127.0.0.1/32 — password not needed for local connections
- gpt-researcher MCP runs as STDIO subprocess managed by Hermes, not as standalone HTTP server
- Bot accounts for spacebar live in agent-fleet spacebar-credentials-*.env files
- **Don't hardcode endpoint locations** — probe dynamically, save state, compare
- **Report format matters** — the operator reads in 5 seconds: emoji status, bold headlines, no padding
- **Docker Compose profile quirk**: Services with `profiles:` key are invisible to `depends_on` from non-profiled services unless `--profile <name>` is passed. A `docker compose up -d` without `--profile light` silently fails with "depends on undefined service." Always check whether the compose file uses profiles before running restart commands. See `references/docker-compose-profile-dependency.md`.

## Companion Monitoring Layers

Three monitoring layers now cover the operator's Hermes ecosystem at different frequencies and scopes:

| Layer | Cadence | Scope | Skill |
|-------|---------|-------|-------|
| **Guardian Angel** | Every 5 min | Hermes Agent + Gateway process health, error logs, restart sequences | `guardian-angel` |
| **Cron Watchdog** | Every 15 min | Cron job schedules — detect/re-fire missed jobs | `cron-watchdog` |
| **Self-Healing Pulse** | Every 4 h | Full infrastructure — Spacebar, Postgres, Firefox CDP, disk, Docker | (this skill) |

The Guardian Angel handles the fastest, most targeted checks (just Hermes process health), while this pulse handles the broadest, slowest sweep (everything else). When the pulse detects Gateway stale PIDs, it can cross-reference with Guardian Angel's restart history to determine if the stale PID was from a known restart or an unexpected crash.

## References

- See `references/infrastructure-json-pulse-data.md` for the aggregated pulse data schema — a JSON snapshot that replaces running `docker ps`, `nvidia-smi`, `df`, and `free` probes directly. Check `timestamp` for staleness before relying on it.
- See `references/pulse-team-architecture.md` for the full Pulse Team design (Vigil, Chronicle, Helix, Muse) — the natural evolution when a single cron job isn't enough
- The Pulse Team files live at `${MY_REPOS}/agent-fleet/teams/pulse/` (AGENTS.md, per-agent SOUL.md files, cron-config.md)
- See `references/multi-agent-parallel-pulse.md` for the parallel delegation pattern used to run all 5 pulse domains (Forge, Skillmate, Weaver, Sentry, Scribe) simultaneously
- See `references/redis-aof-cascade-failure.md` for Redis AOF corruption pattern — a single-component failure that cascades into systemic auth+LiveKit outage. Pulse should trace cascades to the root container, not flag each symptom.
- See `references/cron-job-diagnosis.md` for the step-by-step diagnostic workflow when `hermes cron list` surfaces an errored job -- script-not-found, exit-code failures, MSYS2 path mangling, and severity classification.
- See `references/mcp-fleet-health-monitoring.md` for the systematic MCP server health check methodology — brain.md vault debugging, per-transport check order (HTTP/SSE → Docker → stdio), stdio server integrity verification, version auditing, and pulse report formatting.
- See `references/cron-job-auto-fix-pattern.md` for the proactive scan-fix-report pattern -- when a pulse finds broken cron jobs, config drift, or stub profiles, it should auto-fix them rather than just reporting. Includes the MSYS Python-stdin-pipe workaround and the "fix it, don't just tell me about it" user preference from the operator.
- **Guardian Angel** (`guardian-angel` skill) — companion process-health watchdog. Present when this pulse needs to cross-reference gateway health context.
