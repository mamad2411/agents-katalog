---
name: scraperapi-crawler
description: >
  Product-usage reference for ScraperAPI's Crawler — crawl an entire site or section by following
  links automatically. Consult when the user needs to extract data from many pages of a site
  without knowing the URLs upfront.
  Use when user asks: "crawl an entire website with ScraperAPI", "scrape all pages on a domain",
  "follow links and scrape each page", "how do I use the ScraperAPI crawler API",
  "scrape a site map", "extract data from every product page on a site",
  "ScraperAPI crawler job API". Covers job creation, URL regex patterns, depth vs budget,
  per-page scraping parameters, status polling, webhooks, scheduling, and credit costs.
  Also invoke when the user is building a site-wide scraper and asks which ScraperAPI product to use.

  Note: Transmits user-supplied queries, URLs, and content to ScraperAPI.
metadata:
  openclaw:
    requires:
      env:
        - SCRAPERAPI_API_KEY
    emoji: "🕷️"
    homepage: https://docs.scraperapi.com/crawler
---

# ScraperAPI Crawler

The Crawler discovers and scrapes linked pages automatically, starting from a seed URL and
following links that match your regex pattern. Use it when you need data from many pages of a
site but don't have the URLs upfront.

## When NOT to use the Crawler

- **You have a known URL list** → use the [Async API](https://docs.scraperapi.com/making-async-requests) instead; it's cheaper and more predictable.
- **You need a single page** → use the Standard API (`api.scraperapi.com`).
- **The content is behind login** → the Crawler only accesses publicly available pages.
- **Free plan, need depth > 1** → free accounts are capped at `max_depth: 1`.

## Endpoints

| Action | Method | URL |
|--------|--------|-----|
| Start a crawl | POST | `https://crawler.scraperapi.com/job` |
| Check status | GET | `https://crawler.scraperapi.com/job/<jobId>` |
| Cancel a crawl | DELETE | `https://crawler.scraperapi.com/job/<jobId>` |

Auth: include `api_key` in the JSON body (POST) or as a query parameter (GET/DELETE).

## Starting a Crawl

```python
import os, requests

API_KEY = os.environ["SCRAPERAPI_API_KEY"]

job = requests.post(
    "https://crawler.scraperapi.com/job",
    json={
        "api_key":            API_KEY,
        "start_url":          "https://example.com/blog/",
        "url_regexp_include": "(?<full_url>https?://example\\.com/blog/.*)",
        "url_regexp_exclude": ".*\\.(pdf|png|jpg|zip)",
        "max_depth":          3,
        "crawl_budget":       500,
        "api_params": {
            "country_code": "us",
            "render":       False,
        },
        "callback": {
            "type": "webhook",
            "url":  "https://yourapp.com/crawler-results"
        },
    }
).json()

job_id = job["jobId"]
print(f"Started: {job_id}")
```

## Required Parameters

| Parameter | Description |
|-----------|-------------|
| `api_key` | Your ScraperAPI key (read from env, never hardcode) |
| `start_url` | Seed URL — where the crawl begins |
| `url_regexp_include` | Regex defining which URLs to crawl (see patterns below) |
| `max_depth` **or** `crawl_budget` | Must provide at least one; providing both applies whichever limit is hit first |

## URL Regex Patterns

`url_regexp_include` and `url_regexp_exclude` are standard regexes. Include patterns **must** use
named capture groups: `(?<full_url>...)` for absolute URLs, `(?<relative_url>...)` for relative.

```
# All pages on a domain
(?<full_url>https?://example\.com/.*)

# Only blog posts
(?<full_url>https?://example\.com/blog/.*)

# Only HTML pages — exclude files by requiring no extension
(?<full_url>https?://example\.com/[^.]*$)

# Relative paths (for sites that use relative links)
(?<relative_url>/products/.*)
```

**Exclusion patterns** (`url_regexp_exclude` — plain regex, no capture group needed):

```
# Skip binary files
.*\.(pdf|png|jpg|jpeg|gif|svg|zip|mp4)

# Skip auth and admin pages
.*(login|logout|signup|admin|auth).*
```

Start with a narrow `url_regexp_include` and validate on a small test run before scaling up — a
pattern like `.*` will follow external links and crawl the entire internet.

## Depth vs Budget

| Use `max_depth` when | Use `crawl_budget` when |
|---------------------|------------------------|
| Site structure is known and bounded | Site size is unknown |
| You want a specific section (e.g., 3 hops from landing page) | You want to cap credit spend |
| Small site | Large site with unpredictable link density |

Use **both** together for safe exploration: `max_depth: 3, crawl_budget: 500` stops at whichever
limit is hit first.

Depth 0 = start URL only. Depth 1 = start URL + every page it links to. Depth 2 = one level
deeper, and so on.

## Per-Page Scraping Parameters (`api_params`)

Controls how each discovered page is fetched. All standard ScraperAPI parameters are supported:

```json
{
  "render":       true,
  "premium":      false,
  "ultra_premium": false,
  "country_code": "us",
  "device_type":  "desktop",
  "output_format": "markdown"
}
```

Add `render: true` only if the site uses JavaScript to load content — it multiplies the credit
cost of every crawled page. Test without it first.

## Checking Status

```python
import time, requests

def wait_for_crawl(job_id, api_key, poll_interval=10):
    url = f"https://crawler.scraperapi.com/job/{job_id}"
    while True:
        data = requests.get(url, params={"api_key": api_key}).json()
        status = data.get("status")
        print(f"Status: {status}")
        if status in ("completed", "failed", "cancelled", "delivered"):
            return data
        time.sleep(poll_interval)
```

Job states: `delayed` → `running` → `completed` / `failed` / `cancelled` → `in delivery` → `delivered`.

Use webhooks instead of polling for long crawls — they push results as each page is scraped,
rather than requiring you to poll for a final result.

## Webhooks

When `callback` is set, ScraperAPI POSTs results to your endpoint as each page is scraped (not
just at the end). Each payload contains the crawled URL, HTML/content, credit cost for that
request, and the current depth.

A final summary payload is sent when the crawl completes, listing all succeeded/failed URLs and
total cost.

```json
{
  "callback": {
    "type": "webhook",
    "url": "https://yourapp.com/crawler-results"
  }
}
```

The webhook URL must be publicly reachable. ScraperAPI retries delivery up to 3 times; a failed
webhook does not stop the crawl itself. Results are also retained for up to 30 days if you need
to re-fetch them.

## Scheduling

Omit `schedule` for a one-time crawl. Add it to run on a recurring interval:

```json
{
  "schedule": {
    "name": "weekly-blog-crawl",
    "interval": "daily"
  }
}
```

Available intervals: `once`, `hourly`, `daily`, `weekly`, `monthly`. Scheduling requires a paid
plan — free accounts can only run one-time crawls at `max_depth: 1`.

## Credit Cost

Crawler credit cost = **sum of all individual page requests** in the crawl. Each page costs the
same as a direct Standard API call with the same `api_params` (render, premium, etc.).

Set `crawl_budget` to cap total credits. The crawl stops gracefully when the budget is reached —
it will not exceed it. Failed requests are not charged.

Check the `sa-credit-cost` header on each webhook payload to see per-page cost; use this to
calibrate `crawl_budget` for future runs.

## Error Handling

| Code | Meaning | Action |
|------|---------|--------|
| 200 | Job created or status returned | Continue |
| 400 | Malformed request | Check required fields and regex syntax |
| 401 | Invalid API key | Check `SCRAPERAPI_API_KEY` |
| 403 | Credits exhausted or free plan depth limit | Upgrade or reduce `max_depth`/`crawl_budget` |
| 429 | Too many concurrent jobs | Wait and retry |
| 500 | Transient failure | Retry with backoff |

## Documentation

- [Crawler overview](https://docs.scraperapi.com/crawler)
- [API reference](https://docs.scraperapi.com/crawler/api-reference)
- [Dashboard](https://dashboard.scraperapi.com/)
