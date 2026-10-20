---
name: claude-seo-google
description: >
  Google SEO APIs: Search Console (Search Analytics, URL Inspection, Sitemaps),
  PageSpeed Insights v5, CrUX field data with 25-week history, Indexing API v3,
  and GA4 organic traffic. Provides real Google field data for Core Web Vitals,
  indexation status, search performance, and organic traffic trends. Use when
  user says "search console", "GSC", "PageSpeed", "CrUX", "field data",
  "indexing API", "GA4 organic", "URL inspection", "google api setup",
  "real CWV data", "impressions", "clicks", "CTR", "position data",
  "LCP", "INP", "CLS", "FCP", "TTFB", or "Lighthouse scores".
license: MIT
metadata:
  author: AgriciDaniel
  version: "2.2.0"
  category: seo
---

> **Nota per Kimi Code:** questa skill è convertita dal plugin Claude Code `claude-seo`. I comandi slash (`/seo ...`) non sono disponibili; descrivi semplicemente in linguaggio naturale cosa vuoi analizzare. Gli script sono in `~/.kimi/skills/claude-seo/scripts/`.



# Google SEO APIs

Direct access to Google's own SEO data. Bridges the gap between crawl-based
analysis (existing claude-seo skills) and Google's real-time field data: actual
Chrome user metrics, real indexation status, search performance, and organic traffic.

All APIs are free. Setup requires a Google Cloud project with API key and/or
service account -- run `google setup` for step-by-step instructions.

## Prerequisites

Before executing any command, check credentials:
```bash
~/.kimi/skills/claude-seo/.venv/bin/python ~/.kimi/skills/claude-seo/scripts/google_auth.py --check --json
```

Config file: `~/.config/claude-seo/google-api.json`
```json
{
  "service_account_path": "/path/to/service_account.json",
  "api_key": "<GOOGLE_API_KEY>",
  "default_property": "sc-domain:example.com",
  "ga4_property_id": "properties/123456789"
}
```

If missing, read `references/auth-setup.md` and walk the user through setup.

### Credential Tiers

| Tier | Detection | Available Commands |
|------|-----------|-------------------|
| **0** (API Key) | `api_key` present | `pagespeed`, `crux`, `crux-history`, `youtube`, `nlp` |
| **1** (OAuth/SA) | + OAuth token or service account | Tier 0 + `gsc`, `inspect`, `sitemaps`, `index` |
| **2** (Full) | + `ga4_property_id` configured | Tier 1 + `ga4`, `ga4-pages` |
| **3** (Ads) | + `ads_developer_token` + `ads_customer_id` | Tier 2 + `keywords`, `volume` |

Always communicate the detected tier before running commands.

## Quick Reference

| Command | What it does | Tier |
|---------|-------------|------|
| `google setup` | Check/configure API credentials | -- |
| `google pagespeed <url>` | PSI Lighthouse + CrUX field data | 0 |
| `google crux <url>` | CrUX field data only (p75 metrics) | 0 |
| `google crux-history <url>` | 25-week CWV trend analysis | 0 |
| `google gsc <property>` | Search Console: clicks, impressions, CTR, position | 1 |
| `google inspect <url>` | URL Inspection: index status, canonical, crawl info | 1 |
| `google inspect-batch <file>` | Batch URL Inspection from file | 1 |
| `google sitemaps <property>` | GSC sitemap status | 1 |
| `google index <url>` | Submit URL to Indexing API | 1 |
| `google index-batch <file>` | Batch submit up to 200 URLs | 1 |
| `google ga4 [property-id]` | GA4 organic traffic report | 2 |
| `google ga4-pages [property-id]` | Top organic landing pages | 2 |
| `google youtube <query>` | YouTube video search (views, likes, duration) | 0 |
| `google youtube-video <id>` | YouTube video details + top comments | 0 |
| `google nlp <url-or-text>` | NLP entity extraction + sentiment + classification | 0 |
| `google entities <url-or-text>` | Entity analysis only (for E-E-A-T) | 0 |
| `google keywords <seed>` | Keyword ideas from Google Ads Keyword Planner | 3 |
| `google volume <keywords>` | Search volume lookup from Keyword Planner | 3 |
| `google entity <query>` | Knowledge Graph entity check | 0 |
| `google safety <url>` | Web Risk URL safety check | 0 |
| `google quotas` | Show rate limits for all APIs | -- |

---

## PageSpeed + CrUX

### `google pagespeed <url>`

Combined Lighthouse lab data + CrUX field data.

**Script:** `~/.kimi/skills/claude-seo/.venv/bin/python ~/.kimi/skills/claude-seo/scripts/pagespeed_check.py <url> --json`
**Reference:** `references/pagespeed-crux-api.md`
**Default:** Both mobile + desktop strategies, all Lighthouse categories.

Output merges lab scores (point-in-time Lighthouse) with field data (28-day
Chrome user metrics). CrUX tries URL-level first, falls back to origin-level.

### `google crux <url>`

CrUX field data only (no Lighthouse run). Faster.

