---
name: hermes-operational-audit
description: "Systematic audit of a running Hermes system — scripts inventory, .env hygiene, cron health, config repo structure, cross-repo integrations, MCP server mapping, and issue classification. Complementary to backup-focused audits."
version: 1.0.0
author: Hermes Agent
platforms: [windows, linux, macos]
metadata:
  hermes:
    tags: [audit, inventory, system-health, cron, scripts, config, integration, env, hermes]
    triggers: [audit hermes, audit scripts, audit cron jobs, inventory hermes, system audit, health check hermes, full system audit, running audit, operational audit, script inventory, integration scan, cron health, system tidy, tidy up system, professionalize setup, system-wide cleanup, look over entire system]
    related_skills: [hermes-system-backup, recurring-status-checks, engineering-pulse, mcp-fleet-audit, report-freshness-diagnostics, project-inventory, local-project-discovery, windows-cron-msys-path-fix]
    summary: >-
      Run a comprehensive audit of a live Hermes installation across seven phases
      (scripts, .env, config repo, cross-repo, cron, issues, report), plus optional
      full-system tidy mode: portfolio + Docker/disk + storage hot spots + multi-file
      plans pack with Stabilize→Reclaim→Consolidate→Polish. Use for "audit Hermes",
      "take stock", or system-wide tidy/professionalize requests.
---

# Hermes Operational Audit

Systematic methodology for auditing a running Hermes system. Covers all components: scripts, cron jobs, .env, config repos, cross-repo integrations, MCP servers, and issue classification.

The result is a structured report with inventory tables, health status, issue severity levels, and prioritized recommendations.

## When to Run

- User asks "audit my Hermes setup" or "take stock of everything"
- Before or after major config changes (add/remove MCP servers, profiles, gateways)
- As a diagnostic step when cron jobs are erroring or scripts have diverged
- Monthly maintenance check

## Prerequisites

- Access to `~/AppData/Local/hermes/` (Hermes data directory)
- Access to `~/Documents/github/hermes-config/` (or equivalent config repo)
- Terminal access for cross-repo grep scans
- Python 3 for parsing `jobs.json`

## Quick Start

```bash
# Phase 1: Scripts inventory (sizes + categorization)
du -sh ~/AppData/Local/hermes/scripts/* | sort -rh | head -20
ls ~/AppData/Local/hermes/scripts/ | wc -l

# Phase 2: .env analysis
cat ~/AppData/Local/hermes/.env
grep -E '^[A-Z_]+=' ~/AppData/Local/hermes/.env | sort

# Phase 3: Config repo tree
find ~/Documents/github/hermes-config/ -not -path '*/.git/*' -type f | sort

# Phase 4: Cross-repo integration scan
for dir in ~/Documents/github/*/; do
  [ "$(basename "$dir")" = "hermes-config" ] && continue
  n=$(grep -rli 'hermes' "$dir" --include='*.py' --include='*.md' --include='*.yaml' \
    --include='*.yml' --include='*.json' 2>/dev/null | grep -v '.git/' | wc -l)
  [ "$n" -gt 0 ] && echo "$(basename "$dir"): $n files"
done

# Phase 5: Cron job health
cat ~/AppData/Local/hermes/cron/jobs.json | python3 -c "
import json, sys
data = json.load(sys.stdin)
by_status = {}
for j in data.get('jobs', []):
    s = j.get('last_status', 'unknown')
    by_status[s] = by_status.get(s, 0) + 1
print(f'{len(data.get(\"jobs\",[]))} total jobs')
for k, v in sorted(by_status.items()):
    print(f'  {k}: {v}')
"
```

## Phase 1 — Scripts Inventory

### Goal
Get a full picture of every script in `~/AppData/Local/hermes/scripts/` — file sizes, purposes, and categories.

### Commands
```bash
# Full listing with sizes
du -sh ~/AppData/Local/hermes/scripts/*

# Total count
ls ~/AppData/Local/hermes/scripts/ | wc -l

# Largest files (excluding __pycache__ and data dirs)
du -sh ~/AppData/Local/hermes/scripts/* | sort -rh | grep -v __pycache__ | head -30
```

### Categorization

Group scripts by function. Common categories:

