---
name: seo-api
description: DataForSEO API integration architect for developers. Covers the entire DataForSEO surface — DataForSEO Labs (ranked keywords, keyword ideas/suggestions/related, domain rank overview, competitors, domain/page intersection, subdomains, relevant pages, bulk keyword difficulty, bulk traffic estimation, search intent, historical rank/keyword/SERP data, top searches), SERP (Google + YouTube organic live advanced), Keywords Data (Google Ads search volume, Google Trends, DFS Trends), Backlinks (summary, backlinks, anchors, referring domains/networks, competitors, intersections, bulk metrics, time series), On-Page (instant pages, Lighthouse, content parsing), AI Optimization (LLM mention metrics, ChatGPT scraper, live LLM response, AI keyword data), and Merchant/Business data. For any "how do I…" question about endpoints, parameters, JSON bodies, per-call cost, rate limits, or authentication. Produces ready-to-paste cURL / Python / TypeScript / MCP-tool-call recipes against `https://api.dataforseo.com/v3/*` (HTTP Basic auth) and the `mcp__dataforseo__*` MCP tools. DataForSEO is stateless — no saved projects, rank-tracking state, or stored audits; stateful needs route to GSC (own verified site) / GA4 (own traffic) or scheduled DataForSEO pulls saved to local storage. Distinct from the other SEO skills which produce analysis deliverables (briefs, audits, reports); `seo-api` produces integration recipes. Use when the user asks "how do I use DataForSEO to do X", "what endpoint gives me Y", "cost of workflow Z", "build a rank tracker", "cURL / Python / TypeScript / MCP for DataForSEO", "what's the rate limit", "integrate DataForSEO with Looker / n8n / Sheets / BigQuery", or any direct question about DataForSEO endpoints, parameters, bodies, or wiring.
---
> Built on the DataForSEO MCP server (`mcp__dataforseo__*` tools) and the REST API at `https://api.dataforseo.com/v3/*`. Tool names are cross-checked against the connected server so reference data is never stale.

# DataForSEO API Integration Architect

Help developers ship real integrations against the DataForSEO API. The deliverable is a **code recipe** — a ready-to-paste cURL / Python / TypeScript / MCP-tool-call sequence — for the goal the user describes. The skill knows the whole DataForSEO surface (Labs / SERP / Keywords Data / Backlinks / On-Page / AI Optimization / Merchant & Business Data), the pay-per-call cost model, the Basic-auth setup, and which `mcp__dataforseo__*` tool maps to which REST endpoint.

DataForSEO is **stateless** — it stores nothing on the user's behalf. There are no saved projects, no stored rank tracking, no project-attached audits. Anything that needs to persist between runs is built on a first-party companion (GSC for the own verified site, GA4 for own traffic) or the user's own local storage — never on DataForSEO. There is therefore no "create project / confirm mutation" flow in this skill: DataForSEO calls are read-shaped requests that change no account state.

## Prerequisites

- **DataForSEO MCP server connected.** The skill calls `mcp__dataforseo__*` tools. The server authenticates with **HTTP Basic auth** using `DATAFORSEO_USERNAME` / `DATAFORSEO_PASSWORD` env vars (no OAuth, no shared key). If `/mcp` doesn't list `dataforseo`, emit the install command and stop — see `references/auth-and-keys.md`.

  ```bash
  claude mcp add dataforseo \
    --env DATAFORSEO_USERNAME="$DATAFORSEO_USERNAME" \
    --env DATAFORSEO_PASSWORD="$DATAFORSEO_PASSWORD" \
    -- npx -y dataforseo-mcp-server
  ```

- **(For REST-direct recipes)** `DATAFORSEO_USERNAME` / `DATAFORSEO_PASSWORD` available as env vars so the emitted code can build the Basic header (`-u "$DATAFORSEO_USERNAME:$DATAFORSEO_PASSWORD"`).
- **(Optional) `WebFetch`** for fetching deep guides at `dataforseo.com/apis/*` when the request needs prose beyond what the tool schemas carry.
- User provides an integration goal in plain language (e.g., "build a rank tracker for client X", "pull backlink deltas for 50 domains into BigQuery weekly", "content-brief pipeline for a keyword"). The skill interviews only when the goal is ambiguous.

## Process

1. **Preflight.**
   - Confirm the DataForSEO MCP is reachable. If not, emit the `claude mcp add dataforseo …` command above and stop. See `references/auth-and-keys.md` for Basic-auth and headless/CI patterns.
   - **No credit gate.** DataForSEO is prepaid pay-per-call — there is no pre-run balance check step. Instead, after mapping the calls (step 4), surface a one-line cost note: *"DataForSEO bills per call; this run issues ~N calls. Each list is capped with `limit`/`filters`."* A balance read is only needed if the user explicitly asks — it's a free REST call to `appendix/user_data`, not a skill step.

