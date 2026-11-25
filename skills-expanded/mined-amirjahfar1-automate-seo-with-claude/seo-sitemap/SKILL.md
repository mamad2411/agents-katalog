---
name: seo-sitemap
description: Pull a domain's XML sitemap (and sitemap-of-sitemaps), then compare against what's actually crawled/indexed (GSC indexed pages + a DataForSEO On-Page fetch loop + GSC sitemap ingestion). Surfaces (a) sitemap entries the crawler couldn't find (orphans from the sitemap), (b) crawled/indexed pages missing from the sitemap (probably an oversight), (c) sitemap entries that are now 404, (d) lastmod inconsistencies. Use when the user asks for "sitemap analysis", "check my sitemap", "sitemap vs audit", "missing pages", "orphan pages", or "sitemap health".
---
> Example output: [examples/seo-sitemap-notion-so-20260514/SITEMAP.md](../../examples/seo-sitemap-notion-so-20260514/SITEMAP.md)

# Sitemap Analysis

Compare a domain's XML sitemap against what's actually crawled and indexed — GSC indexed pages (`get_search_analytics` dimensions=["page"]), GSC sitemap ingestion (`get_sitemap_details`), and a DataForSEO `on_page_instant_pages` fetch loop over the declared/indexed URL set. Surface what the sitemap claims vs what's really reachable, in both directions.

## Prerequisites

- DataForSEO MCP server connected.
- GSC (`mcp__gscServer__*`) recommended — it's the authoritative source for which pages Google indexes and which sitemaps Google ingested (the comparison baseline). Firecrawl optional — for URL discovery (`firecrawl_map`) when the sitemap is missing or suspect.
- Claude's `WebFetch` tool available.
- User provides: a target domain. Optional: the sitemap URL if not at `/sitemap.xml` (auto-discovery from `robots.txt` is attempted first).
- **Predecessor (recommended):** `seo-technical-audit` on this domain — its discovered URL set + On-Page fetch results can be reused as the crawl baseline. Without it, this skill builds its own baseline from GSC indexed pages + an On-Page fetch loop.

> *Optional accelerator:* if you have a hosted-crawl MCP you can substitute it for the URL-discovery + fetch loop — not required.

## Process

1. **Validate target & build the crawl baseline**
   - Normalise the domain.
   - Build the "what's really crawled/indexed" baseline this skill compares the sitemap against:
     - **GSC indexed pages** — `mcp__gscServer__get_search_analytics` with `dimensions=["page"]` (pages Google indexes, with clicks/impressions). Authoritative for the user's own verified property.
     - **DataForSEO On-Page fetch loop** — `mcp__dataforseo__on_page_instant_pages` over the discovered URL set (declared sitemap URLs + GSC indexed pages), capped to a top-N ceiling — gives status code, redirects, indexability, depth signals per page.
     - **DataForSEO top pages** — `mcp__dataforseo__dataforseo_labs_google_relevant_pages` (broader domain page inventory than the sitemap in some cases).
   - If `seo-technical-audit` already ran on this domain, reuse its discovered URL set + On-Page results as the baseline instead of re-fetching.
   - **Firecrawl availability check.** If `mcp__firecrawl-mcp__firecrawl_map` is available, Mode-2 (URL discovery via crawl) is offered when the sitemap is missing or suspect. Cost: ~0.5 Firecrawl credits per URL discovered, hard cap 500 URLs (~250 credits). Without Firecrawl, the skill runs Mode-1 only and notes the gap if Mode-2 was needed. User may pass `--no-firecrawl` to force Mode-1 even when Firecrawl is available (saves credits at the cost of orphan/missing analysis when sitemap is broken).