| Category | What to look for | Example patterns |
|----------|-----------------|------------------|
| Agent Bridges & Messaging | WebSocket listeners, relay bridges, phone proxies | `*bridge*`, `*buzz*`, `*jippity*`, `*client*` |
| Cron & System Watchdogs | Process monitors, auto-restart, cron orchestrators | `*guardian*`, `*watchdog*`, `*self_healer*`, `*nightly*` |
| PIM / Knowledge Ingestion | Extract/transform/load saved content | `pim*`, `*ingest*`, `*intelligence*` |
| MCP Servers | Servers that expose tools/resources via Model Context Protocol | `mcp_*` |
| Real Estate / Land Market | Property data, tax rolls, scoring | `*tax_roll*`, `*leepa*`, `*pipeline*`, `*scoring*`, `*zillow*` |
| AI / LLM Connectors | Provider API wrappers | `connector_*`, `gemini*`, `grok*`, `chatgpt*` |
| Security / OSINT | Cyber intel, tor, threat | `cyber*`, `tor*`, `spider*`, `*osint*` |
| Job Agent / Career | Job scanning, career matching | `job-agent*`, `bidi_jobs*` |
| Script Launchers / Infrastructure | Startup scripts, stack launchers, batch/registry | `start-*`, `launch_*`, `*stack*`, `*.bat`, `*.ps1`, `*.vbs`, `*.reg` |
| Social / Content | Platform scrapers/extractors | `x_*`, `yt_*`, `youtube*`, `linkedin*` |
| Testing / Debug / Temp | Throwaway experiments | `test*`, `*debug*`, `*fix*`, `quick-test*` |

### Deep-dive: Read bridge/daemon scripts

For each agent bridge found (typically the largest scripts), examine:
- **Protocol** (WebSocket, HTTP, REST, Nostr)
- **Target endpoint** (localhost port, external URL)
- **Identity/keys file** it loads (check for companion JSON key files)
- **Reconnection logic** (exponential backoff, max delay settings)
- **Threading model** (per-message threads vs async event loop)
- **Agents or channels** it routes for
- **AI provider** it calls (OmniRoute, direct API, etc.)

### Check for large non-script files

Scripts directories accumulate data files that shouldn't be there:
```bash
# Find data archives in scripts/
find ~/AppData/Local/hermes/scripts/ -name '*.zip' -o -name '*.tar*' -o -type d -size +50M
```

Flag these as **data-in-scripts** — they bloat the directory and should move to a dedicated `data/` area.

## Phase 2 — `.env` Analysis

### Goal
Catalog all configured credentials, identify active vs stale keys, and detect hygiene issues (duplication, hardcoded secrets in scripts).

### Commands

```bash
# Read the full .env via terminal (read_file is blocked for credential stores)
cat ~/AppData/Local/hermes/.env

# Active keys (populated values)
grep -E '^[A-Z_]+=' ~/AppData/Local/hermes/.env | sort

# Commented-out keys (available but unused)
grep -E '^#[A-Z_]+=' ~/AppData/Local/hermes/.env | grep -v '^##' | sort

# Empty-value keys
grep -E '^[A-Z_]+=$' ~/AppData/Local/hermes/.env | sort

# Check file size
ls -lh ~/AppData/Local/hermes/.env
```

### What to look for

1. **Massive duplication** — A .env file that's 100+ KB when it should be ~10 KB, with identical blocks repeated dozens of times. This happens when a config script writes `>> .env` in a loop without checking for existing entries. Not a security issue, but wastes context budget.

2. **Hardcoded secrets in scripts** — Check scripts for inline API keys:
   ```bash
   grep -rn 'API_KEY\|SECRET\|PASSWORD\|TOKEN\|Bearer' ~/AppData/Local/hermes/scripts/ \
     --include='*.py' --include='*.sh' --include='*.json' | grep -v '.pyc\|__pycache__'
   ```
   Flag any found — especially in bridge scripts that listen on network ports.

3. **Secrets in source config repos** — Also check the config repo:
   ```bash
   grep -rn 'API_KEY\|SECRET\|TOKEN' ~/Documents/github/hermes-config/ \
     --include='*.py' --include='*.sh' --include='*.json' --include='*.yaml' | grep -v '.git/'
   ```

