# DabbahWala — Claude Code Instructions

## Git Workflow

After making any code changes:
1. **Ask the user before pushing** — confirm the changes look correct
2. **Handle all git operations** — commit, push, create PR, and merge via GitHub API using `$GITHUB_TOKEN`
3. Always target `main` as the base branch for PRs
5. Branch names must start with `claude/` and end with the session ID suffix

### E2E Test Update (mandatory on every commit)

**Every commit that adds or modifies a feature must also:**
1. Add the corresponding test(s) in `app/services/test_harness_service.py` inside the appropriate `_gN_*` function
2. Register those tests in `TESTS.md` under the correct group table

Use the **Group Selection Guide** in `TESTS.md` to pick the right group. If no existing group fits, create a new `_gN_*` function, add its call to `run_full_suite()`, and add a new section to `TESTS.md`.

This applies to **every** commit — including bug fixes, new endpoints, schema changes, n8n workflow additions, and integration changes.

### Pre-PR Doc Check (mandatory)

Before opening any PR, review the branch diff (`git diff main...HEAD`) and update docs if affected:

| Changed | Update |
|---------|--------|
| Schema, stored procs, migrations | `OVERVIEW.md` § Database |
| New/modified API routes or routers | `OVERVIEW.md` § API Layer |
| Agent pipeline logic | `OVERVIEW.md` § The Five Agents |
| n8n workflow added/changed | `OVERVIEW.md` § n8n Workflow Layer |
| External service integration | `OVERVIEW.md` § External Services |
| Next migration number used | `CLAUDE.md` § Database Migrations (increment the number) |
| n8n workflow count changed | `CLAUDE.md` § n8n Workflow Status |
| Any new/modified feature (always) | `TESTS.md` + `app/services/test_harness_service.py` |
| New customer journey, user story, or how-to | `OVERVIEW.md` § Customer Journeys / User Stories / Operations |

If nothing in those categories changed, docs are fine as-is — no update needed.
Commit doc updates in the same branch before opening the PR.
Use `/update-docs` to run the check interactively.

### GitHub Token
The `GITHUB_TOKEN` is stored in `~/.claude/CLAUDE.md` (global memory, never commit it to the repo).
If the env var is empty, read it from that file and use it directly in API calls.

## Deployment
- Hosted on **Render**, auto-deploys on merge to `main`
- Build command: `scripts/render_build.sh` (installs deps + runs all `migrations/*.sql`)
- Start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

## Database Migrations
- All migrations live in `migrations/` and are numbered sequentially
- Next available migration number: **009**
- Use `CREATE TABLE IF NOT EXISTS` / `CREATE INDEX IF NOT EXISTS` for idempotency

### Migration strategy — update existing files when possible

The 5 consolidated files represent the full DB state. Prefer editing them over adding new numbered files:

| Change type | File to update |
|---|---|
| New table, column, or index | `002_tables.sql` |
| New or modified stored function | `003_functions.sql` |
| New trigger or view | `004_triggers_views.sql` |
| Seed / reference data change | `005_seed.sql` |
| New enum value | `001_schema_types.sql` |

Only create a new numbered file (e.g. `006_*.sql`) for changes that **cannot be safely merged** into an existing file:
- One-time data backfills
- Destructive `DROP` / `ALTER … DROP COLUMN` statements
- Any change that must run exactly once and would be wrong to re-run

## Credentials & Integrations

### n8n
- Instance: `https://digitalworker.dataskate.io`
- API key (JWT): `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJkMmFmN2JlMi1hMTYwLTRlZmUtYjFhOC0wMjlmM2U3OWZmMDkiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzcxNTQ3NzAzfQ.lOtKLp-YEdulBGSOD62uKCPTJBHOl_-0rDy2qa79FqE`
- Header: `X-N8N-API-KEY: <key>`
- When creating/updating workflows via API, only send `{name, nodes, connections, settings}` — n8n rejects `staticData`, `pinData`, `tags`, `meta`
- To **activate** a workflow: `POST /api/v1/workflows/{id}/activate` (PATCH is not allowed on this instance)
- To **deactivate** a workflow: `POST /api/v1/workflows/{id}/deactivate`
- Credentials resolve by **name** on first push — use the exact credential name and n8n will auto-match and return the real ID
- Workflow files live in `n8n/` — IDs tracked in `n8n/config.json`
- **⚠️ n8n Variables / environment variables are NOT available on this instance** — never use `$env.ANYTHING` in workflow nodes. Hardcode all values (URLs, phone numbers, static config) directly in the node parameters. This applies to every workflow, past and future.

