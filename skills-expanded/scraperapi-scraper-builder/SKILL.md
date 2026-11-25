---
name: scraperapi-scraper-builder
description: >
  Build and implement web scrapers using ScraperAPI. Use this skill whenever the user asks to
  build, write, create, or implement a scraper, or wants runnable code that extracts data from
  a website. Trigger on: "build me a scraper for [website]", "write a scraper that fetches
  product pages from [ecommerce site]", "I need to scrape [data] from [website]", "create a
  script that extracts [fields] from [URL]", "help me scrape [website] — I need [fields]",
  "write code to scrape [website]", "make a script that scrapes [website]", "implement a
  scraper for [URL]". Guides architectural decisions (structured endpoint vs. raw HTML, JS
  rendering, proxy tier, sync vs. async batch), then generates a complete runnable Python or
  Node.js script with retry logic, error handling, pagination, and credit estimation.

  Note: Transmits user-supplied queries, URLs, and content to ScraperAPI.
metadata:
  openclaw:
    requires:
      env:
        - SCRAPERAPI_API_KEY
      anyBins:
        - python
        - node
    emoji: "🛠️"
    homepage: https://docs.scraperapi.com/
---

# ScraperAPI Scraper Builder

Build production-quality scrapers using ScraperAPI. Work through four phases: gather requirements, probe the target site, make architecture decisions, then generate a complete runnable script.

## Phase 1 — Gather Requirements

Before writing code, collect the following. Pull from the user's prompt; ask only what is missing.

| Info | Default if not specified |
|------|--------------------------|
| Target URL or website | Required — ask if missing |
| Data fields to extract | Ask if vague ("product info" → which fields exactly?) |
| Volume | Infer: single URL / paginated / bulk list of URLs |
| Language | Ask if not clear from context; Python is a reasonable default |
| Output format | stdout JSON |
| Geo-targeting needed? | Infer from site type; confirm for e-commerce pricing |

---

## Phase 2 — Site Reconnaissance

**Before making any architecture decisions, fetch 1–2 sample pages from the target site using ScraperAPI** to observe actual behavior. This replaces guesswork with evidence and costs at most 2 credits.

### What to fetch

Fetch at most two pages:
1. **A listing or category page** (the main target) — e.g., a product grid, search results, or article index
2. **A detail page** (only if the user needs data from individual items) — e.g., a single product, article, or profile

Always start with a **standard request** (no `render`, no `premium`) — the cheapest probe:

```
GET https://api.scraperapi.com/?api_key=<SCRAPERAPI_API_KEY>&url=<target_url>
```

### What to observe

**1. Response status**

| Status | Meaning |
|--------|---------|
| 200 | Proceed to content analysis |
| 403 + body has "Just a moment", `cf-ray`, or "Cloudflare" | Cloudflare detected |
| 403 + body has "DataDome", "PerimeterX", or "Akamai" | Bot manager detected |
| 403 (generic) | Anti-bot protection present; premium proxies likely needed |
| 429 | Rate limited; note for architecture phase |

**2. Content completeness** (for 200 responses)

Signals that `render=true` will be needed:
- Empty SPA containers: `<div id="root"></div>`, `<div id="app"></div>`, `<div id="__next"></div>` with no children
- Framework markers in `<script>` tags: `_next`, `__nuxt__`, `react`, `vue`, `angular`
- Response is mostly `<script>` and `<div>` tags with little visible text
- Target data fields (from Phase 1) are absent from the HTML

If the target data is visibly present in the raw HTML → standard rendering is sufficient, do not enable `render`.

**3. Pagination structure**

Look for the site's pagination scheme in `<a>` hrefs and link tags:
- `<a rel="next">` or `<link rel="next">` → follow-the-next-link pattern
- `?page=N`, `?p=N`, `/page/N/` in hrefs → page-number pagination
- `?start=N` or `?offset=N` → offset-based pagination
- No pagination links + `data-infinite-scroll` or "Load more" button → JS-driven infinite scroll (requires `render=true`)

Note the exact URL pattern — this feeds directly into the pagination loop in Phase 4.

**4. Data structure** (when target fields are visible)