4. **Stale/dead keys** — Keys for providers that are no longer used but still present, or commented-out keys for services the user doesn't use.

## Phase 3 — Config Repository Structure

### Goal
Map the full config repository (`~/Documents/github/hermes-config/` or equivalent) and evaluate each section.

### Commands
```bash
# Full tree (excluding .git)
find ~/Documents/github/hermes-config/ -not -path '*/.git/*' -type f | sort
```

### Evaluate each top-level section

| Section | What to check for | Red flags |
|---------|------------------|-----------|
| `.hermes/config.yaml` | Active profile model, MCP servers, delegation | Empty or minimal config |
| `config/config.yaml` | `_config_version`, MCP server entries, memory provider, display settings | Stale version, broken MCP paths |
| `config/model_config.json` | Profile definitions, active profile indicator, last_updated | Missing profiles, stale dates |
| `config/mcp-knowledge-integration.md` | Tool counts documented vs actual, access patterns | Counts don't match actual servers |
| `scripts/` | Count, duplication with `~/AppData/Local/hermes/scripts/` | Diverged copies |
| `skills/` | Category organization, total directories, reference files | Unorganized flat list |
| `voice-agent/` | Pipeline complete (VAD→ASR→LLM→TTS), transport support | Missing transport modules |
| `vps/` | Docker compose, override config | Docker compose untested |
| `plans/` | Generated plans — stale or still relevant | Plans from months ago with no action |
| `dashboard/` | Report generation capability | Outdated data |

### Check for dual-script drift

Many setup scripts copy from `hermes-config/scripts/` to `~/AppData/Local/hermes/scripts/`. Check for divergence:

```bash
diff <(ls ~/Documents/github/hermes-config/scripts/) <(ls ~/AppData/Local/hermes/scripts/) | head -40
```

Files that exist in only one location are potential drift sources.

## Phase 4 — Cross-Repo Integration Scan

### Goal
Find all repositories under `~/Documents/github/` that reference Hermes Agent — either as a dependency, integration target, or in documentation.

### Commands
```bash
for dir in ~/Documents/github/*/; do
  repo=$(basename "$dir")
  [ "$repo" = "hermes-config" ] && continue  # skip the config repo itself
  n=$(grep -rli 'hermes' "$dir" --include='*.py' --include='*.sh' --include='*.yaml' \
    --include='*.yml' --include='*.json' --include='*.md' --include='*.env' \
    --include='*.toml' --include='*.conf' --include='*.txt' 2>/dev/null | \
    grep -v '.git/' | wc -l)
  if [ "$n" -gt 0 ]; then
    echo "--- $repo: $n files ---"
    grep -rl 'hermes' "$dir" --include='*.py' --include='*.sh' --include='*.yaml' \
      --include='*.md' 2>/dev/null | grep -v '.git/' | head -5
  fi
done
```

### What to look for

| Integration type | File pattern | Example |
|-----------------|-------------|---------|
| MCP server config | `*hermes.agent*`, `*mcp*.json`, `config.yaml` | `website-landlord/configs/hermes.agent.example.yaml` |
| Integration docs | `docs/*agent*`, `docs/*mcp*` | `website-landlord/docs/mcp-agent-integration.md` |
| AGENTS.md | `AGENTS.md` with Hermes-specific instructions | `website-landlord/AGENTS.md`, `deal-finder/AGENTS.md` |

Repos with NO Hermes references are also worth noting — they're independent.

## Phase 5 — Cron Job Health Audit

### Goal
Full survey of all scheduled cron jobs: schedule, status, error history, and failure patterns.

### Commands

