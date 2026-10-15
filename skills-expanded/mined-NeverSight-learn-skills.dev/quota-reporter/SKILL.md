---
name: quota-reporter
description: Install and run a local quota guard that checks current Codex and Claude quota every 15 minutes, syncs the current auth for each source to the shared encrypted auth pool only when it changes, fetches a better auth from the cloud when local quota is low, and stores the user's personal company-email access token locally. Use this whenever a teammate wants to join the shared auth pool, install the 15-minute guard, set up a company-email auth-pool token, or verify that local auth rotation is working.
---

# Quota Guard

This skill installs and runs the local quota guard for Codex and Claude.

## What it does

1. Tracks the current local auth state per source in `~/.agents/auth/known_auth.json`
2. Uploads the current auth for each source to the shared encrypted auth pool only when the auth changed
3. Probes the current local Codex quota and the current local Claude quota to decide whether the current machine should rotate
4. When local quota is low, asks the cloud auth pool for a strictly better auth from the same source and installs it locally
5. Installs a reboot-safe scheduler that runs every 15 minutes
6. Stores the user's personal company-email auth-pool token locally so future runs can upload and fetch without prompting again

## Files

- Combined local guard: `scripts/quota_guard.py`
- Installer: `scripts/install_quota_guard.py`
- Claude statusline hook: `scripts/claude_statusline_probe.py`
- Internal shared helper library: `scripts/quota_reporters.py`
- Remote worker trigger/watch: `scripts/trigger_remote_probe.py`
- Archived legacy scripts: `archive/`
- Skill overview: `README.md`

## Required inputs

You need:

- the shared auth-pool URL, for example `https://quota-report-hub.vercel.app`
- a personal auth-pool user token issued by company email

That same personal token is also used to unlock the hosted dashboard.

## Standard flow

### Install the 15-minute guard

Run:

```bash
python3 scripts/install_quota_guard.py \
  --auth-pool-url https://your-dashboard.vercel.app \
  --email your.name@stardust.ai
```

The installer:

- asks for a company email if one was not provided
- requests an emailed personal token from `/api/auth/issue-token`
- asks the user to paste the token back into the terminal
- writes the local config file under `~/.agents/auth/quota-reporter.json`
- installs the 15-minute scheduler
- writes Claude Code `statusLine` settings to `~/.claude/settings.json`

Token rules:

- only the latest token for an email remains valid
- requesting a new token revokes the old one
- the latest token can still be reused on multiple machines

If the user is not already using a compatible hub, the correct order is:

1. either deploy a new hub with `scripts/deploy_vercel.py` or confirm an existing hub already supports the auth-pool APIs
2. then run `install_quota_guard.py`
3. then paste the emailed token
4. then let the scheduled guard handle the rest

### Run one manual guard cycle

```bash
python3 scripts/quota_guard.py
```

### Trigger one remote cloud probe

```bash
python3 scripts/trigger_remote_probe.py
```

This script:

- triggers the GitHub Actions workflow `probe-auth-pool.yml`
- waits for the newly created `workflow_dispatch` run on `main`
- prints the run id as JSON
- watches the run until it finishes
- then fetches the hub status and returns a compact result row for each auth

If you only want the run id and do not want to attach to the live log:

```bash
python3 scripts/trigger_remote_probe.py --no-watch
```

The guard then:

- updates `~/.agents/auth/known_auth.json`
- uploads the current auth to the auth pool only when needed
- probes the current live Codex auth and Claude auth
- if a local source is below `20%` in `5H` or below `5%` in `1week`, calls `/api/auth/fetch-best` with `source + current local account + current local quota`
- only accepts a server response when it contains a strictly better replacement from that same source
- only replaces local source credentials when the fetched auth is different from what is already installed
- shows a desktop notification after a successful local replacement so the user knows to quit the current Codex or Claude Code session and start a new one
- does nothing when the cloud cannot provide a better auth than the current one
- relies on the cloud auth pool to deduplicate repeated uploads for the same `account_id`, even when raw files differ
- if the same account is refreshed locally, the changed `auth_last_refresh` is enough to trigger a new upload

Operational notes:

- replacing `~/.codex/auth.json` does not hot-switch already running Codex sessions
- the next new Codex session is the one that should pick up the new auth
- the local config file contains a personal token and should stay private
- the cloud dashboard shows the latest cloud-worker probe for each auth entry
- Codex rows are refreshed by the cloud worker
- Claude rows are refreshed by the cloud worker only when the local machine is using a direct Claude subscription. If `~/.claude/settings.json` injects `ANTHROPIC_*` provider credentials, the skill skips Claude cloud uploads for that machine.

## Output expectations

- After installation, show the scheduler type, config path, and Claude statusline settings path.
- After a manual guard run, show the current Codex and Claude probe payloads plus whether a replacement happened for each source.
- If token request, auth upload, or best-auth fetch fails, include the HTTP status and response body.