2. **Clarify the goal.** Ask 1–3 questions only if ambiguous. Skip when the user spelled it out. Useful follow-ups:
   - "One-off run, recurring job (daily/weekly), or a long-lived integration in your product?"
   - "Target location / language — or a specific market code?"
   - "Does this need to remember state between runs (rank history, audit history)? If so, where should it live — GSC (own verified site), GA4 (own traffic), or your own local storage of dated DataForSEO snapshots?"

3. **Identify the surface(s).** Map the goal to one or more DataForSEO surfaces. See `references/api-surface-map.md`.
   - **DataForSEO Labs** — domain/keyword analytics on any target (overview, ranked keywords, competitors, intersections, ideas, difficulty, intent, historical, top searches).
   - **SERP** — live Google/YouTube results + features (AIO, PAA, featured snippet).
   - **Keywords Data** — Google Ads volume, Google Trends, DFS Trends.
   - **Backlinks** — profile, links, anchors, referring domains/networks, competitors, intersections, bulk metrics, time series.
   - **On-Page** — single-URL instant fetch, Lighthouse, content parsing.
   - **AI Optimization** — LLM mention metrics, ChatGPT scraper, live LLM response, AI keyword data.
   - **Merchant / Business Data** — Amazon products, Google Business listings.
   - **Stateful?** If the goal needs persistence over time, the data layer is DataForSEO but the *state* lives in GSC (own verified site — rankings/coverage), GA4 (own traffic/conversions via `mcp__google-analytics__run_report`), or local storage (dated snapshots — the `seo-drift` pattern). Ongoing site audits = the canonical DataForSEO On-Page loop (`on_page_instant_pages` + `on_page_lighthouse`) over a discovered URL set, persisted locally for re-check (see step "ongoing site audit" below). Call this out explicitly.

4. **Map to tools / endpoints.** For every step, name:
   - The MCP tool: `` `mcp__dataforseo__dataforseo_labs_google_ranked_keywords` `` (or the short `dataforseo_labs_google_ranked_keywords` in recipe text).
   - The REST endpoint: `POST /v3/dataforseo_labs/google/ranked_keywords/live` (Basic auth, JSON-array body, result under `tasks[].result[]`).
   - The per-call cost tier (live vs standard) — source from `references/rate-limits-and-credits.md` and each endpoint's docs page. MCP tools always pay the **live** tier.
   - If a tool needs a `location_code` / `language_code` the user didn't supply, insert the resolver (`serp_locations` / `kw_data_google_ads_locations`) or pass the code directly. See `references/api-surface-map.md` § "Parameter resolution".

5. **Note cost (one line, not a gate).** Sum the call count, classify live vs standard tier, and surface the one-line cost note from step 1. Cap each list-shaped call with `limit` + `filters` so it stays cheap and within the MCP inline-size limit. No stop-on-insufficient-funds step — a `402` at run time is the only signal, and it's terminal (top up, don't retry).

6. **Emit code (default) — or run live to fetch data.** Since DataForSEO mutates nothing, "live mode" just means *running the read calls to fetch real data into the deliverable* — there is no mutation to confirm.
   - **Code mode (default)** — emit ready-to-paste cURL, Python (`requests` + `HTTPBasicAuth`), TypeScript (`fetch` + Basic header), and MCP-tool-call variants. The developer runs them. Best for recurring jobs and anything deployed outside the Claude session.
   - **Run-and-fetch mode** — call the `mcp__dataforseo__*` tools now to pull real data and fold the results into `RECIPE.md`/evidence. Read-only by definition; no confirmation prompts. Use when the user wants the data *and* the recipe in one pass.
   - **Hybrid** — fetch a sample live to validate the shape, then emit the recurring code for the full job.

7. **Execute or emit.**
   - **Code mode** — write `code/curl.sh`, `code/python.py`, `code/typescript.ts`, `code/mcp-calls.md`. Each file is complete and runnable, not a fragment. Include handling for `429` (backoff with jitter) and `402` (out of funds — terminal). Always validate per-task `tasks[i].status_code == 20000`. See `references/integration-patterns.md`.
   - **Run-and-fetch mode** — call the tools, log each call to `evidence/03-execution-log.md` (timestamp, tool, args, status), and embed the fetched data in `RECIPE.md`.

