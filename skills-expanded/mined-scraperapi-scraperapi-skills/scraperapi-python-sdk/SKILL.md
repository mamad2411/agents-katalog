---
name: scraperapi-python-sdk
description: >
  Best-practices reference for the ScraperAPI Python SDK (scraperapi-sdk package). Consult
  whenever the user is writing, debugging, or reviewing Python code that calls ScraperAPI. Use
  when user asks: "how do I use ScraperAPIClient", "ScraperAPI Python render example", "Python
  ScraperAPI async", "ScraperAPI premium Python", "how to handle ScraperAPI errors in Python",
  "ScraperAPI structured data Python", "why does my scraperapi_sdk call fail". Covers client
  setup, all request parameters, the escalation ladder (standard → render → premium →
  ultra_premium), async jobs, structured data endpoints, error handling, and credit budgeting. To
  write a complete new scraper from scratch, use scraperapi-scraper-builder; for the Async Jobs
  API in depth (batches, webhooks), use scraperapi-async.

  Note: Transmits user-supplied queries, URLs, and content to ScraperAPI.
metadata:
  openclaw:
    requires:
      env:
        - SCRAPERAPI_API_KEY
    emoji: "🐍"
    homepage: https://docs.scraperapi.com/python
---

# ScraperAPI — Python SDK Best Practices

**Requires:** Python 3.10+ (the SDK uses `list | tuple` annotations, so importing it fails on older versions), `pip install scraperapi-sdk`, `SCRAPERAPI_API_KEY` environment variable.

## Setup

```python
import os
from scraperapi_sdk import ScraperAPIClient

client = ScraperAPIClient(os.environ["SCRAPERAPI_API_KEY"])
```

Never hardcode the API key. Read it from the environment every time.

## Decision Guide

Pick the right call pattern before writing any code.

| Situation | Pattern |
|-----------|---------|
| Single URL, response needed immediately | `client.get()` — synchronous |
| 20+ URLs, or single URL that often times out | Async Jobs API — `requests.post()` to `async.scraperapi.com/jobs` |
| Supported platform (Amazon, Google, Walmart, eBay, Redfin) | Structured Data endpoint — `api.scraperapi.com/structured/<vertical>` |
| Page loads content via JavaScript (React, Vue, Angular) | `client.get()` with `render=True` |
| Site blocks standard proxies | `client.get()` with `premium=True` |

