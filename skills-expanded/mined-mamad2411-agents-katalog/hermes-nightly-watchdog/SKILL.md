---
name: hermes-nightly-watchdog
version: 1.0.0
author: Hermes Agent
license: MIT
description: Overnight auto-restarter that updates Hermes Agent + Gateway, checks repos/Camoufox/PIM, scans AI news, and produces a morning report at 3 AM ET
metadata:
  hermes:
    tags: [hermes, cron, watchdog, overnight, maintenance, camoufox]
    triggers:
      - nightly watchdog
      - overnight restarter
      - morning report
      - hermes auto update
      - nightly maintenance
    related_skills: [hermes-agent, gateway-troubleshooting, self-hosted-communication-server]
---

## Overview

The Hermes Nightly Watchdog runs every night at 3 AM ET via cron. It:
1. Updates Hermes Agent (`hermes update -y`)
2. Checks pip package updates
3. Pulls all git repos (hermes-config, agent-fleet, tor-browser-mcp, hermes-agent)
4. Scans AI news and upstream releases for enhancements
5. Checks the PIM system for new content
6. Checks Camoufox browser health (auto-starts if stopped)
7. Restarts the Hermes Gateway
8. Monitors the gateway for errors
9. Generates a markdown report
10. Commits the report to hermes-config repo

## Schedule

- Cron: `0 3 * * *` (3 AM ET daily)
- Job ID: `1b56cee1074f`
- Delivery: Back to origin chat

## Script Location

`~/.hermes/scripts/hermes-nightly-watchdog.py`

## Report Location

`~/.hermes/nightly-reports/nightly-YYYY-MM-DD.md`

The report is also committed to `${MY_REPOS}/Documents/github/hermes-config/nightly-reports/`.

## Phases

| Phase | Timeout | Description |
|-------|---------|-------------|
| Hermes Agent Update | 300s | `hermes update --check` then `hermes update -y` |
| Pip Updates | 60s | `pip list --outdated` |
| Git Repos | 60s each | Fetch, pull, commit, push for all repos |
| AI News | 30s | Check upstream releases and commits |
| PIM Check | 30s | Check PIM DB size and recent activity |
| Camoufox Check | 30s | Health check against :9377, auto-start if stopped |
| Gateway Restart | 30s + 15s | `hermes gateway stop -> start -> status` |
| Health Check | 10s | Disk, memory, uptime |

## Time Budget & Overall Timeout

The cron wraps the **entire script** in a 120s timeout. With 8 phases and worst-case sub-timeouts summing to ~600s, the script **will** hit the 120s wall on a slow night. Mitigations:
- Run phases in sequence and bail early if a phase has already consumed its share of the global budget.
- Set each sub-phase timeout to at most 30s and skip phases that timed out.
- For manual invocation (bypassing cron), run `python script.py` without a wrapper timeout or run phases individually from the terminal with higher per-phase timeouts.

## Repos Checked

- `~/.hermes/hermes-agent` (Hermes Agent source)
- `${MY_REPOS}/Documents/github/hermes-config` (Config + reports)
- `${MY_REPOS}/Documents/github/agent-fleet` (Gateway runner)
- `${MY_REPOS}/Documents/github/tor-browser-mcp` (Forked MCP server)

## Troubleshooting

- If `hermes update` hangs, check git connectivity in the Hermes repo
- If gateway restart fails, run `hermes gateway status` manually
- The cron runs autonomously; for manual invocation: `python ~/.hermes/scripts/hermes-nightly-watchdog.py`
- If the script times out, run phases individually using the commands in `references/manual-diagnostic-commands.md`.

## Pitfalls & Known Issues

### 1. Total Script Timeout (120s from cron)

The cron job wraps the entire script in a 120s timeout. If any single phase hangs (e.g. `pip list --outdated`, Camoufox health check, git fetch on a slow connection), the entire script is killed. **Mitigation:** For manual runs, invoke phases individually with longer timeouts. For cron, consider shortening sub-phase timeouts or adding a global watchdog that kills early if budget is exhausted.

### 2. `pip list --outdated` Commonly Times Out

On this system with 868 installed packages, `pip list --outdated` checks the network for each package and frequently exceeds the 60s timeout. **Alternatives:**
- Use `pip list --outdated --format=freeze` (lighter parsing, still may time out)
- Use `pip list --format=freeze | wc -l` for a quick package count only
- Run `pip list --outdated` with `--timeout=5` to cap per-request waits
- Skip the phase entirely on the third consecutive timeout

### 3. `free` and `uptime` Not Available on MSYS2/Windows

The `phase_health_check()` function calls `["free", "-h"]` and `["uptime"]`. Neither binary exists under MSYS2/Git Bash on Windows. These silently fail and return empty strings. **Fix:** Replace with:
- Memory: `wmic OS get TotalVisibleMemorySize,FreePhysicalMemory /value` (or `powershell Get-CimInstance Win32_OperatingSystem`)
- Uptime: `wmic OS get LastBootUpTime /value` 
- Or use `cat /proc/loadavg` which does work under MSYS2

### 4. hermes-agent Source Dir May Not Be a Git Repo

The script checks `~/.hermes/hermes-agent` as a git repo. When Hermes is installed via pip (as it is on this system), that directory may not exist or may not be a git checkout. **Fix:** Check if `.git` exists before running git commands, or detect via `pip show hermes-agent | grep Location` to find the actual install path.

### 5. Branch-Agnostic Git Ahead/Behind Check

The script hardcodes `origin/main` for ahead/behind counting. Repos may use other branch names:
- hermes-config → `vps-hybrid`
- agent-fleet → `migration/discord-to-spacebar`
- tor-browser-mcp → `pmb2/hardened-tor-mcp`
**Fix:** Use `@{u}` (upstream tracking reference) instead of a hardcoded branch name: `git rev-list --count HEAD..@{u}` and `git rev-list --count @{u}..HEAD`.

### 6. Camoufox May Not Be Installed, Not Just Not Running

The Camoufox check assumes the browser is installed but stopped. On this system, no Camoufox/Camofox binary is installed at all — no binary on PATH, no process, port 9377 unreachable. **Fix:** Probe in order:
1. `which camofox || which camoufox` → if not found, report "Camoufox not installed" and skip
2. `curl -s http://127.0.0.1:9377/health` → if no response, report "not running"
3. Only attempt auto-start if binary is found

### 7. Gateway May Already Be Running

`hermes gateway stop` followed by `hermes gateway start` when the gateway is already running is a no-op (start reports "already running"). **Fix:** Check `hermes gateway status` first. If running with a valid PID, log it and skip the restart cycle. Only stop/start if the gateway is in a failed state.

### 8. Commit Report: `@{u}` Tracks Correct Remote Branch

When committing the nightly report to hermes-config, the script should use the current branch's upstream tracking reference rather than assuming `origin/main` for push, since hermes-config uses `vps-hybrid` as its default branch.

### Common Script Pitfall: Integer args in subprocess.run()

On Windows, `subprocess.run()` with a command list (`shell=False`) calls `list2cmdline()` internally, which maps `os.fsdecode()` over every element. **All elements must be strings** — passing an integer like `5` or `3` for a CLI flag value (e.g. `["gh", "release", "list", "-L", 5]`) raises `TypeError: expected str, bytes or os.PathLike object, not int` at call time, not at the subprocess level.

**Fix:** Convert all numeric CLI arguments to strings: `["gh", "release", "list", "-L", "5"]`.

**Detection:** Grep for `, \d+],` patterns in subprocess call sites — every match is a potential crash.

This error surfaces at runtime, not at import time, so it may slip past local testing if the affected code path is conditional.