- Identify the repeating container element (e.g., `<li class="product-item">`, `<div class="listing-card">`)
- Note CSS selectors for each target field from Phase 1
- Check for embedded structured data: `<script type="application/ld+json">` (JSON-LD) or `data-*` attributes — these are often cleaner to parse than raw HTML

**5. Internal API endpoints** (bonus)

Scan inline `<script>` blocks for `fetch(` or `axios.get(` calls pointing to internal paths (e.g., `/api/products`, `/_next/data/`). If found, scraping that JSON endpoint is usually simpler and more stable than parsing HTML.

### Site Profile — output of this phase

Summarize findings as a table before proceeding. Every row maps to a specific decision in Phase 3.

```
| Signal                  | Observed                              |
|-------------------------|---------------------------------------|
| HTTP status (standard)  | 200 / 403 / ...                       |
| Anti-bot protection     | None / Cloudflare / DataDome / ...    |
| JS rendering needed     | Yes / No / Uncertain                  |
| Pagination pattern      | ?page=N / rel=next / load-more / ...  |
| Target data visible     | Yes / No (skeleton HTML)              |
| Data container selector | e.g. div.product-card                 |
| Structured data (LD+J)  | Present / Not found                   |
| Internal API detected   | Yes (<path>) / No                     |
```

---

## Phase 3 — Architecture Decisions

Use the Site Profile from Phase 2 as primary evidence for each decision. Work through all six decisions in order, citing specific observations from the profile. Summarize all decisions as a table (see end of this section) before writing any code.

### Decision 1 — Is there a Structured Data endpoint?

Check if the target site is one of the supported verticals. If yes, use it — structured endpoints return clean JSON with no HTML parsing, and they handle rendering and anti-bot automatically. Skip Decisions 2 and 3.

