---
name: seo-technical-audit
description: Focused one-shot technical SEO audit for a domain. Crawlability, indexability, security, mobile, structured data, JS rendering — single-pass deliverable, not a diff. Distinct from `seo-drift` (which tracks changes over time) and from `seo-page` (which audits keywords/traffic for one URL, not technical health). Use when the user asks "technical audit", "site audit", "audit my site", "crawl issues", "indexation issues", or "technical SEO check".
---

> Example output: [examples/seo-technical-audit-linear-app-20260514/TECH-AUDIT.md](../../examples/seo-technical-audit-linear-app-20260514/TECH-AUDIT.md)

# Technical Audit

A one-shot technical SEO audit for a domain. Discovers the URL set (XML sitemap / GSC indexed pages / DataForSEO top pages), loops DataForSEO On-Page checks over it, layers GSC indexation + sitemap truth and field Core Web Vitals, categorizes findings by area (crawlability, indexability, security, mobile, structured data, etc.), severity-sorts within each, and produces a top-10 fix list ranked by impact × effort.

The audit has a single canonical path: a **single-page fast path** (`on_page_instant_pages` + `on_page_lighthouse`) when the target is one URL, and a **full-site path** that loops those same On-Page tools over a capped, traffic-weighted URL set discovered from the sitemap, GSC, and DataForSEO. There is no hosted multi-page crawler — the crawl is rebuilt from tools the user already has.

## Prerequisites

- DataForSEO MCP server connected.
- GSC (`mcp__gscServer__*`) recommended — it's the authoritative source for indexation status and sitemap ingestion truth on the user's own verified property. Firecrawl optional — for URL discovery (`firecrawl_map`) and raw HTML / JSON-LD where attributes matter.
- Claude's `WebFetch` tool available (used for sense-checking robots.txt and sitemap presence, and as a fallback URL-discovery / HTML source when Firecrawl is absent).
- User provides: a target domain (e.g. `example.com`). Optional: target country (default `us`), URL-ceiling override (default: top ~50–100 pages by traffic for large sites).

> *Optional accelerator:* if you have a hosted-crawl MCP you can substitute it for the URL-discovery + per-page fetch loop (steps 1–2) — not required.

## Process

1. **Validate target & preflight.** See `skills/seo-firecrawl/references/preflight.md` for the canonical 3-stage preflight (cost note, Firecrawl availability, Google APIs). Skill-specific notes:
   - Normalise domain (strip protocol, trailing slash) before continuing.
   - DataForSEO bills per call; looping `on_page_instant_pages` over a whole large site is the most expensive operation here. Cap to a documented top-N ceiling (default ~50–100 pages chosen by GSC/DataForSEO traffic + a sitemap sample) and say so in the deliverable. Use the documented `limit`/`ceiling` params to cap DataForSEO On-Page calls.
   - Firecrawl: optional. When available, step 8 (Modern signals checklist) runs on 5 sample URLs and `/robots.txt`, ~6 Firecrawl credits (hard cap). Without it, step 8 is skipped — JS-render canonical/noindex divergence, X-Robots-Tag headers, and AI-crawler robots-rule analysis are unavailable but the full technical-audit deliverable still ships. Pass `--no-firecrawl` to skip step 8 even when Firecrawl is available (saves credits).
   - Google APIs: tier 0 unlocks step 8b (CrUX field data); tier 1 also unlocks step 8c (per-URL GSC Inspection on top 5 traffic pages). See `skills/seo-google/references/cross-skill-integration.md` § "seo-technical-audit" for the full recipe and per-tier branches.

2. **Discover the URL set** (what to audit)
   - **Single-page fast path.** When the target is one URL (not a full domain), skip discovery and run `mcp__dataforseo__on_page_instant_pages` + `mcp__dataforseo__on_page_lighthouse` on that URL — single-page On-Page checks, then jump to step 7.
   - **Full-site path.** Build the URL set from any combination of:
     - **XML sitemap** — `mcp__firecrawl-mcp__firecrawl_map` (or `WebFetch` + parse `/sitemap.xml`, recursing sitemap-of-sitemaps). The declared page inventory.
     - **GSC indexed pages** — `mcp__gscServer__get_search_analytics` with `dimensions=["page"]` — the pages Google actually indexes, each with clicks/impressions for traffic-weighting.
     - **DataForSEO top pages** — `mcp__dataforseo__dataforseo_labs_google_relevant_pages` — top pages by estimated traffic.
   - Union the lists, dedupe, and **cap to a top-N ceiling** (default ~50–100 pages, biased toward GSC/DataForSEO traffic + a sitemap sample). State the ceiling in the deliverable.

