---
name: morgen
description: Manage calendars, events, tasks, and tags through the Morgen API (docs.morgen.so). Use when the user mentions Morgen, asks to list/create/update/delete calendar events or tasks across Google Calendar, Microsoft 365, iCloud, Fastmail, or CalDAV accounts connected through Morgen, or wants to query connected integrations and tags. Credentials live at `~/.config/morgen-skill/credentials.json`.
---

# Morgen

Unified calendar + task operations via the Morgen REST API v3. Morgen is a single surface over Google Calendar, Microsoft 365, iCloud, Fastmail, and CalDAV accounts, plus native Morgen tasks. This skill wraps the HTTP API with `curl` + `jq` helpers.

## Trigger conditions

Invoke this skill when the user says any of:
- "list my calendars" / "what calendars do I have in Morgen" → `scripts/calendars.sh list`
- "show my events for <date range>" / "what's on my calendar" → `scripts/events.sh list`
- "create an event" / "schedule a meeting" → `scripts/events.sh create`
- "update event" / "delete event" / "move event" → `scripts/events.sh update|delete`
- "what's on my TODO list" / "show my todos" / "today's tasks" / "overdue tasks" → `scripts/todos.sh list|today|overdue`
- "add a todo" / "new task for ..." → `scripts/todos.sh add`
- "mark X done" / "complete X" / "reopen X" → `scripts/todos.sh done|reopen`
- "sync my tasks" / "refresh todos" → `scripts/todos.sh sync`
- "list my tasks" / "raw tasks list" (API passthrough without cache) → `scripts/tasks.sh list`
- "create a task" / "add a task" → `scripts/tasks.sh create` (or prefer `todos.sh add` which also updates the cache)
- "complete task" / "close task" / "reopen task" → `scripts/tasks.sh close|reopen`
- "list integrations" / "what accounts are connected" → `scripts/integrations.sh accounts`
- "list tags" / "create a tag" → `scripts/tags.sh list|create`
- "set up Morgen" / "configure Morgen" / credentials file missing → follow the **Setup flow** section below (Claude orchestrates via `scripts/setup.sh --stdin`)

For personal TODO workflows, **prefer `todos.sh`** over the raw `tasks.sh`: it caches the task list locally (`~/.cache/morgen-skill/todos.json`) so filtered reads cost 0 rate-limit points.

## Prerequisites

Before any operation, check the credentials file exists:

    test -f ~/.config/morgen-skill/credentials.json

If it does not exist, run the skill-orchestrated setup flow below.

Dependencies: `curl`, `jq`. If missing, the scripts exit 127 with a message.

## Setup flow (skill-orchestrated)

`setup.sh` supports three modes:

1. **Interactive (TTY only)** — `bash scripts/setup.sh`. User runs this themselves in a terminal when Claude can't.
2. **Non-interactive via stdin** — `bash scripts/setup.sh --stdin <<< "$KEY"`. Preferred for skill orchestration; the key never appears in this script's argv.
3. **Non-interactive via flag** — `bash scripts/setup.sh --key <KEY>`. Convenient but the key is briefly visible in `/proc/<pid>/cmdline`. Acceptable on a personal single-user machine only.

### When the user says "set up Morgen" (or any operation is blocked by missing credentials)

1. Check if credentials already exist:
   ```bash
   test -f ~/.config/morgen-skill/credentials.json
   ```
   - If they exist, ask whether to re-register (re-run only if the user confirms).
   - If missing, proceed.
2. Ask the user to paste their Morgen API key, including this exact caveat:
   > Your key will be stored at `~/.config/morgen-skill/credentials.json` (mode 600). Only paste it here if you trust this terminal and session transcript. Get the key at https://platform.morgen.so → *Developers API*.
3. Once the user replies with the key, run the `--stdin` mode so the key stays out of argv. Quote the key literally inside the here-string:
   ```bash
   bash scripts/setup.sh --stdin <<< '<PASTED_KEY>'
   ```
   The script verifies the key against `/v3/calendars/list` (HTTP 200 = valid) and writes the credentials file with mode 600.
4. On success, confirm to the user with the `Setup complete.` line the script emits, and suggest the natural next step (e.g. `todos.sh sync` or `calendars.sh list`).
5. On failure (non-zero exit), show the stderr verbatim and ask whether to retry with a fresh key.

