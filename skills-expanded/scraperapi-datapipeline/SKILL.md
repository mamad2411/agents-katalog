---
name: scraperapi-datapipeline
description: >
  Product-usage reference for ScraperAPI's DataPipeline — managed, scheduled scraping projects
  that run automatically and deliver results to a webhook or dashboard download.
  Consult when the user needs recurring scraping, has a large list of URLs/ASINs/queries to process,
  or wants to avoid building and maintaining their own scraping infrastructure.
  Use when user asks: "schedule recurring scraping with ScraperAPI", "ScraperAPI DataPipeline",
  "how do I run a scraping project on a schedule", "scrape 10000 ASINs automatically",
  "ScraperAPI managed scraping project", "set up a ScraperAPI pipeline",
  "deliver scraping results to a webhook automatically". Covers project types, input methods,
  scheduling, output delivery, the DataPipeline API, job management, and credit costs.

  Note: Transmits user-supplied queries, URLs, and content to ScraperAPI.
metadata:
  openclaw:
    requires:
      env:
        - SCRAPERAPI_API_KEY
    emoji: "🔄"
    homepage: https://docs.scraperapi.com/data-pipeline
---

# ScraperAPI DataPipeline

DataPipeline is a managed scraping product. You define a project (what to scrape, how often,
where to send results), and ScraperAPI runs it on your schedule without you managing proxies,
retries, or infrastructure.

## When NOT to use DataPipeline