3. **Per-page technical fetch** `mcp__dataforseo__on_page_instant_pages` (looped)
   - Loop `on_page_instant_pages` over the capped URL set. Each call returns status code, redirects, meta/title, headings, canonical, hreflang, structured-data presence, internal/external links, and resource counts.
   - Use `mcp__dataforseo__on_page_content_parsing` for main-content extraction where thin-content / duplicate checks need the body text.
   - Run `mcp__dataforseo__on_page_lighthouse` for lab CWV on the key pages only (homepage + top traffic pages — it's heavier per call).
   - This looped output is the audit's raw crawl: aggregate it by the skill into top-line metrics (pages fetched, health score derived from issue counts, total issues by severity) and per-category issue buckets (crawlability, indexability, mobile, security, structured data, content).

4. **Derive per-issue page lists** (from step 3 fields + GSC)
   - For each significant issue (severity ≥ medium, count ≥ 5), list the affected URLs straight from the `on_page_instant_pages` fields (e.g. pages with a `noindex` robots directive, a non-self canonical, a missing `<title>`, a redirect chain).
   - Enrich indexability buckets with `mcp__gscServer__check_indexing_issues` (coverage-state errors Google reports that the On-Page fetch can't see).
   - This produces the actionable fix list.

5. **Cross-reference key URLs** (aggregate per-URL from step 3)
   - For the top 5 pages by traffic (from `mcp__gscServer__get_search_analytics` clicks, or `mcp__dataforseo__dataforseo_labs_google_relevant_pages`, or homepage + key landing pages if no traffic data), collect all issues for those specific URLs from the looped `on_page_instant_pages` results.
   - This catches cases where one important page concentrates many issues.

5b. **Indexation & sitemap truth (GSC)** `mcp__gscServer__*`
   - Indexation: `mcp__gscServer__inspect_url_enhanced` / `mcp__gscServer__batch_url_inspection` on the top traffic pages (indexed? coverage state? Google-chosen vs user canonical?) — see step 8c for the detailed branch.
   - Sitemap status: `mcp__gscServer__get_sitemaps` / `mcp__gscServer__list_sitemaps_enhanced` / `mcp__gscServer__get_sitemap_details` (what Google ingested, error/warning counts). Surface ingestion errors in the Crawlability category.

6. **Sense-check** `WebFetch`
   - Fetch `/robots.txt` and `/sitemap.xml` directly.
   - Confirm the audit's findings match reality on these critical files (audits sometimes lag behind same-day deploys).
   - **Extended security headers.** WebFetch the homepage and 3 sample URLs (top-traffic landing pages from step 5, fall back to homepage + key landing pages if no keyword data); read response headers and flag any of:
     - `csp_missing` — `Content-Security-Policy` absent.
     - `xframe_missing` — `X-Frame-Options` absent (informational; CSP `frame-ancestors` supersedes).
     - `xcontent_missing` — `X-Content-Type-Options` not set to `nosniff`.
     - `referrer_policy_missing` — `Referrer-Policy` absent.
     - `hsts_no_preload` — `Strict-Transport-Security` present but `preload` directive missing AND domain not on the Chromium HSTS preload list.
   - Map findings via `references/severity-mapping.md` § Security and surface in `evidence/02-issues-by-category/security.md` (and inline into TECH-AUDIT.md's "By category → Security" section).

7. **Categorize and prioritize** using `references/severity-mapping.md`
   - Map each issue code to severity, fix, and effort estimate.
   - Score each finding: severity × affected-page-count / effort.
   - Build the top-10 fix list.

8. **Modern signals checklist** `mcp__firecrawl-mcp__firecrawl_scrape`
   - The `on_page_instant_pages` fetch doesn't execute JS and doesn't expose every response header per page. This step surfaces what's invisible to it.
   - **If Firecrawl available** (~6 Firecrawl credits, hard cap): pick 5 sample URLs from the audit — bias toward high-traffic landing pages and pages already flagged with noindex / canonical issues. For each:
     - **JS-rendered canonical vs initial-HTML canonical (`js_canonical_mismatch`).** Compare `metadata.canonical` (after JS render) against the canonical the audit recorded. Flag any divergence — per Google's Dec-2025 JavaScript SEO guidance, when a canonical in raw HTML differs from one injected by JS, Google MAY use either one, making canonical decisions non-deterministic. JS-injected canonical changes silently break indexing on JS-heavy sites.
     - **JS-rendered noindex.** Check `metadata.robots` for `noindex` after render. Catches client-side-only `noindex` injection that the audit can't see.
     - **X-Robots-Tag header.** Read response headers from `metadata`. Flag any `noindex` / `nofollow` / `none` directives at the HTTP layer.
     - **Dec-2025 JS-SEO risk detection** (Google's December 2025 JavaScript SEO guidance — four risks the static crawler cannot detect):
       - **Risk 1 — Rendering-budget cuts (`js_render_budget`).** Compare initial-HTML body size to rendered-HTML body size. Flag pages where rendered HTML is <50% of initial HTML size after JS execution — indicates Google may exhaust its render budget before the page's actual content loads.
       - **Risk 2 — Hydration mismatch.** Already detected above via `js_canonical_mismatch`; rationale: per the Dec-2025 guidance Google may pick *either* canonical, so any drift is a real-world ranking risk, not just a tidiness issue.
       - **Risk 3 — CSR pitfalls (`js_csr_meta_drift`).** Diff initial-HTML `<title>`, `<h1>`, and `<meta name="description">` against the same fields in the JS-rendered DOM. Flag any divergence — Google does not reliably index content that only appears post-render, so the empty/wrong initial values may be what gets indexed.
       - **Risk 4 — Soft-404 from JS errors (`js_soft_404`).** Flag rendered pages where body text content is <500 chars but the HTTP response status is 200. This pattern indicates a JS render failure that Google treats as a soft-404 — the page returns 200 (so it's "live") but contains no real content (so it's "empty").
     - Then make one additional call: `firecrawl_scrape` on `/robots.txt` (1 credit). Parse for AI-crawler User-Agent rules — `GPTBot`, `ClaudeBot`, `PerplexityBot`, `Google-Extended`, `ChatGPT-User`, `Bytespider`, `CCBot`. Surface allow/disallow scope per agent.
   - **If Firecrawl unavailable:** skip this step. Note in `TECH-AUDIT.md`: `Modern signals (JS canonical/noindex divergence, X-Robots-Tag, AI-crawler robots.txt rules, Dec-2025 JS-SEO risks): skipped — Firecrawl not installed.`

8b. **CWV field data via CrUX** *(only if google-api.json is present, tier ≥ 0)*
   - The looped `on_page_lighthouse` reports lab-only CWV (Lighthouse-flavoured estimates). CrUX returns actual Chrome user p75 metrics — the data Google ranks against.
   - Run `python3 scripts/pagespeed_check.py "https://{domain}" --crux-only --json` for current p75 LCP / INP / CLS / FCP / TTFB.
   - Run `python3 scripts/crux_history.py "https://{domain}" --origin --json` for the 25-week trend per metric (improving / stable / degrading).
   - If CrUX has no field data ("insufficient data"), surface that and continue — low-traffic origins are common.
   - Surface in `TECH-AUDIT.md` as a new section "## Core Web Vitals (field data)" with current p75 + trend per metric, source labelled "CrUX 28-day origin".

8c. **Per-URL indexation status via GSC URL Inspection** *(only if google-api.json is present, tier ≥ 1)*
   - For each of the top 5 traffic pages identified in step 5 (or homepage + key landing pages if no keyword data), run:
     `python3 scripts/gsc_inspect.py "{url}" --site-url "{config.default_property}" --json`
   - Capture `indexStatusVerdict`, `coverageState`, `googleCanonical` (vs `userCanonical`), and `lastCrawlTime` per URL.
   - **Cross-check against the On-Page noindex / canonical findings.** If GSC reports `INDEXED` but the On-Page fetch flagged `noindex`, the fetch is stale or the directive was added recently — flag for re-audit. If GSC reports `EXCLUDED` for a page the On-Page fetch treats as healthy, that's a hidden indexability issue the per-page fetch can't see.
   - **Critical-issue elevation:** any `userCanonical ≠ googleCanonical` divergence on a top-traffic page is added to the Top-10 fix list at Critical severity regardless of `severity-mapping.md`'s default — Google having decided on a different canonical is a real-world ranking problem.
   - If the property isn't verified in GSC for this account, surface "GSC: {domain} not verified — add it in Search Console" and skip 8c only.
   - Surface in `TECH-AUDIT.md` as a new section "## Indexation reality check (GSC URL Inspection)" with one row per top-5-traffic URL: status / canonical-divergence / last-crawled.
   - See `skills/seo-google/references/cross-skill-integration.md` § "seo-technical-audit" for the full recipe and failure modes.

8d. **IndexNow detection** `WebFetch`
   - Detection logic — IndexNow advertises its key one of three ways. Check in this order:
     1. **robots.txt hint:** look in the already-fetched `/robots.txt` (step 6) for an `IndexNow:` directive or a comment referencing the key file path.
     2. **Response header hint:** scan response headers from the homepage WebFetch (step 6) for `x-indexnow-key`, `x-indexnow`, or `x-indexnow-key-location`.
     3. **Conventional path probe:** WebFetch `/<key>.txt` if a key was hinted in (1) or (2). If neither hint exists, additionally probe a small set of conventional locations only when the user's domain has signalled IndexNow elsewhere (e.g. Bing Webmaster integration disclosed in robots.txt).
   - Map findings via `references/severity-mapping.md` § IndexNow:
     - No key advertised anywhere → `indexnow_no_key` (Low; informational — Bing-only benefit).
     - Key advertised but `/<key>.txt` content ≠ advertised key → `indexnow_key_mismatch` (Medium).
     - Key file present and matches but no recent submissions detected → `indexnow_not_submitted_recently` (Low; informational).
   - Detect last-key-rotation date when possible: WebFetch the key file and read the `Last-Modified` response header (or fall back to the file's `Date` header).
   - Surface in `evidence/02-issues-by-category/security.md` (or a new `evidence/02-issues-by-category/indexnow.md` if findings are non-trivial; either way, fold into TECH-AUDIT.md's "By category" section) and add a row to the `TECH-AUDIT.md` Modern signals section showing IndexNow status: configured (Y/N) and last-key-rotation date if detectable.

9. **Synthesise** `TECH-AUDIT.md`

## Output format

Create a folder `seo-technical-audit-{target-slug}-{YYYYMMDD}/` with:

```
seo-technical-audit-{target-slug}-{YYYYMMDD}/
├── TECH-AUDIT.md                       (synthesised top-10 fix list + category summary — primary deliverable; inlines 01-audit-summary header + the six 02-issues-by-category/* tables under "By category")
├── issues.csv                          (every issue: code, severity, count, fix, effort — load-bearing CSV engineering pastes into Jira)
├── 03-key-pages-issues.md              (top 5 traffic pages, all their issues — load-bearing reference engineering / on-call consult per-URL)
└── evidence/
    ├── 02-issues-by-category/          (raw per-category tables — preserved in case a reader wants the unmerged view)
    │   ├── crawlability.md
    │   ├── indexability.md
    │   ├── security.md
    │   ├── mobile.md
    │   ├── structured-data.md
    │   └── content.md
    ├── 04-robots-sitemap-snapshot.md   (raw fetched files — preserved for reproducibility)
    └── 05-modern-signals.md            (JS-render canonical/noindex divergence, X-Robots-Tag, AI-crawler rules — requires Firecrawl)
```

Top-level: `TECH-AUDIT.md` + `issues.csv` + `03-key-pages-issues.md`. The audit summary header (`01-audit-summary`) is already in TECH-AUDIT.md's header; the six per-category tables (`02-issues-by-category/*.md`) are inlined under TECH-AUDIT.md's "By category" section. The raw category files, robots/sitemap snapshot, and modern-signals dump live under `evidence/` for reproducibility.

`TECH-AUDIT.md` follows this shape:

```markdown
# Technical Audit: {domain}

> Audit date {YYYY-MM-DD} · Pages crawled: {n} · Health score: {n}/100

## Summary

| Severity | Count |
|---|---|
| Critical | {n} |
| High | {n} |
| Medium | {n} |
| Low | {n} |

## Top 10 fixes (impact × effort)

| Rank | Issue | Severity | Pages | Fix | Effort |
|---|---|---|---|---|---|
| 1 | {issue name} | {severity} | {n} | {one-line fix} | {S/M/L} |
| ... |

## By category

### Crawlability ({n} issues)
- {issue name} ({n} pages) — {fix}
- ...

### Indexability ({n} issues)
- ...

### Security ({n} issues)
- ...

### Mobile ({n} issues)
- ...

### Structured data ({n} issues)
- ...

### Content ({n} issues)
- ...

### Modern signals ({n} findings — Firecrawl)
- {URL} — initial-HTML canonical `{X}` differs from JS-rendered canonical `{Y}` (`js_canonical_mismatch`)
- {URL} — JS-rendered `noindex` not visible to static crawler
- {URL} — `X-Robots-Tag: noindex` at HTTP layer
- {URL} — rendered HTML <50% of initial HTML size (`js_render_budget` — Google may stop rendering before content loads)
- {URL} — title / H1 / meta description differ between initial HTML and post-render DOM (`js_csr_meta_drift`)
- {URL} — rendered body <500 chars but HTTP 200 (`js_soft_404` — likely JS render failure, treated as soft-404 by Google)
- robots.txt — `GPTBot`: {allow / disallow `/path`}, `ClaudeBot`: {…}, `Google-Extended`: {…}, ...
- IndexNow — configured: {Y/N} · key-file: `/<key>.txt` {found / missing / mismatch} · last-key-rotation: {YYYY-MM-DD or "unknown"}
- (Or: `Modern signals: skipped — Firecrawl not installed`)

### Security headers (extended — WebFetch)

| Header | Homepage | Sample 1 | Sample 2 | Sample 3 | Issue |
|---|---|---|---|---|---|
| Content-Security-Policy | {present/absent} | … | … | … | `csp_missing` if absent |
| X-Frame-Options | {present/absent} | … | … | … | `xframe_missing` if absent (informational; CSP frame-ancestors supersedes) |
| X-Content-Type-Options | {`nosniff`/absent/other} | … | … | … | `xcontent_missing` if not `nosniff` |
| Referrer-Policy | {present/absent} | … | … | … | `referrer_policy_missing` if absent |
| HSTS preload | {preload directive Y/N · on Chromium preload list Y/N} | … | … | … | `hsts_no_preload` if not on list |

## Core Web Vitals (field data — CrUX)

| Metric | p75 (current) | 25-week trend | Threshold | Status |
|---|---|---|---|---|
| LCP | {n} ms | {improving/stable/degrading} | ≤2500 ms good · ≤4000 ms needs improvement | {pass/warn/fail} |
| INP | {n} ms | … | ≤200 ms good · ≤500 ms needs improvement | … |
| CLS | {n} | … | ≤0.1 good · ≤0.25 needs improvement | … |
| FCP | {n} ms | … | ≤1800 ms good · ≤3000 ms needs improvement | … |
| TTFB | {n} ms | … | ≤800 ms good · ≤1800 ms needs improvement | … |

Source: CrUX 28-day origin. If insufficient field data: "CrUX: insufficient data for {domain} (low-traffic origin)."
(Or: `CWV (field data): not configured — run `bash extensions/google/install.sh` for setup.`)

## Indexation reality check (GSC URL Inspection)

| URL | Status | userCanonical → googleCanonical | Last crawled |
|---|---|---|---|
| {top-traffic URL 1} | {INDEXED|EXCLUDED|...} | {URL} {→ different URL if divergent} | {YYYY-MM-DD} |
| {top-traffic URL 2} | … | … | … |
| ... |

Source: GSC URL Inspection (Tier 1). If property not verified: "GSC: {domain} not verified — add it in Search Console."
(Or: `Indexation reality check: not configured (Tier 1 setup required).`)

## Key-page deep dives

### {URL with most issues}
{n} issues found. Top fixes:
1. ...
2. ...

## Recommended cadence
Re-run this skill monthly to catch regressions, or wire `seo-drift` to baseline + diff between audits.
```

`issues.csv` columns: `category,issue_code,issue_name,severity,affected_pages,suggested_fix,effort,priority_score`

## Tips

- DataForSEO allows up to 2,000 calls/min, 30 concurrent. Skills pace sequentially.
- The looped `on_page_instant_pages` fetch is the most expensive operation — cap to the documented top-N ceiling (default ~50–100 pages) and lead with the highest-traffic pages so the budget is spent where impact is highest.
- Looping On-Page over a large URL set takes time (one call per page, sequential). Lead with GSC/DataForSEO top-traffic pages so the most important pages are covered first even if you trim the tail.
- The severity scale comes from the DataForSEO On-Page issue signals (not arbitrary) — see `references/severity-mapping.md` so impact × effort scoring is consistent run-to-run.
- For sites with >10k pages, audit critical sections separately (scope the discovered URL set to one path prefix) rather than fetching the whole site every time.
- Pair with `seo-drift` for regression tracking: this skill is the snapshot, drift is the diff.
- Pair with `seo-sitemap` for orphan/missing-page analysis (it consumes this skill's audit data).
- Don't auto-apply fixes. The skill diagnoses; humans decide which fixes to ship and in what order.
