---
name: scraperapi-zapier
description: >
  Guide users to build Zaps that use the official ScraperAPI Zapier
  integration. Use this skill whenever the user wants to add web scraping,
  SERP data, or e-commerce data to a Zapier workflow through ScraperAPI —
  even when they don't say "skill" or name the integration. Triggers
  include: "build a Zap that scrapes Amazon prices and emails me", "connect
  ScraperAPI to Zapier", "automate a daily Google search scrape in Zapier",
  "use ScraperAPI in a Zap to enrich new leads from a webhook", "how do I
  add ScraperAPI as a step in my Zap", "Zapier workflow to crawl a site
  with ScraperAPI", "extract data from a URL inside Zapier". Produces a
  step-by-step build guide for the Zap editor, since Zapier integrations
  are assembled in the web UI (not imported as JSON).

  Note: Transmits user-supplied URLs, queries, and page content to
  ScraperAPI.
metadata:
  openclaw:
    emoji: "🟧"
    homepage: https://zapier.com/apps/scraperapi/integrations
---

# ScraperAPI in Zapier — Zap Build Guide

This skill helps you guide a user through building a **Zap** that uses the
official **ScraperAPI** Zapier integration. Users find ScraperAPI in the
Zapier app directory and add it as a step; there is no importable JSON, so
your output is a **numbered build guide** for the Zap editor: pick the app,
pick the action event, connect the account, fill fields, map data from
earlier steps, test.

Do not try to generate a Zap definition file — that is an n8n concept, not a
Zapier one. Zaps are built in the browser. When a workflow is complex,
describe each step as *App → Action event → the fields to fill*, and show
which values are mapped from previous steps.

## The one thing to get right first: ScraperAPI is action-only

The ScraperAPI integration exposes **actions only — no triggers**. A Zap
cannot *start* with ScraperAPI. Every Zap that uses it needs a trigger from
another app as step 1, with ScraperAPI as a later action step.

This is the single most common point of confusion, so lead with it. Pick the
trigger that matches the user's intent:

| The user wants to… | Use this trigger (step 1) |
|--------------------|---------------------------|
| Scrape on a schedule (hourly/daily/weekly) | **Schedule by Zapier** |
| Scrape on demand from an incoming request | **Webhooks by Zapier → Catch Hook** |
| Scrape each row of a list | **Google Sheets / Airtable** (New/Updated Row) |
| Scrape when something happens in another app | that app's native trigger (new email, new form entry, etc.) |
| Just test an action once, no real trigger | **Schedule by Zapier** — its test always returns a record |

If the user says "I want a Zap that scrapes X" without naming a trigger, ask
what should *kick it off*, or default to **Schedule by Zapier** for recurring
jobs and **Webhooks by Zapier (Catch Hook)** for on-demand/enrichment jobs.

## Prerequisites the user must have

1. A Zapier account (any plan; multi-step Zaps need a Starter plan or higher).
2. A ScraperAPI API key from `https://dashboard.scraperapi.com/`.
3. The ScraperAPI app connected in Zapier. The first time they add a
   ScraperAPI action, they click **Connect a new account**, paste the API
   key, and Zapier runs a test request to validate it. A wrong key fails
   with a 401 at connect time. Once connected, the account is reusable
   across all their Zaps.

Users search for **"ScraperAPI"** in the action app picker. If it doesn't
appear, the integration may not yet be public for their account — point them
to `https://zapier.com/apps/scraperapi/integrations`.

## Five actions — pick the right one

| Action (label in the editor) | `key` | Use when |
|-------------------------------|-------|----------|
| **Extract Data From URL** | `dataExtraction` | Fetch any single URL and get its HTML / Markdown / text / parsed JSON. The general-purpose scrape. |
| **Get Structured Data** | `getStructuredData` | Get clean, pre-parsed JSON from a supported site (Amazon, Google, eBay, Walmart, Redfin). No HTML parsing needed. |
| **Create Crawler Job** | `crawlerCreateJob` | Follow links from a start URL across many pages, streaming each page to a webhook. |
| **Get Crawler Job Status** | `crawlerGetJobStatus` | Check progress/counters of a crawler job by its Job ID. |
| **Cancel Crawler Job** | `crawlerCancelJob` | Stop an active crawler job by its Job ID. |

