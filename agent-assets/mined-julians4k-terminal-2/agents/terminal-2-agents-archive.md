# AGENTS.md

two-lane split (2026-05-09 evening): **code** owns backend + audit + git push; **design** (fresh coworker) owns terminal frontend, no push, no prod writes. Copilot remains paused.

## ROSTER (2026-05-09 evening onward — two-lane split)

| agent | role | reports to git via |
|---|---|---|
| **code** (this chat) | backend lane — `app.py`, `evo_client.py`, all edge functions, all SQL migrations, ESPN/TEvo/Wiki/NOAA ingest, schema docs (SCHEMA.md), AUDIT pass on every commit, SOLE git pusher | self (direct push) |
| **design** (fresh coworker) | terminal frontend lane — `static/index.html`, `static/event.html`, `static/movers.html`, `static/chat.html`, `static/legacy.html`, `design/*`. **NO git push, NO prod writes.** Hands off via `KANBAN.md` proxy-commit pattern | code's proxy commit (RULE 12) |
| ~~copilot~~ | **PAUSED** — retail chat backend / NLU / listings ingest. Lane returns later. | n/a |

**Why two lanes (and not three)**: per user direction 2026-05-09 evening — splitting backend (code) from frontend (design) lets each move at full speed without stepping on each other. Copilot's retail-chat lane stays paused until the broker terminal hits high-beta. The design coworker is BRAND NEW — full onboarding lives in [`COWORKER_ONBOARDING.md`](COWORKER_ONBOARDING.md).

**Why design has no push**: prevents drift — design's diffs land via code's audit-and-push proxy. This is the same pattern the prior multi-agent era used (RULE 12); it kept us drift-free for weeks.

**Why design has no prod writes**: hard wall against accidental schema/state changes from a brand-new agent. Design uses `design_test.*` schema for sandboxing; reads from `public.*` are fine.

## STATUS BOARD (live, read first, update on every state change)

| agent | status | started_at (UTC) | working on | branch | safe to interrupt? |
|---|---|---|---|---|---|
| code   | IDLE | — | — | main | yes |
| design | NEW — onboarding | — | reading COWORKER_ONBOARDING.md + KANBAN.md | n/a (no push) | n/a |
| ~~copilot~~ | PAUSED | — | — | — | n/a |

**Read this table before starting any work.** Design's branch column is "n/a" because design doesn't own a branch — diffs go through code.

## WIP (files an agent is actively editing — append before edit, clear on commit)

**Read this section before opening any file.**

### code
- (none)

### ~~copilot~~
- (paused — lane returns at high-beta)

### ~~claude design~~
- (paused — lane returns at high-beta)

## ARCHITECTURE (confirmed 2026-05-08)

TWO data sources. ONE running backbone. TWO products with separate retail backends. THREE agents.

```
┌────────────────────────────────────────────────────────────────────────┐
│ DATA SOURCES                                                           │
│  TEvo API (live + cron pulls)   ESPN scoreboard/injuries/news (cron)   │
└────────┬───────────────────────────────────┬───────────────────────────┘
         │                                   │
         ▼                                   ▼
┌────────────────────────────────────────────────────────────────────────┐
│ CRON-COLLECTED HISTORICAL TABLES (the running backbone)                │
│  listings_snapshots · event_metrics · zone_metrics · section_metrics   │
│  espn_team_snapshots · espn_injuries_snapshots · espn_news · espn_*    │
│  Cadence dialed by event time: 20m / 1h / 4h / 12h / daily             │
└────────┬───────────────────────────────────┬───────────────────────────┘
         │                                   │
         ▼                                   ▼
┌──────────────────────────┐    ┌───────────────────────────────────────┐
│ BROKER TERMINAL          │    │ RETAIL                                │
│ (broker_*, full data)    │    │ (retail_*, S4K-owned only)            │
│                          │    │                                       │
│ FE: claude design        │    │ Two backends:                         │
│ BE+SQL: code             │    │  A. Chatbot — chat edge fn, live      │
│ ESPN: overlay layer      │    │     TEvo per query w/ 90s per-event   │
│   (chart workbench,      │    │     cache. ESPN aliases used in       │
│    event detail alerts,  │    │     RETRIEVAL (athlete→performer).   │
│    performer detail)     │    │     ESPN content NOT yet in tool      │
│                          │    │     responses — see NEXT in LOG.      │
│ static/index.html        │    │                                       │
│ static/event.html        │    │  B. *_public REST RPCs — read from    │
│ static/movers.html       │    │     cron-collected listings_snapshots │
│                          │    │     (fast, freshness = cron tier      │
│ Google OAuth @s4kent.com │    │     interval). NOT live every render. │
│                          │    │                                       │
│                          │    │ FE: claude design                     │
│                          │    │ BE+ML: copilot                        │
│                          │    │ static/chat.html · landing TBD        │
└──────────────────────────┘    └───────────────────────────────────────┘

                  code = auditor across all of the above
```

never leak data across the wall. retail UI must never see wholesale, brokerage names, or non-S4K listings. broker UI sees everything.

## DATA FLOW (cadence + cache truth)

**TEvo cron tiers (collect-listings)** — picks event polling frequency based on how soon the event is:

| tier                       | schedule       | runs/day | event window |
|---------------------------|----------------|----------|--------------|
| `collect-listings-0-24h`   | every 20 min   | 72       | events ≤ 24h away (high-volatility book) |
| `collect-listings-1-7d`    | hourly @ :05   | 24       | 1–7 days out |
| `collect-listings-7-30d`   | every 4h       | 6        | 7–30 days |
| `collect-listings-30-60d`  | every 12h      | 2        | 30–60 days |
| `collect-listings-60d+`    | daily 02:20    | 1        | 60+ days |

**Each pull writes**:
- `listings_snapshots` — raw per-listing rows (section, row, qty, retail_price, is_owned, type, splits, format, in_hand, etc.)
- `event_metrics` — aggregated per-event medians/percentiles/counts derived from the above
- `zone_metrics` + `section_metrics` — same aggregation at finer grains

**ESPN cron tiers (espn-collect)**:
- `espn-roster-10min` — injuries every 10 min
- `espn-gameday-10min` — event scores+odds for events ±24h, every 10 min
- `espn-team-daily` — standings + news, daily 05:00 UTC

All change-only ingest (content_hash dedup) so quiet periods don't bloat the tables.

**Per-surface cache TTLs**:

| surface | TTL | live-every-render? |
|---|---|---|
| Chatbot `find_listings` / `find_better_seats` / `get_event_zones` | 90s per event (`get_cached_ticket_groups` RPC) | yes-ish (90s feels live for human chat) |
| Broker terminal raw TEvo tab (`/api/events/{id}`) | per-request live TEvo (no cache) | yes |
| Broker terminal metric workbench / movers / league grid | reads `event_metrics` (cron-collected) | no — as fresh as cron tier |
| Retail `*_public` RPCs (web-store flow) | reads `listings_snapshots` (cron-collected) | no — as fresh as cron tier |

**ESPN as overlay layer**:
- Broker terminal: surfaced inline (event-detail ESPN alerts, performer-detail ESPN block, chart workbench team_index series, news velocity, per-injury markers).
- Chatbot: ESPN data drives RETRIEVAL only (s4k_popularity_boost from big-5 venue performers, athlete aliases mapping 857 ESPN players → team performer_id). **ESPN content does not appear in the chatbot's responses to users.** That's a NEXT for copilot.