8. **Synthesise `RECIPE.md`.** Always written. The deliverable a developer reads to understand what was built or how to build it. See output format below.

## Output format

Folder `seo-api-{slug}-{YYYYMMDD}/` where `{slug}` is a kebab-case summary of the goal (e.g., `acme-rank-tracker`, `bulk-backlinks-bigquery`).

```
seo-api-{slug}-{YYYYMMDD}/
├── RECIPE.md                       (primary deliverable — what was built or how to build it)
├── code/
│   ├── curl.sh                     (cURL one-liners + multi-step bash, Basic auth)
│   ├── python.py                   (requests + HTTPBasicAuth)
│   ├── typescript.ts              (fetch + Basic header)
│   └── mcp-calls.md                (mcp__dataforseo__* sequence — agent-native)
└── evidence/
    ├── 01-preflight.md             (MCP connectivity check; one-line cost note)
    ├── 02-cost-note.md             (per-call count, live/standard tier, cap params)
    ├── 03-params-resolved.md       (location_code / language_code resolved upfront — omit if none needed)
    └── 04-execution-log.md         (mcp__dataforseo__* calls run, with args + status — omit in pure code mode)
```

Top-level: `RECIPE.md` + `code/`. The `evidence/` folder preserves the reasoning trail. `03` and `04` are conditional — a pure code-mode run with no resolved params and no executed calls ships just `01` + `02`.

`RECIPE.md` follows this shape:

```markdown
# {Integration Title}: {target}

> Run dated {YYYY-MM-DD} · Mode: {code | run-and-fetch | hybrid} · ~{N} DataForSEO calls (live tier)

## Goal

{1–2 sentences. What was asked, what's being shipped.}

## API surface map

| Step | MCP tool | REST endpoint | Verb | Cost tier |
|------|----------|---------------|------|-----------|
| 1 | `dataforseo_labs_google_domain_rank_overview` | `/v3/dataforseo_labs/google/domain_rank_overview/live` | POST | live |
| 2 | `dataforseo_labs_google_competitors_domain` | `/v3/dataforseo_labs/google/competitors_domain/live` | POST | live |
| 3 | `backlinks_summary` | `/v3/backlinks/summary/live` | POST | live |
| ... | ... | ... | ... | ... |

## Auth & setup

{Basic-auth header / Python HTTPBasicAuth session / TypeScript fetch wrapper showing exactly how to authenticate. Reference `references/auth-and-keys.md`.}

## Cost note

- ~{N} calls, mostly live tier. DataForSEO bills per call (prepaid, no credits).
- Each list capped with `limit`/`filters` to control per-row cost and stay under the MCP inline-size limit.
- {If stateful: the snapshot/state is persisted in {GSC | GA4 | local storage}, not in DataForSEO.}

## Recipe

### Option A — cURL
(complete bash script in `code/curl.sh`)

### Option B — Python
(complete script in `code/python.py`)

### Option C — TypeScript
(complete script in `code/typescript.ts`)

### Option D — MCP tool calls
(agent-native sequence in `code/mcp-calls.md` — for when this lives inside another Claude/Cursor/Codex workflow)

## Rate limit & retry strategy

- DataForSEO allows up to 2,000 calls/min and 30 concurrent requests. Pace sequentially for batched workflows; small-batch parallelism (≤30 concurrent) is safe.
- 429 handling: exponential backoff with jitter (1s → 2s → 4s → 8s, ±20%). 5xx: same. Treat 402 "balance exhausted" as terminal — no retry. Always check per-task `status_code == 20000`.

## State & persistence (if applicable)

{Where history lives. E.g., "Daily SERP positions appended to BigQuery `seo.rankings`; DataForSEO returns the snapshot, this job persists + diffs it." Or "Own site → GSC is authoritative."}

## What you still need to do

{Concrete next steps. E.g., "Run `python.py` daily via cron at 06:00 UTC", "Wire the Slack webhook for rank drops", "Create the BigQuery table with this schema".}

## Linked docs

- {Direct links to the relevant pages on `dataforseo.com/apis/*`.}

## When to escalate to another skill

- `seo-content-brief` — once the integration pulls keyword data, turn it into editor briefs.
- `seo-technical` — if the goal needs an ongoing site audit. DataForSEO On-Page is single-page, so the audit is rebuilt as the canonical loop: discover a URL set (sitemap / `mcp__gscServer__get_search_analytics` dimension=page / `dataforseo_labs_google_relevant_pages`) → loop `on_page_instant_pages` + `on_page_lighthouse` → GSC `inspect_url_enhanced` / `batch_url_inspection` for indexation → persist results to local storage for re-check.
- `seo-drift baseline` — if the job is to track a domain over time, snapshot it first (local storage).
- `seo-geo` — if the job tracks LLM/AI-search visibility and needs a competitive read.
```

## Tips

- **One credential pair authenticates everything.** Basic auth with `DATAFORSEO_USERNAME` + `DATAFORSEO_PASSWORD` covers every surface — Labs, SERP, Keywords Data, Backlinks, On-Page, AI Optimization, Merchant. No OAuth, no per-surface keys. See `references/auth-and-keys.md`.
- **Body is always a JSON array.** Every POST takes an array of task objects, even for one task. Results come back under `tasks[].result[]`. Always check `tasks[0].status_code == 20000` before trusting `result`.
- **MCP tools are the live tier.** Each `mcp__dataforseo__*` tool hits a `*/live/*` endpoint (the higher-cost synchronous tier). For the cheaper standard/async tier, drop to REST `task_post` + `task_get` — that's a REST-only optimization, not exposed through MCP.
- **Failed tasks are free.** A task with a 40xxx/50xxx `status_code` is not billed. Don't over-engineer retries to "save money".
- **Cap every list with `limit` + `filters`.** Pay-per-row Labs/Backlinks lists get expensive and can overflow the MCP inline-size limit. Use `limit` and server-side `filters` (discover fields via `dataforseo_labs_available_filters` / `backlinks_available_filters`). When a response still overflows, slice the saved file with `jq` or call REST directly (no inline cap).
- **DataForSEO stores nothing.** No projects, no rank history, no stored audits, no disavow. For state-over-time: own verified site → GSC `mcp__gscServer__get_search_analytics`; own traffic/conversions → GA4 `mcp__google-analytics__run_report`; any domain → scheduled `serp_organic_live_advanced` saved to local storage (the `seo-drift` pattern); ongoing audit → the canonical On-Page loop (`on_page_instant_pages` + `on_page_lighthouse` over a sitemap/GSC/`dataforseo_labs_google_relevant_pages` URL set) with results persisted to local storage for re-check. Never claim DataForSEO remembers between runs.
- **Resolve location/language first.** Most calls need `location_code` + `language_code`. Pass the code directly when known (US = `2840`, en = `"en"`), or resolve names via `serp_locations` / `kw_data_google_ads_locations` / `merchant_amazon_locations`. See `references/api-surface-map.md` § "Parameter resolution".
- **AI Overview comes from SERP, not a dedicated endpoint.** Read the AIO / PAA / featured-snippet blocks from `serp_organic_live_advanced` `items[]`. AI *visibility* (LLM mentions) is the separate `ai_opt_llm_ment_*` family.
- **"Domain authority" maps to two signals.** Organic strength → `dataforseo_labs_google_domain_rank_overview`; backlink strength → `backlinks_bulk_ranks` (rank 0–1000). Toxic links → `backlinks_bulk_spam_score`.
- **Inspect the live surface** with MCP Inspector (`npx @modelcontextprotocol/inspector`) pointed at the `dataforseo` server to walk the full tool catalogue and input schemas.

## Works well with

- **Predecessors:** none — entry point for any DataForSEO integration question.
- **Successors (when the integration starts producing data):**
  - `seo-content-brief` — when the integration pulls keyword research that should become editor briefs.
  - `seo-page` — when one URL from the integration needs a keep/refresh/consolidate/kill verdict.
  - `seo-drift baseline` — to snapshot a domain/URL before the integration runs, so regressions are detectable (and to *be* the storage layer for over-time tracking).
  - `seo-technical` — when the integration involves audit-shaped data and the output needs prioritisation.
  - `seo-geo` — when the integration tracks LLM/AI-search visibility and needs a competitive read.

## References

- `references/auth-and-keys.md` — Basic auth (login + password, base64, `Authorization: Basic`), MCP env-var setup, headless/CI patterns, credential rotation, the stateless "no stored state" routing table.
- `references/rate-limits-and-credits.md` — 2,000 calls/min + 30 concurrent, pay-per-call model, live vs standard cost tiers, `limit`/`filters` capping, `402`/`429` handling, backoff template.
- `references/api-surface-map.md` — routing table grouped by surface (Labs / SERP / Keywords Data / Backlinks / On-Page / AI Optimization / Merchant) with `mcp__dataforseo__*` tool names, parameter resolution, decision tree, and the stateless companion-routing table.
- `references/integration-patterns.md` — five canonical recipes copy-paste-ready: weekly report, rank tracker on scheduled SERP pulls, content-brief pipeline, backlink monitor, keyword research bulk job.