Rule of thumb: **prefer Get Structured Data when the site is supported** — it
returns fields you can map directly, and survives layout changes better than
parsing HTML. Fall back to **Extract Data From URL** (with Render or Premium
if needed) for any other site. Reach for **Create Crawler Job** only when
one-URL-at-a-time would mean many sequential steps.

Exact input fields, help text, and output shapes for every action are in
`references/actions-reference.md`. Read it before describing an action's
fields in detail — the field labels are precise and users match them
verbatim in the editor.

## Action 1 — Extract Data From URL

The workhorse. Give it a **URL** (required); everything else is optional
escalation:

- **Render JavaScript** — turn on when the page loads content via JS (React/
  Vue/infinite-scroll). Costs more credits.
- **Country Code** — lowercase two-letter code (`us`, `uk`, `de`) for
  geo-targeting. Note ScraperAPI uses `uk`, not `gb`, for the United Kingdom.
- **Device Type** — Desktop or Mobile.
- **Premium Proxies** / **Ultra Premium** — escalate for protected sites.
  They are **mutually exclusive** — enabling both fails validation.
- **Output Format** — Markdown / Text / CSV / JSON. Defaults to raw HTML.
  Markdown or Text is much smaller than HTML and easier to feed into an
  email or an AI step downstream.
- **Auto Parse** — return structured JSON for autoparse-supported sites.

Output fields: `url`, `status_code`, `content_type`, `body`. The scraped
content is in **`body`** — map that into the next step.

Escalation ladder (cheapest first): plain → **Render** → **Premium** →
**Premium + Render** → **Ultra Premium**. Start cheap; only escalate if the
page comes back blocked or empty. See credit costs below.

## Action 2 — Get Structured Data

This action uses **dynamic dropdowns** that cascade:

1. **Category** — E-commerce / Search and Insights / Real Estate.
2. **Operation** — the list repopulates based on the category (e.g. choosing
   E-commerce shows Amazon/eBay/Walmart operations).
3. **Operation-specific fields** — appear after an operation is chosen (e.g.
   Amazon Product details reveals an **ASIN** field).

Because the fields are dynamic, tell the user to select Category *then*
Operation first, and the remaining fields will render. The full
Category → Operation → field matrix (with required fields, parameter names,
and endpoint paths) is in `references/structured-data-operations.md`.

Output fields: `category`, `operation`, `status_code`, and **`data`** — the
parsed result. Unlike some integrations, `data` comes back already parsed as
an object, so after one test run Zapier exposes its nested fields (e.g.
`data.pricing`, `data.name`) for mapping downstream. No separate parse step.

Supported operations at a glance:

| Category | Vendor | Operations |
|----------|--------|-----------|
| E-commerce | Amazon | Product details, Search, Offers |
| E-commerce | eBay | Search, Product details |
| E-commerce | Walmart | Search, Category browse, Product details, Reviews |
| Search and Insights | Google | Search, Jobs, News, Shopping, Maps search |
| Real Estate | Redfin | Listings for sale, Listings for rent, Search, Agent profile |

## Actions 3–5 — the Crawler

The Crawler follows links from a starting URL. It does **not** return the
scraped pages to the Zap. **Create Crawler Job** returns a `jobId` and
`status: initiated` immediately; each crawled page is POSTed to a **callback
webhook** as the crawl progresses.

**Create Crawler Job** required fields:

- **Start URL** — where the crawl begins.
- **URL Regex (Include)** — links must match this to be crawled. It is tested
  against the URL *path + query + fragment*, not the full URL, so do **not**
  include the scheme or host. Use `.*` to crawl everything, or `^/blog/` to
  stay in a section. Defaults to `.*`.
