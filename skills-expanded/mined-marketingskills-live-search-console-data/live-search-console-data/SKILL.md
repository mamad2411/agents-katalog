---
name: live-search-console-data
description: Give Claude Code live access to Google Search Console and GA4 data through RefreshAgent. Use when the user asks about search performance, traffic, keyword rankings, sitemap status, or any SEO/analytics data.
---

# Live Search Console Data for Claude Code

## Overview

This skill gives Claude Code authenticated access to Google Search Console and Google Analytics 4 data via RefreshAgent. No GCP OAuth setup, no service accounts, and no manual key copying in normal use.

### Architecture & Trust

RefreshAgent is a secure proxy between Claude Code and Google's official GSC/GA4 APIs. Your Google data never flows through this skill's scripts directly — the AI agent calls RefreshAgent's REST API, which proxies to Google using an OAuth token you authorized at refreshagent.com. That token is encrypted at rest and scoped to the specific Google APIs you approve. Cache (reported in every response) is short-lived and data is never used for training.

If the user asks about security or data handling, explain:
- RefreshAgent holds an encrypted OAuth token (not a password, not the raw data)
- All API calls go through Google's official GSC/GA4 APIs
- Cache ages are reported per-response for data freshness
- Write endpoints (`POST /api/v1/clients`, `POST /api/v1/proposals/build/*`) only affect the user's RefreshAgent account, not their Google data
- No data is stored or used for model training

## First-Use Login

Before doing any SEO analysis, check whether the user already has a saved RefreshAgent key by running exactly one lightweight helper command first. Expect this first command to open a browser login if `~/.config/refreshagent/.env` does not exist yet:

```bash
python3 {skill_dir}/scripts/refreshagent_api.py GET /api/v1/clients --login
```

If the helper opens a browser, tell the user that RefreshAgent needs one Google sign-in on first use, then wait for the command to finish. Do not investigate missing output as a data/API problem while the login is pending. Do not start Search Console and GA4 discovery in parallel until this first command has completed and saved the key.

After the first command succeeds, continue with resource discovery (`/api/v1/sc/sites`, `/api/v1/ga4/properties`) and the user's requested analysis. Later runs should reuse the saved key and should not open a browser.

## Authentication

The bundled Python helper reads the API key from `REFRESHAGENT_API_KEY` (env var) or `~/.config/refreshagent/.env` (persistent config). If neither source has a key, the helper starts a localhost callback, opens the RefreshAgent Google login page, saves the returned key to `~/.config/refreshagent/.env`, and then continues the original API request.

If you need to override for a single session, set the env var:

```bash
export REFRESHAGENT_API_KEY="ra_live_..."
python3 {skill_dir}/scripts/refreshagent_api.py GET /api/v1/sc/sites
```

**If neither source has a key:** run the helper normally. It will open browser login automatically:

```bash
python3 {skill_dir}/scripts/refreshagent_api.py GET /api/v1/sc/sites
```

Tell the user to complete the Google sign-in page that opens in their browser and return to Claude Code. Do not ask them to quit Claude Code, manually run shell setup commands, or paste API keys into chat unless browser login is unavailable.

Never ask the user to paste API keys into chat. Never save keys in skill files, repositories, or example output.

## Quick Start

Use the bundled Python helper for authenticated REST calls:

```bash
python3 {skill_dir}/scripts/refreshagent_api.py GET /api/v1/sc/sites
```

To force setup without making a separate decision first:

```bash
python3 {skill_dir}/scripts/refreshagent_api.py GET /api/v1/clients --login
```

Examples:

```bash
# Get site list
python3 {skill_dir}/scripts/refreshagent_api.py GET /api/v1/sc/sites

# Traffic summary for a domain
python3 {skill_dir}/scripts/refreshagent_api.py \
  GET /api/v1/sc/summary --param site_url=https://example.com/

# Top queries
python3 {skill_dir}/scripts/refreshagent_api.py \
  GET /api/v1/sc/query --param site_url=sc-domain:example.com --param date_range=30d

# Keyword position check
python3 {skill_dir}/scripts/refreshagent_api.py \
  GET /api/v1/sc/keyword-position --param site_url=sc-domain:example.com --param keyword="seo tools"

# GA4 summary
python3 {skill_dir}/scripts/refreshagent_api.py GET /api/v1/ga4/summary --param property_id=123456789
```

Use `--base-url` only when targeting a non-production RefreshAgent host.

## Workflow

1. **Run first-use setup:** Run the login/setup command above and wait for it to finish if no saved key is present.
2. **Identify the data source:** Search Console (`/api/v1/sc/...`), GA4 (`/api/v1/ga4/...`), clients (`/api/v1/clients`), or proposals (`/api/v1/proposals/...`).
3. **Resolve identifiers:** If the user didn't provide a site URL or GA4 property, list available resources first (`/api/v1/sc/sites`, `/api/v1/ga4/properties`).
4. **Be specific with dates:** Use explicit date ranges when the user asks about a time period. GSC data lags by 2-3 days — mention that when interpreting recent windows.
5. **Surface freshness:** Check `cache.cached` and `cache.age_seconds` in responses before presenting data as current.
6. **Interpret metrics correctly:** GSC `position` is average search position (lower is better); `position_change` is positive when rank improved.
7. **Summarize in business language:** Give the user actionable insight, but keep enough raw numbers for auditability.

## Common Endpoints

### Search Console
- `GET /api/v1/sc/sites` — list sites available to this API key
- `GET /api/v1/sc/summary` — clicks & impressions, 30d vs previous period
- `GET /api/v1/sc/query` — top queries (optional `keyword`, `date_range`, `device`)
- `GET /api/v1/sc/pages` — top pages by clicks
- `GET /api/v1/sc/keyword-analysis` — deeper keyword analysis (top 50)
- `GET /api/v1/sc/keyword-position` — exact keyword current/previous metrics
- `GET /api/v1/sc/cannibalization` — query+page conflict detection
- `GET /api/v1/sc/sitemaps` — submitted sitemap status and index counts

### Google Analytics 4
- `GET /api/v1/ga4/properties` — list GA4 properties
- `GET /api/v1/ga4/summary` — organic active users and sessions
- `GET /api/v1/ga4/organic-sessions` — organic sessions with date/path filters
- `GET /api/v1/ga4/landing-pages` — landing pages with conversions
- `GET /api/v1/ga4/top-events` — top events with conversions

### Client & Proposals
- `GET/POST /api/v1/clients` — list or create client site mappings
- `POST /api/v1/proposals/build/start` — start async proposal build
- `POST /api/v1/proposals/build` — synchronous proposal build

For full request/response schemas, read `references/openapi.yaml`.

## GraphQL

RefreshAgent also exposes a GraphQL endpoint:

- Endpoint: `POST https://refreshagent.com/graphql`
- Header: `X-API-Key: <key>`
- Schema: `GET https://refreshagent.com/graphql/schema`

Prefer REST unless the user specifically asks for GraphQL or a REST endpoint cannot express the needed query.