### Gmail / SMTP
- Credential name in n8n: **`Gmail-SMTP`** (credential ID: `Sk6XzPNPnJTXHEbr`)
- Used by: `action_queue_executor` (`send_email_report` action), `broadcast_dispatch` (email channel)
- Host: `smtp.gmail.com`, Port: 465, SSL on
- Reports sent to: `REPORT_EMAIL_TO` env var (default `core@dabbahwala.com`)

### Google OAuth
- **Google Drive OAuth2** — n8n credential ID: `LUu1v42BgnEflv6f`
  - Used by: `action_queue_executor` (`upload_google_drive` action), `google_docs_sync`
- **Google Docs OAuth2** — n8n credential ID: `FcNSuTgdmTt3M4D5`
  - Used by: `google_docs_sync` (reads doc content for chatbot index)
- Drive folder for chatbot docs: `1O0ES9uiDL6AWf9QMMYiyRUWGtymDjPF5`

### Airtable
- API key: stored in Render env as `AIRTABLE_API_KEY` and in `~/.claude/CLAUDE.md` (never commit to repo)
- Base ID: `appuy2VTIao6XVpIW`
- Menu table: **`Menu Catalog`** (table ID: `tblmZBNdQvmFcvVai`) — fields: Item Name, Category, Is Veg, Description, Image URL, Price, Added Date
  - Airtable = active items only; deleting a row marks it discarded in Postgres (via daily sync)
  - History tracked in `menu_catalog_history` in Postgres
- Agent Playbook table: **`Agent Playbook`** (table ID: `tbljWs6hKWbYFufnM`) — fields: Rule Name, Category, Instruction, Priority, Active, Created By
  - Synced to Postgres `agent_playbook` table daily at 6 AM via `[Agent Rules] Playbook Sync` (ID: `FXuYcwQeBQ72Xxyu`)
  - Categories: exclusion, priority, inference, decision, messaging, general

### n8n Workflow Status (2026-02-26)
- **27 total workflows**: 26 active-scheduled + 1 manual-only (`[System] Connectivity Check`) — 9 deleted total (manual forms and one-shot imports removed)
- All workflows use **centralized credentials**: single "DW Admin Secret" HTTP Header Auth → `GET /api/credentials` bootstrap
- All workflows renamed to **12-feature taxonomy** format: `[Feature Group] Descriptive Name`
- Full ID mapping in `n8n/config.json`

**Deleted (no longer in n8n):**
- `[System] Daily Tests` (`M7bwNMGrUMRvAHH4`) — superseded by `[System] Feature Tests`
- `[Claude — Evidence] Weekly Menu Sync` (`sb0jHek7Q9gPeCUd`) — superseded by `[Menu] Catalog Sync`
- `[Claude — Inference] Goal-Oriented Agent Cycle` (`NzNeVrjbIoKGge5M`) — duplicate of `[Growth] Goal Agent`
- `[Broadcast] Broadcast Form` (`mUptDrymXZrtlrp8`) — unused manual form, nothing calls it
- `[Chatbot] Query Form` (`gm3qFxu22akrTV3Z`) — unused manual form, nothing calls it