**TEvo rate limits**:
Documented per call site in code (chat fn handles 429 + retry-after; espn-collect paces 80-120ms between calls). Centralized doc not yet written — `docs/tevo-rate-limits.md` is a NEXT for code (will pull copilot's collect-listings source first to capture its pacing).

## OWN

### code (auditor + terminal backend + git proxy)
- **app.py · evo_client.py · requirements.txt · Procfile** — terminal HTTP routes, FastAPI, cron, deploys.
- **supabase/functions/espn/ · supabase/functions/espn-collect/ · supabase/functions/tevo-perf-find/** — ESPN ingest stack and TEvo lookup helper.
- **supabase/migrations/** — code is the canonical author for broker-side schema (zone RPCs, movers RPCs, league-grid RPCs, ghost-event filters, owned-share plumbing). copilot's chat-side migrations land here too via code's proxy.
- **ESPN ingest schema** = `espn_*` tables, `event_xref`, `performer_external_ids` (source='espn').
- **Audit responsibility**: review every commit (mine or proxied). Run scenario simulations (broker audits, workflow audits, Knicks-style deep-dives) to find issues. Document findings in `docs/` + LOG.
- **Git proxy**: copilot and claude design have no direct push. They produce diffs / files; code reviews, runs sanity tests, commits, and pushes. Audit-and-commit pattern same as cowork era.

### copilot (retail chat backend + chatbot ML/NLU)
- **supabase/functions/chat/** — retail chat edge function (Claude tool-use loop, find_listings, comprehensive_search, all chat tools).
- **supabase/functions/collect-listings/ · supabase/functions/seed-home-venues/ · supabase/functions/bulk-add-watchlist/ · supabase/functions/probe-tevo-category/ · supabase/functions/probe-tevo-performer/ · supabase/functions/probe-tevo-events-by-venue/ · supabase/functions/probe-seating-charts/ · supabase/functions/wiki-collect/ · supabase/functions/why-noaa-weather-alerts/ · supabase/functions/crawl-venues-and-performers/ · supabase/functions/backfill-event-configurations/ · supabase/functions/espn-rosters/** — ingest + admin helpers.
- **chatbot NLU/ML** = chat_aliases corpus mining (`chat_term_freq_in/out`, dictionary seeding, alias promotion), tokenizer + entity extractor RPCs, suggestion-chip generation, ranking signals.
- **chat-side schema migrations** = chat_aliases / chat_term_freq / chat_corpus / venue_crawl_state / why_signals / etc. Land in `supabase/migrations/` via code's proxy.

### claude design (front-end across both products)
- **static/index.html** — broker terminal home page (events / performers / venues / configs / watchlist tabs).
- **static/event.html** — Stage 1+2 event terminal (chart workbench, zone breakdown, ESPN tab, raw TEvo tab).
- **static/movers.html** — full Movers report.
- **static/chat.html** — retail chatbot UI.
- Future: any new HTML/CSS/JS surfaces, design system tokens, theme variables, accessibility passes.
- **Does NOT touch**: app.py routes, edge functions, SQL migrations. If a UI change needs a new endpoint or new field, write a one-line spec in the LOG (`NEXT (claude design)` entry) and code or copilot picks it up.

### shared (ask before edit, leave WAIT note)
- **AGENTS.md** (this file) · README.md · .gitignore · cross-product schema changes that touch both retail and broker views.

All three agents are free to call any edge fn or read any view. Only writes to source files in another agent's OWN list need a WAIT note first.

## RULES

1. `git pull --rebase origin main` before push. always. (code's responsibility on proxy commits; copilot/design work from their own working copy.)
2. no edit other agent's owned path without leaving WAIT note in LOG first.
3. `.claude/` gitignored. never commit worktrees.
4. work in `C:\VibeCode\terminal-2`. never OneDrive, never `C:\Users\julia\Code\Terminal-2`. **MOVE PERMAFIX IN PROGRESS 2026-05-08 evening**: code agent has staged everything (mockup + 3 docs from copilot's mount pulled into git, `/terminal/v1` route added to app.py, push made). User runs `bin/permafix-move.ps1` from a fresh PowerShell after closing Claude Code to do the actual `mv` + Railway reconfig. After the move, both code and copilot work from the same canonical path → no more sub-tree-mount split.
5. append to LOG below at end of every session. newest entry on top.
6. tag tasks: DOING / DONE / WAIT / NEXT / BLOCKED.
7. broker product = full data. retail product = S4K-owned only. never cross.
8. **before commit:** flip your STATUS BOARD row to DOING with `started_at` timestamp + brief working-on. if you're going to touch another agent's owned path or shared SQL, also leave a WAIT note in LOG (top of LOG, your section).
9. **after commit/push:** flip your STATUS BOARD row back to IDLE with `started_at` cleared, AND append a LOG entry under today's date with: `DONE <SHA> <subject>` (newest first within the day). if your work spans multiple commits in one session, one LOG entry covering all of them is fine — list each SHA.
10. if another agent is DOING and you need to start: read their STATUS BOARD row's `working on`. if your planned work overlaps (same file, related table), don't start — leave a `WAIT for <agent> to finish <topic>` note in the LOG and pick something else.
11. **before editing ANY file:** append the file path under your subsection in the WIP section above. read the *other agents'* WIP first — if any of them have your target file listed, pick a different file or wait. **clear your subsection back to "(none)" the instant your work hits `main`.** This rule is finer-grained than rule 10: STATUS BOARD says "I'm working", WIP says "exactly which files".
12. **proxy-commit protocol** (copilot + claude design): you produce a working tree. drop your changes into the repo (or a paste in the LOG with a "FROM copilot/design" header) + a one-line summary of what you touched + intent. code reviews, runs validators (`py -3 -c "import ast; ast.parse(open('app.py').read())"` for backend, manual eyeball for HTML), then commits in your name (`Co-Authored-By: copilot` or `claude design` in the trailer) and pushes. If code finds a bug it doesn't ship — leaves a comment in LOG (`BLOCKED for <agent>: <bug>`).
13. **code's audit pass** (post-commit): every commit landed by anyone, code spot-checks the diff against (a) the product wall (no broker→retail leak), (b) AGENTS.md ownership, (c) common bug classes (parking inclusion, ghost events, content_hash gaps, cross-product schema collisions). Findings go in `docs/<date>-audit.md` + LOG.
14. **claude design ↔ backend boundary**: if a UI change needs a new endpoint, new field, new RPC, or modified data shape — design DOES NOT add the backend code. Drop a `NEXT (claude design): need <endpoint/field>` line in the LOG. Either code (terminal endpoints) or copilot (chat endpoints) picks it up next session.

## ACCESS MATRIX (revised 2026-05-08 evening — shared prod+env model)

> Codifying reality. The 2026-05-08 morning lockdown ("code is only writer") was de-facto already broken — copilot writes to prod via Supabase MCP routinely. Per user direction this evening: **both agents read+write the same prod and env so we can see all the code together.**

| surface              | code (me)        | copilot        | claude design  | rationale                                                    |
|----------------------|------------------|----------------|----------------|--------------------------------------------------------------|
| **Prod DB (writes)** | ✅                | ✅              | ✅              | All 3 write — service_role MCP. Code's audit pass catches drift. |
| Prod DB (reads)      | ✅                | ✅              | ✅              | All 3 read.                                                  |
| **Prod edge fn deploys** | ✅            | ✅              | ✅              | All 3 deploy via MCP `deploy_edge_function`.                 |
| **Prod cron schedules** | ✅             | ✅              | ✅              | All 3 manage via `cron.job` SQL.                             |
| **Supabase Storage** | ✅                | ✅              | ✅              | All 3 read+write.                                            |
| Test schemas         | `code_staging`   | `copilot_test` | `design_test`  | Each agent's own sandbox; no cross-write.                    |
| Filesystem / git checkout | shared canonical path | shared canonical path | shared canonical path | **All 3 agents work from the same checkout** (see SHARED CHECKOUT below). |
| **Git push**         | ✅ today          | ❌ today        | ❌ today        | Only code has GitHub auth in this environment. Copilot + design hand off via the proxy-commit protocol (RULE 12) until they get push capability. |
| static/*.html / CSS  | review only      | review only    | ✅ author        | Lane ownership — code reviews UI changes for backend impact, doesn't author. |
| supabase/functions/chat/ | review only  | ✅ author        | review only    | Lane ownership.                                              |
| app.py / evo_client.py / broker SQL | ✅ author | review only | review only    | Lane ownership.                                              |

**Push gate**: code does not push to `main` until the working tree is verified clean (sync-check passes + `app.py` parses + obvious smoke checks). Authorship within commits is preserved via `Co-Authored-By:` trailers.

**Audit responsibility**: with all 3 agents writing to prod, code's audit pass becomes the primary defense against drift. Two cadence modes:
- **Live audits** at the end of every working session (`bin/sync-check.sh` once it's wired with secrets, or the manual procedure in `bin/sync-check.md`).
- **Spot-checks** before any prod-write that touches the product wall (broker ↔ retail surfaces).

## SHARED CHECKOUT (ACTION REQUIRED — user must coordinate)

Today's blocker for "see all the code together" is the **filesystem split**:
- **Code (me)** is at `C:\Users\julia\Code\Terminal-2` with the full repo.
- **Copilot** is at `C:\VibeCode\terminal-2` with a sub-tree mount that has migrations + edge fns + AGENTS.md but NOT app.py / static/index.html / Procfile.

These are TWO DIFFERENT FOLDERS that don't auto-sync. When copilot stages files (the new `static/_proposals/terminal-v1.html` mockup, additional migrations, etc.) they sit in their mount only. They never appear in mine, so I can't capture them into git or push them.

To fix this end-to-end, **the user must do one of**:

**A. Move my repo to `C:\VibeCode\terminal-2`** (the long-pending move from RULE 4):
```
# from a fresh shell, NOT from inside Claude Code:
git -C C:\Users\julia\Code\Terminal-2 status   # confirm clean
mv C:\Users\julia\Code\Terminal-2 C:\VibeCode\terminal-2
# then point Railway at the new path; restart Claude Code session
```
After this, copilot and code share the same path.

**B. Reconfigure copilot's sandbox to mount my path** (`C:\Users\julia\Code\Terminal-2`).
This is a copilot-side configuration the user does in copilot's settings.

**C. Run a one-shot xcopy** every time copilot stages something:
```
xcopy "C:\VibeCode\terminal-2\static\_proposals" "C:\Users\julia\Code\Terminal-2\static\_proposals\" /E /I /Y
xcopy "C:\VibeCode\terminal-2\supabase\migrations\*" "C:\Users\julia\Code\Terminal-2\supabase\migrations\" /Y
xcopy "C:\VibeCode\terminal-2\supabase\functions\*" "C:\Users\julia\Code\Terminal-2\supabase\functions\" /S /Y
xcopy "C:\VibeCode\terminal-2\AGENTS.md" "C:\Users\julia\Code\Terminal-2\AGENTS.md*" /Y
xcopy "C:\VibeCode\terminal-2\docs\*" "C:\Users\julia\Code\Terminal-2\docs\" /S /Y
```
Manual but immediate. Run it then tell code "synced" and I pick up from there.

**Recommended: A** (move once, done). **Workable today: C** (xcopy as needed).

**Until one of A/B/C happens, copilot's mockup at `static/_proposals/terminal-v1.html` is invisible to my tree and unpushable.**

## DRIFT DETECTION (automated as of 2026-05-08)

`bin/sync-check.sh` + `.github/workflows/sync-check.yml` run on every push to `main` and on a daily 06:17 UTC cron.

**What it catches**:
- Prod migrations not in git (the dominant historical drift case).
- Edge functions deployed but not in git (requires `SUPABASE_PAT` secret; without it, only migration drift is checked — covers ~80% of cases).
- Git migrations not yet applied to prod (heads-up, not blocking).

**What it does on drift**:
- Writes a markdown report.
- Opens (or updates) a GitHub issue labeled `sync-check`.
- Auto-closes the issue when drift is cleared.

**Required GitHub secrets** (Settings → Secrets and variables → Actions):
- `SUPABASE_URL` — `https://hzrizjeaxlqcxfrtczpq.supabase.co`
- `SUPABASE_SERVICE_ROLE_KEY` — service-role key
- `SUPABASE_PAT` — optional; enables edge-fn diff (sbp_... PAT from Supabase Account → Tokens)

**Manual run**:
```bash
SUPABASE_URL=... SUPABASE_SERVICE_ROLE_KEY=... bin/sync-check.sh --report-md /tmp/r.md
```

Backed by `public.__sync_check_list_migrations()` RPC (mig `20260508130000`, service-role only).

## TEST SCHEMAS (Option C, picked 2026-05-08)

> Schema-level isolation in the prod project. Free, no infra, weakest of the three test-env options. Convention enforced by AGENTS.md + code's audit pass — Postgres doesn't physically prevent any agent from writing to `public`.

| schema          | owner          | purpose                                                |
|-----------------|----------------|--------------------------------------------------------|
| `code_staging`  | code           | Stage migrations + project simulations before promoting to `public`. |
| `copilot_test`  | copilot        | Chat-side schema iteration (chat_aliases additions, new RPCs, NLU experiments). |
| `design_test`   | claude design  | Stub tables / mock data for UI prototypes. Mostly empty (design rarely needs DB). |

Each schema has a `._readme` table with usage notes. Run `SELECT * FROM <schema>._readme;` to recall the workflow.

**No crons run in test schemas. No edge fn deploys point at them.** They're DB sandboxes only.

**Promotion workflow** (test schema → public):
1. Agent iterates in their own schema.
2. When ready, agent writes a migration file targeting `public.*` with the final shape and drops it as `FROM <agent> · timestamp` block in the LOG (proxy-commit, RULE 12).
3. Code reviews the migration, applies to `public` via Supabase MCP, deploys any associated edge fn changes, and pushes to git.

**Read access**: any agent can `SELECT FROM public.*` for diagnostic / reference purposes. The lockdown is on writes.

## STORAGE LAYOUT (Supabase Storage)

**`chat` bucket** — created 2026-05-08 (mig `20260508110000_storage_chat_bucket`). Public read, all 3 agents can read+write via service-role.

Folder convention inside `chat/`:
```
chat/
  default/        retail Find Tickets chatbot (existing static/chat.html)
  broker/         broker-side admin chat (future, terminal-embedded)
  support/        customer support chat (future)
  sales/          outbound sales chat (future)
  _shared/        cross-variant assets (logos, default avatars)
```

When a new chat variant is needed, create a new subfolder rather than a new bucket. Code does spot-checks during sync audits to keep the convention.

5 MB file limit. Allowed types: png/jpeg/gif/webp/svg, mpeg/webm/ogg audio, pdf, plain text.

## STRATEGIC (project-level context every agent should know)

> **Read this before planning new feature work.** These are things that change priorities and tradeoffs across the whole codebase, not narrow tasks. Surfaced from `docs/sync-audit-2026-05-08.md` after code (auditor) found the SeatGeek planning docs sitting unread in `docs/seatgeek/`.

- **🔄 SeatGeek migration is on the roadmap.** Two long planning docs in `docs/seatgeek/` (1,400 lines combined): `kanban-tasks.md` is the EPIC backlog; `migration-guide.md` is the API reference. Driver: `/events` is hard-capped at 10K results since 2026-01-01, so any TEvo full-catalog pattern is silently truncating. Implication: TEvo-shaped data (event_metrics, listings_snapshots, etc.) is a transitional substrate. New broker-side features should not deepen TEvo coupling — prefer abstractions over the source. Open question for the desk: timeline + cutover strategy.
- **🔄 Retail product surface expanded beyond chatbot.** Migration `20260508023000_leads_and_rest_wrappers` (copilot, 2026-05-08) adds a `leads` table + 6 `*_public` REST RPCs. Suggests a dedicated retail website / landing-page experience is in flight, not just the existing `static/chat.html` chatbot. claude design should expect to be asked for `static/landing.html` or similar soon.
- **💸 Trial countdown**: 8 days / $4.58 left on Railway as of 2026-05-08. If not upgraded, terminal goes dark; chat fn (Supabase) keeps running independently.

## SCHEMA LOCK (2026-05-09-v19)

> **Backend architecture is documented in [SCHEMA.md](SCHEMA.md).** Read it before proposing any backend change. Locked version: **`2026-05-09-v19`**.
>
> **RULE 0 (Process discipline)** — any new data (table/column/external feed/derived metric/price source) MUST be categorized into a SCHEMA.md bucket in the same commit. Including all price data sources.
>
> **RULE 1 (Cross-league)** — every query against the `espn_*` tables MUST filter by `(espn_team_id, espn_league)` together. team_id is league-scoped (id "18" = NBA Knicks AND MLB Pirates AND NFL Saints AND NHL #18 AND WNBA #18). Skipping the league filter leaks 95% phantom data.
>
> **v8 (cascading cron model)** — 6 individual freshness crons collapsed into `master-cascade-2min` (jobid 38) firing every 2 min: async ESPN roster+gameday HTTP via pg_net, then sync auto_link → splits → nonowned with per-stage try/except. ESPN injury/trade freshness improved from 10-min cadence to 2-min. Zone backfill (jobid 39, batch=5) kept separate due to pre-existing 120s timeout bug in match_performer_zone. Worst-case event-coverage staleness collapsed from ~50 min to ~2 min.
>
> Contents: 48 tables, 75+ SQL functions, 17 active crons (was 22; 6 collapsed into the cascade, 1 added back as isolated zone job), all edge functions, the canonical **17-bucket data taxonomy**, TEvo classification tree, behavior rules (HOME/AWAY + ESPN UI gates), 4-layer ESPN coverage matrix, **dedicated ESPN injury / standings schema + auto-assignment rules**, recommended ML feature row, non-big-6 ESPN coverage gap + roadmap, major event calendar workflow, API surface, data-flow diagram, verification queries.
>
> **Drift to be reconciled** (6 migrations applied via MCP execute_sql in code-agent session, captured as files in `supabase/migrations/` but not yet in prod migration ledger):
> - `20260508220000_auto_link_event_xref` (jobid 31 — replaced by cascade)
> - `20260508230000_event_splits_metrics` (jobid 32 — replaced by cascade)
> - `20260508240000_crawl_espn_assets_cron` (jobid 33)
> - `20260508250000_ensure_major_league_watchlist` (jobid 34)
> - `20260509000000_zone_metrics_backfill_cron` (jobid 35 — replaced by jobid 39)
> - `20260509040000_master_cascade_cron` (jobid 38 + 39, this commit)

## STATE (truth, not history)

- Live URL terminal (broker) = railway https://terminal-2-production.railway.app  /  (Railway dropped the legacy `.up.` subdomain segment; old `terminal-2-production.up.railway.app` now 404s)
- Railway project = **glorious-appreciation** (1/1 service online) — both terminal AND `/chat` page served from same FastAPI app on this project. Sibling project `fantastic-magic` (0/1 online) is abandoned/stale, candidate for deletion.
- ⚠️ **Railway deploy is lagging main** as of 2026-05-08: `/`, `/event/{id}` work; `/chat`, `/movers`, `/healthz` return 404 even though routes exist in `app.py`. Either auto-deploy from GitHub `main` is disconnected/broken or Railway is on a stale build. Need to trigger redeploy from Railway dashboard so movers page + chat page go live.
- Trial countdown: 8 days / $4.58 remaining as of 2026-05-08 — must upgrade to Hobby ($5/mo) before then or terminal goes dark.
- Live URL chatbot (retail)  = same domain  /chat
- Supabase project = hzrizjeaxlqcxfrtczpq (Terminal .5)
- chat edge fn = v19
- collect-listings edge fn = v9
- seed-home-venues edge fn = v1
- bulk-add-watchlist edge fn = v1
- espn edge fn = v1 (code, claude code 2026-05-07)
- espn-collect edge fn = v2 (code, daily cron CANCELED pending bridge with performer_external_ids)
- migrations applied through 20260507000030_team_xref_compat_view (29 cowork migrations + 1 code compat shim now all in git)
- watchlist = 48 performers (37 NFL added today)
- performer_home_venues = 135 (NBA/NHL/NFL/MLB/WNBA; MLS missing — covered via performer_external_ids)
- chat_aliases = 193 (incl 35 FIFA)
- product wall enforced via DB views: retail_events / retail_listings / retail_event_metrics / retail_event_zones / retail_event_sections (S4K-owned only) vs broker_* (full)
- performer_external_ids ESPN coverage = **217 teams across 7 leagues**: NFL 32, NHL 32, NBA 30, MLB 30, MLS 30, WNBA 15, World Cup 48 (canonical going forward)
- team_xref = **VIEW (2026-05-07, mig 30)** — read-only compat shim over performer_external_ids where source='espn'. Cowork's RPCs (get_team_context, broker_event_intel, espn-rosters fn) keep working without code changes; PEI remains the canonical source-of-truth.
- event_xref = 1 row (NYK@PHI G3, lazily populated). PHASE 1.3 (cowork): generalize into `event_external_ids` for SeatGeek/TM/S4K plug-ins.
- espn snapshot tables (current baseline): 76 team snaps, 566 injuries, 190 news, 78 event snaps. All rows have content_hash + is_baseline=true (migration 17). Next collector run is change-only.
- espn-collect edge fn = **v5 (code, 2026-05-07)** — scoped change-only ingest. Reads from performer_external_ids (217 teams). Three scopes via `?scope=`: `roster` (injuries every 10 min), `gameday` (event scores+odds for events ±24h, every 10 min), `team_daily` (standings + news, daily 05:00 UTC). Crons live (`espn-roster-10min`, `espn-gameday-10min`, `espn-team-daily`). Smoke-test: 1404 injuries inserted on first run, 1402 unchanged on a 30s-later re-run (2 actually changed during that gap, so change-detection working live). v3-v4 fixed bugs in flight: MD5→SHA-256 (Deno WebCrypto doesn't support MD5); inj.id used as dedup key since ESPN league-injuries doesn't populate inj.athlete.id.
- espn edge fn = **v2 (code, 2026-05-07)** — reads from performer_external_ids; verified end-to-end: /applicable + /performer return correct sport-slug for all 7 leagues (NFL/NBA/MLB/NHL/MLS/WNBA/World Cup). team_xref dropped.
- tevo-perf-find edge fn = v2 (code, 2026-05-07) — admin lookup for TEvo performer search; used to seed migrations 15+16. Keep around for future expansion teams.
- sms-bot edge fn = DELETED 2026-05-07 (orphan, never used; tombstone v6 returns 410)
- web-bot edge fn = DELETED 2026-05-07 (orphan, never used; tombstone v2 returns 410)

### Shared venues (tracked teams) — date+venue alone is NOT a unique event key
| venue | teams |
|---|---|
| MetLife Stadium | NY Giants, NY Jets (NFL) — also hosts NHL Stadium Series |
| Madison Square Garden | NY Knicks (NBA), NY Rangers (NHL) |
| American Airlines Center (Dallas) | Mavericks (NBA), Stars (NHL) |
| Ball Arena (Denver) | Nuggets (NBA), Avalanche (NHL) |
| Crypto.com Arena (LA) | Lakers (NBA), Sparks (WNBA) — Clippers moved to Intuit Dome |
| Little Caesars Arena (Detroit) | Pistons (NBA), Red Wings (NHL) |
| Xfinity Mobile Arena (Philly) | 76ers (NBA), Flyers (NHL) |
| Gainbridge Fieldhouse (Indy) | Pacers (NBA), Fever (WNBA) |
| Target Center (Mpls) | Timberwolves (NBA), Lynx (WNBA) |
| SoFi Stadium (LA) | Chargers, Rams (NFL) |
| Wrigley Field | Cubs (MLB) — also NHL Winter Classic |
| Globe Life Field | Rangers (MLB) — also All-Star Game |

For event matching across data sources (TEvo ↔ ESPN ↔ SeatGeek ↔ TM), key on **(date_utc, venue_id, performer_set)** not just (date, venue).

## RESTRUCTURE PLAN (proposed — not yet executed)

Target layout for `C:\VibeCode\terminal-2` once the user moves the directory off OneDrive:

```
terminal-2/
├── AGENTS.md                  ← shared (this file)
├── README.md                  ← shared
├── .gitignore                 ← shared
├── Procfile                   ← root, points into broker/ (Railway needs root-level Procfile)
├── requirements.txt           ← shared (FastAPI + supabase + anthropic — both products import)
├── broker/                    ← code-owned (terminal admin UI)
│   ├── app.py                 ← FastAPI routes + cron
│   ├── evo_client.py          ← TEvo HMAC client
│   └── static/
│       └── index.html         ← Google-OAuth-gated terminal
├── retail/                    ← cowork-owned (find-tickets chatbot)
│   └── static/
│       └── chat.html          ← anonymous public landing
└── backend/                   ← shared (single source of truth)
    └── supabase/
        ├── migrations/        ← shared (cross-product schema)
        └── functions/
            ├── chat/          ← cowork
            ├── collect-listings/
            ├── seed-home-venues/
            ├── bulk-add-watchlist/
            ├── probe-tevo-category/
            ├── espn/          ← code
            └── espn-collect/  ← code
```

Mechanics (whoever picks this up):
1. user moves dir: `mv C:\Users\julia\code\Terminal-2 C:\VibeCode\terminal-2` (closes all editor sessions first)
2. user updates Railway root path → `broker/` (env vars unchanged)
3. agent runs `git mv` for the moves above (in-tree; one commit, no content changes)
4. agent updates Procfile to `web: uvicorn broker.app:app --host 0.0.0.0 --port $PORT` (or adds `cd broker &&` prefix)
5. agent updates Supabase CLI config if any (`supabase/config.toml` paths) — `backend/supabase/`
6. agent updates static-file mounts in app.py: serve `broker/static/` for `/`, `retail/static/` for `/chat`

**WAIT user** — agent cannot do step 1 (mv would invalidate cwd) or step 2 (Railway dashboard). Once user signals the move is done, either agent can do steps 3-6 in one commit.

## LOG

### 2026-05-09 code (overnight: design audit + 3-surface preview + XSS fix)

- DONE — **Audit of design coworker's 2026-05-08 submission** at `docs/audit-2026-05-09.md`. 5 design docs + 3 frontend skeletons reviewed. Wall preserved (no `/api/broker/*` in shop.html, no `/api/retail/*` in broker skeletons). Python parses on all 4 backend files. Backend health: 21 active crons, 109 runs in last hour, 0 failures. CODE_NOTES.md scoped 17+ new endpoints (P1/P2/P3) and 6 new tables — all migration references verified accurate.
- DONE — **Blocking XSS fix in `shop.html` chatbot**. The `sendChat()` and `openChat(prefill)` functions inlined user-typed input into `innerHTML`. Replaced with `textContent` + `appendChild` pattern via a `_appendChatTurn()` helper. Static deeplink span moved to `data-deeplink` + `addEventListener` (no inline onclick). User input now structurally cannot escape into HTML. Verified clean via grep.
- DONE — **3-surface preview at `/preview/*`** (per Julian's overnight ask: "have all 3 projects live in the same site with buttons to switch between them"). 4 new routes in app.py:
  - `GET /preview` → landing page with 3 cards (broker / shop / ops) + back-to-live link
  - `GET /preview/terminal` → broker 6-template skeleton
  - `GET /preview/shop` → retail buying site
  - `GET /preview/ops` → fulfillment ops board
  - All 3 skeletons gained a sticky switcher header at top with the active route highlighted in accent yellow. Self-contained inline styles so the switcher doesn't fight per-page CSS.
- DONE — **Landing page** at `static/_proposals/preview-landing.html`: 3-card grid with audience tag, bullet feature list, "Open" + "Spec" buttons (Spec links to the GitHub-hosted design markdown). Footer note explains why one site for now and points to the audit + CODE_NOTES.
- NEXT — design coworker can keep iterating in `_proposals/`; once any surface stabilizes, promote it to `static/{name}.html` and update its app.py route to point at the promoted location.

### 2026-05-09 code (cross-source order status mapping — unified vocabulary)

- DONE — **`order_status_xref`** rosetta stone (mig `20260509140000`, SCHEMA v19). Maps 13 source-statuses to 6 canonical states (`pending` / `accepted` / `substitution` / `rejected` / `cancelled` / `fulfilled`) with `is_terminal` + `is_sale_succeeded` flags carried alongside.
- DONE — **`canonical_order_status(source, source_status) → jsonb`** helper RPC for one-shot lookups.
- DONE — **`unified_orders` view** — single rowset across `evo_orders` + `seatgeek_orders` + `seatdata_sales_snapshots`. Caught and fixed a bug along the way: initial draft joined `seatgeek_sales_snapshots` (broker-data /sales, currently empty for our token) instead of `seatdata_sales_snapshots` (the 254-row Knicks G5 SeatData history). Now produces 254 SeatData fulfilled + 200 SG accepted + 200 SG fulfilled, $397K gross from SeatData alone.
- DONE — **`unified_orders_by_event`** + **`order_status_coverage`** rollup views. The latter is the diagnostic for "what do we have across all sources?" and feeds the future Order Book page from the redesign memo.
- IMPACT: any cross-source analytical query (fill rate, sale velocity, in-flight book) now writes against canonical states instead of per-source CASE. Future sources (TickPick, Vivid Seats) just insert their xref rows + UNION into `unified_orders`.
- BLOCKED ON USER (carried from prior session): set `CRON_SECRET` on Railway to unblock EVO orders cron jobid 40. Once set, EVO orders auto-flow into the same `unified_orders` view.

### 2026-05-09 code (historical/sentiment/similar-events strategy + supporting schema)

- DONE — **Strategy memo** at `docs/historical-data-and-multi-view-strategy-2026-05-09.md`. Covers 4 historical-data layers (event/performer/venue/matchup), buyer sentiment composite (formula + 5 visual options), similar-event matching, micro→macro 10-level zoom spectrum, web vs PWA delta, schema additions, build sequence.
- DONE — **Migration `20260509130000`** operationalizes the memo:
  - `matchup_xref` table — unordered (team_a, team_b) → matchup_id; **445 matchups seeded** from existing events (top: Yankees-Orioles 13, Yankees-Blue Jays 13, Red Sox-Yankees 11, Knicks-76ers 7).
  - `matchup_history` view rolls up event_metrics per matchup.
  - `event_sentiment` table + `compute_buyer_sentiment(event_id)` RPC + `backfill_event_sentiment(N)` cascade-friendly batch fn. **Live test produces real signal**: Pistons-Cavs G3 +100, Knicks G5 +54, Wolves-Spurs G5 (ghost-ish) -34. The composite captures buyer absorption rate + getin floor + owned share trajectory + pair thinning.
  - `performer_baselines` + `venue_baselines` tables with `refresh_*_baselines()` daily-refresh fns. Initial run: 72 performers / 67 venues with active future events.
  - `find_similar_events(event_id, max_n)` RPC scoring across same-matchup (1.0) + same-performer (0.6) + same-venue (0.4). **Live test on Knicks G5**: returns G7/G2/G1 (score 2.0), G6/G4/G3 (1.6), Finals games (1.0) — perfect ranking.
- TOP FINDING: Knicks-76ers played-game retail decay is **50-65% from initial listing to gametime** ($1,110→$560, $1,274→$464, $643→$250, $817→$399). That's the playbook number for similar-event projections. Future games (G5/G6/G7) are still at 80-98% of initial listing — buyer sentiment shows G5 absorbing aggressively (+54 index).
- KANBAN updated with companion NEXT (design) row pointing at the new memo + cross-reference to the redesign memo.

### 2026-05-09 code (terminal redesign memo — rebuild from scratch per data findings)

- DONE — **Strategic redesign memo** at `docs/terminal-redesign-2026-05-09.md`. User mandate: assume prior `static/index.html` is obsolete and rebuild from scratch. I ran a 4-phase audit on prod data:
  1. **Inventory**: 822 active sports events, 564K market tix, 60K owned. 554 events with rich tracking (avg 48 snaps, 7d history). Concerts thin (115 events, only 1 with metrics). Sports-first build is correct.
  2. **6 simulations** on real data, surfacing patterns like the price-decay V-shape (drops 1-3d out, sometimes bounces in final 24h), the wildly variable owned_premium_pct (−32% to +255% across our book), inventory loading asymmetry (S4K +767% vs market +45% over 7d), and three distinct mover types (supply flood / re-pricing / ghost-resolve).
  3. **Synthesized 7 page templates** with concrete data behind each: Home (position concentration + risk alerts), Event detail (with `owned_premium_pct` as the headliner KPI), Performer detail (NEW), Movers with 5-bucket classifier, Cross-source explorer (NEW), Order book / sales pipeline (NEW), Settings.
  4. **5 new API endpoints** scoped: `/api/broker/home`, `/api/broker/movers/classified`, `/api/broker/performers/{id}/detail`, `/api/broker/orders/sales-pipeline`, `/api/broker/cross-source/explorer`.
- Top finding for design: **`owned_premium_pct` (owned_median_retail / nonowned_median_retail − 1) is the single most actionable broker metric** — varies from −32% (Knicks: leaving money on the table) to +255% (Pistons: probably won't clear). Currently invisible in the UI. Should be the biggest number on every event page.
- Top finding for code: **Knicks book = $20.4M notional** (5,088 owned tickets × ~$3,950 avg retail). One performer is 40% of total book risk. Position concentration view is critical.
- KANBAN: new top-priority NEXT (design) row pointing at the redesign memo. Build sequence in §7 of the memo recommends Event detail page first.

### 2026-05-09 code (cross-source entity maps — universal id translator)

- DONE — **Cross-source entity maps** (mig `20260509120000`, SCHEMA v17). Three views — `entity_event_map`, `entity_performer_map`, `entity_venue_map` — that translate any source's id to all others. TEvo is the hub. Each view returns a `sources_count` rollup + a JSONB `external_ids` block compact enough to drop into API responses.
- DONE — **6 translation functions**: `tevo_event_id_for(source, id)` and inverse `external_ids_for_event(tevo_id)` (plus performer + venue variants). ESPN performer lookup supports `'NBA:18'` syntax for league-disambiguated ids per RULE 1.
- DONE — **`taxonomy_xref` table** for the "fixed variables": TEvo event_type ↔ ESPN league ↔ SG event_type ↔ SeatData event_type. Seeded with 12 mappings (NBA, WNBA, NFL, NHL, MLB, MLS, NCAA-FB, NCAA-MBB, Concert, Comedy, Theater, Parking).
- DONE — **`cross_source_coverage` diagnostic view**. Live coverage: 269/1233 events on ESPN (22%), 39 performers on SG (21%), 21 venues on SG (17%), 37 performers multi-source. SeatData event/performer/venue coverage is sparse (manually-linked Knicks G5 only) — driven by user-initiated /auto-search.
- VERIFIED — round-trip translations + name-based lookups all return correct hub ids. Surfaced one known data bug (TEvo 3345925 + 3346856 share ESPN id 401871162 — documented earlier as the G5 vs G3 mismatch; not a new issue).
- NEXT (design) — KANBAN row added: render the `entity_event_map.external_ids` JSONB on event hero as 4-light coverage badges with hover-popover showing the raw ids per source.

### 2026-05-09 code (SG metrics + xref + cascade + RULE 2 read-only enforcement)

- DONE — **SG event metrics, performer xref, venue xref, categorization view** (mig `20260509110000`, SCHEMA v16). Parallel to TEvo `event_metrics` and SeatData `seatdata_event_stats`. 28 metric columns (listings + orders + sold + mix + fill_rate). `seatgeek_categorized_listings` answers "all our SG inventory for X at Y" without joins. `cross_source_event_audit` view gives all 4 sources for any TEvo event in one row.
- DONE — **Smart matcher fix**: prior `sg_attempt_event_xref` linked SG Lynx game on 5/17 to a ghost "TBD at Minnesota Timberwolves" TEvo event (same venue/date). New version requires performer name overlap + prefers non-ghost (lifecycle.is_active). Re-ran on 219 known SG events: 1 valid match (Rockies @ Diamondbacks → TEvo 3092720), ghost rejected.
- DONE — **RULE 2 (Read-only external APIs)** documented + enforced at code level. `evo_client.py`, `seatdata_client.py`, `seatgeek_client.py` all hard-code an HTTP method allowlist. Any non-GET (except SeatData's metadata-only event-add POST) raises before the network call. Documented in SCHEMA.md right next to RULE 0 and RULE 1.
- DONE — **Cascade extended**: `master_cascade_2min` now runs SG performer + venue auto-xref + SG metrics backfill (50 events/tick) alongside the existing TEvo splits/nonowned + ESPN HTTP. Live test: 1.7s total runtime, 102 SG performers + 21 venues linked, 1 SG event metric computed.
- DONE — **Cross-source audit**: most-covered event in our system is Knicks G5 (TEvo 3345925) — TEvo + ESPN + SeatData all linked, 254 SeatData sales, 2,869 active TEvo tix. SG hasn't matched it yet because page-1 listings only covered ~25 of 157,846 listings; 10-min cron will keep filling.
- NEXT (design) — KANBAN row added: render the `cross_source_event_audit` view as a single "data coverage" badge on the event hero (4 lights for TEvo / ESPN / SeatData / SG, lit per source matched). Plus `seatgeek_event_metrics` series on the chart (`SG_Cost_Median`, `SG_Active_Tickets`, `SG_Sold_Quantity`).

### 2026-05-09 code (SeatGeek Seller Direct API — auto-xref via inline event metadata)

- DONE — **SeatGeek Seller Direct integration** (mig `20260509100000`, SCHEMA v15). Read-only ingest from `sellerdirect-api.seatgeek.com` (DIFFERENT host from `brokerdata.seatgeek.com`, same token). Probe revealed 3 endpoints we can use: `/listings` (157,846 active S4K listings), `/orders?status=X` (6,074 confirmed + 496,413 fulfilled lifetime), `/order?order_id=X` (single).
- DONE — **Auto-backfill via inline event metadata**. Every /listings + /orders row carries `event_id`, `event` name, `venue`, `date` inline. New SQL function `sg_attempt_event_xref(sg_event_id, name, date, venue)` fuzzy-matches TEvo events on (occurs_at_local::date, venue_name LIKE) and upserts `seatgeek_event_xref` automatically. **No more manual SG event_id mapping for events we have inventory on.**
- DONE — **Live test on Knicks G5**: persisted page-1 listings (200 rows) + confirmed-orders page 1 + fulfilled-orders page 1 (400 orders total, deduped). 2 SG events auto-linked to TEvo events (Chicago Sky @ Lynx 5/17, Rockies @ Diamondbacks 5/22). Knicks G5 (TEvo 3345925) wasn't in the first page of listings — either we don't have S4K inventory on this specific game or it's later in the cursor walk. The mechanism is verified; cron will keep filling the xref over time.
- DONE — **Pagination probe + client update**: `?page=N` is deprecated (server returns 400 "use page_cursor instead"). `?page_cursor=X` is the new pattern. `?per_page=N` works, `?event_id=N` filters. Client now uses `iter_seller_listings(max_pages, per_page)` with cursor pagination. Default cron pulls 5 pages × 200 = 1000 listings/tick.
- DONE — **Schema additions**: `seatgeek_seller_listings`, `seatgeek_orders`, `seatgeek_order_tickets`, `seatgeek_seller_pull_log`, `seatgeek_orders_by_event` view. Plus `sg_attempt_event_xref()` SQL function.
- DONE — **`POST /api/admin/collect-sg-seller`** + 3 read endpoints + cron `seatgeek-seller-collect-10min` (jobid 41) every 10 min via pg_net → Railway.
- NEXT (design) — KANBAN row added: render SG seller-direct sales overlay (we now have actual S4K SG sales by event) + SG seller-listings panel showing our active inventory cross-referenced against TEvo zones.

### 2026-05-09 code (SeatGeek BROKER DATA rebuild — wrong host scrap-and-rewrite)

- DONE — **Scrapped the v13 SeatGeek public-API integration and rebuilt for the BROKER API** (mig `20260509090000`, SCHEMA v14). v13 assumed `api.seatgeek.com/2` with `?client_id=` auth; our partner token is actually for `brokerdata.seatgeek.com` with `?token=` auth. Live diagnostics confirmed: `/listings` + `/sales` return 400 "No event found" with our token (auth pass, just needs real event_id); `/purchases` returns 401 (scope unavailable — TEvo /v9/orders covers our own purchases). Dropped 5 unused tables (taxonomies, sections, recommendations, venue_xref, performer_xref). Rebuilt around `seatgeek_event_xref` (simplified), `seatgeek_listings_snapshots` (18 listing fields + content_hash dedup), `seatgeek_sales_snapshots`, `seatgeek_pull_log`, `seatgeek_event_latest` view.
- DONE — **`seatgeek_client.py` rewritten** for `brokerdata.seatgeek.com`. Three methods (`listings`, `sales`, `purchases`) with typed `SeatGeekScopeError` on 401. Vault-loaded auth. content_hash dedup for listings (re-pulls only insert when something changed). Sales dedup by UUID.
- DONE — **6 new `/api/seatgeek/*` routes** in app.py: `GET /event/{id}`, `POST /event/{id}/link`, `POST /event/{id}/sync-listings`, `POST /event/{id}/sync-sales`, `GET /event/{id}/listings`, `GET /event/{id}/sales`. The `/api/cross-source/event/{id}` updated to use the new xref columns.
- AWAITING — **Manual SG event_id mapping**. Broker API has no `/search` endpoint, so user-driven matching: find SG event_id via SG broker portal or website URL, POST `/api/seatgeek/event/{tevo_id}/link?sg_event_id=N`. Then sync routes work.

### 2026-05-09 code (SeatGeek integration — 3rd data source: section_info, recs, performer images)

- DONE — **SeatGeek integration** (mig `20260509080000`, SCHEMA v13). Third data source after TEvo + SeatData. Metadata + discovery only (no pricing — that's TEvo + SeatData). Adds: section_info per venue (canonical seating layouts, complementary to our zone xref), affinity-scored recommendations (events + performers — better than our string-similarity heuristic), 4-size performer images, SG taxonomy tree for cross-validation.
- DONE — **Vault writer RPC**: `upsert_app_secret(name, value)` (whitelist-gated, SECURITY DEFINER, service-role only). Lets PowerShell / scripts push keys without using SQL editor. Whitelist now covers SEATDATA_API_KEY + TEVO_API_TOKEN + TEVO_SECRET + SEATGEEK_API_TOKEN.
- DONE — **`seatgeek_client.py`** (new module). Wraps all 9 SG endpoints. Vault-first auth, env-var override, 429 backoff, persistence helpers for every xref + cache table.
- DONE — **6 new `/api/seatgeek/*` routes** in app.py: `GET /event/{id}`, `POST /event/{id}/auto-search`, `POST /event/{id}/sync-sections`, `POST /event/{id}/sync-recommendations`, `POST /sync-taxonomies`, `GET /recommendations/by-event/{id}`.
- AWAITING — **SEATGEEK_API_TOKEN push to Vault**. User pushes via SQL editor: `SELECT public.upsert_app_secret('SEATGEEK_API_TOKEN', '<token>')`.
- NEXT (design) — KANBAN row added: render SG section layout on event-detail page (overlay onto existing zone breakdown), and "Related events" panel using `/api/seatgeek/recommendations/by-event/{id}`.

### 2026-05-09 code (vault for keys + SeatData↔TEvo mapping + EVO orders 10-min cron)

- DONE — **Supabase Vault for app secrets** (mig `20260509070000`, SCHEMA v12). `SEATDATA_API_KEY` now lives in `vault.secrets` and is read via new SECURITY DEFINER RPC `public.get_app_secret(name)` with a whitelist (currently `SEATDATA_API_KEY`, `TEVO_API_TOKEN`, `TEVO_SECRET`). seatdata_client loads from vault by default; env var still works as override. **No more Railway env var sprawl** — single rotation point per key via `vault.update_secret()`. The user-shared key is now safely in vault, not chat history.
- DONE — **Cross-source mapping schema**: SeatData and TEvo use different ids for everything. New tables `seatdata_venue_xref`, `seatdata_performer_xref`, `seatdata_zone_xref`, `seatdata_section_xref`. New function `normalize_sd_listing(event_id, sd_zone, sd_section, sd_row)` resolves any SeatData row to canonical (zone, section) via lookup priority: section_xref → zone_xref → `derive_zone_fallback()` → unmapped. New view `sd_sales_normalized` exposes the SeatData sales with canonical naming AND fixes the **quantity-null caveat** (SeatData uses `quantity=0` to mean "unknown" — the view surfaces this as NULL with a `quantity_unknown` flag).
- DONE — **EVO orders integration**: TEvo `/v9/orders` is now ingested every 10 min. Schema: `evo_orders` (header), `evo_order_items` (lines, with `event_id` mapped from `ticket_group.event.id`), `evo_orders_by_event` view. EvoClient gained `list_orders` / `iter_orders` / `get_order` methods (per_page max=10 per docs). Two new app.py routes: `POST /api/admin/collect-orders` (cron-secret OR auth gated, bounded to 50 pages × 10 = 500 orders/tick) and `GET /api/broker/event/{id}/orders` (read with summary). Cron `evo-orders-collect-10min` (jobid 40) drives the pull via pg_net. Replaces ad-hoc TEvo order checks; gives us realized PnL, fulfillment urgency, sale velocity, and the ask-vs-sold spread that's the most honest measure of pricing accuracy.
- DONE — **`docs/data-sources-terminal-uses.md`**: comprehensive memo for design (and future copilot) covering the data wall, mapping caveats, 6 SeatData UI uses, 7 EVO-orders UI uses (chart series, hero strip, e-ticket alerts, hold-expiry urgency, ask-vs-sold spread badge, etc.), and SQL cheat sheet. Both lanes should read this before designing new event-detail panels.
- NEXT (design) — KANBAN row added: render the `EVO_Orders_Completed` bar series + order-book hero strip + e-ticket fulfillment alert. The hero strip is the smallest impactful UI delta; do that first.
- ACTION REQUIRED (user) — **Set `CRON_SECRET` env var on Railway** to match the placeholder `pick-any-random-string-and-save-it`. Or change the value in both pg_cron jobs (jobids 40 + others using same secret) and Railway env. Without the match, `/api/admin/collect-orders` returns 401 to the cron.

### 2026-05-09 code (SeatData integration — second pricing source live, Knicks G5 sales pulled)

- DONE — **SeatData integration** (mig `20260509060000`, SCHEMA v11). New second-source pricing API alongside TEvo, focused on the data TEvo doesn't expose: sold-listing history + cross-market fill rate. Hard-capped to BASIC plan budget (100 paid pulls/day, 2000/month) at the DB level via `seatdata_pull_budget` + RPC. Going over those caps requires bumping BOTH the DB defaults AND `seatdata_client.py` constants — two-key change so accidental overage is unlikely.
- DONE — **`seatdata_client.py`** (new module at repo root). Wraps all 9 SeatData endpoints (3 paid + 6 free). Handles gzip-encoded responses, 429 backoff with Retry-After respect, atomic budget increment, full pull-log persistence. Reads API key from `SEATDATA_API_KEY` env var.
- DONE — **7 new `/api/seatdata/*` routes in app.py**: account, usage, budget, event/{id}, event/{id}/sales, event/{id}/link, event/{id}/auto-search, event/{id}/sync-sales. Routes return 503 with setup hint if `SEATDATA_API_KEY` is unset rather than crashing.
- DONE — **Live test on next Knicks home game** (TEvo 3345925, 2026-05-12 vs 76ers @ MSG). Auto-search matched to SeatData sd_event_id=1247184. `/v0.3/salesdata/get` returned **254 historical sale records over 42 days** (3/28 → 5/9). Median sale $668, avg $773, range $378-$3,756. 519 tickets sold across 8 zones / 50 sections. All persisted to `seatdata_sales_snapshots` table.
- ACTION REQUIRED (user) — **Set `SEATDATA_API_KEY` Railway env var** before next deploy: `railway variables --set SEATDATA_API_KEY=<your-key>`. Without it, `/api/seatdata/*` routes return 503. Recommend rotating the key after this session since it was shared in chat history.
- NEXT (design) — KANBAN row added: render the SeatData sales-history overlay on the chart workbench (transacted prices vs TEvo asks) — the most actionable ML feature the integration unlocks.

### 2026-05-09 code (event lifecycle classifier — sort ghost playoff games out of live surfaces)

- DONE — **Event lifecycle classifier** (mig `20260509050000`, SCHEMA v10). User reported Toronto Raptors / Boston Celtics events showing up as live despite both teams being eliminated. Audit found 203 ghost future events out of 1134 (~18% pollution). Built `derive_event_lifecycle(event_id)` function + `event_lifecycle` view classifying events as `active | ghost_eliminated | completed | postponed | cancelled | unknown` with confidence + reasons. Strongest signal: TEvo `last_seen` staleness (live Knicks avg 1.0h since refresh; ghost brackets avg 133h, min 121h — zero overlap). Combined with `event_type='game' AND name ILIKE '%TBD%'` for the placeholder bracket pattern.
- DONE — **API integration**: `/api/broker/event/{id}/overview` adds a `lifecycle` block. `/api/broker/movers` and `/api/portfolio` default to excluding non-active events with `?include_inactive=true` opt-in. Portfolio response now includes `inactive_excluded_count` so the UI can flag "we hid N ghost events". `/api/broker/performers/by-league/{league}` accepts the flag but currently only as passthrough — the SQL RPC needs a JOIN against the lifecycle view (NEXT in KANBAN).
- DONE — **Distribution check**: 1045 active / 95 completed / 89 ghost_eliminated / 2 postponed / 1 cancelled across 1232 events. Spot-verified on 8 known events (5 Raptors/Celtics scenarios + 1 concert + 1 active Knicks game + 1 NBA Finals ghost).
- NEXT (design) — KANBAN row added: render the lifecycle status badge on event hero + watchlist rows + movers list (ghost / completed / postponed visual treatment).
- NEXT (code) — KANBAN row added: rewrite `get_performers_by_league` SQL RPC to filter ghost events from the home/road aggregates.

### 2026-05-09 code (lane re-split: code = backend, design = frontend; chart range bug fix)

- DONE — **Lane re-split per user direction**: code becomes backend + audit + git-push lane; a fresh **design** coworker takes the terminal frontend (`static/*.html`, `design/*`). Copilot stays paused. New onboarding doc [`COWORKER_ONBOARDING.md`](COWORKER_ONBOARDING.md) covers the full contract — file ownership, no-push rule, `design_test` schema for sandboxing, hand-off pattern via KANBAN, and what good work looks like. New shared work board [`KANBAN.md`](KANBAN.md) has NEXT / DOING / BLOCKED / DONE columns; seeded with 7 NEXT rows (4 design, 3 code) so the design coworker has work waiting on day one.
- DONE — **Chart range bug fix**. User reported 30d view only displayed ~24 hours of data despite `range=30d` being requested. Root cause: Chart.js was auto-fitting the time x-axis to the union of populated datasets, and two new default series (`nonowned_median_retail`, `splits_min_q`) only have data from 2026-05-08 ~22:00 onward (introduced yesterday). With those series in the chart, the time-axis collapsed to the youngest series' window. Fix: backend now returns `range_meta: {range, hours, since, until}`; frontend pins Chart.js x-axis `min`/`max` explicitly to the requested window. Auto-picks time `unit` (hour for ≤24h, day otherwise) + sane `stepSize` so 30d gets a label every 3 days instead of "May 8" repeated. Added Robinhood-style smooth opacity fade during range fetch + 320ms `easeOutQuart` transition between renders.
- NEXT (design) — chart polish row in KANBAN: hover crosshair, relative timestamps in tooltip, `[`/`]` keyboard range step, hover state on inactive range buttons.
- NEXT (code) — investigate `listings_snapshots(event_id, captured_at, is_ancillary)` index; if missing, adding may unlock folding zone backfill back into the master cascade.

### 2026-05-09 code (solo phase, cascading cron model + 2-min ESPN freshness)

- DONE — **Cascading cron model** (mig `20260509040000`, SCHEMA v8): per user direction "run all crons as cascading events instead of one at a time. Also run the evo injury and trade chrons every 2 minutes for freshest news." Replaced 6 individual freshness crons with a single `master-cascade-2min` (jobid 38) that fires every 2 min. ESPN roster+gameday HTTP via `pg_net.http_post` (async), then sync chain: `auto_link_event_xref` → `backfill_event_splits_metrics(50)` → `backfill_event_nonowned_median(50)`. Per-stage try/except returns a JSONB summary. Verified runtime ~150-200ms per tick — well under the 2-min cycle and the 120s cron statement_timeout. ESPN injury/trade cadence bumped from 10 min → 2 min. Worst-case event coverage staleness collapsed ~50 min → ~2 min.
- DONE — **Zone backfill split out** (`zone-backfill-isolated-10min`, jobid 39, batch=5). `backfill_stale_zone_metrics(50)` had been silently failing every run for hours pre-cascade (jobid 35) — `match_performer_zone` LATERAL join exceeds the 120s cron statement_timeout. Forcing zones into a 2-min cycle would have turned every cascade tick red. Fix-the-cause NEXT: investigate the LATERAL cost + add an index on `listings_snapshots(event_id, captured_at, is_ancillary)` if missing.
- DONE — **Side-fix: `auto_link_event_xref` NOT NULL bug** on `event_xref.espn_slug`. Pre-cascade, jobid 31 had been silently failing on every run (the column was added later, function never updated). Cascade caught it via the per-stage error reporter on first invocation. Added a hardcoded league→slug CASE for the 7 leagues (NBA / WNBA / MLB / NHL / NFL / MLS / unknown). NEXT: replace with a `league_slug` lookup table.
- NEXT (code) — **Index audit** for `listings_snapshots`. If `(event_id, captured_at, is_ancillary)` index is missing, the zone backfill timeout may be solved by an index alone rather than function rewrite.
- NEXT (code) — Replace the league→slug CASE with a proper `league_slug` lookup table; will be needed when SeatGeek migration lands and we stop assuming a single-source ESPN slug.

### 2026-05-09 code (solo phase, midnight sweep + RULE 1)

- DONE — **SCHEMA.md v6 + RULE 1**: documented the ESPN cross-league filter rule explicitly as a top-level rule in AGENTS.md and a dedicated section in SCHEMA.md. Includes column-by-column schema for `espn_injuries_snapshots` + `espn_team_snapshots`, the `is_baseline` known-bug callout (only MLB+NHL detect changes correctly; other 5 leagues always = true), and an auto-assignment hooks table covering every endpoint/RPC that touches espn_* tables.
- DONE — **`midnight-catchup-sweep` cron** (jobid 36, mig 20260509020000): daily 00:00 UTC sweep that runs all 4 idempotent backfills in coordinated order (auto_link_event_xref → backfill_stale_zone_metrics → backfill_event_splits_metrics → ensure_major_league_watchlist_coverage). First fire 2026-05-10 00:00 UTC. Returns a JSONB summary so prod logs show the sweep impact (linked, recomputed, splits updated, watchlist additions). Component fns idempotent — running after intra-day crons just no-ops.

### 2026-05-09 code (solo phase begin)

- **LANE CONSOLIDATION** (per user direction): copilot and claude design lanes paused. code (this chat) becomes sole owner of the entire Terminal-2 stack until the broker terminal hits high-beta status. ROSTER + STATUS BOARD updated above. Lanes return on re-split — copilot picks back up retail chat + NLU + listings ingest; claude design picks up dedicated front-end polish.
- DONE — **CRITICAL: cross-league injury / standings bleed fix.** chart-data was filtering by `espn_team_id` only across 4 queries (injuries, standings, last5, roster_moves). Since `espn_team_id` is league-scoped (id "18" = NBA Knicks AND MLB Pirates AND NFL Saints AND NHL #18 AND WNBA #18), the queries pulled rows from every league with that team_id. For Knicks G5 chart: 12 real rows became ~229. Added `.eq("espn_league", home_league)` to all four queries (only `_news_series` and `_injury_load_series` were already correctly filtering). User caught it from MLB injuries appearing on the NBA event chart.
- DONE — **Recent Big Moves panel** on event page (commit 0f1924c): snap-over-snap detector for ≥3% price moves OR ≥100 tix swings. Plain-English Read column ("Inventory dump", "Demand spike", "Possible snapshot oscillation"). Surfaces things like the Knicks G5 −9.3% drop on 5/4.
- DONE — **Event hero nav buttons** (commit 0f1924c): home/away logos clickable to performer page; venue name in subline is an underlined link; explicit "→ team", "→ venue" button row under accent bar.
- DONE — **Injury overlay filter relaxed**: was `is_baseline=false` ("real status flips"), but espn-collect's is_baseline detection only works for MLB+NHL. NBA/NFL/MLS/WNBA/WC always come back is_baseline=true → 0 markers ever showed. Removed strict filter, added `is_change` flag per row so frontend can color/label differently. Fix-the-cause NEXT: get espn-collect's is_baseline detection working for the 5 affected leagues.
- DONE — **SCHEMA.md v5** (commit a94022a): replaced single-checkmark "ESPN coverage" table with 4-layer matrix (performer mapping / team standings / game-day snapshots / event xref). Reveals MLS/NHL/NFL/WNBA/WC have full performer-level coverage but ZERO event-level snapshots/xref because espn-collect.gameday only iterates NBA + MLB. Documented as a copilot-lane NEXT — but with copilot paused, this becomes a code-lane TODO.

### 2026-05-08 code (claude code session, late-evening — second sync audit)

- DONE — **Captured 2 new copilot edge functions into git** (audit-and-commit, no source until now):
  - `crawl-espn-team-assets` v2 — drains the `espn_asset_crawl_state` queue. Pulls up to 30 pending performers per invocation, hits ESPN /teams/{id}, upserts `performer_metadata` (logos / colors / ESPN URLs) and `venue_assets` (hero / map / capacity). Auth: `verify_jwt=false` + internal `X-Cron-Secret` placeholder. **No cron driving it yet** (queue progressed 35→65 pending=104 via manual triggers).
  - `probe-espn-data` v1 — diagnostic helper that hits 10 ESPN endpoints and walks the responses for image/logo/color/link fields. Useful for figuring out what we're not yet capturing.
- DONE — **Resolved migration count mismatch as a false positive.** Git=83, prod=82. Diff was historical naming convention (early-day pre-rename pass) where some older migrations have date prefixes in git but bare slugs in prod (e.g. `git: 20260507000020_drop_team_xref` ↔ `prod: drop_team_xref`). All schema changes accounted for; no real drift.
- DONE — **Asset crawl progress check**: 65/169 done (was 35 last audit), 104 pending. The fn works when invoked. Still no cron — manual drain only. NEXT (copilot) from prior turn still standing.
- ✅ ESPN crons all healthy: 11 runs in last 3h, 0 errors, injuries flowing in.
- ⚠️ `listings_snapshots` continues growing (1.94 GB / 7.82M rows / 459 events as of last check). Storage runaway fix still on cowork's lane.
- NEXT (copilot) — **Add a cron for `crawl-espn-team-assets`**. Recommend `*/3 * * * *` calling the fn with `{"limit": 30}` body. At 30/tick × 20 ticks/hour, the 104 remaining pending rows finish in under 4 minutes of cron uptime. After that the cron just keeps the asset state fresh as new performers get added to `espn_asset_crawl_state`. Internal `X-Cron-Secret` is currently a placeholder — fine for now since `verify_jwt=false` and the fn is internal-helper class.

### 2026-05-08 code (claude code session, evening — sync audit + simulation pass)

- DONE — **Sync audit caught 2 missing prod migrations. Captured into git.**
  - `20260508091000_tighten_ghost_filter_48h` — applied to prod earlier today (version 20260508155337) when I tightened the ghost filter from 7d to 48h. I patched the prior `20260508090000` file in-place instead of creating a separate file; capturing the standalone version now to keep git aligned with prod's migration ledger.
  - `20260508140000_espn_team_and_venue_assets` — copilot's work (applied 18:46 UTC). Adds 14 ESPN-asset columns to `performer_metadata` (logos, colors, ESPN URLs), new `venue_assets` table, `v_event_seating_chart` view, 3 `*_public` asset RPCs, and `espn_asset_crawl_state` queue table seeded with 169 performers (NBA/WNBA/MLB/NHL/NFL/MLS).
- DONE — **Simulation pass on the new asset infrastructure**:
  - **35 / 169 ESPN team assets fetched, 134 still pending.** Last fetch was 2026-05-08 18:52 UTC. The crawler appears to have been run once manually (or one cron tick) — 35 teams completed, then stopped. No active cron is driving the queue.
  - **performer_metadata fill**: 35/845 performers have `espn_team_id` + `logo_default_url` + `color_primary` (just the 35 that got crawled).
  - **venue_assets**: 34 venues with `hero_image_url` populated, **0 with `map_image_url`, 0 with `capacity`**. The hero-fetch worked for those 34; map + capacity fetchers either don't exist yet or aren't running.
  - **ESPN crons all healthy** post the verify_jwt fix from earlier today: 11 runs in last 3h, 0 errors, injuries inserting steadily (302 + 28 + 5 + 6 across recent runs).
  - **Test schemas (code_staging / copilot_test / design_test)**: only the _readme tables exist. No real usage yet — expected, no work has happened in those sandboxes.
  - **listings_snapshots** still growing: 1.94 GB / 7.82M rows / 459 events (+62 MB / +640k rows in last ~24h). Storage audit fix (change-only ingest) still on cowork's lane.
- NEXT (copilot) — **Drive the ESPN asset crawl to completion + add a cron**: 134/169 performers stuck in `espn_asset_crawl_state.status='pending'`. Either (a) finish the manual run that processed 35 earlier, OR (b) ship a cron + edge fn to drain the queue (recommend `*/5 * * * *` calling an `espn-fetch-team-assets` fn that processes N pending rows per tick). Without this, the new `get_performer_assets_public` / `get_event_assets_public` RPCs return mostly NULLs.
- NEXT (copilot) — **Wire venue_assets map_image_url + capacity fetcher**: `venue_assets` has 34 rows with hero URLs but 0 maps and 0 capacities. Either extend the asset crawler to also pull these from ESPN's venue endpoint, or accept current scope. The `v_event_seating_chart` view + `get_venue_assets_public` RPC already expose these fields — they'll just stay NULL until populated.
- DONE — **ARCHITECTURE confirmed with user + locked into AGENTS.md**. New diagram, new DATA FLOW section (cron tier table, per-surface cache TTLs, ESPN-as-overlay caveat). Two retail backends now explicit (chatbot live-with-90s-cache vs `*_public` RPCs reading cron-collected data). ESPN-context-in-chat called out as aspirational (retrieval only today; content not threaded into tool responses). TEvo rate limits noted as needing a centralized doc.
- NEXT (copilot) — **decide retail web-store freshness**: either keep current cron-collected `*_public` RPCs (fast, freshness = cron tier) OR switch to live TEvo per render (slower, always fresh, more rate-limit pressure). User flagged as open question. Current path is cron-collected; see `*_public` RPCs in mig 20260508023000.
- NEXT (copilot) — **thread ESPN context into chatbot tool responses**. Today: ESPN drives RETRIEVAL only (s4k_popularity_boost, athlete aliases). Chatbot doesn't surface ESPN content (injuries, standings, news) in tool results. Possible enhancement: add an ESPN-context tool to the chat fn loop, OR thread relevant injuries into `find_listings` results when an event's home/away team has active injuries. Open scope; coordinate with user before building.
- NEXT (code) — **write `docs/tevo-rate-limits.md`** after pulling `collect-listings` source into git via the proxy-commit / audit-and-capture pattern. Need to document: chat fn 90s cache + 429 retry-after, espn-collect 80-120ms pacing, collect-listings cron tier pacing (TBD pending source pull), centralized "if you call TEvo, here's your budget" reference.

### 2026-05-08 code (claude code session)

- DONE deploy — **chat fn v27 LIVE on prod** (Supabase project `hzrizjeaxlqcxfrtczpq`, deploy id `d9e3adc0-9b10-4224-bef9-c442458e4bd5`, version 27, status ACTIVE, verify_jwt=true). Smoke-test: unauthenticated POST returns 401 as expected. v27 source uploaded inline via MCP `deploy_edge_function` in a single tool call (60KB payload).
- DONE e96b41a — **chat fn v27** (cowork lane, user directive): listings cap raised from 6/12 to a hard 10, schema default 10. New system-prompt rule: when `total_matching_filters > count` the bot must ask ONE filtering question (qty / row / budget / section) before showing 10 raw listings. `find_better_seats` left at 6/12 (different UX, showing alternatives not match-dump). Source committed; v27 deployed in next turn via supabase MCP.
- DONE 12e18c9 — **Audit + Movers tab + storage doc**: captured 12 cowork migrations + 4 new edge fns into git (corpus_mining_v2, dictionary_seed, venue_crawl_state, event_type_5w_search, chat_suggestion_chips, chip_min_200_tickets, performer_metadata_genre_map, classify_performer_categories, schedule_venue_crawl, why_signals_schema, stopwords_round2; probe-tevo-performer, crawl-venues-and-performers v2, probe-tevo-events-by-venue, why-noaa-weather-alerts). Wrote `docs/storage-audit-2026-05-08.md` flagging listings_snapshots at **1.876 GB / 7.18M rows / 458 events / 16k avg rows-per-event** — change-only ingest pattern (same as espn-collect v3) projected to cut 80–95% of waste; partitioning + archival as follow-ups. Built `/movers` page (Bloomberg-style winners/losers report, 4 quadrants: owned-winners, owned-losers, market-winners, market-losers), levels: events / performers / venues, windows: 6h / 24h / 3d / 7d, segment filter: both / owned / market. Owned events get amber border. Added `/api/broker/movers` endpoint computing pct deltas vs window-back. Nav link added from event terminal. Storage optimization is a WAIT for cowork (collect-listings is their lane).
- DONE 4b6ea0c — **Broker terminal redesign — Stage 2 (chart + overlays + cadence-over-chart)**: Chart.js multi-axis line chart with 6 default series — owned median $, market median $, owned tix count, market tix count, home win %, away win %. Vertical overlay markers for injuries (red, dashed) + roster moves (purple). Last-5 W/L strip in pane header (H + A teams, green W / red L blocks). Cadence chip strip directly above chart with live countdowns per data type (listings / espn injuries / espn team) — chip flashes green on update, blue when polling, falls back to grey at rest. Per-series toggle pills below chip strip; toggles persist to localStorage (`evt_series_toggles_v1`). Stages 4 (equivalent sections — zone-level for now per user) + 5 (interactive map — using TEvo seating_chart_medium URL only per user) effectively shipped via Stage 1's zone breakdown table + static image. New `/api/broker/event/{id}/chart-data` endpoint returns 6 series + 2 overlay streams + last-5 records + home/away team identification (resolved via event_xref → espn_event_snapshots).
- DONE 41a7ef7 — **Broker terminal redesign — Stage 1**: shipped the new `/event/{id}` page (Bloomberg/Robinhood hybrid). 4-pane shell: top-left = event header + 8 metric cards w/ delta arrows + zone breakdown table (owned/market split, S4K-owned highlighted); top-right = seating chart (static image) + zone chip placeholders; middle = chart pane placeholder (Stage 2 wires `/api/events/{id}/series`); tabs = Sections (deltas per metric column), ESPN (home/away + odds + injuries via espn fn), Raw TEvo (full /v9/ticket_groups w/ S4K-owned chip on `office.brokerage.id=1768`). Added 5 new endpoints (`/api/broker/event/{id}/{overview,section-metrics,raw-tevo,espn,cadences}`). Per-section pollers schedule off own `last_pull_at + cadence + jitter` for natural cascade across events. Delta arrows + 1s yellow flash on metric value change. Stage 2 (time-series chart with player/injury overlays), Stage 4 (equivalent sections), Stage 5 (interactive map) still pending — all data sources confirmed available; need user nod on FanVenues license + equivalent-section rule.
- DONE 7e7e3a6 — **Second-pass audit + commit (chat + remaining gaps)**: re-checked prod vs git state. chat fn v26 source already in git from prior pass — verified intact (785 lines, full retail chat including TEvo lookup, Anthropic tool loop, audience-aware filters). Captured 3 cowork edge fns that were missing from git: `bulk-add-watchlist` v1, `probe-tevo-category` v1, `diag-ticket-groups` v6. Captured 2 cowork migrations missing from git: `20260425000002_store_github_pat` (token REDACTED in committed file — real token stays only in prod settings table) and `20260506000003_layered_zones_curated_first_keyword_fallback` (zone_rules + derive_zone_fallback + get_event_zones_rollup). Confirmed git's existing performer_zones/chat_aliases/fifa_aliases files contain the v2/v3 content cowork applied (no overwrite needed).

### 2026-05-07 code (claude code session)

- DONE d44ab45 — **Audit + commit cowork's prod work as their git proxy**: pulled SQL of 14 cowork migrations and source of 5 cowork edge fns from prod via MCP. Wrote them to git verbatim. Resolved migration version collisions: cowork's originals 18, 19, 20, 21, 25 were renumbered in git to 25, 26, 27, 28, 29 to avoid conflict with code's 18, 19, 20, 21. Added migration 30 (`team_xref_compat_view`) which resurrects team_xref as a read-only view over performer_external_ids — fixes all cowork RPCs (get_team_context, broker_event_intel, etc.) and the espn-rosters fn that referenced the dropped table. Updated OWN to reflect cowork's expanded surface (athlete history, wiki context, broker dashboard helpers, seating charts) and the "code is git proxy" arrangement.
- DONE 772ba18 — **PING cowork** (see ⚠️ at top of cowork section): flagged migration version collisions on 18-21, 13 cowork migrations + 5 edge fn deploys not in git, broken `espn-rosters` (reads dropped team_xref), and broker-lane crossings on `broker_dashboard_helpers_v2` / `broker_event_map_rpcs`. Asking them to commit + renumber + WIP-tag.
- DONE 89f911c — **espn-collect v5 + pg_cron schedules**: split espn-collect into 4 scopes via `?scope=` (roster / gameday / team_daily / all). Bugfixes mid-flight: v3 used MD5 (Deno doesn't support); v4 used inj.athlete.id (ESPN doesn't populate it in league-injuries). v5 uses SHA-256 + inj.id dedup key. Smoke-test verified change-only behavior live: first run 1404 inserts, re-run 30s later showed 2 inserts + 1402 unchanged (real ESPN data changed during the gap). Migration 21 scheduled three pg_cron jobs at the cadence you specified: roster every 10 min, gameday every 10 min (offset by 5 min), team_daily at 05:00 UTC. Old `espn-rosters-10min` (called nonexistent fn) + `espn-collect-daily` crons unscheduled.
- DONE 199fb15 — **espn fn v2 + slug bug fix + team_xref drop**: refactored `lookupTeamXref` to read from `performer_external_ids` (canonical, 217 teams). Deployed espn fn v2. Smoke-test caught a bug: `meta.espn_slug` mixed sport-slugs ("basketball/nba", correct) with team-slugs ("new-england-patriots", "bra", wrong) — Patriots/Brazil/etc. returned empty data because espn fn called bogus paths. Migration 18 fixed all 217 rows: `meta.espn_slug` is now always the sport-slug; the prior team-slug is preserved as `meta.espn_team_slug`. Migration 19 dropped now-redundant `unique (team_id, league, captured_at)` constraints (change-only ingest already prevents semantic dupes via content_hash). Verified change-only RPC end-to-end via SQL test (3 calls, 2 rows persisted, "unchanged" path correctly UPDATEs last_seen_at). Migration 20 dropped `team_xref` table. WIP cleared. NEXT note added for Twitter/social alerts feature.
- DONE f9eec71 — **WIP-section workflow**: added WIP section (between STATUS BOARD and ARCHITECTURE) where each agent appends in-flight file paths before edit and clears on commit. Added rule 11 spelling out the workflow. Updated rule 4: `C:\VibeCode\terminal-2` is now the canonical work-dir directive (still WAIT on user-driven `mv` + Railway root reconfig — git repo physically at `C:\Users\julia\Code\Terminal-2` until then). Noted discrepancy: a hand-seeded starter AGENTS.md exists at `C:\VibeCode\terminal-2\AGENTS.md` (no STATUS BOARD / STATE / LOG sections); when the move happens, the git-tracked one in this commit supersedes it.
- DONE cbf3a5e — **World Cup ESPN map (48/48) + change-only ESPN ingest**: pulled ESPN's 48 FIFA national teams; matched 22 against home_venues + 25 via tevo-perf-find + 1 manual (Türkiye→Turkey); migration 16 added 48 World Cup rows to performer_external_ids (now 217 across 7 leagues). Migration 17 added content_hash + last_seen_at + is_baseline columns to espn_team_snapshots / espn_injuries_snapshots / espn_event_snapshots, plus upsert_espn_*_snapshot RPCs. Backfilled all 720 existing rows as baseline. Deployed espn-collect v3 (reads from performer_external_ids, uses change-only RPCs); next run is delta-only. WAIT note added below for cowork's World Cup venue+date sweep.
- DONE 34d483f — **ESPN coverage full**: pulled all 169 teams from ESPN public API (NFL/NBA/MLB/NHL/MLS/WNBA), name-matched 110 against `performer_home_venues`, deployed `tevo-perf-find` edge fn (admin lookup) to search TEvo for the remaining 59 unmatched teams, manually fixed 2 (Atlanta United, CF Montréal). Migration 15 inserts 131 new rows into performer_external_ids (idempotent NOT EXISTS guard); applied to prod. Final coverage: 169/169 across big-5 + WNBA. Documented venue-shares for future event-key strategy.
- DONE 77502a3 — drop sms-bot + web-bot dirs from repo (tombstones already live in prod v6/v2 returning 410); migration 14 bridges team_xref → performer_external_ids (38 rows backfilled, applied to prod via MCP); team_xref marked DEPRECATED in DB comment + AGENTS.md STATE; restructure plan documented above.
- DONE dc14107 — coordination protocol: STATUS BOARD + pre/post-commit rules (8/9/10) + agent↔product mapping clarified (code = broker terminal, cowork = retail chat).
- DONE d602d18 — retro-doc batch: migrations 12 (team_xref) + 13 (event_xref + espn_*); espn + espn-collect Edge Function source; restored AGENTS.md (architecture diagram + rule 7); resolved fa4739b/38985f0 v2.10 conflict by skipping fa4739b.
- DONE 2026-05-07 ~20:00 UTC — canceled rogue cron `espn-collect-daily`; abandoned worktree branch `claude/frosty-volhard-a3a6d8` (8 commits behind, on deleted bot.py).
- WAIT cowork — **listings_snapshots storage runaway** (1.876 GB, 7.18M rows, growing fast). See `docs/storage-audit-2026-05-08.md`. Recommended fix: change-only ingest in collect-listings (same pattern as espn-collect v3 mig 17). Add content_hash + last_seen_at + is_change + removed_at columns; only INSERT when (section, row, qty, retail_price, wholesale_price, is_owned) tuple differs from prior. Projected 80-95% reduction. After that, partition listings_snapshots by month for O(1) drop. Both squarely in your lane (collect-listings + listings_snapshots schema).
- WAIT cowork — espn fn (v1) still reads team_xref. Bridge has landed (performer_external_ids has all 217 ESPN rows). Either agent can redeploy espn fn v2 reading from performer_external_ids; until then the deprecated team_xref must stay in DB. Daily collector cron stays unscheduled until espn-collect v3 baseline run is verified clean.
- ~~WAIT cowork — espn-gameday post-state pickup is broken.~~ **RESOLVED 2026-05-08** (commit pending). Root cause was NOT the content_hash (that's correctly computed over state+status+scores). It was that `espn-collect` was deployed with `verify_jwt=true` while the cron commands send only `X-Cron-Secret` (no `Authorization` header). Supabase's edge gateway 401'd every invocation before the function code ran. cron logged "succeeded" because the HTTP POST itself completed — with a 401 body. Fixed by redeploying espn-collect v6 with `verify_jwt=false` (mirrors collect-listings — the function's internal X-Cron-Secret check is the correct auth boundary for an internal helper). Verified working immediately: first post-fix cron run inserted 5 event_snaps + matched 2 new event_xref rows + captured Knicks G3 betting line drift (away ML −102 → +102 between yesterday and today, marking the Anunoby hamstring news). Similar gateway-vs-cron mismatch caught in the audit on `backfill-event-configurations-5min` and `crawl-venues-and-performers-3min` — both already include Authorization headers in their cron commands so they were fine. Pattern for future cron-driven internal fns: deploy with `verify_jwt=false` AND include an internal X-Cron-Secret check; never rely on JWT for internal pg_cron callers.
- WAIT cowork — **World Cup venue+date sweep / auto-tracker**. World Cup events don't fit cowork's seed-home-venues (category=performer) flow because they're scattered across venues with no clean "FIFA" TEvo category that returns the event-level performers reliably. Better pattern: TEvo `/v9/events?venue_id=X&occurs_at.gte=Y&occurs_at.lte=Z` for each known World Cup venue, then classify by name/performer match → auto-track. Inputs ready: 22 World Cup venues already in `performer_home_venues` where league='World Cup' (Allegiant, AT&T, Levi's, MetLife, Hard Rock, Sporting Park, Wembley, Olympiastadion Berlin, Allianz, Estadio da Luz, etc.). Suggested fn name: `seed-world-cup-events` or generalize `seed-home-venues` to also do venue-window event sweeps. Once landed, all events at WC venues during tournament window (June 11 – July 19, 2026) get auto-tracked, and the FIFA national teams in the event name get matched to performer_external_ids (source='espn', league='World Cup') for ESPN context. Same pattern can later cover Olympics, NCAA tourney sites, concert venues, etc.
- WAIT user — repo move from `C:\Users\julia\code\Terminal-2` → `C:\VibeCode\terminal-2` per RESTRUCTURE PLAN above. Filesystem mv + Railway root reconfig are user-driven; in-tree git mv (steps 3-6) is agent-driven once user signals done. **Note:** user has seeded a starter AGENTS.md at the new path. When the move happens, replace it with the git-tracked AGENTS.md (which has STATUS BOARD / WIP / STATE / LOG sections the seed lacks).
- NEXT chatbot in broker terminal — embed chat fn but with `audience='broker'` flag + full broker tools. Spec to be written as a GitHub issue. Will need chat fn v20 to accept audience param (cowork's lane).
- NEXT (heads-up from user 2026-05-07) — **Twitter / similar social feeds for terminal alerts**. Use case: surface real-time signals (insider trading patterns of social mentions, breaking injuries, news velocity, beat reporter scoops) into the broker terminal as alert chips next to the affected events/performers. Likely needs: a feed-ingest edge fn (twitter API or alt like nitter/X-search), a `social_alerts` table keyed by performer_id/event_id with content_hash dedup (same change-only pattern as espn-collect), terminal UI chips that pull from `social_alerts` filtered by what's selected. Decisions before starting: which provider (X API tier, alt sources), how to filter signal-from-noise (verified accounts only? specific lists?), retention (keep last 24h or all-time).

### 2026-05-07 cowork

- ✅ **PING resolved by code (2026-05-08 00:50 UTC)** — user clarified cowork lacks git auth, so code is now committer/auditor for cowork's prod deploys. Next session, cowork can keep deploying via MCP; code will pull + commit on cadence. This block stays here as record. Original ping below:
- ⚠️ **PING from code (2026-05-07 23:55 UTC)** — read this before your next deploy:
  1. **Migration version collisions.** You shipped `20260507000018_system_placeholder_zones`, `..._000019_canonical_zone_names`, `..._000020_hybrid_zone_coexistence`, `..._000021_chat_audit_findings`. I shipped `..._000018_espn_fix_sport_slug`, `..._000019_drop_redundant_unique_constraints`, `..._000020_drop_team_xref`, `..._000021_espn_collect_cron_schedules` at the same numbers. Postgres applied both (different timestamps), but our git tree only has mine. We need to renumber on a future commit so the migration history is consistent. Also: please pick the next free version (current max is `...000024` in DB).
  2. **Your migrations 12-17, 22-24 are NOT committed to git.** Specifically: `espn_athletes_and_history`, `team_playoff_context`, `wiki_context`, `team_context_with_wiki`, `broker_dashboard_helpers_v2`, `tevo_ticket_groups_cache`, `event_configuration_and_seating_chart`, `broker_event_map_rpcs`, `schedule_event_config_backfill`. Same story for edge fns: `espn-rosters` v2, `wiki-collect` v1, `probe-seating-charts` v1, `backfill-event-configurations` v2, and chat v20-v26. **Please commit them so the repo reflects prod.** Otherwise we lose your work if anything ever rebuilds from git.
  3. **`espn-rosters` is broken.** It reads `team_xref` which I dropped in mig 20 (the team_xref data lives in `performer_external_ids` where `source='espn'` now — 217 rows across all big-5 + WNBA + World Cup, full sport-slug + abbr in `meta`). Quick fix is the same pattern I used in `espn-collect` v3. Your `espn-rosters-10min` cron was already orphaned (calling that fn name) and I unscheduled it in my mig 21, so nothing is actively erroring — but the fn body still won't run if invoked manually.
  4. **Broker-lane crossings.** `broker_dashboard_helpers_v2` and `broker_event_map_rpcs` are squarely my lane per OWN. Not undoing anything (the work looks legit), just flagging — please WAIT-note before broker-side changes so I can review compatibility with my UI work.
  5. **WIP section was empty during all of the above.** Per rule 11, please list files you're editing under `### cowork` before starting. Otherwise I have no way to know what's in flight.

  Replies welcome under this section. I'll re-read on my next session.

- DONE migrations 02-11 (zone_metrics, section_metrics depth, retail/broker views, performer_home_venues, chat_tracked_events, performer_external_ids, chat_corpus_word_pool, chat_aliases + extractor, fifa_aliases)
- DONE chat v15-v19 (URL strip, auto-track, home/away, curated S4K zones, search noise strip)
- DONE collect-listings v9 (zone+section breakdowns, chat-tracked sweep)
- DONE seed-home-venues v1 (135 teams)
- DONE chat_aliases seed 193 entries
- DONE retail/broker view wall (data separation enforced in SQL)
- DONE chat_corpus + word pool aggregator
- WAIT MLS home venues (TEvo category name unknown — try "Major League Soccer" / "Soccer" variants on next probe)
- WAIT FIFA category_id (probe req 1402 still pending). Once known: invoke bulk-add-watchlist with that cat_id.
- NEXT chat fn v20 — wire extract_chat_entities into request flow as system hint. (also: accept `audience` param to support broker-side chatbot embed — see code's NEXT note above)
- NEXT ESPN/odds ingest (#50) — **partially done by code**. Bridge with code's team_xref → performer_external_ids landing soon. Then this NEXT becomes "wire the data into broker UI cards + retail nudges".
- NEXT OSS LLM swap (#45) — Groq/Together/DeepSeek; OpenAI-compat adapter
- NEXT multi-channel sales (#56) — SMS / WhatsApp / Messenger adapters all hit same chat edge fn
- NEXT playoff series state (#57) — depends on ESPN ingest
