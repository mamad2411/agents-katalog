---
name: hevy-central-db-logging
description: Use this skill when the user wants to sync Hevy App workouts, routines, exercise templates, exercise history, or body measurements into a central PostgreSQL-compatible database; build a Hevy API ingestion pipeline; backfill Hevy workout history; or schedule reliable Hevy-to-DB fitness logging with update/delete handling.
license: MIT
compatibility: Requires network access to https://api.hevyapp.com, a Hevy Pro API key, Python 3, and a PostgreSQL-compatible database such as Postgres, Supabase, Neon, or Railway.
metadata:
  author: Hermes Agent
  version: "1.1.0"
  tags: [fitness, hevy, api, postgres, workout-logging, sync, cron, webhooks]
  related_skills: [fitness-live-session-logging, fitness-postgres-sync-hardening]
---

# Hevy Central DB Logging

## Purpose

Set up a complete Hevy App logging flow into a central DB:

```text
Hevy API -> backfill/events sync -> normalized Postgres tables -> analytics/review layer
```

Use PostgreSQL-compatible storage by default. SQLite is fine for a toy demo, but a real central fitness stack needs Postgres so agents, dashboards, cron jobs, and reviews read the same source of truth.

## Source docs and linked files

Primary API docs: `https://api.hevyapp.com/docs/`

Read these support files when needed instead of guessing:

- `references/hevy-openapi-endpoints.md` — endpoint map from the Hevy Swagger docs.
- `references/postgres-schema.sql` — normalized schema plus analytics view.
- `references/hevy-sync-implementation.md` — starter Python sync script.
- `references/verification-queries.sql` — post-setup verification SQL.
- `assets/agent-prompt.md` — copy/paste prompt for another agent.

## Hevy API facts

- Base URL: `https://api.hevyapp.com`
- Auth: every endpoint uses header `api-key: <HEVY_API_KEY>`.
- Hevy API is currently experimental and requires Hevy Pro.
- Do not use Bearer auth for Hevy API calls. Bearer tokens are only for your own optional webhook receiver.
- Do not print, log, or commit API keys, database URLs, `.env` files, raw workout exports, or private fitness data.
- Use `pageSize=10`, especially for `/v1/workouts/events`; larger values have been observed to fail.

## Endpoint priority

Implement in this order:

1. `GET /v1/user/info` — verify credentials and store user identity.
2. `GET /v1/workouts` — initial backfill of workout history.
3. `GET /v1/workouts/count` — sanity-check backfill completeness.
4. `GET /v1/workouts/events?since=<ISO>` — incremental update/delete sync.
5. `GET /v1/workouts/{workoutId}` — repair or spot-check a single workout.
6. `GET /v1/exercise_templates` and `GET /v1/exercise_templates/{id}` — exercise metadata.
7. `GET /v1/exercise_history/{exerciseTemplateId}` — targeted history checks.
8. `GET /v1/body_measurements` and `GET/PUT/POST /v1/body_measurements/{date}` — weight/body metrics.
9. Routine endpoints: `/v1/routines`, `/v1/routines/{id}`, `/v1/routine_folders`, `/v1/routine_folders/{id}`.
10. Avoid `POST`/`PUT` to Hevy unless the user explicitly asks for bidirectional sync.

## Target architecture

Create these DB tables at minimum:

- `fitness.hevy_users`
- `fitness.hevy_workouts`
- `fitness.hevy_exercises`
- `fitness.hevy_sets`
- `fitness.hevy_deleted_workouts`
- `fitness.hevy_sync_state`
- `fitness.hevy_raw_events`
- `fitness.hevy_exercise_templates`
- `fitness.hevy_body_measurements`

Rules:

- Preserve raw Hevy JSON in `jsonb` columns for audit/debugging.
- Keep Hevy raw values untouched. Put dumbbell-per-hand or bodyweight volume conventions in SQL views or derived analytics tables.
- Store both `start_time` and `updated_at`; use `start_time` for the training timeline and `updated_at` for sync/debugging.
- Use `exercise_template_id` as stable identity when available; exercise titles can change.
- Treat `distance_meters`, `duration_seconds`, `custom_metric`, and `rpe` as first-class fields, not edge-case junk.
- Do not physically delete workouts by default. Mark `hevy_workouts.deleted_at` and record the delete event.

## Setup sequence

### 1. Prepare secrets

Use env vars or a secret manager. Never hardcode secrets.

```bash
export HEVY_API_KEY="..."
export DATABASE_URL="postgresql://user:password@host:5432/dbname"
export HEVY_SYNC_SINCE_DEFAULT="1970-01-01T00:00:00Z"
```

For open-source repos, ship only `.env.example`:

```text
HEVY_API_KEY=
DATABASE_URL=postgresql://postgres:postgres@127.0.0.1:5432/fitness_logs
HEVY_SYNC_SINCE_DEFAULT=1970-01-01T00:00:00Z
```

### 2. Smoke-test Hevy auth

```bash
curl -fsS https://api.hevyapp.com/v1/user/info \
  -H "api-key: $HEVY_API_KEY" \
  -H 'accept: application/json'
```

