---
name: scraperapi-async
description: >
  Product-usage reference for ScraperAPI's Async Jobs API — submit scraping jobs in the background
  and retrieve results via polling or webhook, including batch jobs up to 50,000 URLs.
  Consult when the user is scraping many URLs, needs non-blocking requests, or wants webhook delivery.
  Use when user asks: "how do I scrape 1000 URLs with ScraperAPI", "ScraperAPI async jobs",
  "batch scraping with ScraperAPI", "submit a scraping job and poll for results",
  "ScraperAPI webhook callback", "scrape URLs in the background", "ScraperAPI batchjobs endpoint".
  Covers single jobs, batch jobs (up to 50k URLs), webhook callbacks, all apiParams,
  async-exclusive parameters, binary response decoding, retention policy, and error handling.
metadata:
  openclaw:
    requires:
      env:
        - SCRAPERAPI_API_KEY
    emoji: "⚡"
    homepage: https://docs.scraperapi.com/making-async-requests
---

# ScraperAPI Async Jobs API

The Async API submits scraping jobs in the background and retries them for up to 24 hours to
maximize success. Results are retrieved by polling a status URL or received automatically via
webhook.

## When NOT to use Async

- **Single URL, result needed immediately** → use the Standard API (`api.scraperapi.com`) — simpler and returns inline.
- **Need to follow links across a site** → use the [Crawler](https://docs.scraperapi.com/crawler).
- **Need recurring scheduled scraping** → use [DataPipeline](https://docs.scraperapi.com/data-pipeline).

Use Async when: scraping 20+ URLs, the target site is slow or flaky, you want webhook delivery,
or you need to scrape PDFs/images.

## Endpoints

| Action | Method | URL |
|--------|--------|-----|
| Submit single job | POST | `https://async.scraperapi.com/jobs` |
| Submit batch (up to 50k) | POST | `https://async.scraperapi.com/batchjobs` |
| Check / retrieve job | GET | `https://async.scraperapi.com/jobs/<jobId>` |
| Cancel job | DELETE | `https://async.scraperapi.com/jobs/<jobId>` |

Auth: `apiKey` in the JSON request body (note: `apiKey` camelCase, unlike the Standard API's `api_key`).

## Single Job

```python
import os, requests, time

API_KEY = os.environ["SCRAPERAPI_API_KEY"]

# Submit
r = requests.post(
    "https://async.scraperapi.com/jobs",
    json={
        "apiKey": API_KEY,
        "url":    "https://example.com/product/123",
        "apiParams": {
            "render":       True,
            "country_code": "us",
        }
    }
)
job = r.json()
# {"id": "...", "status": "running", "statusUrl": "...", "url": "..."}

# Poll
def poll(status_url, interval=5, max_wait=120):
    deadline = time.time() + max_wait
    while time.time() < deadline:
        data = requests.get(status_url).json()
        if data["status"] == "finished":
            return data["response"]["body"]
        if data["status"] == "failed":
            raise RuntimeError(f"Job failed: {data.get('failReason')}")
        time.sleep(interval)
    raise TimeoutError("Job did not finish in time")

html = poll(job["statusUrl"])
```

Finished job response shape:
```json
{
  "id": "...",
  "status": "finished",
  "statusUrl": "...",
  "url": "https://example.com/product/123",
  "response": {
    "headers": { "content-type": "text/html", "sa-final-url": "...", "sa-statuscode": "200" },
    "body": "<!doctype html>...",
    "statusCode": 200
  }
}
```

## Batch Jobs (up to 50,000 URLs)

```python
jobs = requests.post(
    "https://async.scraperapi.com/batchjobs",
    json={
        "apiKey": API_KEY,
        "urls": [
            "https://example.com/page/1",
            "https://example.com/page/2",
            # ... up to 50,000
        ],
        "apiParams": {"country_code": "us"}
    }
).json()
# Returns a list of {id, status, statusUrl, url} — one per submitted URL

results = [poll(job["statusUrl"]) for job in jobs]
```

For workloads over 50,000 URLs, split into multiple batch requests. Use webhooks (below) instead
of polling when batches are large — polling 10,000 status URLs serially is slow.

## Webhook Callbacks

Use webhooks to receive results without polling. ScraperAPI POSTs the completed job payload to
your URL when the scrape finishes.

```python
requests.post(
    "https://async.scraperapi.com/jobs",
    json={
        "apiKey": API_KEY,
        "url":    "https://example.com/",
        "callback": {
            "type": "webhook",
            "url":  "https://yourapp.com/scraperapi/callback"
        }
    }
)
```

Webhook mechanics:
- By default, only successful jobs trigger the callback.
- Set `"expectUnsuccessReport": true` to also receive failed job payloads.
- ScraperAPI retries delivery 3 times; if all fail, the job is cancelled.
- Webhook URL must be publicly accessible.
- For testing without a server, use [webhook.site](https://webhook.site).

Failed job callback payload:
```json
{
  "id": "...",
  "attempts": 50,
  "status": "failed",
  "failReason": "failed_due_to_timeout",
  "url": "https://example.com/"
}
```

## All Request Body Parameters

```json
{
  "apiKey":               "YOUR_KEY",
  "url":                  "https://example.com",
  "urls":                 ["url1", "url2"],
  "method":               "GET",
  "headers":              { "Accept-Language": "en-US" },
  "body":                 "foo=bar",
  "callback":             { "type": "webhook", "url": "https://..." },
  "expectUnsuccessReport": false,
  "timeoutSec":           600,
  "meta":                 { "jobLabel": "batch-42" },
  "apiParams": {
    "autoparse":          false,
    "country_code":       "us",
    "keep_headers":       false,
    "device_type":        "desktop",
    "follow_redirect":    true,
    "premium":            false,
    "ultra_premium":      false,
    "render":             false,
    "wait_for_selector":  ".content",
    "screenshot":         false,
    "retry_404":          false,
    "output_format":      "html",
    "max_cost":           10
  }
}
```

### Async-exclusive parameters

| Parameter | Type | Purpose |
|-----------|------|---------|
| `expectUnsuccessReport` | boolean | Receive webhook payload for failed jobs too |
| `timeoutSec` | integer | Override default job timeout (seconds) |
| `meta` | object | Custom metadata — echoed back in every response/callback for correlation |

`meta` is especially useful for tracking which batch or workflow a job belongs to:
```json
{ "meta": { "batchId": "run-2024-06", "sourceFile": "urls.csv" } }
```

### Passing a POST request to the target site

```python
requests.post(
    "https://async.scraperapi.com/jobs",
    json={
        "apiKey":  API_KEY,
        "url":     "https://api.example.com/search",
        "method":  "POST",
        "headers": {"content-type": "application/x-www-form-urlencoded"},
        "body":    "query=scraperapi&page=1",
    }
)
```

## Binary Responses (PDFs and Images)

When the target URL returns binary content, the response body is Base64-encoded in
`response.base64EncodedBody`.

```python
import base64

r = requests.post(
    "https://async.scraperapi.com/jobs",
    json={"apiKey": API_KEY, "url": "https://example.com/report.pdf"}
)
job = r.json()

# ... wait or poll ...
result = requests.get(job["statusUrl"]).json()
pdf_bytes = base64.b64decode(result["response"]["base64EncodedBody"])
with open("report.pdf", "wb") as f:
    f.write(pdf_bytes)
```

## Retention Policy

Job results are stored for **up to 72 hours** (24 hours guaranteed) after the job finishes.
After that, the data is deleted — resubmit the job if you need it again.

Retrieve results before the retention window closes. For long pipelines, prefer webhooks so
results are pushed to your system immediately upon completion.

## Error Handling

| Status | Meaning | Action |
|--------|---------|--------|
| Job `finished`, `statusCode: 200` | Success | Use `response.body` |
| Job `finished`, `statusCode: 403` | Target blocked the scrape | Retry with `premium: true` in `apiParams` |
| Job `failed`, `failReason: failed_due_to_timeout` | Timed out after 24h retries | Check if target is reachable; try `render: false` |
| HTTP 401 on submission | Bad API key | Check `SCRAPERAPI_API_KEY` |
| HTTP 403 on submission | Out of credits or plan limit | Check dashboard |
| HTTP 429 on submission | Too many concurrent submissions | Back off and re-submit in batches |

Use `max_cost` in `apiParams` to cap per-request credit spend — requests that would exceed the
cap return a 403 rather than consuming more credits than expected.

## Credit Cost

The Async API uses the same credit costs as the Standard API:

| Request type | Credits |
|---|---|
| Standard | 1 |
| `render: true` | 10 |
| `premium: true` | 10 |
| `ultra_premium: true` | 30 |
| Failed requests | 0 |

Async jobs that fail after exhausting all retries are **not charged**.

## Documentation

- [Async API overview](https://docs.scraperapi.com/making-async-requests)
- [Batch jobs](https://docs.scraperapi.com/making-async-requests)
- [Dashboard & credits](https://dashboard.scraperapi.com/)
