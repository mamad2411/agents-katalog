---
name: gram-cli
description: Instagram operations through the gram/glam CLI for login/cookie auth, profile post downloads, stories/highlights capture, and account checks. Use when asked to read or download Instagram content, verify gram-cli auth, or run publication asset collection flows from gram-cli.
cluster: social-media
version: 1.0.0
---

# Gram CLI

## Overview

Use this skill to operate Instagram workflows via a deterministic wrapper:
`scripts/run-glam.sh` (which prefers `<gram-cli-repo>/.venv/bin/glam`).
Default behavior is read/download mode. Treat auth persistence updates as state-changing.

If you need a custom binary path, set `GRAM_CLI_BIN`.

## Capability Map

- Identity/preflight: `check`, `whoami`
- Auth setup: `login` (browser profile cookie extraction, optional save)
- Read/download: `profile`, `post`, `stories`, `highlights`
- Global behavior: `--json`, `--quiet`, `--output`, config loading via `--config`

Load command specifics from `references/commands.md` and auth details from `references/authentication.md`.

## Workflow

### 1. Preflight

1. Confirm CLI availability:
   - `bash scripts/run-glam.sh --help`
2. Confirm runtime:
   - `bash scripts/run-glam.sh --version`
3. Check auth state:
   - `bash scripts/run-glam.sh check`
   - `bash scripts/run-glam.sh whoami`

If auth checks fail, report exact error and stop before downloads that require authentication.

### 2. Read/Download Defaults

Use read/download commands by default:

- `glam profile <username> [--posts|--stories|--highlights] [--limit N] [--resume]`
- `glam post <instagram-post-url>`
- `glam stories [<username>]`
- `glam highlights <username>`

Use the wrapper form in execution:

- `bash scripts/run-glam.sh profile <username> ...`
- `bash scripts/run-glam.sh post <url> ...`
- `bash scripts/run-glam.sh stories <username> ...`
- `bash scripts/run-glam.sh highlights <username> ...`

Guardrails:

- Prefer bounded fetches (`--limit`) for large profiles.
- Use `--resume` when re-running profile exports.
- Use `--output <dir>` to control publication asset destinations.
- Prefer `--json` for machine-readable downstream pipelines.

### 3. State-changing Actions

Treat these as state-changing:

- `glam login --save` (writes credentials/config)

Run state-changing actions with explicit confirmation when the write target/config change is not already approved.

### 4. Publishing Asset Pattern

For publication pipelines:

1. Collect sources with read commands (`profile`/`post`/`stories`/`highlights`).
2. Summarize what was downloaded (count, paths, failures).
3. Return deterministic file paths for downstream OpenClaw publishing agents.

## Auth and Config Notes

Auth precedence:

1. Environment vars (`INSTAGRAM_SESSIONID`, `INSTAGRAM_CSRFTOKEN`, `INSTAGRAM_DS_USER_ID`)
2. Config file (`~/.config/glam/config.json5`, legacy fallback `~/.config/gram/config.json5`)
3. Browser extraction via `login --chrome-profile` or `--firefox-profile`

Use `login --print-env` only when explicitly requested; avoid printing secrets by default.

Deterministic binary resolution order:

1. `GRAM_CLI_BIN` (if set)
2. `<gram-cli-repo>/.venv/bin/glam`
3. `glam` in `PATH`
4. `gram` in `PATH`

## Maintenance

Refresh help snapshot when CLI changes:

```bash
bash scripts/capture_help_snapshot.sh
```

This writes `references/help-snapshot.txt`.
