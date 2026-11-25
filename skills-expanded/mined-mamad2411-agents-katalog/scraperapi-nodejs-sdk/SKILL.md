---
name: scraperapi-nodejs-sdk
description: >
  Best-practices reference for the ScraperAPI Node.js / JavaScript SDK (scraperapi-sdk npm package).
  Consult whenever the user is writing, debugging, or reviewing JavaScript or TypeScript code that
  calls ScraperAPI. Use when user asks: "scrape a website with Node.js and ScraperAPI",
  "ScraperAPI JavaScript example", "how do I use scraperapi-sdk in Node",
  "ScraperAPI TypeScript", "ScraperAPI async await Node.js", "ScraperAPI POST request JavaScript",
  "Node.js ScraperAPI render", "ScraperAPI account info Node". Covers both CommonJS and ESM import
  styles, Promises and async/await, all request parameters, POST/PUT requests, account info,
  error handling, and credit costs.
metadata:
  openclaw:
    requires:
      env:
        - SCRAPERAPI_API_KEY
    emoji: "🟩"
    homepage: https://docs.scraperapi.com/nodejs
---

# ScraperAPI — Node.js SDK Best Practices

**Requires:** Node.js 14+, `npm install scraperapi-sdk`, `SCRAPERAPI_API_KEY` environment variable.

## Setup

```js
// CommonJS
const scraperapiClient = require('scraperapi-sdk')(process.env.SCRAPERAPI_API_KEY);

// ES Modules / TypeScript
import ScraperAPIClient from 'scraperapi-sdk';
const scraperapiClient = new ScraperAPIClient(process.env.SCRAPERAPI_API_KEY);
```

Never hardcode the API key. Read it from the environment every time.

## Decision Guide

| Situation | Pattern |
|-----------|---------|
| Single URL, result needed now | `scraperapiClient.get(url)` |
| 20+ URLs or batch work | Async Jobs API — `fetch/axios` to `async.scraperapi.com/jobs` |
| Supported platform (Amazon, Google, Walmart, eBay, Redfin) | Structured Data endpoint — `api.scraperapi.com/structured/<vertical>` |
| Page loads content via JavaScript | `.get(url, { render: true })` |
| Site blocks datacenter proxies | `.get(url, { premium: true })` |
| Need to POST a form or JSON body to the target | `.post(url, options)` |

## Basic Usage

```js
// GET — returns HTML as a string (Promise-based)
const html = await scraperapiClient.get('https://example.com/');

// With parameters
const html = await scraperapiClient.get('https://example.com/', {
  render: true,
  country_code: 'us',
});

// Without async/await (Promise chain)
scraperapiClient.get('https://example.com/')
  .then(html => console.log(html))
  .catch(err => console.error(err));
```

## POST and PUT Requests

```js
// POST — forward a JSON body to the target site
const result = await scraperapiClient.post('https://example.com/api', {
  body: JSON.stringify({ query: 'example' }),
  headers: { 'Content-Type': 'application/json' },
});

// PUT — same signature, different HTTP method
const result = await scraperapiClient.put('https://example.com/resource', {
  body: JSON.stringify({ name: 'updated' }),
  headers: { 'Content-Type': 'application/json' },
});
```

## Parameter Reference

### Rendering

```js
// Render JavaScript before returning HTML
// Use when: page uses React/Vue/Angular, or initial scrape returns empty content
// Cost: +10 credits
const html = await scraperapiClient.get('https://spa-site.com/', { render: true });

// Wait for a specific element before capturing (requires render: true)
const html = await scraperapiClient.get('https://spa-site.com/', {
  render: true,
  wait_for_selector: '.product-list',
});

// Screenshot (auto-enables rendering)
const html = await scraperapiClient.get('https://example.com/', { screenshot: true });
```

Start without `render: true`. Add it only when the response is missing expected content.

### Proxies and Geotargeting

```js
// Route through a specific country — no extra credit cost
const html = await scraperapiClient.get('https://example.com/', { country_code: 'gb' });

// Premium residential/mobile proxies
// Cost: 10 credits (25 with render: true)
const html = await scraperapiClient.get('https://hard-site.com/', { premium: true });

// Ultra-premium — for the toughest anti-bot protections
// Cost: 30 credits (75 with render: true)
// Incompatible with custom headers — keep_headers is ignored when ultra_premium is set
const html = await scraperapiClient.get('https://hardest-site.com/', { ultra_premium: true });
```

`premium` and `ultra_premium` are mutually exclusive — never set both.
Escalation order: standard (1 cr) → render (10 cr) → premium (10 cr) → ultra_premium (30 cr).

### Sessions (Sticky Proxy)

```js
// Reuse the same proxy IP across requests (same session_number = same IP)
// Sessions expire 15 minutes after last use
const page1 = await scraperapiClient.get('https://example.com/page1', { session_number: 42 });
const page2 = await scraperapiClient.get('https://example.com/page2', { session_number: 42 });
```

### Headers and Device Type

