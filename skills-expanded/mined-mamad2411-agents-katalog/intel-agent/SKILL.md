---
name: intel-agent
description: Reconnaissance tool that takes a target URL and desired data points, tests extraction methods (API, JSON-in-HTML, Cheerio, Browser) via proxy-mcp traffic interception, tests protection levels, and outputs a structured intelligence report with per-data-point strategies.
license: MIT
---

# Intel Agent: Data Point Reconnaissance

## When This Skill Activates

Activate when user requests:
- "recon [URL]"
- "intel report for [URL]"
- "find how to extract [data] from [URL]"
- "discover data from [URL]"
- "what's the best way to get [data] from [site]"
- "how would I scrape [data points] from [URL]"

**This skill does NOT implement scrapers.** It discovers extraction methods and outputs a structured intelligence report. For implementation, hand off to the web-scraper skill.

**References** (loaded on demand):
- `reference/tool-reference.md` — Tool signatures, known limitations, important rules
- `reference/data-point-types.md` — Type classification and search strategies per type
- `reference/report-schema.md` — Report output format
- `strategies/cheerio-vs-browser-test.md` — Cheerio vs Browser extraction test procedure
- `strategies/proxy-escalation.md` — Three-tier protection testing procedure

---

## Input Parsing

Extract from the user's request: **Target URL** and **Data points** to extract.

Normalize each data point into a type (text / numeric / boolean / list / nested) with search terms. See `reference/data-point-types.md` for type classification and search strategies.

If data points are NOT specified, ask the user before proceeding.

---

## The Workflow

Six steps, executed sequentially. Each step builds on the previous.

### Step 1: Initialize & Capture Baseline Traffic

```
proxy_start(persistence_enabled: true, capture_profile: "full", session_name: "recon-[domain]-[YYYYMMDD]")
interceptor_chrome_launch(url: "[target URL]", stealthMode: true)
interceptor_chrome_devtools_attach(target_id)
```

Note: `proxy_start` with `persistence_enabled: true` auto-starts a session. A subsequent `proxy_session_start()` will return the existing session (not error), but the cleaner pattern is to pass `session_name` directly to `proxy_start`.

**1a. Capability check** — Inspect the attach response:
- If `"native-fallback mode"` warning: try `interceptor_chrome_devtools_pull_sidecar()`, then detach + re-attach
- If sidecar available → **FULL_MODE**. If still unavailable → **DEGRADED_MODE** (`screenshot()` and `snapshot()` unavailable, Step 2c skipped)

**1b. Capture baseline**:
```
humanizer_idle(target_id, 3000)
interceptor_chrome_devtools_screenshot()   # FULL_MODE only
```

**Record**: Session name/ID, capability mode, page load status, loading behavior (SSR vs SPA), interstitials, framework indicators.

**Dismiss interstitials**: Use the rendered DOM snapshot (if FULL_MODE) or screenshot to identify cookie/popup selectors. `humanizer_click(target_id, "[accept selector]")` then `humanizer_idle(target_id, 1000)`. If the first selector fails, try alternatives. Multiple popups may appear sequentially (e.g., Cloudflare challenge then cookie consent).

### Step 2: Scan Response Bodies for Data Points

For each data point, search three locations to determine extraction methods.

#### 2a. Raw HTML body (Cheerio method)

```
proxy_list_traffic(url_filter: "[target domain]")
proxy_get_exchange(exchange_id)   # main HTML document
```

**Body truncation**: If `bodySize` >> preview length, use `proxy_search_session_bodies(session_id, text: "...", content_type_contains: "html")` to search the full decompressed body. For retrieving the complete body of a specific exchange, use `proxy_get_session_exchange(session_id, exchange_id, include_body: true)`. See `reference/tool-reference.md` Known Limitations. If body is truncated and no full body available, defer to Step 2c or mark **INCONCLUSIVE**.

Search for data point values. If found → **Cheerio works**.

#### 2b. JSON blobs in HTML (JSON-in-HTML method)

Search raw HTML for: `application/ld+json`, `__NEXT_DATA__`, `__INITIAL_STATE__`, `__NUXT__`, `__APOLLO_STATE__`, `__RELAY_STORE__`. Parse and search for data points. If found → **JSON-in-HTML works** (preferred over Cheerio).

#### 2c. Rendered DOM (Browser method)

**FULL_MODE**: `interceptor_chrome_devtools_snapshot()` — search for data points. If found only here → **Browser required**.

**DEGRADED_MODE**: Skip. Mark unfound data points as **INCONCLUSIVE**.

#### 2d. Decision matrix

| Raw HTML? | JSON Blob? | Rendered DOM? | Method |
|-----------|-----------|---------------|--------|
| Yes | — | — | Cheerio |
| — | Yes | — | JSON-in-HTML (preferred) |
| Yes | Yes | — | JSON-in-HTML (preferred) or Cheerio |
| No | No | Yes | Browser required |
| No | No | No | Requires interaction → Step 2e |
| Truncated | — | N/A (DEGRADED) | INCONCLUSIVE |