2. **Build URL lists** `WebFetch` (sitemap) + `mcp__firecrawl-mcp__firecrawl_map` (optional Mode-2)
   - **Mode-1 (default).** Try `https://{domain}/sitemap.xml`. If 404, fetch `/robots.txt` and look for `Sitemap:` directives. For sitemap-of-sitemaps, recursively fetch each child sitemap. Build the canonical URL list from the sitemap.
   - **Mode-2 trigger.** Switch on Mode-2 when (a) no sitemap is reachable, (b) the sitemap returns < 10% of the baseline crawled/indexed page count (GSC indexed pages + On-Page fetch loop), or (c) the user explicitly requests `--discover`. Always surface the trigger and the cost estimate to the user before running Mode-2.
   - **Mode-2 execution** (requires Firecrawl): call `firecrawl_map(url=domain, limit=500)`. The response is the URL list Firecrawl could discover from the homepage and internal linking. Use this list as the "sitemap-equivalent" in step 6 — the diffs run identically, just with discovered URLs in place of declared sitemap URLs.
   - **If Mode-2 is needed but Firecrawl is unavailable:** continue with whatever sitemap data Mode-1 returned (possibly empty). Surface clearly in `SITEMAP.md`: `Mode-2 (Firecrawl URL discovery) needed but Firecrawl not installed — sitemap-vs-audit diffs run on partial data only.`

3. **Pull the crawled/indexed pages** `mcp__gscServer__get_search_analytics` (dimensions=["page"]) + `mcp__dataforseo__on_page_instant_pages` (looped)
   - GSC indexed pages = the URLs Google actually serves. The On-Page fetch loop confirms each URL's status code, redirects, indexability, and depth signals.
   - Together these are "what's really reachable/indexed" — the baseline the sitemap is diffed against.

4. **Pull domain pages** `mcp__dataforseo__dataforseo_labs_google_relevant_pages`
   - Domain-level page inventory (broader than the indexed/fetched set in some cases).

5. **Identify orphan pages** (from internal-link signals)
   - An orphan is a URL with no internal links pointing at it. Derive this from the looped `on_page_instant_pages` results: build the internal-link graph from each page's link list, then flag any indexed/sitemap URL that no other page links to. GSC pages that get impressions but appear in no other page's link set are the highest-confidence orphans.

6. **Compute the four diffs**
   - **Missing from sitemap:** URLs in the baseline (GSC indexed pages + `on_page_instant_pages` status-200 indexable URLs) that don't appear in the sitemap. Probably should be added.
   - **Orphans from sitemap:** URLs in the sitemap that no other page links to (cross-ref the step-5 internal-link graph). The sitemap is the only thing pointing at them — investigate whether they should be linked internally.
   - **Broken sitemap entries:** sitemap URLs that returned non-200 when fetched via `on_page_instant_pages`. Remove from sitemap or fix the URL.
   - **Lastmod issues:** sitemap entries where (a) all `<lastmod>` dates are identical (lazy generation) or (b) `<lastmod>` is older than GSC's `lastCrawlTime` for the page (from URL Inspection) even though the page changed (stale).