- **One-off scrapes of a known URL list** → use the [Async API](https://docs.scraperapi.com/making-async-requests) — faster, cheaper, no project setup.
- **Exploring a site without known URLs** → use the [Crawler](https://docs.scraperapi.com/crawler).
- **Need results in real-time within your code** → Async API is programmable; DataPipeline is scheduled.
- **Free plan, need recurring execution** → recurring schedules require a paid plan.

Use DataPipeline when: scraping runs on a fixed schedule, the input list is large (up to 100,000
items), results should flow to a webhook automatically, or you want email notifications on job
completion.

## Base URL and Auth

```
Base URL: https://datapipeline.scraperapi.com/api
Auth:     ?api_key=YOUR_KEY  (query parameter on every request)
```

## Project Types

Set `projectType` in the create request to choose what to scrape:

| Type | Input |
|------|-------|
| `urls` | Raw HTML from any URL |
| `urls_with_js` | Same but with JavaScript rendering |
| `google_search` | Search queries |
| `google_news` | Search queries |
| `google_jobs` | Search queries |
| `google_shopping` | Search queries |
| `google_maps` | Search queries |
| `amazon_product` | ASINs |
| `amazon_search` | Search queries |
| `amazon_offers` | ASINs |
| `walmart_product` | Product IDs |
| `walmart_search` | Search queries |
| `walmart_category` | Category IDs |
| `walmart_reviews` | Product IDs |
| `ebay_product` | 12-digit product IDs |
| `ebay_search` | Search queries |
| `redfin_listing_for_sale` | Listing URLs |
| `redfin_listing_for_rent` | Listing URLs |
| `redfin_listing_search` | Search result URLs |
| `redfin_agent_details` | Agent profile URLs |

## Creating a Project

```python
import os, requests

API_KEY = os.environ["SCRAPERAPI_API_KEY"]
BASE    = "https://datapipeline.scraperapi.com/api"

project = requests.post(
    f"{BASE}/projects",
    params={"api_key": API_KEY},
    json={
        "name":               "Weekly Amazon price monitor",
        "projectType":        "amazon_product",
        "schedulingEnabled":  True,
        "scrapingInterval":   "weekly",
        "scheduledAt":        "now",
        "projectInput": {
            "type": "list",
            "list": ["B09V3KXJPB", "B08N5WRWNW"]   # ASINs
        },
        "apiParams": {
            "country_code": "us"
        },
        "webhookOutput": {
            "url":             "https://yourapp.com/pipeline-results",
            "webhookEncoding": "multipart_form_data_encoding"
        },
        "notificationConfig": {
            "notifyOnSuccess": "with_every_run",
            "notifyOnFailure": "with_every_run"
        }
    }
).json()

print(f"Project created: id={project['id']}")
```

### Create request fields

| Field | Required | Description |
|-------|----------|-------------|
| `name` | No | Human-readable project name |
| `projectType` | Yes | What to scrape (see table above) |
| `schedulingEnabled` | No | `true` to enable recurring schedule |
| `scrapingInterval` | Yes (if scheduled) | See scheduling options below |
| `scheduledAt` | No | `"now"` to run immediately on create |
| `projectInput` | Yes | Input data (see input methods below) |
| `apiParams` | No | Standard ScraperAPI parameters |
| `webhookOutput` | No | Webhook delivery config |
| `notificationConfig` | No | Email notification settings |

## Input Methods

### Direct list (up to 500 items)

```json
{
  "projectInput": {
    "type": "list",
    "list": ["query one", "query two", "B09V3KXJPB"]
  }
}
```

### CSV file (up to 100,000 items)

Upload a CSV with one URL/query/ASIN per line — no header rows, no commas. Do this through the
[dashboard](https://dashboard.scraperapi.com/projects) when creating a project; the API accepts
list inputs only.

### Webhook input (dynamic polling)

```json
{
  "projectInput": {
    "type": "webhook",
    "webhookUrl": "https://yourapp.com/input-items"
  }
}
```

ScraperAPI polls your webhook URL for the item list when the job starts. One item per line;
no commas. Useful for dynamically generated lists (e.g., new ASINs added since the last run).

## Scheduling Options

| `scrapingInterval` | Description |
|-------------------|-------------|
| `"once"` | Run a single job immediately |
| `"hourly"` | Every hour |
| `"daily"` | Once per day |
| `"weekly"` | Once per week |
| `"monthly"` | Once per month |
| `"cron"` | Custom cron expression (use `cron` field instead of `interval`) |

Recurring schedules (`hourly`, `daily`, `weekly`, `monthly`, `cron`) require a paid plan.

Set `"scheduledAt": "now"` to trigger the first run immediately when the project is created.

## Output / Delivery

### Webhook delivery

Results are POSTed to your webhook URL as they complete. The `webhookEncoding` field controls
the format:

```json
{
  "webhookOutput": {
    "url":             "https://yourapp.com/results",
    "webhookEncoding": "multipart_form_data_encoding"
  }
}
```

### Dashboard download

Omit `webhookOutput` and results are saved for download in the
[DataPipeline dashboard](https://dashboard.scraperapi.com/projects). Results are retained for
**30 days** then automatically deleted.

Output formats by project type:
- `urls` / `urls_with_js` → HTML wrapped in JSONL
- Structured types (Amazon, Google, Walmart, eBay, Redfin) → JSON or CSV

## Managing Projects

```python
# List all projects
projects = requests.get(f"{BASE}/projects", params={"api_key": API_KEY}).json()

# Get a single project
project = requests.get(f"{BASE}/projects/525", params={"api_key": API_KEY}).json()

# Update (partial update — only include fields to change)
requests.patch(
    f"{BASE}/projects/525",
    params={"api_key": API_KEY},
    json={
        "scrapingInterval": "daily",
        "apiParams":        {"premium": True},
        "notificationConfig": {"notifyOnSuccess": "never"}
    }
)

# Delete / archive (irreversible without support)
requests.delete(f"{BASE}/projects/525", params={"api_key": API_KEY})
```

Updatable fields: `scrapingInterval`, `scheduledAt`, `outputFormat`, `apiParams`, `notificationConfig`.

## Managing Jobs

```python
# List jobs for a project
jobs = requests.get(
    f"{BASE}/projects/525/jobs",
    params={"api_key": API_KEY}
).json()

# Cancel a running job
requests.delete(
    f"{BASE}/projects/525/jobs/{job_id}",
    params={"api_key": API_KEY}
)
# Running requests within the job finish first; final status becomes "Cancelled"
```

A new job can only start if no other job for that project is currently running.

## Notification Config

```json
{
  "notificationConfig": {
    "notifyOnSuccess": "with_every_run",
    "notifyOnFailure": "with_every_run"
  }
}
```

Options for both fields: `"never"`, `"with_every_run"`, `"daily"`, `"weekly"`.

## `apiParams` Reference

All standard ScraperAPI parameters are supported inside `apiParams`:

| Parameter | Purpose |
|-----------|---------|
| `country_code` | Geotarget (e.g. `"us"`, `"gb"`) |
| `render` | JavaScript rendering |
| `premium` | Premium residential proxies |
| `ultra_premium` | Ultra-premium proxies (mutually exclusive with `premium`) |
| `device_type` | `"desktop"` or `"mobile"` |
| `output_format` | `"text"` or `"markdown"` for LLM pipelines |
| `autoparse` | Structured JSON extraction for supported sites |
| `keep_headers` | Forward custom headers |
| `follow_redirect` | Control redirect handling |
| `wait_for_selector` | Wait for CSS selector (requires `render: true`) |
| `screenshot` | Capture screenshot (auto-enables rendering) |
| `retry_404` | Retry 404 responses |

## Credit Costs

DataPipeline uses the same underlying credit rates as the Standard API. Cost is the sum of all
requests in a job run. Preview the estimated cost before launching a project from the dashboard.

Only successful `200` and `404` responses are charged; failed requests are not.

## Limits

| Limit | Value |
|-------|-------|
| Max input items | 100,000 per job |
| Direct list input | 500 items |
| Data retention | 30 days |
| Free plan concurrency | 5 connections |
| Free plan scheduling | One-time runs only |

## Documentation

- [DataPipeline overview](https://docs.scraperapi.com/data-pipeline)
- [Dashboard — manage projects](https://dashboard.scraperapi.com/projects)
- [API reference](https://docs.scraperapi.com/data-pipeline/api-reference)
