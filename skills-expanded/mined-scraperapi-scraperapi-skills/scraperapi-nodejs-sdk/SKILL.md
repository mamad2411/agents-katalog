---
name: scraperapi-nodejs-sdk
description: >
  Best-practices reference for the ScraperAPI Node.js / JavaScript SDK (scraperapi-sdk npm
  package). Consult whenever the user is writing, debugging, or reviewing JavaScript or TypeScript
  code that calls ScraperAPI. Use when user asks: "how do I use scraperapi-sdk in Node",
  "ScraperAPI JavaScript example", "ScraperAPI TypeScript", "ScraperAPI async await Node.js",
  "ScraperAPI POST request JavaScript", "Node.js ScraperAPI render", "ScraperAPI account info
  Node". Covers CommonJS and ESM imports, Promises and async/await, all request parameters,
  POST/PUT requests, account info, error handling, and credit costs. To write a complete new
  scraper from scratch, use scraperapi-scraper-builder; for the Async Jobs API in depth (batches,
  webhooks), use scraperapi-async.

  Note: Transmits user-supplied queries, URLs, and content to ScraperAPI.
metadata:
  openclaw:
    requires:
      env:
        - SCRAPERAPI_API_KEY
    emoji: "🟩"
    homepage: https://docs.scraperapi.com/nodejs
---

# ScraperAPI — Node.js SDK Best Practices

**Requires:** Node.js 18+ (the snippets use the global `fetch`), `npm install scraperapi-sdk`, `SCRAPERAPI_API_KEY` environment variable.

## Setup

```js
// CommonJS
const scraperapiClient = require('scraperapi-sdk')(process.env.SCRAPERAPI_API_KEY);

// ES Modules / TypeScript — the default export is a factory function, not a class
import scraperapi from 'scraperapi-sdk';
const scraperapiClient = scraperapi(process.env.SCRAPERAPI_API_KEY);
```

The package ships type definitions in `dist/` but doesn't declare them in `package.json`, so TypeScript reports a missing declaration file. Add `declare module 'scraperapi-sdk';` to a `.d.ts` file in your project, or set `noImplicitAny: false`.

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
// GET — resolves to { body, headers, statusCode }, not a string
const res = await scraperapiClient.get('https://example.com/');
if (res.statusCode === 200) console.log(res.body);

// With parameters
const res = await scraperapiClient.get('https://example.com/', {
  render: true,
  country_code: 'us',
});

// Without async/await (Promise chain)
scraperapiClient.get('https://example.com/')
  .then(res => console.log(res.statusCode, res.body))
  .catch(err => console.error(err)); // network errors only, see Error Handling
```

Every method (`get`, `post`, `put`) resolves even when ScraperAPI returns 401, 403, 429 or 500, so always check `res.statusCode` before using `res.body`.

## POST and PUT Requests

```js
// POST — forward a JSON body to the target site
const res = await scraperapiClient.post('https://example.com/api', {
  body: JSON.stringify({ query: 'example' }),
  headers: { 'Content-Type': 'application/json' },
});

// PUT — same signature, different HTTP method
const res = await scraperapiClient.put('https://example.com/resource', {
  body: JSON.stringify({ name: 'updated' }),
  headers: { 'Content-Type': 'application/json' },
});
```

## Parameter Reference

### Rendering

```js
// Render JavaScript before returning HTML
// Use when: page uses React/Vue/Angular, or initial scrape returns empty content
// Cost: 10 credits per request (instead of 1)
const res = await scraperapiClient.get('https://spa-site.com/', { render: true });

// Wait for a specific element before capturing (requires render: true)
const res = await scraperapiClient.get('https://spa-site.com/', {
  render: true,
  wait_for_selector: '.product-list',
});

// Screenshot (auto-enables rendering)
const res = await scraperapiClient.get('https://example.com/', { screenshot: true });
```

Start without `render: true`. Add it only when the response is missing expected content.

### Proxies and Geotargeting

```js
// Route through a specific country — no extra credit cost
const res = await scraperapiClient.get('https://example.com/', { country_code: 'gb' });

// Premium residential/mobile proxies
// Cost: 10 credits (25 with render: true)
const res = await scraperapiClient.get('https://hard-site.com/', { premium: true });

// Ultra-premium — for the toughest anti-bot protections
// Cost: 30 credits (75 with render: true)
// Incompatible with custom headers — keep_headers is ignored when ultra_premium is set
const res = await scraperapiClient.get('https://hardest-site.com/', { ultra_premium: true });
```

`premium` and `ultra_premium` are mutually exclusive — never set both.
Escalation order: standard (1 cr) → render (10 cr) → premium (10 cr) → premium+render (25 cr) → ultra_premium (30 cr).

### Sessions (Sticky Proxy)

```js
// Reuse the same proxy IP across requests (same session_number = same IP)
// Sessions expire 15 minutes after last use
const page1 = await scraperapiClient.get('https://example.com/page1', { session_number: 42 });
const page2 = await scraperapiClient.get('https://example.com/page2', { session_number: 42 });
```

`session_number` can't be combined with `premium` or `ultra_premium`.

### Headers and Device Type

```js
// Forward your own headers to the target site
// Note: keep_headers is ignored when ultra_premium: true
const res = await scraperapiClient.get('https://example.com/', {
  keep_headers: true,
  headers: { 'Accept-Language': 'en-US', 'Referer': 'https://google.com' },
});