- **Callback Webhook URL** — where each page result is sent (see the pattern
  below — this must be a **Catch Hook** in a *separate* Zap).
- Plus **either Max Depth or Crawl Budget** — at least one is required, or the
  job is rejected. Max Depth caps link depth (start URL is depth 0); Crawl
  Budget caps total API credits spent.

Optional fields mirror Extract Data From URL (Render, Country Code, Device
Type, Premium/Ultra Premium, Output Format, Auto Parse).

**Get Crawler Job Status** / **Cancel Crawler Job** each take just the **Job
ID** returned at creation. Status returns `done` / `failed` / `active`
counters.

## How the crawler callback works — the critical gotcha

Crawler results arrive as HTTP POSTs from ScraperAPI's infrastructure, not as
the action's output. Only a **Webhooks by Zapier → Catch Hook** trigger can
receive them, and it **must be a different Zap** than the one that created the
job. You cannot loop the results back into the creating Zap.

```
Zap A (starts the crawl):
  [Trigger] → ScraperAPI: Create Crawler Job
              Callback Webhook URL = <the Catch Hook URL from Zap B>

Zap B (receives each page):
  Webhooks by Zapier (Catch Hook) → process the page → store / notify
```

Build order: create **Zap B** first, copy its Catch Hook URL, then paste that
URL into **Zap A**'s Callback Webhook URL field. Tell the user this sequence
explicitly — it's the number-one crawler mistake.

## Working with the output in later steps

After you add a ScraperAPI action, add the steps that *do something* with the
result. Zapier learns the available output fields from a **test run**, so tell
the user to run the test before mapping fields downstream.

- **Extract Data From URL** → map `body` (and `status_code` to gate on
  success). If `body` is large HTML, set **Output Format = Markdown or Text**
  to shrink it — this matters for email bodies and for AI steps with token
  limits.
- **Get Structured Data** → map the nested `data` fields (e.g.
  `data.pricing`, `data.name`, `data.reviews`).
- Common downstream steps: **Filter by Zapier** (only continue if a price
  changed / status is 200), **Formatter by Zapier** (extract a number, format
  a date), **Google Sheets** (append a row), **Gmail/Slack** (notify), or an
  AI step (summarize the scraped text).

## Common Zap patterns

Match the user's request to one of these before inventing something complex.

### Scheduled monitor — recurring scrape → check → notify

```
Schedule by Zapier (e.g. every day)
  → ScraperAPI: Get Structured Data (Amazon Product details, ASIN = …)
  → Filter by Zapier (only continue if price dropped)
  → Google Sheets (log price history)  and/or  Gmail (alert)
```

Great for price tracking, SERP monitoring, availability checks.

### On-demand enrichment — incoming request → scrape → respond/store

```
Webhooks by Zapier (Catch Hook)
  → ScraperAPI: Get Structured Data or Extract Data From URL
              (URL/query mapped from the webhook payload)
  → Formatter / Filter
  → write to CRM / append to Sheet / Slack
```

Useful for lead enrichment and on-demand lookups. Webhook payload fields are
mapped straight into the ScraperAPI action's input.

### List fan-out — scrape every row of a sheet

```
Google Sheets (New or Updated Row)  [or Airtable]
  → ScraperAPI: Extract Data From URL (URL = the row's URL column)
  → Formatter (pull out the fields you need)
  → Google Sheets (update the same row with results)
```

Zapier runs the action once per triggering row. For large backfills, mind the
per-run credit cost and your plan's task limits.

### Multi-page crawl — two-Zap callback pattern

See "How the crawler callback works" above. Zap A creates the job; Zap B's
Catch Hook receives each page.

## Credit budgeting — warn the user

ScraperAPI charges credits per successful request. A scheduled or list-driven
Zap can burn credits quietly. When a Zap scrapes many URLs per run or runs
frequently, estimate the per-run and monthly cost in your reply.