**Script:** `~/.kimi/skills/claude-seo/.venv/bin/python ~/.kimi/skills/claude-seo/scripts/pagespeed_check.py <url> --crux-only --json`

### `google crux-history <url>`

25-week CrUX History trends. Shows whether CWV metrics are improving, stable, or degrading.

**Script:** `~/.kimi/skills/claude-seo/.venv/bin/python ~/.kimi/skills/claude-seo/scripts/crux_history.py <url> --json`
**Reference:** `references/pagespeed-crux-api.md`

Output includes per-metric trend direction, percentage change, and weekly p75 values.

---

## Search Console

### `google gsc <property>`

Search Analytics: clicks, impressions, CTR, position for last 28 days.

**Script:** `~/.kimi/skills/claude-seo/.venv/bin/python ~/.kimi/skills/claude-seo/scripts/gsc_query.py --property <property> --json`
**Reference:** `references/search-console-api.md`
**Default:** 28 days, dimensions=query,page, type=web, limit=1000.

Includes quick-win detection: queries at position 4-10 with high impressions.

### `google inspect <url>`

URL Inspection: real indexation status from Google.

**Script:** `~/.kimi/skills/claude-seo/.venv/bin/python ~/.kimi/skills/claude-seo/scripts/gsc_inspect.py <url> --json`

Returns: verdict (PASS/FAIL), coverage state, robots.txt status, indexing state,
page fetch state, canonical selection, mobile usability, rich results.

### `google inspect-batch <file>`

Batch inspection from a file (one URL per line). Rate limited to 2,000/day per site.

**Script:** `~/.kimi/skills/claude-seo/.venv/bin/python ~/.kimi/skills/claude-seo/scripts/gsc_inspect.py --batch <file> --json`

### `google sitemaps <property>`

List submitted sitemaps with status, errors, warnings. Sitemap contents report
submitted counts only; URL Inspection API is the indexation truth for whether
specific URLs are indexed.

**Script:** `~/.kimi/skills/claude-seo/.venv/bin/python ~/.kimi/skills/claude-seo/scripts/gsc_query.py sitemaps --property <property> --json`

---

## Indexing API

### `google index <url>`

Notify Google of a URL update.

**Script:** `~/.kimi/skills/claude-seo/.venv/bin/python ~/.kimi/skills/claude-seo/scripts/indexing_notify.py <url> --json`
**Reference:** `references/indexing-api.md`

The Indexing API is officially for JobPosting and BroadcastEvent/VideoObject pages.
Always inform the user of this restriction. Daily quota: 200 publish requests.

### `google index-batch <file>`

Batch submit URLs from a file. Tracks quota usage.

**Script:** `~/.kimi/skills/claude-seo/.venv/bin/python ~/.kimi/skills/claude-seo/scripts/indexing_notify.py --batch <file> --json`

---

## GA4 Traffic

### `google ga4 [property-id]`

Organic traffic report: daily sessions, users, pageviews, bounce rate, engagement.

**Script:** `~/.kimi/skills/claude-seo/.venv/bin/python ~/.kimi/skills/claude-seo/scripts/ga4_report.py --property <id> --json`
**Reference:** `references/ga4-data-api.md`
**Default:** 28 days, filtered to Organic Search channel group.

### `google ga4-pages [property-id]`

Top organic landing pages ranked by sessions.

**Script:** `~/.kimi/skills/claude-seo/.venv/bin/python ~/.kimi/skills/claude-seo/scripts/ga4_report.py --property <id> --report top-pages --json`

---

## YouTube (Video SEO)

YouTube mentions have the strongest AI visibility correlation (0.737). Free, API key only.

### `google youtube <query>`

Search YouTube for videos. Returns title, channel, views, likes, duration.

**Script:** `~/.kimi/skills/claude-seo/.venv/bin/python ~/.kimi/skills/claude-seo/scripts/youtube_search.py search "<query>" --json`
**Reference:** `references/youtube-api.md`
**Quota:** 100 units per search (10,000 units/day free).

### `google youtube-video <video_id>`

Detailed video info + tags + top 10 comments.

**Script:** `~/.kimi/skills/claude-seo/.venv/bin/python ~/.kimi/skills/claude-seo/scripts/youtube_search.py video <video_id> --json`
**Quota:** 2 units (video details + comments).

---

## NLP Content Analysis

Google's own entity/sentiment analysis. Enhances E-E-A-T scoring.

### `google nlp <url-or-text>`

Full NLP analysis: entities, sentiment, content classification.

**Script:** `~/.kimi/skills/claude-seo/.venv/bin/python ~/.kimi/skills/claude-seo/scripts/nlp_analyze.py --url <url> --json` or `--text "..."`
**Reference:** `references/nlp-api.md`
**Free tier:** 5,000 units/month. Requires billing enabled on GCP project.

### `google entities <url-or-text>`

Entity extraction only (faster, less quota).

**Script:** `~/.kimi/skills/claude-seo/.venv/bin/python ~/.kimi/skills/claude-seo/scripts/nlp_analyze.py --url <url> --features entities --json`

