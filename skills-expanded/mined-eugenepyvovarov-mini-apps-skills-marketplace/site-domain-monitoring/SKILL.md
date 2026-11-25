---
name: Site Domain Monitoring
description: Monitor websites/domains and check (1) domain registration expiration (RDAP with optional WHOIS fallback), (2) SSL certificate expiration, and (3) optional HTTP responsiveness (expect 200). Use when user needs a table view of site health/expiry and to emit notifications when SSL/domain expires in less than N days or a site becomes unresponsive.
category: Monitoring
keywords: domain expiry, ssl certificates, rdap, monitoring, notifications
tags: infrastructure, maintenance, security
---

## 1) Mini-application purpose
- User problem this skill solves: Keep a small database of sites and regularly detect expiring domains/SSL certs and broken HTTP 200 responses, with a compact table view.
- Target user: Someone maintaining multiple sites/domains and wanting early warning (< 10 days by default).
- Primary success metric: A single `check` run returns a table and clear alerts for any site that is expiring soon or failing HTTP checks.

## 2) End-to-end flows

### `setup_wizard`
- Trigger: "Set up site expiry monitor", "start tracking these domains", "create the database for checks".
- Inputs:
  - Optional: threshold days (default: 10)
  - Optional: enable HTTP 200 check per site (default: enabled)
  - One or more sites (domain and/or URL)
- Step-by-step behavior:
  1. Confirm skill root (this folder) and inferred project root (two levels above `skills/`).
  2. Create the standard data layout under `<project_root>/.skills-data/site-expiry-monitor/`.
  3. Initialize the SQLite DB (`sites.db`).
  4. Add the provided sites to the DB.
  5. Run a first check and show the table.
- Success output: A populated DB and a first-run table.
- Error handling:
  - If RDAP cannot find domain expiry, keep `domain_expiry` blank and continue.
  - If SSL connect fails, record the error and continue.
  - If HTTP check fails, record the status/error and continue.
- Re-entry condition: Re-run setup to add more sites, or run `list`/`check` anytime.

### `primary_operation`
- Trigger: "Check all sites", "show me the status table", "notify me if anything is expiring", "is example.com still healthy".
- Inputs:
  - Optional: `--threshold-days` (default: 10)
  - Optional: `--notify` (send macOS notification if there are alerts)
  - Optional: filter by `--id` or `--domain`
- Step-by-step behavior:
  1. Load DB from `<project_root>/.skills-data/site-expiry-monitor/data/sites.db`.
  2. For each selected site:
     - Fetch SSL certificate `notAfter` for `<domain>:443`.
     - Fetch domain expiry via RDAP; optionally fall back to `whois` if RDAP fails.
     - If enabled for the site, request the URL and require HTTP 200.
  3. Update last-check fields in the DB.
  4. Print a table view with expiry dates, days remaining, HTTP status, and alert reasons.
  5. If `--notify` and any alerts exist, send a single macOS notification summarizing alerts.
- Success output: Updated DB + a printed table + (optional) notification.
- Error handling: Never stop the whole run because one site fails; keep partial results and per-site errors.
- Re-entry condition: Safe to run repeatedly (cron/launchd).

### `status_check`
- Trigger: "List tracked sites", "what are we monitoring", "show current config".
- Inputs: None (optionally `--json`).
- Step-by-step behavior:
  1. Print a table of tracked sites and their last-known check state.
- Success output: Table view (or JSON).
- Error handling: If DB missing, instruct to run `init` / setup wizard.
- Re-entry condition: Anytime.

## 3) Setup wizard
- Step sequence (must be numbered and fixed):
  1. collect_scope
  2. collect_inputs
  3. validate_and_confirm
  4. write_state
  5. verify
  6. handoff

1. `collect_scope`
   - Question: "Use project root `/Users/eugenep/Projects/skill-app` and data dir `<project_root>/.skills-data/site-expiry-monitor/`?"
   - Default: yes (auto-infer when skill lives under `*/skills/<skill-name>/`).
   - Stop condition: User confirms or provides `--project-root` override.

2. `collect_inputs`
   - Question: "Which sites should be tracked (domains/URLs), and should HTTP 200 checks be enabled?"
   - Accepted inputs: list of domains (`example.com`) and/or URLs (`https://example.com/`).
   - Defaults: `threshold_days=10`, `check_http=true`, `expected_status=200`.

3. `validate_and_confirm`
   - Validation rules:
     - Domain must be a hostname (no scheme, no path).
     - URL must be http/https.
   - Confirm exact actions: create data dirs, create/update DB, insert site rows.

4. `write_state`
   - Commands (run from this skill root):
     - `python3 scripts/ensure_skill_data.py --skill-root .`
     - `python3 scripts/setup_envs.py --skill-root . --python`
     - `python3 scripts/site_expiry_monitor.py init`
     - `python3 scripts/site_expiry_monitor.py add --domain example.com --url https://example.com/ --label Example`

5. `verify`
   - Command: `python3 scripts/site_expiry_monitor.py check --threshold-days 10`
   - Stop condition: Table prints and at least one row appears.

6. `handoff`
   - Next steps:
     - Run on-demand checks: `python3 scripts/site_expiry_monitor.py check --notify`
     - List tracked sites: `python3 scripts/site_expiry_monitor.py list`
     - Schedule periodic checks (cron/launchd): run the `check --notify` command on an interval.

## 4) Action contract (AI execution policy)
- Only use these writable paths without confirmation:
  - `.codex/skills/site-expiry-monitor/`
  - `<project_root>/.skills-data/site-expiry-monitor/`
- Avoid broad discovery commands unless explicitly requested.
- Prefer these deterministic commands:
  - `python3 scripts/ensure_skill_data.py --skill-root .`
  - `python3 scripts/setup_envs.py --skill-root . --python`
  - `python3 scripts/site_expiry_monitor.py init|add|remove|list|check`

## 5) Local data and env
- Mutable state lives under `<project_root>/.skills-data/site-expiry-monitor/`:
  - DB: `data/sites.db`
  - RDAP cache: `cache/rdap_dns.json`
- `.skills-data/site-expiry-monitor/.env` keys created by `ensure_skill_data.py`:
  - `SKILL_ROOT`, `SKILL_NAME`, `SKILL_DATA_ROOT`, `SKILL_DATA_DIR`
- Python venv (optional): `.skills-data/site-expiry-monitor/venv/python/`

## 6) Completion checklist
- `setup_wizard`, `primary_operation`, `status_check` flows defined.
- Setup wizard ≤ 6 steps and runnable commands included.
- Data paths are confined to skill root and `.skills-data/site-expiry-monitor/`.
- Script prints a table and can emit notifications on alert conditions.
