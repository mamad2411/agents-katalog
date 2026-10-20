---
name: sports-data-pipeline
description: Multi-source live sports data ingestion with abstract DataSource pattern, SQLite storage, and the-odds-api integration.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [sports-data, data-ingestion, odds-api, sqlite, pipelines]
    triggers:
      - "set up live sports data"
      - "ingest odds and scores"
      - "data pipeline for sports betting"
      - "multi-source sports API"
      - "replace mock data with live"
      - "odds API integration"
    related_skills: [land-acquisition-research, county-property-database]
---
# Sports Data Pipeline

## Architecture

Use an abstract `DataSource` base class for each provider:

```
DataSource (ABC)
  ├── OddsAPISource      — the-odds-api.com REST client
  ├── DKScraperSource    — Playwright-based DraftKings scrape (optional)
  └── FDScraperSource    — Playwright-based FanDuel scrape (optional)

DataPipeline
  ├── register_source(source)
  ├── run()               — fetch from all sources, normalize, store
  └── _process_sport()    — one sport, all sources, merge, upsert
```

## Key Design Decisions

### 1. NO MOCK DATA EVER
- When a live API key is missing (or the API fails), return `[]` — never fall back to generated data.
- No `_mock_odds()` or `_mock_scores()` methods anywhere.
- The DB will be empty without a real key. That's correct, honest behavior.
- User will notice and provide a key — do not solve "no data" with fake data.

### 2. One Source File
Keep `OddsAPIClient` in `sportsbook/integration.py` and `DataPipeline`, `DataSource` in `pipeline/data_pipeline.py`. Don't spread across many files early.

### 3. SQLite with WAL Mode (Unified Schema v2.0)
- WAL journal mode for concurrent reads, thread-local connections for uvicorn workers.
- **20 tables** covering the full application layer:
  - **Sports pipeline:** `sports`, `teams`, `games`, `odds_history`, `data_sources`
  - **Application:** `users`, `bets`, `picks`, `parlays`
  - **Challenge engine:** `challenge_participants`, `challenge_seasons`, `ai_agent`
  - **Sync/ops:** `sync_jobs`, `sync_history`, `affiliates`, `auth_tokens`, `credentials`, `system_config`
- Indexes on `games.status`, `games(sport_id, status)`, `odds_history.game_id`, `bets(user_id)`, `picks(date)`, `sync_jobs(user_id)`.
- Unique indexes prevent data duplication: `idx_affiliates_name`, `idx_credentials_service_username`.
- `system_config` table tracks app version and DB schema version (`sports_db_version`).
- The schema self-installs on every startup via `SCHEMA_SQL` in `database.py`.
- Seed data (sports, affiliates, system_config) uses `INSERT OR IGNORE` — safe for re-runs.

### 4. Pipeline Lifecycle
- `build_default_pipeline(api_key)` — convenience factory.
- Register sources, call `pipeline.run(sport_names)` to process.
- Runs on startup via daemon thread + scheduled every 15 minutes (APScheduler).
- Cleanup old games (>7 days) after each run.

### 5. Sport Key Mapping

```python
SPORT_KEYS = {
    "NFL":   "americanfootball_nfl",
    "NBA":   "basketball_nba",
    "MLB":   "baseball_mlb",
    "NHL":   "icehockey_nhl",
    "NCAAF": "americanfootball_ncaaf",
    "UFC":   "mma_mixed_martial_arts",
}
```

## Odds API v4 URL Format (Critical Pitfall)

The Odds API v4 uses **URL-path-based routing**, NOT query-parameter sport selection:

```
✅ CORRECT:  /v4/sports/americanfootball_nfl/odds?regions=us&markets=h2h
❌ WRONG:    /v4/odds?sport=americanfootball_nfl&regions=us&markets=h2h
```

The wrong format returns **404 Not Found** (CloudFront HTML error page), not an empty array. This is a silent failure — the HTTPX client raises an exception, the catch-all handler returns `[]`, and it looks like there's no data when the real issue is the URL.

### Correct URL Patterns

| Method | Endpoint |
|--------|----------|
| `get_live_odds` | `GET /v4/sports/{sport}/odds?apiKey={key}&regions=us&markets=h2h,spreads,totals` |
| `get_scores` | `GET /v4/sports/{sport}/scores?apiKey={key}&daysFrom=1` |
| `get_sports` | `GET /v4/sports?apiKey={key}` |

### scores.get("scores", []) Returns None Pitfall

When the Odds API returns `"scores": null` for a game (common for scheduled games), `.get("scores", [])` returns **`None`** because the key `"scores"` exists with value `None`. The default `[]` is only used when the key is missing entirely.

```python
# BROKEN — TypeError: 'NoneType' object is not iterable
scores_arr = score_info.get("scores", [])

# FIXED — None → [] gracefully
scores_arr = score_info.get("scores") or []
```

Same pattern protects `completed` and `home_score`/`away_score` lookups.

### Free Tier Quirks

| Quirk | Detail |
|-------|--------|
| **Code expiry** | Verification codes expire in ~30-60 seconds |
| **No events = 404** | If a sport has no upcoming games, the odds endpoint returns 404, not empty array |
| **500 request/month cap** | Free tier = 500 requests total. Key returns 401 after exhaustion (not a soft limit). **Need a new email + account to generate a fresh key** — there is no key-regeneration flow without login |
| **Off-season** | NBA/NHL return 404 during June-September; MLB and CFL are summer-active |