```js
// Forward your own headers to the target site
// Note: keep_headers is ignored when ultra_premium: true
const html = await scraperapiClient.get('https://example.com/', {
  keep_headers: true,
  headers: { 'Accept-Language': 'en-US', 'Referer': 'https://google.com' },
});

// Emulate mobile or desktop browser
const html = await scraperapiClient.get('https://example.com/', { device_type: 'mobile' });
```

### Response Format and Autoparse

```js
// Structured JSON for supported sites (Amazon, Google, etc.)
const data = await scraperapiClient.get('https://amazon.com/dp/B09V3KXJPB', { autoparse: true });

// Markdown — useful for LLM pipelines or documentation tools
const md = await scraperapiClient.get('https://docs.example.com/', { output_format: 'markdown' });

// Plain text
const text = await scraperapiClient.get('https://example.com/', { output_format: 'text' });
```

## Account Information

```js
// Returns usage stats: concurrent request usage, total requests, account limits
const account = await scraperapiClient.account();
console.log(account);
```

Use this to monitor credit consumption and concurrency limits programmatically.

## Escalation Ladder

```js
async function scrapeWithEscalation(url) {
  const tiers = [
    {},                                    // 1 credit
    { render: true },                      // 10 credits
    { premium: true },                     // 10 credits
    { premium: true, render: true },       // 25 credits
    { ultra_premium: true },               // 30 credits
  ];
  for (const params of tiers) {
    const html = await scraperapiClient.get(url, params);
    if (html && html.includes('<html')) return html;
  }
  return null;
}
```

## Async Jobs (for Batches)

The sync SDK blocks on each call. For 20+ URLs, use the async endpoint directly to fan out jobs.

```js
const API_KEY = process.env.SCRAPERAPI_API_KEY;

async function submitJob(url, apiParams = {}) {
  const res = await fetch('https://async.scraperapi.com/jobs', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ apiKey: API_KEY, url, apiParams }),
  });
  return res.json(); // { id, status, statusUrl }
}

async function pollJob(job, maxWaitMs = 120_000, intervalMs = 5_000) {
  const deadline = Date.now() + maxWaitMs;
  while (Date.now() < deadline) {
    const res = await fetch(job.statusUrl);
    const data = await res.json();
    if (data.status === 'finished') return data.response.body;
    if (data.status === 'failed') throw new Error(`Job ${job.id} failed`);
    await new Promise(r => setTimeout(r, intervalMs));
  }
  throw new Error(`Job ${job.id} timed out`);
}

// Batch — submit all, then collect
const urls = ['https://example.com/p1', 'https://example.com/p2'];
const jobs = await Promise.all(urls.map(submitJob));
const results = await Promise.all(jobs.map(pollJob));
```

## Structured Data Endpoints

For supported platforms, use structured endpoints instead of raw HTML — they return clean JSON
without parsing logic.

```js
async function structuredGet(vertical, params) {
  const query = new URLSearchParams({ api_key: API_KEY, ...params });
  const res = await fetch(`https://api.scraperapi.com/structured/${vertical}?${query}`);
  if (!res.ok) throw new Error(`${res.status} ${res.statusText}`);
  return res.json();
}

// Google SERP
const serp = await structuredGet('google/search', { query: 'javascript scraping' });

// Amazon product
const product = await structuredGet('amazon/product', { asin: 'B09V3KXJPB' });

// Walmart search
const items = await structuredGet('walmart/search', { query: 'standing desk' });
```

See [structured data docs](https://docs.scraperapi.com/nodejs) for all verticals and required fields.

## Error Handling

```js
async function safeScrape(url, params = {}) {
  try {
    return await scraperapiClient.get(url, params);
  } catch (err) {
    const status = err?.response?.status ?? err?.status;
    if (status === 401) throw new Error('Invalid API key — check SCRAPERAPI_API_KEY');
    if (status === 403) throw new Error('Blocked or out of credits — try premium or ultra_premium');
    if (status === 429) throw new Error('Rate limit — reduce concurrency or switch to async');
    if (status === 500 || status === 503) throw new Error('Transient error — retry with backoff');
    throw err;
  }
}
```

Status codes: 200 success, 401 bad key, 403 blocked/no credits, 404 not found (target),
429 rate limit, 500/503 transient (not charged, safe to retry).

## Credit Cost Reference

| Request type | Credits |
|---|---|
| Standard | 1 |
| `render: true` | 10 |
| `premium: true` | 10 |
| `premium: true` + `render: true` | 25 |
| `ultra_premium: true` | 30 |
| `ultra_premium: true` + `render: true` | 75 |

## Documentation

- [Node.js SDK getting started](https://docs.scraperapi.com/nodejs)
- [SDK method reference](https://docs.scraperapi.com/nodejs/making-requests-or-nodejs/sdk-method-or-nodejs)
- [API status codes](https://docs.scraperapi.com/nodejs/handling-and-processing-responses/api-status-codes)
- [Account information](https://docs.scraperapi.com/nodejs/account-information)
- [Dashboard & credits](https://dashboard.scraperapi.com/)