7. **Validation**
   - **GSC sitemap ingestion** `mcp__gscServer__get_sitemaps` / `mcp__gscServer__list_sitemaps_enhanced` / `mcp__gscServer__get_sitemap_details` — confirm Google ingested the sitemap and read its error/warning counts (what Google itself flags). Surface ingestion errors alongside the local diffs.
   - URL count <50,000 per file (sitemap protocol limit). Flag if exceeded.
   - Sitemap referenced in `robots.txt`.
   - Encoding: each URL is XML-safe (ampersands escaped, etc.).
   - HTTPS consistency: sitemap URLs match the canonical protocol.
   - **`<lastmod>` is the only optional tag Google still consumes.** Validate it (step 6). `<priority>` and `<changefreq>` have been **explicitly ignored by Google for years** (per [Google's sitemap docs](https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap) — "Google ignores `priority` and `changefreq` values"). Don't validate them; if present, flag as low-signal noise the user can strip to shrink the sitemap.

8. **Synthesise** `SITEMAP.md`

## Output format

Create a folder `seo-sitemap-{target-slug}-{YYYYMMDD}/` with:

```
seo-sitemap-{target-slug}-{YYYYMMDD}/
├── SITEMAP.md                       (synthesised report — primary deliverable)
├── recommended-sitemap-diff.md      (proposed changes: add X, remove Y — load-bearing artefact engineering applies to sitemap.xml)
└── evidence/
    └── source-data.md               (consolidated raw step output: fetched sitemap content, Firecrawl-discovered URLs if Mode-2 ran, GSC indexed-pages + On-Page fetch baseline, GSC sitemap-ingestion details, the four diffs (missing/orphans/broken/lastmod-issues) — preserved for reproducibility)
```

Top-level: `SITEMAP.md` + `recommended-sitemap-diff.md`. The seven raw step files (`01-sitemap-raw`, `01b-firecrawl-discovered`, `02-audit-pages`, `03-missing-from-sitemap`, `04-orphans-from-sitemap`, `05-broken-entries`, `06-lastmod-issues`) are consolidated into a single `evidence/source-data.md` document with the same per-step section headers — a reader who needs to replay the diff has all raw inputs in one file rather than seven.

`SITEMAP.md` follows this shape:

```markdown
# Sitemap Analysis: {domain}

> Sitemap pulled {YYYY-MM-DD} · Crawl baseline {baseline-date}

## Mode

- **Mode-1 (sitemap-vs-audit):** {ran / skipped — no sitemap reachable}
- **Mode-2 (Firecrawl URL discovery):** {ran with {n} URLs / not triggered / triggered but Firecrawl not installed}

## Health summary

| Metric | Value | Status |
|---|---|---|
| Sitemap URLs (Mode-1) | {n} | — |
| Discovered URLs (Mode-2, if ran) | {n} | — |
| Crawled/indexed URLs (200, indexable) | {n} | — |
| Missing from sitemap (probable adds) | {n} | {🔴 if >5%} |
| Orphans from sitemap (probable cuts or link-ins) | {n} | {🟡 if >5} |
| Broken sitemap entries (non-200) | {n} | {🔴 if >0} |
| Lastmod issues | {n} | {🟡 if uniform; 🔴 if stale} |

## Recommended changes

### Add to sitemap ({n} URLs)
- {URL} — indexed in GSC / fetched at status 200, indexable, but absent from sitemap.
- ...

### Remove from sitemap ({n} URLs)
- {URL} — returns {status code}.
- ...

### Investigate (orphan from sitemap, {n} URLs)
- {URL} — in sitemap but not reachable via internal links. Either link from {suggested parent} or remove from sitemap.
- ...

### Fix lastmod ({n} URLs)
- {URL} — lastmod is {date} but GSC last crawled the page on {date} and the page changed since.
- ...

## Validation

- Total URL count: {n} ({✓ under 50k limit | ✗ exceeds — split into sitemap-of-sitemaps})
- Referenced in robots.txt: {✓/✗}
- HTTPS consistency: {✓/✗}
- Encoding: {✓/✗}

## Apply
- See `recommended-sitemap-diff.md` for the proposed sitemap.xml changes.
- After applying, re-run `seo-technical-audit` to refresh the On-Page crawl baseline, then re-run this skill to verify.
```

## Tips

- Run `seo-technical-audit` first to reuse its On-Page crawl baseline, or let this skill build its own from GSC indexed pages + the On-Page fetch loop.
- Re-run after deploys that change page inventory (new content, removed pages, URL restructures).
- Sitemap-of-sitemaps fan-out can be large for big sites — the skill recursively fetches all child sitemaps. For sites with 50+ child sitemaps, fetching dominates runtime; not credit cost.
- `<priority>` and `<changefreq>` are dead signals — Google explicitly ignores both. Don't waste time tuning them; if your sitemap generator emits them, the bytes are pure overhead. `<lastmod>` is still consumed, so keep that one accurate.
- The "investigate orphans" list is often the highest-leverage finding — pages that exist but aren't linked are usually accidentally orphaned, and adding a couple of internal links can revive them.
- Pair with `seo-drift` to track sitemap composition over time (URL count, lastmod patterns).
- Cost: GSC indexed-pages reads are free; reusing `seo-technical-audit`'s already-fetched On-Page results avoids re-fetching. The DataForSEO `on_page_instant_pages` loop and `dataforseo_labs_google_relevant_pages` call bill per call — cap the loop to the top-N ceiling and cap the relevant-pages call with `limit`. Mode-2 adds Firecrawl credits at ~0.5 per discovered URL — surface the estimate before triggering.
