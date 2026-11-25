---
name: plex
description: Use this skill when you need to work with Plex Media Server through the shell command surface under `scripts/commands/`. It can verify connectivity, list libraries, search media, inspect sessions and metadata, read the Watchlist, and trigger a library refresh.
---

# Plex Skill

## Overview
- Public command surface: `scripts/commands/`
- Internal runtime: `scripts/lib/`
- Output: JSON by default

## Main Rule

Use `scripts/commands/` as the public interface.
Do not call `scripts/lib/` directly.

## Requirements

- Bash
- `curl`
- Plex server URL and token

Keep runtime config in `assets/env`, created from `assets/env.example`, and never expose a real `PLEX_TOKEN`.
HTTPS requests use `curl -k` by default.

## Public Interface

- `scripts/commands/server/*`
- `scripts/commands/watchlist/*`

## Output Rules

- Commands return JSON on success.
- Commands return JSON on failure with `success: false` and an `error` message.
- `refresh_section.sh` is a write action and should only be used when the user explicitly asks for a scan.

## Commands

### Server

```bash
scripts/commands/server/ping.sh
scripts/commands/server/libraries.sh
scripts/commands/server/search.sh --query "Alien" --limit 20
scripts/commands/server/recently_added.sh --section-id 1 --limit 10
scripts/commands/server/sessions.sh
scripts/commands/server/metadata.sh --rating-key 12345
scripts/commands/server/refresh_section.sh --section-id 1
```

### Watchlist

```bash
scripts/commands/watchlist/list.sh
scripts/commands/watchlist/list.sh --filter movie
scripts/commands/watchlist/list.sh --sort titleSort:asc
```

## JSON Contract

- base envelope: `{"success": true, ...}` or `{"success": false, "error": "..."}`
- ping: `{"success":true,"server":{"friendlyName":"...","version":"...","machineIdentifier":"...","platform":"...","updatedAt":1700000000}}`
- libraries: `{"success":true,"count":1,"libraries":[...]}`
- search and recently added: `{"success":true,"count":N,"items":[...]}`
- sessions: `{"success":true,"count":N,"sessions":[...]}`
- metadata: `{"success":true,"ratingKey":12345,"found":true,"items":[...]}`
- watchlist: `{"success":true,"count":N,"items":[...]}`

## Operational Notes

- Config precedence is CLI flags, then shell environment variables, then `assets/env`.
- Create `assets/env` from `assets/env.example`.
- The Watchlist uses Plex Discover cloud APIs. The other commands use the local Plex server API.
- Public wrapper scripts delegate parsing and output shaping to `scripts/lib/plex_runtime.sh`.

## Safety Boundaries

- Read commands are safe by default.
- `refresh_section.sh` is the only supported write command.
- Internal test files under `tests/` are not public API.
- The Watchlist is a Plex Discover cloud feature. It is not part of the local Plex server API.
- Never print or store real `PLEX_TOKEN` values in chat, logs, or fixtures.
