---
name: follow-tool-openseo
description: OpenSEO (every-app/open-seo) — MIT self-hosted SEO platform, MCP + agent skills, BYO DataForSEO
argument-hint: "[workflow: keyword-research|rank-tracking|backlinks|site-audit|ai-visibility]"
related:
  - follow-my-techstack
  - deep-research
  - create-cloudflare
  - follow-service-cloudflare
  - open-web-for-config-secret
---

## Goal

Run SEO work (keyword research, rank tracking, competitor insights, backlinks, site audits, AI visibility) with OpenSEO (MIT, `every-app/open-seo`) — an open-source Semrush/Ahrefs alternative you self-host, expose to agents over MCP, and pay only usage-based DataForSEO costs — no subscription

## Scope

Use when a project needs real SEO data + agent workflows without a paid suite — the catalog `SEO Platform` entry

- Self-host: Docker (simple, personal) or Cloudflare (recommended, internet-facing, works on free plan) — hosted app.openseo.so ($10/mo) is optional, not the default here
- Data requires a BYO DataForSEO API key (pay-per-use to DataForSEO directly) — there is no free data source
- Static on-page review (meta, structured data, robots) can start with `/follow-tool-lighthouse`-style audits; OpenSEO adds market data

## Execute

### 1. Self-Host

> Goal: get your own instance running

1. Clone `every-app/open-seo`; read `docs/SELF_HOSTING_DOCKER.md` (quick) or `docs/SELF_HOSTING_CLOUDFLARE.md` (multi-device/team — preferred; deploy via `/follow-service-cloudflare` + `/create-cloudflare`)
2. Create a DataForSEO API key — see `docs/DATAFORSEO_API_KEY.md`; open the signup page via `/open-web-for-config-secret` and let the user fill credentials
3. Put the key in env/secret store only (`.env` git-ignored, `/follow-secret-manager` default) — never commit it (`/check-secrets`)

### 2. Connect Your Agent (MCP)

> Goal: the coding agent queries SEO data directly

1. Follow `openseo.so/docs/agent-setup` to register the OpenSEO MCP server with the agent
2. For Devin: register via `/create-devin-global-mcp` pointing at your self-hosted instance
3. Install the pre-built agent skills or build focused ones (`/seo-audit`, `/keyword-research`, `/competitor-analysis`, `/seo-coach`)

### 3. Run A Workflow

> Goal: answers saved as reports, not chat noise

1. Keyword research: seed topic → volume/KD/intent + live SERPs → cluster and save keywords to the workspace
2. Rank tracking: add tracked keywords/competitors; review position deltas over time
3. Site audit: crawl target pages, surface technical issues with file-level evidence → route fixes through `/improve seo` / `/deep-review-codebase-then-fix`
4. AI visibility: review AI mentions/citations/prompts for the brand
5. Every agent run persists as an OpenSEO report — share the link instead of pasting tables

### 4. Keep Costs Honest

> Goal: usage-based, not subscription-based

1. Self-hosted cost = raw DataForSEO usage (the hosted product adds ~28% margin — self-hosting is cheaper per request)
2. Budget check before large crawls/rank sweeps: estimate DataForSEO request counts first; report-only when the user hasn't approved spend

## Rules

### 1. Your Data, Your Instance

- Prefer the self-hosted path; connect the hosted service only on explicit request — API keys stay in secrets managers, out of repos and logs

### 2. SEO Fixes Land In Code

- Findings are not done until applied: technical audit items → `/fix` with evidence; content/keyword outputs feed the project docs/plan via `/create-plan-in-dot-devin` when bulk work follows

### 3. No Invented Metrics

- Quote volumes/difficulty/positions only from OpenSEO/DataForSEO output — never estimate "high search volume" without a fetched number

## Expected Outcome

- A self-owned SEO stack (MIT code, BYO usage-priced data, no lock-in subscription)
- Agent workflows (keyword research, audits, tracking) reproducible through MCP + skills
- Every audit surfaced as a verified, shareable report with code fixes tracked in the repo