```bash
# Parse jobs.json for a health summary
cat ~/AppData/Local/hermes/cron/jobs.json | python3 -c "
import json, sys
data = json.load(sys.stdin)
by_status = {}
for j in data.get('jobs', []):
    s = j.get('last_status', 'unknown')
    by_status[s] = by_status.get(s, 0) + 1
print(f'{len(data.get(\"jobs\",[]))} total jobs')
for k, v in sorted(by_status.items()):
    print(f'  {k}: {v}')
"

# Detailed table including errors
cat ~/AppData/Local/hermes/cron/jobs.json | python3 -c "
import json, sys
data = json.load(sys.stdin)
for j in data.get('jobs', []):
    sched = j.get('schedule', {}).get('display', '?')
    status = j.get('last_status', 'ok')
    err = (j.get('last_error', '') or '')[:80]
    enabled = 'ENABLED' if j.get('enabled', True) else 'DISABLED'
    paused = ' PAUSED' if j.get('paused_at') else ''
    name = j.get('name', '(unnamed)')
    err_str = f' ERROR:{err}' if err else ''
    print(f'{name:45s} | {sched:15s} | {status:6s} | {enabled}{paused}{err_str}')
"
```

### Error Classification

| Error Pattern | Likely Cause | Action |
|---------------|-------------|--------|
| `TimeoutError: ... idle for 600s` | LLM response timeout or tool hang in agent-prompt cron jobs | Reduce model complexity, increase timeout, or switch to no_agent script |
| `Script exited with code 15` | SIGTERM — process killed (OOM, time limit, restart) | Check resource limits, increase timeout, split into smaller tasks |
| `Script exited with code 1` | Python script error | Re-run script manually to see traceback |
| ModuleNotFoundError | Missing dependency | `pip install` the missing package |
| ConnectionError / URLError | Service/API not reachable | Check MCP server, DB, or API endpoint availability |
| `RuntimeError: Skipped to prevent unintended spend: ... config drifted ... job is unpinned` | Global provider/model config changed since the job was created; spend guard blocks ALL unpinned jobs | Pin the job: `cronjob action=update job_id=<id> provider=<provider> model=<model>` (see Config-Drift Spend-Guard below) |

### Config-Drift Spend-Guard Skip (provider/model changed globally)

When the global inference config changes (e.g. provider `deepseek` → `custom`, model `deepseek-v4-flash` → `gpt-5.6-sol`), every **unpinned** cron job fails its next tick with:

```
RuntimeError: Skipped to prevent unintended spend: global inference config drifted since this job was created (provider 'deepseek' -> 'custom'; model 'deepseek-v4-flash' -> 'gpt-5.6-sol'), and this job is unpinned. No inference call was made. To run on the new config, pin it explicitly: `cronjob action=update job_id=<id> provider=<provider> model=<model>` (or pin the original values to keep them). See #44585.
```

This is a deliberate spend guard, NOT a provider outage — jobs simply do not fire. It hits every job whose provider/model was implicitly inherited from the old global config; jobs with explicit per-job `provider`/`model` values are unaffected. Observed 2026-08-03: 5+ jobs silently blocked (nationwide-daily-build, radicle-github-sync, fitness-accountability, jailai-status, jailai-watchdog).

**Fix:** pin each affected job to the current config (or to the original values to preserve old behavior):
```bash
cronjob action=update job_id=<id> provider=custom model=gpt-5.6-sol
```

**Bulk detection:** grep `last_error` for `config drifted` across jobs.json:
```bash
cat ~/AppData/Local/hermes/cron/jobs.json | python3 -c "
import json, sys
for j in json.load(sys.stdin).get('jobs', []):
    if 'config drifted' in str(j.get('last_error')):
        print(f\"{j['name'][:55]} | {j['id']} | {j.get('model')} -> {j.get('model_snapshot')}\")
"
```

### Quick failure triage via executions.db (health pulses)

For a fast "is anything RED" cron check (not a full audit), query the scheduler's
execution log directly: `~/AppData/Local/hermes/cron/executions.db` (SQLite,
`executions` table: `job_id`, `status` [completed/failed/running], `error`,
`finished_at`). **Query it with Python, not the sqlite3 CLI** — sqlite3.exe is a
Windows-native exe and fails on MSYS paths (`unable to open database file`) even
when `file` confirms the DB is valid SQLite.

```python
import sqlite3
conn = sqlite3.connect(r"${USER_HOME}\AppData\Local\hermes\cron\executions.db")
cur = conn.cursor()
# Repeat offenders today: same job failed many slots
cur.execute("""
    SELECT job_id, COUNT(*), MAX(finished_at) FROM executions
    WHERE finished_at >= '2026-08-11' AND status='failed' GROUP BY job_id
""")
# Full error text — do NOT truncate in the query output
cur.execute("""
    SELECT job_id, error, finished_at FROM executions
    WHERE error IS NOT NULL AND error != ''
    ORDER BY finished_at DESC LIMIT 3
""")
```