Expected shape: `data.id`, `data.name`, `data.url`.

If this fails with `401`/`403`, stop and ask the user to regenerate or provide the Hevy API key through the secret manager. Do not continue with mocked data.

### 3. Apply schema

Use `references/postgres-schema.sql`.

```bash
psql "$DATABASE_URL" -f references/postgres-schema.sql
```

### 4. Create the sync script

Use `references/hevy-sync-implementation.md` as the starter implementation for `hevy_sync.py`.

Required CLI flags:

- `--init-user`
- `--backfill`
- `--events`
- `--max-pages`
- `--json`

Dependencies:

```bash
python -m venv .venv
. .venv/bin/activate
pip install httpx psycopg[binary] python-dotenv
```

### 5. Initialize user and backfill

```bash
python hevy_sync.py --init-user --json
python hevy_sync.py --backfill --max-pages 2 --json
python hevy_sync.py --backfill --json
```

For large accounts, keep the limited backfill first. It catches schema/API bugs cheaply before a full run.

### 6. Run incremental sync twice

```bash
python hevy_sync.py --events --json
python hevy_sync.py --events --json
```

The second run should normally be zero-change unless the Hevy account changed between runs.

## Incremental sync behavior

Use `/v1/workouts/events` as the primary ongoing sync path.

For each event:

- `type=updated`: upsert the workout, then replace child exercise/set rows for that workout inside the same transaction.
- `type=deleted`: insert/update `hevy_deleted_workouts`, set `hevy_workouts.deleted_at`, and keep the raw delete event.
- Always write raw event JSON to `hevy_raw_events`.
- Advance `fitness.hevy_sync_state.workouts_events_since` only after successful processing in the same DB transaction.

Do not append child sets on update. That double-counts edited workouts. Delete-and-replace child rows for the changed workout is simpler and safer.

## Scheduling options

Pick one scheduler. Keep output quiet unless there is new data or a real failure.

### Cron

```cron
*/30 * * * * cd /path/to/hevy-stack && . .venv/bin/activate && python hevy_sync.py --events --json >> logs/hevy-sync.log 2>&1
```

### systemd user timer

Create a oneshot service that runs `hevy_sync.py --events --json`, then a persistent timer with `OnBootSec=2min` and `OnUnitActiveSec=30min`.

### Hermes no-agent cron

Use a wrapper script under `~/.hermes/scripts/`:

- empty stdout = silent success
- one-line summary = new workouts synced
- one-line alert = actionable failure

## Optional webhook receiver

If Hevy developer settings expose webhooks, use them only as a trigger. Keep the events poller as fallback.

Receiver behavior:

1. Accept `POST /hevy/webhook`.
2. Verify your own shared secret header, e.g. `Authorization: Bearer <WEBHOOK_TOKEN>`.
3. Append the raw webhook payload to JSONL for audit.
4. Trigger `python hevy_sync.py --events --json` asynchronously.
5. Return `202` quickly.

Never trust webhook payloads as canonical. Use them to wake the sync job, then read canonical data from the Hevy API.

## Verification

Run `references/verification-queries.sql` after setup.

Minimum checks:

- `GET /v1/user/info` succeeds with `api-key` header.
- Schema exists under `fitness` schema.
- Backfill inserts workouts, exercises, and sets.
- `/v1/workouts/count` roughly matches active non-deleted workout count after full backfill.
- `/v1/workouts/events` succeeds with `pageSize=10`.
- Running event sync twice is idempotent.
- Deleted workout events mark rows deleted instead of disappearing.
- Raw JSON exists for audit.
- Analytics view returns top exercises without mutating raw Hevy values.
- Scheduler/timer has a recent successful run.
- No secrets are present in git, logs, chat output, or copied docs.

## Common pitfalls

1. **Wrong auth header:** Hevy uses `api-key`, not `Authorization: Bearer`.
2. **Mandatory webhooks:** bad idea. The portable path is polling `/v1/workouts/events`.
3. **No delete handling:** edited/deleted Hevy workouts must update the DB.
4. **Double-counting updates:** replace child rows on each workout update.
5. **Mutating raw Hevy values:** keep raw `weight_kg`; apply conventions in analytics views.
6. **Huge page sizes:** use `pageSize=10`.
7. **No cursor:** store the events `since` cursor/timestamp in `hevy_sync_state`.
8. **Cursor advanced before commit:** cursor update belongs in the successful DB transaction.
9. **No second-run test:** always run event sync twice.
10. **Secret leaks:** never echo expanded secrets or raw `.env` contents.

## Response contract

When setup succeeds, report only:

```text
Done.
- DB: connected
- Hevy auth: OK
- Backfill: <n> workouts / <n> sets
- Incremental sync: OK, second run zero-change
- Scheduler: <cron/systemd/Hermes>, next run <time>
- Files: <paths>
```

When blocked, report only the failing layer and next fix:

```text
Blocked: Hevy auth failed with HTTP 401/403.
Likely fix: regenerate the Hevy API key in Hevy developer settings and update HEVY_API_KEY in the secret manager.
```

No backend log dumps unless the user asks.