**Do not** echo the API key back in your own messages, and do not log it. If you must reference it, say "the key you provided".

**Do not** run setup unprompted. The triggers are: explicit user request ("set up Morgen", "configure Morgen"), or a blocked operation that encountered exit code 2 (missing credentials) / 3 (rejected key).

## Authentication

Morgen uses a static API key sent as:

    Authorization: ApiKey <KEY>

The key is stored at `~/.config/morgen-skill/credentials.json` as:

    {"api_key": "..."}

There is no OAuth refresh flow — if the key is revoked, re-run `setup.sh`.

## Rate limits

- **100 points per 15-minute window**, per user.
- `/list` endpoints cost **10 points** each. All other endpoints cost **1 point**.
- Response headers to watch: `RateLimit-Limit`, `RateLimit-Remaining`, `RateLimit-Reset`, `Retry-After`.
- On 429, respect `Retry-After` (seconds) before retrying. The helper surfaces the 429 response body so you can see the wait period.

Practical implication: avoid looping `list` calls. Cache `accountId` and `calendarId` values from one `calendars list` or `integrations accounts` call and reuse them for the whole session.

## Script usage

All scripts live in this skill directory's `scripts/` folder.

### setup.sh — one-time API key registration

    bash scripts/setup.sh                    # interactive (TTY required)
    bash scripts/setup.sh --stdin <<< "$K"   # non-interactive, key via stdin
    bash scripts/setup.sh --key "$K"         # non-interactive, key via argv (argv visible in /proc briefly)

All modes verify the key against `/v3/calendars/list` before writing `~/.config/morgen-skill/credentials.json` (mode 600). See the **Setup flow** section above for the end-to-end skill-orchestrated flow.

### calendars.sh — calendars

    bash scripts/calendars.sh list
    bash scripts/calendars.sh update <accountId> <calendarId> <metadata_json>

`list` returns the `calendars[]` array. Each calendar has `id`, `accountId`, `integrationId`, `name`, `color`, `myRights`, and `morgen.so:metadata`. Always call this once per session to resolve `(accountId, calendarId)` pairs — events endpoints require both.

### events.sh — calendar events

    bash scripts/events.sh list <accountId> <calendarIds> <startISO> <endISO>
    bash scripts/events.sh create <json_body>
    bash scripts/events.sh update <json_body> [seriesUpdateMode]
    bash scripts/events.sh delete <accountId> <calendarId> <eventId> [seriesUpdateMode]

- `calendarIds` is a comma-separated list.
- `start` / `end` are ISO 8601; max window is 6 months.
- `seriesUpdateMode` ∈ {`single` (default), `all`, `future`} for recurring events.
- `create` body requires `accountId`, `calendarId`, `title`, `start`, `duration` (ISO 8601 duration like `PT1H`), `timeZone`, `showWithoutTime`.
- `update` body requires `accountId`, `calendarId`, and either `id` or (`masterEventId` + `recurrenceId`).
- **Update gotcha**: `start`, `duration`, `timeZone`, and `showWithoutTime` form an atomic group — if you send any one of them, you must send all four, or the API returns HTTP 400 (`MRG_ERR_VALIDATION_FAILED: Properties start, duration, timeZone and showWithoutTime must be provided together`). To patch just one time field (e.g. change `duration`), include the existing values for the other three. `timeZone` may be `null` for floating events. Other fields (`title`, `description`, `location`, etc.) can be patched individually without this constraint.

### tasks.sh — Morgen tasks

    bash scripts/tasks.sh list [limit] [updatedAfterISO]
    bash scripts/tasks.sh get <taskId>
    bash scripts/tasks.sh create <json_body>
    bash scripts/tasks.sh update <json_body>
    bash scripts/tasks.sh move <taskId> [previousId] [parentId]
    bash scripts/tasks.sh close <taskId> [occurrenceStart]
    bash scripts/tasks.sh reopen <taskId> [occurrenceStart]
    bash scripts/tasks.sh delete <taskId>

- `create` requires `title`; optional: `description`, `due`, `timeZone`, `priority`, `progress`, `tags`, `relatedTo`.
- `update` requires `id`; other fields are patch-style.
- `close`/`reopen` take an optional `occurrenceStart` for recurring task instances.
- Mutation endpoints return HTTP 204 (no body) on success — the helper prints `{"ok":true}`.