Use the sync SDK for simple, single-URL work. For batches, the SDK has `ScraperAPIAsyncClient` (single jobs only); use raw `requests` for `/batchjobs` or when you need control over polling — see [Async Jobs](#async-jobs-for-batches).

## Basic Usage

```python
# Simple scrape. Returns str for text/HTML, dict for JSON (autoparse, output_format=json), bytes otherwise
html = client.get(url="https://example.com/")

# With parameters
html = client.get(
    url="https://example.com/",
    params={"render": True, "country_code": "us"}
)
```

## Parameter Reference

### Rendering

```python
# Render JavaScript before returning HTML
# Use when: page uses React/Vue/Angular, or initial scrape returns empty/partial content
# Cost: 10 credits per request (instead of 1)
html = client.get(url="https://spa-site.com/", params={"render": True})

# Wait for a specific element before capturing (requires render=True)
# Use when: content loads lazily and simple render still misses it
html = client.get(
    url="https://spa-site.com/",
    params={"render": True, "wait_for_selector": ".product-list"}
)

# Capture a screenshot (auto-enables rendering)
html = client.get(url="https://example.com/", params={"screenshot": True})
```

Start without `render=True`. Add it only when the response is missing expected content — it increases cost and latency.

### Proxies and Geotargeting

```python
# Route through a specific country — no extra cost
html = client.get(url="https://example.com/", params={"country_code": "us"})

# Premium residential/mobile proxies — for sites that block datacenter IPs
# Cost: 10 credits per request (25 with render=True)
html = client.get(url="https://hard-site.com/", params={"premium": True})

# Ultra-premium — for the toughest anti-bot protections
# Cost: 30 credits per request (75 with render=True)
# Note: incompatible with custom headers (keep_headers is ignored)
html = client.get(url="https://hardest-site.com/", params={"ultra_premium": True})
```

`premium` and `ultra_premium` are mutually exclusive — never set both. Escalate gradually:
standard (1 cr) → render (10 cr) → premium (10 cr) → premium+render (25 cr) → ultra_premium (30 cr).

### Sessions (Sticky Proxy)

```python
# Reuse the same proxy IP across multiple requests
# Use for: multi-page flows, pagination, login-state scraping
# Sessions expire 15 minutes after last use; any integer is a valid session ID
html1 = client.get("https://example.com/page1", params={"session_number": 42})
html2 = client.get("https://example.com/page2", params={"session_number": 42})
```

`session_number` can't be combined with `premium` or `ultra_premium`.

### Headers and Device Type

```python
# Forward your own headers to the target site
# Note: keep_headers is incompatible with ultra_premium=True
html = client.get(
    url="https://example.com/",
    params={"keep_headers": True},
    headers={"Accept-Language": "en-US", "Referer": "https://google.com"}
)

# Emulate mobile or desktop user-agent
html = client.get(url="https://example.com/", params={"device_type": "mobile"})
```

### Response Format

```python
# Default: raw HTML
html = client.get(url="https://example.com/")

# Structured JSON for supported sites (Amazon, Google, etc.)
# autoparse extracts fields like title, price, reviews automatically
data = client.get(url="https://amazon.com/dp/B09V3KXJPB", params={"autoparse": True})

# Markdown — useful for LLM pipelines
text = client.get(url="https://docs.example.com/", params={"output_format": "markdown"})

# Plain text
text = client.get(url="https://example.com/", params={"output_format": "text"})

# Binary content (PDFs, images)
content = client.get(url="https://example.com/report.pdf", params={"binary_target": True})
```

## Escalation Ladder

Always start cheapest. Move up only when the site blocks the previous tier.

```python
from scraperapi_sdk import ScraperAPIException

def scrape_with_escalation(url):
    for params in [
        {},                       # 1 credit
        {"render": True},         # 10 credits
        {"premium": True},        # 10 credits
        {"premium": True, "render": True},  # 25 credits
        {"ultra_premium": True},  # 30 credits
    ]:
        try:
            result = client.get(url=url, params=params)
        except ScraperAPIException as e:
            resp = getattr(e.original_exception, "response", None)
            if resp is not None and resp.status_code in (401, 403):
                raise  # bad key, out of credits or max_cost hit: a pricier tier won't help
            continue  # 500 or timeout: try the next tier
        if isinstance(result, str) and "<html" in result.lower():
            return result
    return None
```

`client.get` raises on any non-2xx, so each tier needs its own `try`. Credits above are for a normal site; Google, Amazon and bot-protected sites cost more (see [Credit Cost Reference](#credit-cost-reference)).

Log which tier succeeded so you can start there next time for the same domain.

## Async Jobs (for Batches)

The sync SDK blocks on each call, and `client.get` gives up after 55 seconds while ScraperAPI may keep retrying for up to 70 (requests cancelled before 70s are still charged). For slow targets, call `client.make_request(url=..., params=..., timeout=70)`, which returns the raw `requests.Response`. For 20+ URLs, use the async endpoint: it submits jobs in the background and lets you poll or receive webhooks.

The SDK's `ScraperAPIAsyncClient` covers single jobs:

```python
from scraperapi_sdk import ScraperAPIAsyncClient

async_client = ScraperAPIAsyncClient(os.environ["SCRAPERAPI_API_KEY"])
job = async_client.create("https://example.com/", api_params={"render": True})
# wait() checks max_retries times, then returns the job as-is, even if it is still running
data = async_client.wait(job["id"], cooldown=10, max_retries=60)
if data["status"] == "finished":
    body = data["response"]["body"]
```

For more control, or for `/batchjobs`, use `requests` directly:

```python
import os, requests, time

API_KEY = os.environ["SCRAPERAPI_API_KEY"]

def submit_job(url, extra_params=None):
    payload = {
        "apiKey": API_KEY,
        "url": url,
        "apiParams": extra_params or {},
        "expectUnsuccessReport": True,  # without it, a job that fails never reaches "failed"
    }
    r = requests.post("https://async.scraperapi.com/jobs", json=payload, timeout=10)
    r.raise_for_status()
    return r.json()  # {"id": "...", "status": "running", "statusUrl": "..."}

def poll_job(job, max_wait=600, interval=10):
    # Jobs can keep retrying for up to 24h; pick a deadline that fits your use case
    deadline = time.time() + max_wait
    while time.time() < deadline:
        data = requests.get(job["statusUrl"], timeout=10).json()
        if data["status"] == "finished":
            return data["response"]["body"]
        if data["status"] == "failed":
            raise RuntimeError(f"Job failed: {job['id']}")
        time.sleep(interval)
    raise TimeoutError(f"Job {job['id']} did not finish in {max_wait}s")

# Batch pattern: submit all, then collect, so one bad job doesn't lose the rest
urls = ["https://example.com/page1", "https://example.com/page2"]
jobs = [submit_job(u) for u in urls]
results = {}
for j in jobs:
    try:
        results[j["url"]] = poll_job(j)
    except (RuntimeError, TimeoutError) as e:
        results[j["url"]] = None
        print(e)
```

Use webhooks (`"callback": {"type": "webhook", "url": "https://yourapp.com/cb"}`) when you control a server — eliminates polling entirely. See [async docs](https://docs.scraperapi.com/asynchronous-api).

For very large batches (up to 50,000 URLs), use `https://async.scraperapi.com/batchjobs` with a `"urls": [...]` array.

## Structured Data Endpoints

Use these instead of scraping raw HTML when the target platform is supported. They return clean JSON and require no parsing logic; they're billed at the target site's rate (5 credits for Amazon, 25 for Google).

```python
import os, requests

API_KEY = os.environ["SCRAPERAPI_API_KEY"]

def structured_get(vertical, params):
    """Call a structured data endpoint synchronously."""
    url = f"https://api.scraperapi.com/structured/{vertical}"
    r = requests.get(url, params={"api_key": API_KEY, **params}, timeout=70)
    r.raise_for_status()
    return r.json()

# Google SERP
results = structured_get("google/search", {"query": "best Python web scrapers"})

# Amazon product details
product = structured_get("amazon/product", {"asin": "B09V3KXJPB"})

# Walmart product search
items = structured_get("walmart/search", {"query": "standing desk", "tld": "com"})
```

Supported verticals: `google/search`, `google/news`, `google/jobs`, `google/shopping`,
`google/mapssearch`, `amazon/product`, `amazon/search`, `amazon/offers`,
`walmart/product`, `walmart/search`, `walmart/category`, `walmart/review`,
`ebay/product`, `ebay/search/v2`, `redfin/forsale`, `redfin/forrent`, `redfin/search`, `redfin/agent`.

The SDK also has shortcut methods: `client.google.search(query)`, `client.amazon.product(asin)`, `client.walmart.product(product_id)`, `client.ebay.searchV2(query)`, `client.redfin.forsale(url)` and so on. They send geotargeting as `country`, while the endpoints document `country_code`, so use `structured_get` above when you need a specific country.

See [structured data docs](https://docs.scraperapi.com/python/making-requests/structured-data-collection-method) for required parameters per vertical.

## Error Handling

The SDK wraps every failure (HTTP errors, timeouts, connection errors) in `ScraperAPIException`. The original `requests` exception is on `e.original_exception`; for HTTP errors, its `.response` carries the status code.

```python
import os
from scraperapi_sdk import ScraperAPIClient, ScraperAPIException

client = ScraperAPIClient(os.environ["SCRAPERAPI_API_KEY"])

def scrape(url, params=None):
    try:
        return client.get(url=url, params=params or {})
    except ScraperAPIException as e:
        resp = getattr(e.original_exception, "response", None)
        if resp is None:
            # Timeout or connection error: no status code. Retry, or use make_request(timeout=70)
            raise RuntimeError(f"Network error or timeout: {e.original_exception}") from e
        status = resp.status_code
        if status == 401:
            raise ValueError("Invalid API key — check SCRAPERAPI_API_KEY") from e
        if status == 403:
            # Credits exhausted, or the request would cost more than max_cost. Retrying won't help
            raise RuntimeError("Out of credits or over max_cost — check https://dashboard.scraperapi.com/billing (don't retry)") from e
        if status == 429:
            # Concurrent request limit — back off and retry
            raise RuntimeError("Rate limit — reduce concurrency or switch to async") from e
        if status == 500:
            # ScraperAPI already retried for 70s (not charged) — retry; on protected sites escalate to premium/ultra_premium
            raise RuntimeError("Request failed after retries — retry or escalate") from e
        raise
```

Status code reference: 200 success, 400 malformed request, 401 bad key, 403 credits exhausted or `max_cost` exceeded (don't retry), 404 target not found (charged),
429 concurrency limit, 500 failed after 70s of retries (not charged — retry, then escalate to premium/ultra_premium on protected sites).

## Credit Cost Reference

| Request type | Credits |
|---|---|
| Standard | 1 |
| `render=True` | 10 |
| `premium=True` | 10 |
| `premium=True` + `render=True` | 25 |
| `ultra_premium=True` | 30 |
| `ultra_premium=True` + `render=True` | 75 |

Those are the costs on a normal site. Some sites cost more per request:

| Site | Credits |
|---|---|
| Amazon, Walmart, eBay | 5 |
| Google, Bing (all subdomains) | 25 |
| LinkedIn | 30 |
| Sites behind Cloudflare, DataDome, PerimeterX or Akamai | 10 |

Combined costs vary by site; check the exact price with `/account/urlcost` or the `sa-credit-cost` header before a large run.

You're charged for `200` and `404` responses, and for requests you cancel before ScraperAPI's 70s
of retries finish. Each response's `sa-credit-cost` header shows what it cost; preview a cost
without spending credits with `GET https://api.scraperapi.com/account/urlcost?api_key=...&url=...`
(it accepts the same parameters). Source: https://docs.scraperapi.com/getting-started/quick-start/credits-and-requests-costs

Add `"max_cost": N` to any request to cap credit spend — returns 403 if the request would exceed N credits.

## Documentation

- [Python SDK getting started](https://docs.scraperapi.com/python)
- [Request parameters](https://docs.scraperapi.com/python/making-requests/customizing-requests)
- [Structured data endpoints](https://docs.scraperapi.com/python/making-requests/structured-data-collection-method)
- [Async API](https://docs.scraperapi.com/asynchronous-api)
- [Dashboard & credits](https://dashboard.scraperapi.com/)