See `strategies/cheerio-vs-browser-test.md` for the detailed procedure.

#### 2e. Trigger interactions for missing data points

For data points not found: `proxy_clear_traffic()`, interact (scroll, click), `humanizer_idle()`, then re-check DOM + traffic.

#### 2f. Full-page scroll capture (MANDATORY)

Scroll the entire page before API sniffing to capture lazy-loaded API calls:

1. `proxy_clear_traffic()`
2. Scroll 2-3x: `humanizer_scroll(target_id, delta_y: 800)` + `humanizer_idle(target_id, 1500)`
3. **Mid-scroll visual check** (FULL_MODE only): `interceptor_chrome_devtools_screenshot()` — inspect for interstitials (CAPTCHA, cookie consent, PX challenge, modals). If an overlay is detected, dismiss it (`humanizer_click` on the dismiss selector, then `humanizer_idle`) before continuing. If a hard block (CAPTCHA) is detected, stop scrolling and proceed to Step 3 with traffic captured so far.
4. Scroll 2-3x more: `humanizer_scroll(target_id, delta_y: 800)` + `humanizer_idle(target_id, 1500)`
5. `humanizer_idle(target_id, 3000)` — let deferred calls complete
6. `interceptor_chrome_devtools_screenshot()` + `interceptor_chrome_devtools_snapshot()` (FULL_MODE only) — final state
7. `proxy_list_traffic()` — review newly triggered API calls

**MANDATORY** even if all data points already found — lazy APIs often provide better-structured data.

### Step 3: Sniff APIs

#### 3a. Filter existing traffic

```
proxy_list_traffic(url_filter: "/api/")
proxy_list_traffic(url_filter: "/graphql")
proxy_list_traffic(url_filter: "/_next/data/")
proxy_list_traffic(url_filter: "/wp-json/")
proxy_list_traffic(url_filter: ".json")
proxy_search_traffic(query: "application/json")
interceptor_chrome_devtools_list_network(resource_types: ["xhr", "fetch"])
```

#### 3b. Trigger more traffic via interactions

`proxy_clear_traffic()` → interact (pagination, search, filters, detail click, load more, sort) → `humanizer_idle()` → `proxy_list_traffic()`.

#### 3c. Inspect each discovered endpoint

`proxy_get_exchange(exchange_id)` — Record: URL, method, headers, auth, body, response structure, pagination, data points covered, rate limits. See `reference/report-schema.md` Section 4 for the full endpoint template.

### Step 4: Test Protection Levels

See `strategies/proxy-escalation.md` for the detailed procedure.

**Tier 1 (Direct)**: Already tested. Check cookies, status codes, challenges:
```
interceptor_chrome_devtools_list_cookies()
proxy_search_traffic(query: "403")
proxy_search_traffic(query: "challenge")
```

**TLS verification**: `proxy_list_tls_fingerprints(hostname_filter: "[target domain]")`. JA3 varies + JA4 stable = Chrome passthrough. JA3 identical = proxy re-terminates. See `strategies/proxy-escalation.md` for interpretation matrix.

**Tier 2 (Datacenter)**: `proxy_set_upstream("[dc proxy]")` → navigate → compare to baseline.

**Tier 3 (Residential)**: `proxy_set_upstream("[res proxy]")` → navigate → compare.

**Clean up**: `proxy_clear_upstream()`.

| Direct | Datacenter | Residential | Minimum Required |
|--------|-----------|-------------|-----------------|
| OK | OK | OK | Direct |
| Blocked | OK | OK | Datacenter proxy |
| Blocked | Blocked | OK | Residential proxy |
| Blocked | Blocked | Blocked | Residential + stealth + CAPTCHA solving |

### Step 5: Rank Extraction Methods

For each data point, rank available methods. **Priority**: API > JSON-in-HTML > Cheerio > Browser.

Per method include: source details (endpoint/selector/JSON path), required proxy level, confidence (High/Medium/Low).

### Step 6: Generate Intelligence Report

Compile findings into the report format. See `reference/report-schema.md` for the complete structure.

**6a. Export session evidence**:
```
proxy_session_stop()
proxy_export_har(session_id: "[session_id]", output_file: "recon-[domain]-[YYYYMMDD].har", include_bodies: true)
```

Include session name, ID, and HAR path in Section 6 of the report.

---

## What This Skill Does NOT Do

This skill is **pure discovery**. It does NOT write scraping code, create Actors, implement pagination, or deploy anything.

**Handoff**: After generating the report:
```
Intelligence report complete. To implement a scraper based on these findings,
use the web-scraper skill:
  "scrape [data points] from [URL] using the intel report above"
```