// Emulate mobile or desktop browser
const res = await scraperapiClient.get('https://example.com/', { device_type: 'mobile' });
```

### Response Format and Autoparse

```js
// Structured JSON for supported sites (Amazon, Google, etc.)
const res = await scraperapiClient.get('https://amazon.com/dp/B09V3KXJPB', { autoparse: true });

// Markdown — useful for LLM pipelines or documentation tools
const res = await scraperapiClient.get('https://docs.example.com/', { output_format: 'markdown' });

// Plain text
const res = await scraperapiClient.get('https://example.com/', { output_format: 'text' });
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
    const res = await scraperapiClient.get(url, params);
    // bad key, out of credits or max_cost hit: a pricier tier won't help
    if (res.statusCode === 401 || res.statusCode === 403) throw new Error(`ScraperAPI ${res.statusCode}: ${res.body}`);
    if (res.statusCode === 200 && res.body.includes('<html')) return res.body;
  }
  return null;
}
```

Credits above are for a normal site; Google, Amazon and bot-protected sites cost more (see [Credit Cost Reference](#credit-cost-reference)).

## Async Jobs (for Batches)

The sync SDK waits on each call and sets no timeout of its own. For 20+ URLs, use the async endpoint directly to fan out jobs.

```js
const API_KEY = process.env.SCRAPERAPI_API_KEY;

async function submitJob(url, apiParams = {}) {
  const res = await fetch('https://async.scraperapi.com/jobs', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    // without expectUnsuccessReport, a job that fails never reaches "failed"
    body: JSON.stringify({ apiKey: API_KEY, url, apiParams, expectUnsuccessReport: true }),
  });
  return res.json(); // { id, status, statusUrl }
}

// Jobs can keep retrying for up to 24h; pick a deadline that fits your use case
async function pollJob(job, maxWaitMs = 600_000, intervalMs = 10_000) {
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

// Batch — submit all, then collect; allSettled so one failed job doesn't lose the rest
const urls = ['https://example.com/p1', 'https://example.com/p2'];
const jobs = await Promise.all(urls.map(u => submitJob(u)));
const results = await Promise.allSettled(jobs.map(j => pollJob(j)));
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

The SDK only rejects on network errors (DNS, connection reset). HTTP errors from ScraperAPI resolve normally, so read `statusCode`. It also sets no timeout; ScraperAPI can take up to 70s, so cap the wait yourself.

```js
const withTimeout = (p, ms = 75_000) =>
  Promise.race([p, new Promise((_, rej) => setTimeout(() => rej(new Error('Timed out')), ms))]);

async function safeScrape(url, params = {}) {
  const res = await withTimeout(scraperapiClient.get(url, params)); // rejects on network error or timeout
  const { statusCode, body } = res;
  if (statusCode === 200 || statusCode === 404) return res; // 404 is the target's answer (charged)
  if (statusCode === 401) throw new Error('Invalid API key — check SCRAPERAPI_API_KEY');
  if (statusCode === 403) throw new Error("Out of credits or over max_cost — check https://dashboard.scraperapi.com/billing (don't retry)");
  if (statusCode === 429) throw new Error('Rate limit — reduce concurrency or switch to async');
  if (statusCode === 500) throw new Error('Failed after ScraperAPI retried for 70s (not charged) — retry; on protected sites add premium or ultra_premium');
  throw new Error(`ScraperAPI ${statusCode}: ${body.slice(0, 200)}`);
}
```

`Promise.race` stops waiting but doesn't cancel the underlying request.

Status codes: 200 success, 400 malformed request, 401 bad key, 403 credits exhausted or `max_cost` exceeded (don't retry), 404 not found (target, charged),
429 concurrency limit, 500 failed after 70s of retries (not charged — retry, then escalate to premium/ultra_premium on protected sites).

## Credit Cost Reference

| Request type | Credits |
|---|---|
| Standard | 1 |
| `render: true` | 10 |
| `premium: true` | 10 |
| `premium: true` + `render: true` | 25 |
| `ultra_premium: true` | 30 |
| `ultra_premium: true` + `render: true` | 75 |

Those are the costs on a normal site. Some sites cost more per request:

| Site | Credits |
|---|---|
| Amazon, Walmart, eBay | 5 |
| Google, Bing (all subdomains) | 25 |
| LinkedIn | 30 |
| Sites behind Cloudflare, DataDome, PerimeterX or Akamai | 10 |

Combined costs vary by site; check the exact price with `/account/urlcost` or the `sa-credit-cost` header before a large run. Add `max_cost: N` to any request's options to cap what it can spend (ScraperAPI returns 403 instead).

You're charged for `200` and `404` responses, and for requests you cancel before ScraperAPI's 70s
of retries finish. Each response's `sa-credit-cost` header shows what it cost; preview a cost
without spending credits with `GET https://api.scraperapi.com/account/urlcost?api_key=...&url=...`
(it accepts the same parameters). Source: https://docs.scraperapi.com/getting-started/quick-start/credits-and-requests-costs

## Documentation

- [Node.js SDK getting started](https://docs.scraperapi.com/nodejs)
- [SDK method reference](https://docs.scraperapi.com/nodejs)
- [API status codes](https://docs.scraperapi.com/nodejs/handling-and-processing-responses/api-status-codes)
- [Account information](https://docs.scraperapi.com/nodejs/account-information)
- [Dashboard & credits](https://dashboard.scraperapi.com/)