**Key workflow IDs:**
| Workflow | ID | Schedule |
|---|---|---|
| [Order Intake] Order Collector | `AePBXRdPKkUQpHIT` | Every 30 min |
| [Order Intake] Feedback Sync | `0pQY0otcvnGj8WBH` | Every hour |
| [Order Intake] Daily CSV Upload | `6ZYQwdkmS5Nni05u` | Daily 1 PM EST |
| [SMS] Inbound Collector | `xcNObK3qdU1wdf3f` | Every 30 min |
| [SMS] Dispatch Queue | `w2bVQQ4hy33OdY1R` | Every 10 min |
| [Broadcast] Dispatch | `oDEse7EvWHj6UVM4` | Every 1 hour |
| [Email Campaigns] Performance Tracker | `ctCLyHDQc1VckMqL` | Every hour |
| [Email Campaigns] Campaign Sync | `nCcBt9USIYxlOaJT` | Every 6 hours |
| [Email Campaigns] Campaign Setup | `NbnkM3nTFKSgtcfb` | Daily midnight |
| [Intelligence] Contact Sweep | `FcbBt0AIlkYoa01X` | Daily 7 AM |
| [Intelligence] Stage Runner | `h80nX24myWwsbxuB` | Every hour |
| [Intelligence] Lapsed Re-engagement | `S3jSnWb3UTv9HmJL` | Daily (random offset) |
| [Intelligence] AI Stack | `VreWonSUTk4VCXPF` | Daily 9 AM |
| [Field Agent] Outcome Sync | `chfGgYIjyTw6QP5m` | Every 4 hours |
| [Field Agent] Daily Brief | `kOI33cFH4bM8OCaf` | Daily 7:30 AM |
| [Agent Rules] Playbook Sync | `FXuYcwQeBQ72Xxyu` | Daily 6 AM |
| [Menu] Catalog Sync | `baZV5ViA5lXNCTWR` | Weekly Mon 6:30 AM |
| [Growth] Competitor Research | `GozoSXHiazEdhpni` | Weekly Mon 6:30 AM |
| [Growth] Goal Agent | `w5kYj5vNsNW53W4n` | Daily 9 AM |
| [Growth] Weekly Growth Agent | `Nbut2tjjksGvQYzH` | Weekly Mon 7:30 AM |
| [Reports] Daily Activity Report | `91bMjrZxiCPTglEI` | Daily 8 AM |
| [Reports] Daily Outcome Report | `fONTnqi4l9DT3aCo` | Daily 8:30 AM |
| [Chatbot] Docs Sync | `oHtGvkCLTWYkxNZ0` | Every 30 min |
| [Chatbot] Docs Reindex | `7mn3Ys0xMmZnZQIC` | Weekly Mon 2 AM |
| [System] Action Queue | `RzR3ZNYlty7cuTDY` | Every 30 min |
| [System] Feature Tests | `zlKQKfJ18QGIwogq` | Daily 5 AM |
| [System] Connectivity Check | `ipSHdFUZMj2D0r0t` | Manual only |

**26 workflows are active-scheduled. `[System] Connectivity Check` is manual-only (execute on demand from n8n).**

- Credential IDs: only `DW Admin Secret` (HTTP Header Auth) remains; all others removed from n8n
- All other integration keys fetched at runtime via `GET /api/credentials` (requires `ADMIN_SECRET` Render env var)

### Python Router Reorganization (2026-02-26)
- `app/routers/orders.py` — merged from `shipday_historical.py` + `shipday_sync.py`; prefix `/api/shipday`
- `app/routers/sms.py` — renamed from `telnyx.py`; prefix stays `/api/telnyx`
- `app/routers/menu.py` — renamed from `airtable_menu.py`; prefix stays `/api/menu`
- Old files (`shipday_historical.py`, `shipday_sync.py`, `telnyx.py`, `airtable_menu.py`) superseded; do not create new files with those names

### Three-Engine Terminology (2026-02-26)
- **Stage Engine** = pure SQL rules that move contacts between lifecycle stages (`run_lifecycle_cycle()`) — no Claude
- **Contact Sweep** = hourly rule-based loop (COLLECT→PROFILE→SIGNAL→ROUTE→DISPATCH) — no Claude, triggers AI Stack when needed
- **AI Stack** = 4-layer Claude pipeline per-contact (Observer→Advisor→Orchestrator→Reports)
- DB tables: `contact_observations` (Observer output), `action_plans` (Advisor output), `orchestrator_log`, `action_queue`

### Instantly
- API key (Bearer): stored in Render env as `INSTANTLY_API_KEY`
- Value: `OThjYmE4NjQtMjMwYS00ZGM2LWIzMTgtNWY2YzYxZTZmNDEyOmVwbU1CSFRWa3ZiaQ==` (base64 `workspace_id:secret` — used as `Authorization: Bearer` for all Instantly v2 calls including lead writes)
- **Never use `X-API-Key` header** — the base64 credential only works as a Bearer token
- Old deprecated key `c7kf84j4c54vhjpcc5yv7k35tgs5` must NOT be used — it is read-only and rejects POST /leads

### GitHub
- Token: `GITHUB_TOKEN` env var — used for PR creation/merge via GitHub API
- Repo: `vivek-dataskate/DabbahWala`