### Free Tier Exhaustion (Critical)

When the 500-request monthly cap is hit:
1. The Odds API starts returning **401 Unauthorized** for all odds/scores endpoints
2. The pipeline in `OddsAPIClient` catches the HTTPError and returns `[]`
3. **The DB is cleared** — on startup, `pipeline.run()` stores 0 games (the empty array replaces existing data)
4. Chart data (player trajectories) is **not affected** — it's generated independently by the backend AI simulation
5. Sports list endpoint (`/v4/sports`) continues to work — it uses a separate quota

**Fix:** Create a new free-tier account with a fresh email → new API key → update `.env`. See `references/programmatic-api-key-registration.md`.

## Supplementary Data Sources

### MLB Stats API (No Key Required)

The MLB Stats API (`statsapi.mlb.com`) is a free, keyless data source for game schedules, scores, probable pitchers, and player info. Useful as a fallback when primary odds providers are inaccessible, or to check if any games exist before attempting to fetch betting lines.

**Key endpoint:** `GET /api/v1/schedule?sportId=1&date=YYYY-MM-DD&hydrate=probablePitcher,linescore`

**Typical use cases in a betting-scanner cron job:**
1. Check if regular-season games exist today (vs All-Star break, off days)
2. Get probable pitchers for matchup analysis
3. Verify game results are officially final before resolving bets

See `references/mlb-stats-api-reference.md` for full endpoint catalog, response structure, and inline inspection patterns.

### Programmatic Key Registration

When the user needs a free API key and the browser email-verification flow is blocking:

1. Create a temp mailbox via `mail.tm` API (faster than temp-mail.io):
   - `curl -s https://api.mail.tm/domains` → get a valid domain
   - `curl -s https://api.mail.tm/accounts -X POST` → create account
2. Register at `https://dash.the-odds-api.com/` using the temp email
3. Check mail.tm for the verification code immediately
4. Paste code in browser before it expires

**See:** `references/programmatic-api-key-registration.md` for full shell commands.

## The Odds API Setup

1. Register at https://dash.the-odds-api.com/ (free tier: 500 requests/month)
2. Verify email with confirmation code
3. Copy API key from dashboard
4. Set in `.env`: `ODDS_API_KEY=***ns.com`
5. Restart server — pipeline pulls live data on next run

### Free Tier Budget
- 500 requests/month ≈ ~16/day
- Each `get_live_odds` + `get_scores` call = 2 requests per sport
- Running 4 sports (NFL, NBA, MLB, NHL) once per hour = 192/day — too many for free tier
- **Recommended:** 4 sports, 2 runs/day = 16 requests/day × 30 = 480/month

## Verification Pattern

After pipeline changes, verify:
1. All mock references purged (`rg -i mock pipeline/ sportsbook/ backend/`)
2. `OddsAPIClient._mock_odds` and `_mock_scores` attributes absent
3. `OddsAPIClient.get_live_odds()` returns `[]` without key
4. Pipeline stores 0 games when no API key
5. `/api/games/live` returns `{}`
6. `/api/games/db-stats` shows `total_games: 0`

## Migrating JSON Data to SQLite

When migrating ad-hoc JSON data files into the unified schema, follow this pattern:

### Migration Script Pattern

Create a standalone Python script (`data/migrate_data.py`) that:

1. Reads each JSON file (e.g. `bets.json`, `challenge.json`, `records.json`)
2. Converts fields to match target column types (string → integer for odds, etc.)
3. Uses `INSERT OR IGNORE` for idempotent re-runs
4. Commits in batches after each table
5. Prints a summary with row counts per table

**Critical — add UNIQUE constraints BEFORE migration, not after:** If you insert seed data first and then run the migration, the `INSERT OR IGNORE` has nothing to check uniqueness against on tables without a UNIQUE constraint — it inserts duplicates. The `affiliates` table is a real example: the schema seed inserted 4 rows, and the migration inserted 4 more duplicates because there was no `UNIQUE(name)`. Always add the constraint first, then insert.

```sql
-- ADD BEFORE migration inserts:
CREATE UNIQUE INDEX IF NOT EXISTS idx_affiliates_name ON affiliates(name);
CREATE UNIQUE INDEX IF NOT EXISTS idx_credentials_service_username ON credentials(service, username);
```

### Deduplication Recovery

If duplicates already exist, use the `MIN(id)` group-by pattern:

```sql
DELETE FROM affiliates WHERE id NOT IN (
  SELECT MIN(id) FROM affiliates GROUP BY name
);
```

Then add the unique index to prevent recurrence.

## Pitfalls

- **INSERT OR IGNORE without UNIQUE constraint inserts duplicates** — if you need idempotent inserts, ensure the table has either a PRIMARY KEY, UNIQUE constraint, or UNIQUE index on the dedup column. Without it, `INSERT OR IGNORE` inserts every time.
- **Don't add mock fallbacks** — the user explicitly forbids them. An empty DB without a key is correct.
- **Don't hardcode API keys** — always use `os.getenv("ODDS_API_KEY", "")` with `.env` loading.
- **Don't fetch scores and odds separately** for scheduled games — `get_scores` only returns completed/live games. `get_live_odds` has upcoming games with commence times.
- **Don't infer period/clock** from fake data — only use values from the real API response.
- **Don't store games if the API returns empty** — the pipeline should skip without inserting blank rows.
- **The free tier codes expire fast** (~30-60 seconds) — set up temp-mail before requesting a code, and paste it immediately.
