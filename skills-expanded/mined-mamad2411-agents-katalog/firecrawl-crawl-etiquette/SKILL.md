---
name: firecrawl-crawl-etiquette
description: Choose between scrape, map, crawl, and search, keep Firecrawl credit costs under control, and crawl politely (limits, depth, robots). Use before starting any multi-page Firecrawl job.
---

# Firecrawl Etiquette and Cost Control

## Pick the cheapest tool that answers the question

| Need | Use | Why |
|---|---|---|
| Content of known URL(s) | `/v2/scrape` (batch the list) | 1 page = 1 unit of work, no discovery overhead |
| List of URLs on a site | `/v2/map` | Returns thousands of links fast without scraping any of them |
| "Everything under /docs" | `/v2/map` then scrape the filtered list, or `/v2/crawl` with `includePaths` | Map+scrape gives you an exact budget before spending it |
| Answers from the open web | `/v2/search` (optionally with `scrapeOptions`) | One call replaces search-then-scrape loops |
| Structured fields across pages | `/v2/extract` with a schema | LLM extraction beats scraping everything and parsing later |

Crawl is the most expensive primitive: it discovers, queues, and scrapes.
Reach for it only when you genuinely do not know the URL set in advance.

## Bound every crawl

Never start an unbounded crawl. Defaults are generous (`limit` 10000), so
set your own:

- `limit`: hard page cap. Start at 20 to 100, raise only after inspecting
  results.
- `maxDiscoveryDepth`: 1 or 2 catches most doc sites.
- `includePaths` / `excludePaths` (regex on pathname): scope to the section
  you need; exclude `/tag/`, `/page/`, locale duplicates, print views.
- Leave `crawlEntireDomain`, `allowSubdomains`, `allowExternalLinks` off
  unless you have a reason; each multiplies the frontier.

Dry-run pattern: `/v2/map` first, count the links matching your filters,
then crawl with `limit` set just above that count.

## Cost levers

- **Cache first**: `maxAge` on scrape (default 2 days) serves cached copies
  and costs less time; only force `maxAge: 0` when freshness matters.
- **Formats**: request only what you consume. `markdown` alone is the
  cheapest useful output; screenshots, `json` format, and `actions` add
  latency and cost.
- **`onlyMainContent: true`** (default): smaller payloads, fewer tokens
  downstream.
- Watch `creditsUsed` in search responses and the dashboard usage page; a
  `402` mid-job means credits ran out.

## Politeness and legality

- Respect robots.txt and site terms; do not crawl paywalled or
  login-gated content you are not entitled to. Use `actions` for pages you
  legitimately have access to, not to evade access controls.
- Keep crawl `limit` and concurrency modest on small sites; hammering a
  hobby server is bad citizenship even when it is technically possible.
- Identify a contact or slow down if a site returns rising 429/503 rates.
- Cache aggressively instead of re-crawling the same site on a loop; for
  standing freshness needs, schedule small incremental crawls rather than
  full re-crawls.

## Failure handling

- `429`: exponential backoff, then resume. Crawl jobs are async; poll
  `GET /v2/crawl/{id}` instead of restarting the job (restarts double the
  spend).
- Partial results are normal: check per-page `metadata.statusCode` and
  re-scrape only the failures.