### integrations.sh — connected accounts and providers

    bash scripts/integrations.sh accounts
    bash scripts/integrations.sh providers

- `accounts`: lists the user's connected accounts with `accountId`, provider, auth status.
- `providers`: lists available integration providers (no auth required).
- **Connecting or disconnecting accounts must be done in the Morgen app**, not via API.

### todos.sh — cached TODO workflow (recommended for personal task management)

    bash scripts/todos.sh sync                 # refresh local cache (1 list call, 10 pts)
    bash scripts/todos.sh list [--all] [--tag <id>] [--priority <n>]
    bash scripts/todos.sh today                # tasks due today
    bash scripts/todos.sh overdue              # not completed, due before now
    bash scripts/todos.sh show <idOrPrefix>
    bash scripts/todos.sh add <title> [--due <ISO>] [--priority <n>] [--tz <IANA>] [--description <text>]
    bash scripts/todos.sh done <idOrPrefix>
    bash scripts/todos.sh reopen <idOrPrefix>
    bash scripts/todos.sh delete <idOrPrefix>

Design: **manual sync, cache-first reads, API-first writes**.

- `sync` is the only command that calls `/tasks/list` (10 pts). Do it once per session.
- `list`, `today`, `overdue`, `show` read from the local cache → **0 rate-limit points, instant**.
- `add`, `done`, `reopen`, `delete` hit the API (1 pt each) and then patch the local cache in place. If the API call fails, the cache is untouched.
- Short-ID prefixes (e.g. `aaaa1111`) resolve against the cache. Ambiguous prefixes error out with the list of matches.
- Stale-cache warning fires automatically when the cache is older than `MORGEN_STALE_SECONDS` (default 3600 = 1 hour). Output still works; only a stderr notice appears.
- No automatic sync, no conflict resolution — if you (or the mobile app) diverges, the next `sync` wins. For personal use this is almost always what you want.

Environment overrides:

- `MORGEN_CACHE_DIR` — cache directory (default `~/.cache/morgen-skill`)
- `MORGEN_STALE_SECONDS` — stale-warning threshold in seconds (default `3600`)

When to prefer `tasks.sh` instead:
- you explicitly want a fresh read-through to the API
- you're scripting something that doesn't need the local cache
- you need non-TODO task features (`move`, recurring occurrence closes, etc.)

### tags.sh — tags

    bash scripts/tags.sh list [limit] [updatedAfterISO]
    bash scripts/tags.sh get <tagId>
    bash scripts/tags.sh create <name> [hexColor]
    bash scripts/tags.sh update <tagId> [name] [hexColor]
    bash scripts/tags.sh delete <tagId>

`delete` is a soft-delete — the tag reappears in sync payloads with `deleted: true`.

## Path rules & invariants

- Do not hardcode `accountId` or `calendarId` — resolve them fresh from `calendars list` or `integrations accounts` because IDs can change if a user reconnects an account.
- Event `start` is an **ISO 8601 local datetime without offset** (e.g. `2026-04-21T14:00:00`). The separate `timeZone` field carries the offset. Do **not** pass a `Z`-suffixed UTC string in `start`.
- `duration` is ISO 8601 duration, not seconds. `PT25M`, `PT1H`, `PT1H30M`.
- Event `list` `start`/`end` are ISO 8601 UTC (with `Z`), unlike event-body `start`.
- Task `due` follows the same local-datetime + `timeZone` convention.

## Error handling

If any script exits non-zero, show its stderr to the user verbatim. Do not retry auth errors automatically (exit code 3) — surface them so the user can re-run setup.

Exit code reference:
- 0 — success
- 1 — bad argument, missing positional, or malformed JSON
- 2 — credentials.json missing (→ user should run `setup.sh`)
- 3 — API key rejected, HTTP 401/403 (→ user should re-run `setup.sh`)
- 4 — Morgen returned 404 (resource not found)
- 5 — Other API error (timeout, 5xx, unexpected body)
- 6 — Rate-limited, HTTP 429 (respect `Retry-After` before retrying)
- 64 — usage error
- 127 — missing dependency (`curl` or `jq`)

## Resources

- `references/api-reference.md`: endpoint table with fields, methods, and notes.
- `references/examples.md`: common workflows (scheduling a meeting, triaging tasks, bulk tag cleanup).
- Upstream docs: https://docs.morgen.so/