| Setting | Approx credits per request |
|---------|----------------------------|
| Standard request | 1 |
| Render JavaScript | 10 |
| Premium Proxies | 10 |
| Premium + Render | 25 |
| Ultra Premium | 30 |
| Ultra Premium + Render | 75 |
| Structured Data endpoint | the site's rate: 5 for Amazon/Walmart/eBay, 25 for Google |

Those are normal-site costs. Some sites cost more per request: Amazon, Walmart
and eBay 5, Google and Bing 25, LinkedIn 30, sites behind Cloudflare/DataDome/
PerimeterX/Akamai 10. `200` and `404` responses are charged; failed (`500`)
requests are not. For current pricing, link to
`https://docs.scraperapi.com/getting-started/quick-start/credits-and-requests-costs`.

## Common mistakes — ❌ wrong / ✅ right

### Trying to start a Zap with ScraperAPI

```
❌ Trigger: ScraperAPI …            (no such thing — action-only)
✅ Trigger: Schedule by Zapier → Action: ScraperAPI
```

### Enabling Premium and Ultra Premium together

```
❌ Premium Proxies = Yes  AND  Ultra Premium = Yes   → validation error
✅ Pick one. Ultra Premium is the strongest tier; use it alone.
```

### Country code as `gb` instead of `uk`

```
❌ Country Code = gb        ✅ Country Code = uk   (ScraperAPI uses uk, not gb)
```

`uk`-not-`gb` is a ScraperAPI-wide convention. Case, however, is
endpoint-specific: **Extract Data From URL** and the **Crawler** actions expect
lowercase (`us`, `uk`, `de`), while **Get Structured Data** accepts uppercase
codes (`US`, `GB`, `DE`) as shown in its own field help.

### Crawler with neither depth nor budget

```
❌ Create Crawler Job with Max Depth and Crawl Budget both empty  → rejected
✅ Set at least one — e.g. Max Depth = 2, or Crawl Budget = 5000
```

### Include-regex written against the full URL

```
❌ URL Regex (Include) = ^https://example\.com/blog/
✅ URL Regex (Include) = ^/blog/     (matches path+query+fragment, no host)
```

### Expecting crawler pages back in the same Zap

```
❌ Create Crawler Job → next step reads the crawled pages   (they never arrive)
✅ Zap A creates the job; Zap B (Catch Hook) receives each page POST
```

### Mapping output fields before testing the step

Zapier only knows an action's output fields after a successful **test run**.
Map `body` / `data.*` into later steps only after testing the ScraperAPI step,
or the fields won't be available to pick.

### Huge HTML body downstream

A full HTML `body` can exceed field limits and bloat AI steps. Set **Output
Format = Markdown/Text**, or use **Get Structured Data** where supported.

## When to read what

| If you need… | Read |
|--------------|------|
| Exact input fields, help text, and output shape for an action | `references/actions-reference.md` |
| The full Category → Operation → field matrix for Get Structured Data | `references/structured-data-operations.md` |

## Related skills and ecosystem

- **`scraperapi-n8n`** — same job, different automation platform. Use it when
  the user is in n8n rather than Zapier. It produces importable workflow JSON;
  this skill produces a Zap-editor build guide.
- **`scraperapi-mcp`** — use when the user wants Claude itself to call
  ScraperAPI directly, rather than wiring it into a Zap.
- **`scraperapi-async` / `scraperapi-crawler`** — deeper references for the
  underlying async and crawler products the Zapier actions call.

## Documentation

- ScraperAPI on Zapier: `https://zapier.com/apps/scraperapi/integrations`
- ScraperAPI docs: `https://docs.scraperapi.com/`
- ScraperAPI dashboard (API key): `https://dashboard.scraperapi.com/`
- Zapier — set up an action step: `https://help.zapier.com/hc/en-us/articles/8496257774221-Set-up-your-Zap-action`
- Zapier — Webhooks by Zapier (Catch Hook): `https://help.zapier.com/hc/en-us/articles/8496288690317-Trigger-Zaps-from-webhooks`