---

## Keyword Research (Google Ads)

Gold-standard keyword volume data. Requires Google Ads account.

### `google keywords <seed>`

Generate keyword ideas from seed terms.

**Script:** `~/.kimi/skills/claude-seo/.venv/bin/python ~/.kimi/skills/claude-seo/scripts/keyword_planner.py ideas "<seed>" --json`
**Reference:** `references/keyword-planner-api.md`
**Requires:** Ads developer token + customer ID in config (Tier 3).

### `google volume <keywords>`

Search volume for specific keywords (comma-separated).

**Script:** `~/.kimi/skills/claude-seo/.venv/bin/python ~/.kimi/skills/claude-seo/scripts/keyword_planner.py volume "<kw1>,<kw2>" --json`

---

## Supplementary

### `google entity <query>`

Knowledge Graph entity check. Verifies brand presence.

**Reference:** `references/supplementary-apis.md`
Uses Knowledge Graph Search API with API key.

### `google safety <url>`

Web Risk API check for malware/social engineering flags.

**Reference:** `references/supplementary-apis.md`

### `google quotas`

Display rate limits table. Read `references/rate-limits-quotas.md`.

---

## Reports

After any analysis command, offer to generate a PDF/HTML report.

### `google report <type>`

Generate a professional PDF report with charts and analytics.

**Script:** `~/.kimi/skills/claude-seo/.venv/bin/python ~/.kimi/skills/claude-seo/scripts/google_report.py --type <type> --data <json> --domain <domain> --format pdf`

| Type | Input | Output |
|------|-------|--------|
| `cwv-audit` | PSI + CrUX + CrUX History data | Core Web Vitals audit with gauges, timelines, distributions |
| `gsc-performance` | GSC query data | Search Console report with query tables, quick wins |
| `indexation` | Batch inspection data | Indexation status with coverage donut chart |
| `full` | All data combined | Comprehensive Google SEO report (all sections) |

**Workflow:**
1. Run data collection commands (pagespeed, gsc, inspect-batch, etc.)
2. Save JSON output to file: `~/.kimi/skills/claude-seo/.venv/bin/python ~/.kimi/skills/claude-seo/scripts/pagespeed_check.py <url> --json > data.json`
3. Generate report: `~/.kimi/skills/claude-seo/.venv/bin/python ~/.kimi/skills/claude-seo/scripts/google_report.py --type cwv-audit --data data.json --domain <domain>`

**Convention:** After completing analysis, suggest: "Generate a report? Use `google report <type>`"

---

## Rate Limits

| API | Per-Minute | Per-Day | Auth |
|-----|-----------|---------|------|
| PSI v5 | 240 QPM | 25,000 QPD | API Key |
| CrUX + History | 150 QPM (shared) | Unlimited | API Key |
| GSC Search Analytics | 1,200 QPM/site | 30M QPD | Service Account |
| GSC URL Inspection | 600 QPM | 2,000 QPD/site | Service Account |
| Indexing API | 380 RPM | 200 publish/day | Service Account |
| GA4 Data API | 10 concurrent | ~25K tokens/day | Service Account |

## Cross-Skill Integration

- **claude-seo-audit**: Spawns `claude-seo-google` agent for live CWV + indexation data (conditional)
- **claude-seo-technical**: Uses pagespeed_check.py for real CWV field data
- **claude-seo-performance**: CrUX field data supplements Lighthouse lab data
- **claude-seo-sitemap**: GSC sitemap status shows submitted counts, errors, and warnings; use URL Inspection for indexation truth
- **claude-seo-content**: GSC query data informs keyword targeting
- **claude-seo-geo**: GSC search appearance data includes AI Overview references

## Output Format

- CWV metrics: traffic-light rating (Good / Needs Improvement / Poor)
- Performance reports: tables with sortable columns
- Always include data freshness note
- Save reports as `GOOGLE-API-REPORT-{domain}.md`
- Use templates from `assets/templates/` for structured output

## Technical Notes

- INP replaced FID on March 12, 2024. Never reference FID.
- CLS values from CrUX are string-encoded (e.g., "0.05"). Scripts handle parsing.
- CrUX 404 = insufficient traffic, not an auth error.
- Search Analytics data has 2-3 day lag.
- `round_trip_time` replaced `effectiveConnectionType` in CrUX (Feb 2025).
- Custom Search JSON API is closed to new customers (2025).

## Error Handling

| Scenario | Action |
|----------|--------|
| No credentials configured | Run `google setup`. List Tier 0 commands that work with just an API key. |
| Service account lacks GSC access | Report error. Instruct: add `client_email` to GSC > Settings > Users > Add. |
| CrUX data unavailable (404) | Report insufficient Chrome traffic. Suggest PSI lab data as fallback. |
| GA4 property not found | Report error. Show how to find property ID in GA4 Admin > Property Details. |
| Indexing API quota exceeded | Report 200/day limit. Suggest prioritizing most important URLs. |
| Rate limit (429) | Wait and retry with exponential backoff. Report which API hit the limit. |