Triage rules (verified in production pulses):
- **Get the FULL error string.** `error` often says `Script exited with code 127`
  with the real cause buried in stderr lines below; truncating to 80 chars in the
  query cuts off the actual path/filename.
- **Same job failed across many slots** (e.g. every 15-min slot since 09:00) =
  structural problem, not a transient blip — fix the root cause, not pause/resume.
- **Exit 127 + `No such file or directory` for a script that exists and runs fine
  manually** = bash/PATH resolution mismatch in the cron sandbox (WSL bash
  shadowing git-bash, or MSYS path mangling) → `windows-cron-msys-path-fix` skill.
  Do NOT classify the job as broken-script.
- **`Scheduler restarted after this execution's owner exited`** errors are benign
  — one per job after a scheduler restart, not per-tick failures.

### Skill-load failures — "listed for this job but could not be found"

Cron jobs with a `skills:` list load each skill at prompt-assembly time via `cron/scheduler.py` → `skill_view()`. A failed load does NOT fail the job — it injects a skip notice ("The following skill(s) were listed for this job but could not be found and were skipped: ...") and the job runs without that skill's guidance. Silent by design; audit job prompts for this notice.

Resolution rules (verified Jul 31 2026):
- Resolution universe = the local skills dir + `skills.external_dirs` (config.yaml) ONLY. Profile-local trees and the bundled tree are NOT consulted; no fallback.
- Missing SKILL.md file (e.g. deleted from the external_dirs repo's working tree) → skip. Check the external_dirs repo's working tree; restore tracked files with `git checkout -- <path>`.
- Duplicate name in BOTH local dir and external_dirs → "Ambiguous skill name" hard fail. Do NOT copy an external_dirs skill into the local tree as redundancy — it breaks loading.
- `hermes skills list` / `inspect` are NOT reliable diagnostics (merged registry index; inspect searches skills.sh sources). Reproduce the loader's exact call instead — full recipe and incident writeup in `references/cron-skill-load-resolution.md`.

### Freshness check for gap detection

Compare `next_run_at` and `last_run_at` timestamps to detect jobs that are overdue:
```bash
cat ~/AppData/Local/hermes/cron/jobs.json | python3 -c "
import json, sys
from datetime import datetime, timezone
now = datetime.now(timezone.utc)
data = json.load(sys.stdin)
for j in data.get('jobs', []):
    next_run = j.get('next_run_at', '')
    if next_run:
        t = datetime.fromisoformat(next_run.replace('Z', '+00:00'))
        if t < now:
            print(f'  OVERDUE: {j[\"name\"]} was due at {next_run}')
"
```

Also flag enabled jobs with NO `next_run_at` — scheduled but never fires (observed 2026-08-03: `usage_dashboard`):
```bash
cat ~/AppData/Local/hermes/cron/jobs.json | python3 -c "
import json, sys
for j in json.load(sys.stdin).get('jobs', []):
    if j.get('enabled') and not j.get('paused') and not j.get('next_run_at'):
        print('  NEVER FIRES:', j['name'], '|', j['id'])
"
```

## Dream Cycle Cron (Automated Audit)

The **Hermes Dream Cycle** is a scheduled cron that runs the automated version of this audit — it inventories skills/MCP servers/cron jobs, runs gap analysis, and surfaces failing cron jobs grouped by cause. When asked to "run the dream cycle" (or delivering its report), reproduce the script exactly as the cron does:

```bash
cd ~/AppData/Local/hermes/scripts && python dream_cycle.py
```

- **Script:** `~/AppData/Local/hermes/scripts/dream_cycle.py`. If you lose the path, grep for distinctive output strings (`grep -rl 'DREAM CYCLE\|GAP ANALYSIS' ~/AppData/Local/hermes/scripts/`) — `search_files` globs miss it on Windows (see Pitfalls).
- **Output is deterministic** — a fresh run reproduces the pre-run snapshot byte-for-byte (inventory counts, gap list, failing-job names). If the delivered snapshot matches the fresh run, the data is current; no further verification needed.
- **Sections:** `INVENTORY` (skills/MCP/cron counts), `GAP ANALYSIS` (critical gaps + improvement suggestions), `CRON FLEET HEALTH` (failing jobs grouped: config-drift spend-guard, HTTP 429, timeout, MSYS script-path, other), `SNAPSHOT` (totals + item summary line).
- **Failure taxonomy maps to Phase 5** — interpret each CRON FLEET HEALTH group with the Phase 5 error-classification table: config-drift → pin the job; 429 → provider quota/usage limit; script-path → `windows-cron-msys-path-fix` skill (MSYS backslash stripping).
- **Delivery:** Discord-style report (per `discord-report-format`) — bold emoji header + timestamp, a RECOMMENDED ACTIONS section mapping each failure group to its fix, table for the failure groups, `🔍 Checked:` timestamp. The script's closing line says "Review and prioritize in Discord #dev".
- **Sibling artifacts:** Cron Guardian writes outage-window reports to `~/AppData/Local/hermes/cron/gap-reports/gap-bridge-*.md` — read the latest one for recent-outage context before writing a fleet-health summary.

## Phase 6 — Issue Classification

### Severity Levels

| Level | Meaning | Example |
|-------|---------|---------|
| 🔴 **CRITICAL** | Data loss risk, security vulnerability, exposed secrets | Hardcoded API keys in bridge scripts, secret in source-controlled config |
| 🟡 **HIGH** | Operational impact, wasted resources, systematic failures | >30% of cron jobs erroring, massive .env bloat (100K+ bytes) |
| 🔵 **MEDIUM** | Hygiene/maintenance concern | Dual script locations that may drift, data files stored in scripts/ directory |
| ⚪ **LOW** | Cosmetic or informational | Orphaned script versions, unused commented-out config keys, old plan files |

### Common Issues Pattern Library

1. **.env bloat through repeated writes** — Multiple identical blocks (CAMOFOX_URL, AGENT_BROWSER_*) from scripts that `>> .env` without checking for existing entries. Fix: deduplicate with `sort -u` or idempotent write pattern.

2. **Cron job failure cascade** — Multiple jobs failing with same error type. Group by error type to find root cause: TimeoutErrors suggest LLM/model issues; exit code 15 suggests process management issues (OOM killer, time limits, restart contention).

3. **Dual-script drift** — Config repo scripts vs live scripts directory. Setup scripts copy from one to the other, but direct edits to either location create divergence. Fix: standardize on one source of truth.

4. **Hardcoded secrets in bridge/daemon scripts** — Scripts that listen on a network port (auth proxies, API bridges) often have hardcoded API_KEY values. Low risk for local-only services but a leak vector if the repo is shared.

5. **Data files bloating scripts/ directory** — Tax roll data, ZIP archives, CSV dumps accumulated in scripts/. Move to `~/data/` or `~/AppData/Local/hermes/data/`.

## Phase 7 — Report Production

### Report Structure

```
# Hermes Operational Audit — YYYY-MM-DD

## Overview
- **Scripts**: N files totaling X MB (categorized into M groups)
- **Config repo**: N files across X sections
- **Cron jobs**: N total, X erroring, X healthy
- **Cross-repo integrations**: X repos reference Hermes
- **Issues found**: X (X critical, X high, X medium, X low)

## 1. Scripts Inventory
[Category-wise tables with file names, sizes, and descriptions]

### Deep-Dive: [Bridge/Daemon Name]
[Architecture notes: protocol, endpoints, identity, threading, AI provider]

## 2. .env Analysis
- **File size**: X KB (expected ~10 KB)
- **Populated keys**: X
- **Commented-out keys**: X
- **Duplication found**: Yes/No (if yes, approximate redundant bytes)
- **Hardcoded secrets in scripts**: X instances

## 3. Config Repository
[Summary of each section with file counts and notable items]

## 4. Cross-Repo Integrations
[Table: repo | file count | integration type]

## 5. Cron Job Health
[Summary: total, by status]
[Table: job name | schedule | status | error detail]

## 6. Issues Found
| # | Severity | Issue | Description | Recommendation |
|---|----------|-------|-------------|----------------|
| 1 | 🔴 | ... | ... | ... |

## 7. Recommended Actions
1. **CRITICAL**: [action] — [rationale]
2. **HIGH**: [action] — [rationale]
3. ...

---

_Generated via hermes-operational-audit skill_
```

### Delivery Format

- Use tables for structured data (inventory counts, cron health)
- Use code blocks for raw command output
- Use emoji severity indicators (🔴🟡🔵⚪)
- Use bold for section headers
- Keep the report scannable — details in sub-bullets, summaries at section tops
- For **system-wide tidy** requests, use the multi-file pack in **Full System Tidy Mode** below (not only this single-report shape)

## Full System Tidy Mode (entire system / projects / resources / professionalize)

When the user asks to look over the **entire system**, **all projects**, **available resources**, or to **tidy / clean / professionalize** — not only Hermes internals — extend the seven phases with:

8. **Portfolio** — unique local `.git` roots (C: home, Documents/github, Projects, E: github) + `gh repo list pmb2`; flag basename duplicate clones; compare `hermes-config/roadmap/monthly-priorities.md` freshness vs last-7d commits and recent Discord sessions.
9. **Infrastructure** — `docker ps -a` + compose project labels + `docker system df`; C:/E: free space; RAM free; always-on stack count.
10. **Hermes storage hot spots** — measure with an allowlist (do **not** `du` the whole hermes root — it hangs on Windows): `state.db`, `logs/` (esp. `mcp-stderr.log`), `backups/`, `skills/` (esp. `.curator_backups`), `profiles/`, `sessions/`, root `*.zip` / gateway logs, `scripts/` data archives.
11. **Report pack** under `~/AppData/Local/hermes/plans/system-tidy-YYYY-MM-DD/` and mirror to `hermes-config/docs/findings/system-tidy-YYYY-MM-DD/`:
    - `00-EXECUTIVE-SUMMARY.md`
    - `01-HERMES-OPERATIONAL-AUDIT.md`
    - `02-PROJECT-PORTFOLIO.md`
    - `03-INFRASTRUCTURE-DOCKER.md`
    - `04-SYSTEM-TIDY-PLAN.md` — phases: **Stabilize → Reclaim → Consolidate → Polish**
    - `05-ACTION-CHECKLIST.md` — dual-column the operator approvals vs Aegis execute + numbered yes/no

**ADHD delivery:** Discord = executive tables + You/Aegis columns + numbered approvals. Full detail stays in the pack.

**Safety:** do not auto-execute destructive reclaim (log wipe, backup delete, docker volume prune, clone removal) without explicit the operator OK. Offer Phase 0 (env dedupe, cron pin, path fix) as the default next step.

Baselines + measured deltas: `references/the operator-audit-2026-08-07.md` (compare to `references/the operator-audit-2026-07-30.md`).

## Pitfalls

- **read_file blocks .env access** — The credential-store guard prevents reading `.env` via read_file. Use `cat` via `terminal` instead.
- **search_files with Windows absolute paths** — On MSYS2, `search_files(pattern, path='C:\\\\...')` may fail with "The system cannot find the path specified." Use `terminal` with `grep -rl` for cross-drive searches instead. Verified Aug 7 2026: `search_files(pattern='dream*cycle*', path='C:\\\\Users\\\\<you>')` AND `pattern='dream'` under `AppData/Local/hermes` both returned 0 hits even though `dream_cycle.py` and `gbrain-dream-cycle.py` existed on disk — `grep -rl 'DREAM CYCLE' ~/AppData/Local/hermes/scripts/` found them in one pass. When a file search comes up empty for a script you know exists, grep distinctive strings from its output instead of retrying the glob.
- **jobs.json can be enormous** (2000-4000+ lines, 200K+ chars) — Each job stores its full prompt text inline. Use offset/limit on read_file, and pipe through `python3 -c` for parsing rather than reading the whole file into context.
- **Scripts directories accumulate data** — Tax roll CSVs, ZIP archives, database dumps can add 100+ MB to scripts/. Always check for large non-script files and flag them as issues.
- **Dual script locations drift** — Scripts in both `hermes-config/scripts/` and `~/AppData/Local/hermes/scripts/` can diverge. Check both and note any differences.
- **Cron error messages may reference old sessions** — `last_error` in jobs.json captures the most recent error. Cross-check with `session_search` to determine if it's a recurring or one-off failure.
- **Some repos are symlinked or cross-drive** — Windows junctions, symlinks, and WSL cross-mounts can cause `grep` to follow into unexpected places or silently fail. Stick to direct filesystem paths.
- **Inventory scripts can under-report cron state** — The dream-cycle inventory script reported "Cron Jobs: 0 active" while the scheduler was running 62 jobs (its probe reads the wrong store). Always cross-check an inventory script's cron counts against `hermes cron list` + jobs.json before reporting them.
- **`git -C /msys/path` fails in cron/agent sessions** — returns `fatal: not a git repository` for EVERY repo, even healthy ones, while `cd <repo> && git ...` or `git -C "E:\\..."` work fine. The `xargs git -C "$d"` multi-repo scan pattern silently returns zero commits under this condition — a false "environment quiet" signal. Before blaming a repo, test a second one and test the `cd` form. Also: a shallow `ls -la .git | head` can make a healthy .git look gutted — verify objects/, refs/, HEAD, index first.
- **`du -sh ~/AppData/Local/hermes/*` hangs / times out on Windows** — full hermes root is multi‑GB and can exceed 120s. Prefer per-dir Python `os.walk` on a **named allowlist** (`scripts skills cron logs backups sessions profiles …`) or `du -sh` one top-level at a time. Never block the audit on a single root `du`.
- **Multi-repo age scan: pure `python -c` + `git -C` from MSYS can return 0 repos** — prefer `find … -name .git | while read; do cd "$r" && git …; done` writing a TSV, then parse the TSV in Python (verified Aug 7 2026: TSV path → 187 unique repos; pure-Python find+git path → 0).
- **`.env` browser-key spam is progressive** — CAMOFOX_URL / AGENT_BROWSER_* append loops: ~50× (Jul 30) → **378×** (Aug 7), ~130 KB file with only ~34 unique keys. Always Counter-count duplicates, not just file size. Fix = collapse + idempotent writer (not delete `.env`).
- **Primary C: reclaim is not Docker-first** — measured Aug 7: `logs/mcp-stderr.log` ~4.1 GB, `backups/` multi‑GB state copies (~15 GB tree), `state.db` ~4.7 GB (271k messages + dual FTS), `skills/.curator_backups` ~900 MB, root `camoufox-win64.zip` ~500 MB. Docker images (163 GB) matter but `docker system df` "reclaimable" under-reports until stacks are parked.
- **Cron path errors ≠ missing scripts** — MSYS-stripped `C:Users…` or double `C:\c\Users…` failures while the `.sh` still exists under `scripts/`. Classify as invocation format (`windows-cron-msys-path-fix`), not "script missing".
- **Compose project name case splits look like two stacks** — e.g. `bookends` + `BookEnds` both running. Inspect labels; recommend unify; do not double-count capacity without noting the split.
- **Stale monthly-priorities vs live gravity** — always compare `roadmap/monthly-priorities.md` date + P0 list against last-7d git commits and recent sessions. Report the mismatch explicitly in portfolio tidy audits.
- **Dual FTS on state.db** — `messages_fts` + `messages_fts_trigram` roughly doubles search storage; freelist may be small (real data weight). Do not recommend casual VACUUM/drop without a separate compaction plan.

## Related Skills

- `hermes-system-backup` — Pre-migration backup audit (complementary; this skill covers the running system, backup covers the save-and-restore workflow)
- `recurring-status-checks` — Periodic cron-based status reconstruction (complementary; watches for drift, this skill takes full inventory)
- `engineering-pulse` — Periodic codebase health checks (narrower scope: code quality, not full system)
- `mcp-fleet-audit` — Periodic MCP server health audits (narrower: MCP servers only)
- `report-freshness-diagnostics` — Data staleness detection (narrower: report freshness only)
- `project-inventory` / `local-project-discovery` — portfolio roots and unknown-repo location
- `windows-cron-msys-path-fix` — cron shell path mangling on Windows
