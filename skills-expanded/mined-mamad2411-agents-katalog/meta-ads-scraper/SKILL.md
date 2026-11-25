---
name: meta-ads-scraper
description: >
  Discover DTC / e-commerce brands running video ads on Meta (Facebook/Instagram) via the ColdIQ
  marketplace Meta Ads endpoint, to expand Target Account Lists. Use when building net-new DTC/
  e-commerce/subscription prospect lists, finding brands spending on Meta video ads, discovering
  companies in a vertical (baby, jewelry, wine, supplements), or finding companies with active
  creative teams. Triggers on "Meta ads", "Facebook Ad Library", "find DTC brands", "scrape ads",
  "ecommerce prospect list", "brands running video ads", "ad library search". Do NOT use for
  LinkedIn ads (use the linkedin-ad-library endpoint), firmographic database search (see
  apollo-search / coldiq-search-enrich), or contact enrichment (see contact-enrichment).
---

# Meta Ad Library Search

Find brands actively running video ads on Meta — a strong signal of marketing budget + digital
maturity — and turn them into net-new accounts for DTC/e-commerce clients.

This replaces any local Playwright/SQLite Meta scraper with ColdIQ's async Meta Ads endpoint — no
local browser, no database to maintain. The valuable part — the 135-term search strategy — is
preserved below as the query set you submit.

## ColdIQ Marketplace Endpoints

| Task | Method | Path | Credits | Endpoint ID | Notes |
|------|--------|------|---------|-------------|-------|
| Start a Meta Ads search | POST | `/v1/meta-ads/search` | flat | `meta_ads.search.create` | Async; returns `jobId` |
| Get search results | GET | `/v1/meta-ads/search/{jobId}` | free | `meta_ads.search.result` | 202 running, 200 done |

## How to run

For each search term, submit a job and poll for results (see
[resources/async-job-pattern.md](resources/async-job-pattern.md)):

1. Submit one keyword/term (or URL).
   → **POST** `/v1/meta-ads/search` · flat · `meta_ads.search.create`
   ```json
   { "query": "shop now free shipping", "country": "US" }
   ```
2. Poll until done, then read the ads.
   → **GET** `/v1/meta-ads/search/{jobId}` · free · `meta_ads.search.result`

Iterate over the term set below (one job per term), accumulate brands, then de-dup.

## Search strategy — 135 terms across 4 phases

Key insight: **universal DTC ad language beats niche product keywords.** A jewelry, baby, and
supplements brand all run "shop now free shipping". A brand with **10+ video ads** = real ad
operation (budget + creative team + performance-marketing leadership).

- **Phase 1 — Universal DTC video hooks (35, US):** "shop now free shipping", "use code save",
  "subscribe and save", "limited time offer", "before and after results", "real customers real
  results", "try risk free", "as seen on shark tank", "best selling", "clinically proven results",
  "watch what happens", "I tried this", "honest review", "game changer product", "why everyone is
  switching", "claim your free sample", "exclusive offer today only", "save 20 percent", "first
  order free", "bundle and save", "selling out fast" …
- **Phase 2 — Gap verticals (47, US):** Baby & Parenting (baby essentials, nursery must haves,
  toddler snacks, diaper subscription, postpartum, maternity wear, baby food organic, kids vitamin
  gummies…); Jewelry & Accessories (fine jewelry, engagement ring, personalized jewelry, dainty
  jewelry, birthstone, mens jewelry…); Wine & Spirits (wine delivery, craft spirits, tequila, wine
  club, natural wine, mezcal, hard seltzer, non alcoholic spirits…); Dairy & Alt-Dairy (oat milk,
  plant based milk, greek yogurt, cheese subscription, grass-fed butter, kefir probiotic…).
- **Phase 3 — Brand-adjacent signals (33, US):** subscription box, curated subscription, auto ship,
  member exclusive; just launched new brand, DTC brand launch, founder story, small batch artisan;
  free returns, BOGO, flash sale, new arrivals, trending now; valentine/mothers day/fathers day/
  holiday gift guide/summer essentials.
- **Phase 4 — Canada (20, CA):** rerun the top Phase 1–3 terms targeting Canada.

## After scraping — next steps

1. **De-dup** discovered brands (see [list-dedup](../list-dedup/SKILL.md)).
2. **Resolve & enrich** each brand: domain → company LinkedIn → firmographics
   (see [coldiq-search-enrich](../lima-data-api/SKILL.md), [contact-enrichment](../contact-enrichment/SKILL.md)).
3. **Score** against the client ICP (see [tam-scoring](../tam-scoring/SKILL.md)).
4. **Pull contacts** for qualified companies, then load to a campaign (see [instantly-api](../instantly-api/SKILL.md)).

## Quality notes

- Filter to brands with **10+ video ads** for serious ad operations; lower the threshold (5+) for
  smaller verticals.
- Advertiser names from Meta need cleanup before enrichment (strip "LLC", emoji, store suffixes).
- A brand with many ads but no resolvable domain is usually a marketplace seller — deprioritize.
