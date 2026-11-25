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

- **One-off scrapes of a known URL list** → use the [Async API](https://docs.scraperapi.com/asynchronous-api) — faster, no project setup.
- **Exploring a site without known URLs** → use the [Crawler](https://docs.scraperapi.com/scraperapi-crawler-v2.0).
- **Need results in real-time within your code** → Async API is programmable; DataPipeline is scheduled.

Use DataPipeline when: scraping runs on a schedule, the input list is large (up to 100,000 items
per project), results should flow to a webhook automatically, or you want email notifications
about job runs.

## Base URL and Auth

```
Base URL: https://datapipeline.scraperapi.com/api
Auth:     ?api_key=YOUR_KEY  (query parameter on every request)
```

## Project Types

Set `projectType` in the create request to choose what to scrape. If you omit it, the project
type is `urls`.

| Type | Input |
|------|-------|
| `urls` | Any URLs (raw HTML). For JavaScript-heavy pages, add `"render": true` in `apiParams` |
| `google_search`, `google_news`, `google_jobs`, `google_shopping`, `google_maps_search` | Search queries |
| `google_ai_mode`, `google_gemini`, `chatgpt`, `perplexity` | See the [endpoints reference](https://docs.scraperapi.com/data-pipeline/datapipeline-endpoints/endpoints-and-parameters) |
| `amazon_product`, `amazon_offer` | ASINs |
| `amazon_search` | Search queries |
| `walmart_product`, `walmart_review` | Product IDs |
| `walmart_search` | Search queries |
| `walmart_category` | Category IDs |
| `ebay_product` | Product IDs |
| `ebay_search` | Search queries |
| `homedepot_product`, `homedepot_search`, `homedepot_reviews` | See the endpoints reference |
| `redfin_forsale`, `redfin_search`, `redfin_agent` | Redfin URLs |

The docs spell the Redfin rentals type as `refin_forrent`; if the API rejects it, contact support
rather than guessing. An unknown type fails with a 400:
`/projectType: must be equal to one of the allowed values`.

## Creating a Project

```python
import os, requests

API_KEY = os.environ["SCRAPERAPI_API_KEY"]
BASE    = "https://datapipeline.scraperapi.com/api"

resp = requests.post(
    f"{BASE}/projects",
    params={"api_key": API_KEY},
    json={
        "name":              "Weekly Amazon price monitor",
        "projectType":       "amazon_product",
        "schedulingEnabled": True,
        "scrapingInterval":  "weekly",
        "scheduledAt":       "now",
        "projectInput": {
            "type": "list",
            "list": ["B09V3KXJPB", "B08N5WRWNW"]   # ASINs
        },
        "apiParams": {
            "outputFormat": "csv"
        },
        "webhookOutput": {
            "url": "https://yourapp.com/pipeline-results"
        },
        "notificationConfig": {
            "notifyOnSuccess": "never",
            "notifyOnFailure": "with_every_run"
        }
    }
)
resp.raise_for_status()   # a 400 body names the field that failed validation
project = resp.json()
print(f"Project created: id={project['id']}")
```

The smallest valid project is just an input list; everything else has a default:

```json
{"projectInput": {"type": "list", "list": ["https://example.com/"]}}
```

### Create request fields

| Field | Description |
|-------|-------------|
| `projectInput` | What to scrape (see input methods below) |
| `projectType` | What kind of data (see table above); defaults to `urls` |
| `name` | Human-readable project name |
| `schedulingEnabled` | `true` / `false` |
| `scrapingInterval` | How often to run (see scheduling below) |
| `scheduledAt` | ISO 8601 timestamp of the next run, or `"now"` |
| `apiParams` | Scraping parameters (see below) |
| `webhookOutput` | Webhook delivery config |
| `notificationConfig` | Email notification settings |

`id` and `createdAt` are set by ScraperAPI.

## Input Methods

### Direct list

```json
{
  "projectInput": {
    "type": "list",
    "list": ["query one", "query two"]
  }
}
```

Items are URLs, queries, ASINs or IDs, depending on the project type.

### CSV file (dashboard)

In the [dashboard](https://dashboard.scraperapi.com/projects) you can upload a CSV of up to
100,000 items, one per line, with no header row and no commas. The dashboard's text field takes
up to 500 items.

### Webhook input

```json
{
  "projectInput": {
    "type": "webhook_input",
    "url": "https://yourapp.com/input-items"
  }
}
```

On every run, ScraperAPI downloads the item list from that URL. Return one item per line, with
no commas. Useful for dynamically generated lists (e.g., new ASINs added since the last run).

## Scheduling Options

| `scrapingInterval` | Description |
|-------------------|-------------|
| (omitted) | Scrape once (the default) |
| `"hourly"` | Every hour |
| `"daily"` | Once per day |
| `"weekly"` | Once per week |
| `"monthly"` | Once per month |
| a cron expression, e.g. `"0 0 * * 1"` | Custom schedule (five fields: minute, hour, day of month, month, day of week) |

Set `"scheduledAt": "now"` to trigger a run immediately, on create or later via `PATCH`.

## Output / Delivery

### Webhook delivery

```json
{
  "webhookOutput": {
    "url": "https://yourapp.com/results"
  }
}
```

Add `"webhookEncoding": "multipart_form_data_encoding"` if your receiver expects multipart form
data. Set `"webhookOutput": null` to stop webhook delivery.

### Dashboard download

Results are always available for download on the project's page in the
[DataPipeline dashboard](https://dashboard.scraperapi.com/projects), and through each job's
`resultUrl`. Results are delivered as a zipped file and kept for **30 days**, then deleted
permanently.

Output formats:
- `urls` projects → HTML, wrapped in JSONL
- Structured types (Amazon, Google, Walmart, eBay, Redfin) → JSON (default, wrapped in JSONL) or
  CSV. Choose with `"apiParams": {"outputFormat": "csv"}` or `"json"`.

## `apiParams`

The DataPipeline examples use these, written as shown:

| Parameter | Purpose |
|-----------|---------|
| `outputFormat` | `"json"` or `"csv"`, structured project types only |
| `render` | JavaScript rendering |
| `premium` | Premium residential proxies |

The docs point to the [Async API parameter list](https://docs.scraperapi.com/asynchronous-api/callbacks-and-api-params)
for the rest, but don't confirm that every one works in a project. If you need another parameter,
check the endpoints reference and read the 400 message if the API rejects it.

## Managing Projects

```python
# List all projects
projects = requests.get(f"{BASE}/projects", params={"api_key": API_KEY}).json()

# Get a single project
project = requests.get(f"{BASE}/projects/{project_id}", params={"api_key": API_KEY}).json()

# Update: send only the fields that change
requests.patch(
    f"{BASE}/projects/{project_id}",
    params={"api_key": API_KEY},
    json={
        "scrapingInterval": "daily",
        "apiParams":        {"premium": True},
        # both keys are required whenever notificationConfig is sent
        "notificationConfig": {"notifyOnSuccess": "weekly", "notifyOnFailure": "weekly"}
    }
)

# Archive (restoring it needs ScraperAPI support)
requests.delete(f"{BASE}/projects/{project_id}", params={"api_key": API_KEY})
```

## Managing Jobs

```python
# List jobs for a project
jobs = requests.get(
    f"{BASE}/projects/{project_id}/jobs",
    params={"api_key": API_KEY}
).json()

# Cancel a running job
requests.delete(
    f"{BASE}/projects/{project_id}/jobs/{job_id}",
    params={"api_key": API_KEY}
)
# Running requests within the job finish first; then the job's status becomes cancelled
```

Each job reports `status`, `successfulTasks`, `failedTasks`, `inProgressTasks`, `cancelledTasks`,
`credits`, `resultUrl` and `errorReportUrl`. A job is marked as an error when more than half of
its requests fail.

A new job can only start if no other job for that project is currently running.

## Notification Config

```json
{
  "notificationConfig": {
    "notifyOnSuccess": "never",
    "notifyOnFailure": "with_every_run"
  }
}
```

Notifications are emails. Send both keys whenever you send `notificationConfig`:
- `notifyOnSuccess`: `"never"`, `"with_every_run"`, `"daily"`, `"weekly"`
- `notifyOnFailure`: `"with_every_run"`, `"daily"`, `"weekly"` (no `"never"`)

## Credit Costs

DataPipeline jobs cost the same as standard API requests: 1 credit per normal request, 5 for
e-commerce sites (Amazon, Walmart, eBay), 25 for search engines (Google), and more with
`render` or `premium`. See the [DataPipeline credit costs](https://docs.scraperapi.com/data-pipeline/jobs-and-costs-management/credit-costs)
page for the full table. A job's cost is the sum of its requests, so it depends on how many
succeed; each job reports its total in `credits`.

## Limits

| Limit | Value |
|-------|-------|
| Max input items | 100,000 per project |
| Dashboard text field | 500 items |
| Concurrent jobs per project | 1 |
| Result retention | 30 days |

## Documentation

- [DataPipeline overview](https://docs.scraperapi.com/data-pipeline)
- [Endpoints and parameters](https://docs.scraperapi.com/data-pipeline/datapipeline-endpoints/endpoints-and-parameters)
- [How to use the API](https://docs.scraperapi.com/data-pipeline/datapipeline-endpoints/how-to-use)
- [Dashboard — manage projects](https://dashboard.scraperapi.com/projects)