Supported verticals (verify against [docs](https://docs.scraperapi.com/python/making-requests/structured-data-collection-method)):
- Amazon: `product`, `search`, `offers`, `reviews`
- Google: `search`, `news`, `jobs`, `shopping`, `maps`
- Walmart: `product`, `search`, `category`
- eBay: `product`, `search`
- Redfin: `listing`, `search`
- Indeed: `jobs`, `job`
- LinkedIn: `profile`, `jobs` (availability may vary)

Endpoint pattern: `GET https://api.scraperapi.com/structured/<site>/<type>?api_key=...&<required_param>=...`

### Decision 2 — Does the page require JavaScript rendering?

Enable `render=true` only when the Site Profile confirms that target data was absent in the standard response. Cost: ~10 credits/req.

- Site Profile says "Target data visible: No" or "JS rendering needed: Yes" → enable `render=true`
- Site Profile says "Target data visible: Yes" → do not enable `render=true`
- Site Profile says "Uncertain" → fetch one more sample with `render=true` and compare

Do not enable `render=true` speculatively — the Phase 2 probe is the evidence.

### Decision 3 — Does the site have anti-bot protection?

Use the Site Profile's "Anti-bot protection" row as the starting point. Escalate gradually — never start at the highest tier.

- Site Profile says "None" → start with standard
- Site Profile says "Cloudflare" or any bot manager → start with `premium=true` (~10 credits)
- `premium=true` still returns 403 → escalate to `ultra_premium=true` (~30 credits)

`ultra_premium=true` and `premium=true` are mutually exclusive — never set both.

### Decision 4 — What is the volume?

| Volume | Approach |
|--------|----------|
| 1–10 URLs | Sync loop, no special handling |
| 10–100 URLs | Sync with 1 req/sec rate limiting |
| >100 URLs | Async Jobs API (`POST https://async.scraperapi.com/batchjobs`) |

For async batches, the script submits all URLs, then polls until all jobs complete. See [references/code-templates.md](references/code-templates.md) for the async pattern.

### Decision 5 — Is session state needed?

Add `session_number=<int>` when:
- The scraper must follow a login flow
- Multi-step checkout or auth-gated pages
- Pagination state must be maintained across requests

Pick any integer as the session ID. Requests with the same `session_number` are routed through the same proxy IP.

### Decision 6 — Is geo-targeting needed?

Add `country_code` (ISO-3166, e.g., `us`, `gb`, `de`) when:
- Scraping prices that vary by region
- Target site redirects or blocks based on geography
- SERP results should be localized

### Architecture summary table

Before generating code, print this table:

```
| Parameter      | Value      | Reason                            |
|----------------|------------|-----------------------------------|
| url            | ...        | target                            |
| render         | true/false | (why)                             |
| premium        | true/false | (why)                             |
| ultra_premium  | true/false | (why)                             |
| country_code   | us / –     | (why)                             |
| session_number | N / –      | (why)                             |
| volume mode    | sync/async | (why)                             |
```

---

## Phase 4 — Generate Code

Ask for language if not already known (default: Python). Generate a **complete, runnable script** — not pseudocode or snippets. See [references/code-templates.md](references/code-templates.md) for the base templates to adapt.

Use the Site Profile from Phase 2 to pre-fill the parsing logic: if a data container selector was identified (e.g., `div.product-card`), write it directly into the `extract()` function rather than leaving a TODO. If JSON-LD was found, parse `<script type="application/ld+json">` instead of navigating the HTML tree. If an internal API path was found, target that endpoint instead of the page HTML.

### Python script structure

1. `argparse` CLI with `--url`, `--pages`, `--output`, `--max-credits`, plus flags for all ScraperAPI params decided in Phase 3
2. API key from `os.environ["SCRAPERAPI_API_KEY"]` — never hardcoded
3. `scrape()` function with exponential backoff retry (5 attempts)
4. Status code handling per the error table below
5. Credit estimate printed to stderr before any requests
6. Pagination loop using the pattern identified in the Site Profile, with 1 req/sec rate limit for sync mode
7. `extract()` function pre-filled with selectors from the Site Profile (or a TODO if none were identified)
8. Output as JSON to stdout or `--output` file

### Node.js script structure

Same flags and behavior as above. Use `node-fetch@2` + `commander`. Match the user's existing module format (ESM vs. CommonJS) if known, otherwise default to CommonJS.

### Always include at the top of the generated script

```python
# Requirements: pip install requests  (Python)
# Requirements: npm install node-fetch@2 commander  (Node.js)
# Usage: SCRAPERAPI_API_KEY=your_key python scraper.py --url "https://example.com" --pages 5
```

---

## Credit Cost Reference

| Configuration | Credits per request |
|---------------|---------------------|
| Standard | 1 |
| `render=true` | ~10 |
| `premium=true` | ~10 |
| `ultra_premium=true` | ~30 |
| Structured endpoint | 1–10 (varies by vertical) |

Print a cost estimate before executing: `# Estimated: 50 pages × 10 credits = ~500 credits`

The generated script must include a `--max-credits` flag that aborts if the estimate exceeds the budget.

---

## Error Handling

| Status | Action |
|--------|--------|
| 200 | Parse and return |
| 401 | Abort — invalid API key, do not retry |
| 403 | Retry with `premium=true`; if still blocked, try `ultra_premium=true` |
| 404 | Skip this URL — page does not exist |
| 429 | Exponential backoff and retry; switch to async for large batches |
| 500/503 | Exponential backoff, max 5 attempts |

---

## Validation Checklist

Before presenting the script:

- [ ] Site Profile was produced in Phase 2 and each architecture decision cites it
- [ ] API key is read from `$SCRAPERAPI_API_KEY` env var — not hardcoded
- [ ] Retry logic covers 429, 500, 503 with exponential backoff
- [ ] `--max-credits` guard is present and enforced before the first request
- [ ] Credit estimate is printed to stderr before any requests are made
- [ ] If using a structured endpoint: vertical name matches the cheatsheet exactly
- [ ] If async: script includes polling loop or webhook handling, not just job submission
- [ ] `ultra_premium` and `premium` are not both set
- [ ] Setup instructions comment is at the top of the script
- [ ] A TODO comment marks where the user should add their parsing logic

---

## References

- [references/code-templates.md](references/code-templates.md) — Python and Node.js base templates (sync + async)
- [ScraperAPI docs](https://docs.scraperapi.com/)
- [Structured Data endpoints](https://docs.scraperapi.com/python/making-requests/structured-data-collection-method)
- [Async API](https://docs.scraperapi.com/making-async-requests)
- [Parameter reference](https://docs.scraperapi.com/python/making-requests/customizing-requests)
- [Dashboard](https://dashboard.scraperapi.com/)
