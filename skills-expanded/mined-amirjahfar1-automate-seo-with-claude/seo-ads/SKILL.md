---
name: seo-ads
description: Paid-search competitive landscape for a domain or keyword. Reconstructs the paid footprint keyword-by-keyword from live SERP ad blocks — advertisers, ad copy patterns, who else bids on the same keywords, CPC/competition signals, SERP shopping/ad-pack visibility — and produces a competitive ads brief plus a recommended bid-keyword shortlist. Use when the user asks "paid search analysis", "competitor ads", "PPC competitive", "ad copy intelligence", "shopping pack", "who bids on this keyword", or "paid keyword footprint".
---
> Example output: [examples/seo-ads-hostinger-com-20260514/ADS.md](../../examples/seo-ads-hostinger-com-20260514/ADS.md)

# Paid-Search Intelligence (Ads)

Map the competitive paid-search landscape around a domain's or keyword's target terms, reconstructed keyword-by-keyword from the live SERP ad block. Output: a brief on who is bidding (and on what copy), who else bids on the same terms, ad-copy patterns the leading advertisers use, CPC/competition signals, SERP ad+shopping presence per keyword, and a recommended bid-keyword shortlist.

> **Limitation — read this first.** Domain-level "all keywords a competitor bids on" requires a paid-keyword database. This skill reconstructs the paid footprint keyword-by-keyword from live SERP ad blocks — narrower than a paid-keyword database, but needs no extra subscription. In **domain mode**, you supply (or the skill seeds) the keyword set to probe; the skill cannot enumerate every term a competitor secretly bids on, only what surfaces as ads for the keywords probed.

## Prerequisites

- DataForSEO MCP server connected. (Provides the live SERP ad blocks and Google Ads CPC/competition data the paid landscape is reconstructed from.)
- GA4 already connected (`mcp__google-analytics__*`) for own paid-traffic performance (Paid Search channel).
- User provides: (a) a target domain OR a target keyword (skill detects which), (b) a seed keyword set when in domain mode (the terms to probe — derive from the brand's category/products if the user gives none), (c) target country (default `us`).

## Process

1. **Validate input & preflight**
   - Determine: domain mode (probe a seed keyword set and isolate the target brand's ads) or keyword mode (analyse the bidding landscape for one keyword).
   - In domain mode, assemble the seed keyword set: use the user's list if provided, otherwise derive ~10–20 head terms from the brand's category, products, and homepage. State the seed set explicitly — it defines the footprint this run can see.
   - DataForSEO bills per call; this run issues ~10–25 calls (one SERP call per seed keyword + one volume/CPC batch). Use the documented `limit`/`ceiling` params to cap.

2. **Domain mode — reconstruct paid footprint** `mcp__dataforseo__serp_organic_live_advanced` (per seed keyword) + `mcp__dataforseo__kw_data_google_ads_search_volume`
   - For each seed keyword, call `serp_organic_live_advanced` and read the paid/ad block (`tads`/`bads`) plus the shopping pack (`sads`). Keep only the rows where the target domain is the advertiser.
   - For each such keyword: keyword, ad position, ad copy (title + description), display/destination URL.
   - Enrich every seed keyword with `kw_data_google_ads_search_volume` for search volume, CPC, competition, and competition_index (the bidding landscape).
   - Sort by traffic-weighted score (`volume × CTR-by-paid-position × bid-share`).
   - This is the reconstructed footprint — it covers only the seed keywords probed, not every term the domain bids on (see limitation above).

3. **Keyword mode** `mcp__dataforseo__serp_organic_live_advanced` (read the live paid/ad block) + `mcp__dataforseo__kw_data_google_ads_search_volume`
   - Call `serp_organic_live_advanced` on the target keyword and read every advertiser in the ad block.
   - For each: domain, ad position, ad copy, URL.
   - Surface the top 10 advertisers + their copy patterns. Pull CPC, competition, and competition_index for the keyword with `kw_data_google_ads_search_volume` to quantify the bidding landscape.

4. **Intent enrichment** `mcp__dataforseo__dataforseo_labs_google_keyword_ideas` (filter interrogatives: who/what/why/how/can/does…)
   - For the keyword(s) in scope, mine question-phrased variants.
   - Identifies question-phrased intent variants worth bidding on (often cheaper, higher conversion). Pull their CPC/competition with `kw_data_google_ads_search_volume`.

5. **SERP ad/shopping presence** `mcp__dataforseo__serp_organic_live_advanced`
   - For top 5 keywords (domain mode) or the target keyword (keyword mode):
     - Use SERP-feature filters to detect ad-pack composition: `tads` (top ads above organic), `bads` (bottom ads below organic), `sads` (shopping ads / Google Shopping pack), `mads` (mobile/map-pack ads).
     - Top SERP ad slots (positions 1-4 above organic, 1-3 below).
     - Shopping pack presence (carousel of product cards).
     - Image pack, local pack — these displace ad inventory.
   - Capture which advertisers occupy those slots.

6. **Ad copy pattern analysis**
   - Cluster ad headlines + descriptions by recurring patterns.
   - Identify: USP language used by leaders, pricing/discount mentions, audience segmentation, CTA verbs.
   - Highlight outliers (advertisers doing something different).

7. **Competitor footprint gap (domain mode)** `mcp__dataforseo__serp_organic_live_advanced` (per seed keyword)
   - From the per-keyword ad blocks already collected in step 2, build the advertiser-by-keyword matrix: for each seed keyword, list every advertiser holding an ad slot.
   - Identify the top recurring competitor advertisers (those appearing across the most seed keywords).
   - Diff: seed keywords where competitors hold ad slots but the target domain does not.
   - This becomes the highest-leverage portion of the bid-keyword shortlist (step 8). Note it is scoped to the seed set, not the competitor's full paid footprint.
   - Skip in keyword mode (no domain to gap against).

8. **Own paid performance (own domain only)** `mcp__google-analytics__run_report`
   - When the target domain is the user's own GA4-connected property, pull paid performance from GA4 filtered to the Paid Search channel: sessions, conversions, and (where available) revenue by landing page / campaign. Use `run_conversions_report` for conversion-goal detail.
   - This grounds the bid-keyword shortlist in first-party outcomes (which paid landing pages actually convert), not just SERP-observed competition.
   - Skip when analysing a third-party domain (no GA4 access to it).

9. **Recommended bid-keyword shortlist**
   - For domain mode: footprint gap from step 7 + adjacent question-intent variants, weighted by own paid performance (step 8) where available.
   - For keyword mode: question-intent and long-tail variants that are likely cheaper than the head term.
   - Each row: keyword, est. CPC, est. volume, who else bids, why-recommended.

10. **Synthesise** `ADS.md`

## Output format

Create a folder `seo-ads-{target-slug}-{YYYYMMDD}/` with:

```
seo-ads-{target-slug}-{YYYYMMDD}/
├── ADS.md                              (synthesised brief — primary deliverable; inlines paid footprint, bidding landscape, SERP ad/shopping pack, ad copy patterns, competitor footprint gap)
├── recommended-keywords.csv            (bid-keyword shortlist — load-bearing CSV the PPC team pastes into bid tooling)
└── evidence/
    ├── 01-paid-footprint.md           (domain mode: target's reconstructed paid footprint across seed keywords — raw step output)
    ├── 02-bidding-landscape.md        (keyword mode: advertisers on the keyword — raw step output)
    ├── 03-question-variants.md        (keyword-ideas interrogative enrichment + CPC/competition)
    ├── 04-serp-ad-shopping-pack.md    (SERP feature inventory per keyword)
    ├── 05-ad-copy-patterns.md         (clustered headline/description patterns)
    └── 06-competitor-footprint-gap.md (domain mode: advertiser-by-keyword matrix + gap vs target across seed set)
```

Step files 01, 02, 04, 05, 06 are inlined as sections in `ADS.md`; the copies in `evidence/` preserve the raw step outputs for reproducibility.

`ADS.md` follows this shape:

```markdown
# Paid-Search Intelligence: {target}

> Snapshot dated {YYYY-MM-DD} · Country: {country} · Mode: {domain | keyword}

## Footprint summary
- Paid keywords: {n}
- Estimated paid traffic: {n}/mo
- Average CPC: ${n}
- SERP slots covered: {n} of top-4 above organic across {n} target keywords

## Top 10 paid keywords (domain mode)

| Keyword | Volume | CPC | Position | Ad copy excerpt |
|---|---|---|---|---|
| {kw} | {n} | ${n} | {pos} | "{headline} — {snippet}" |
| ...

## Bidding landscape (keyword mode — for "{keyword}")

| Advertiser | Position | Ad copy excerpt | URL |
|---|---|---|---|
| {domain} | {pos} | "{headline} — {snippet}" | {url} |
| ...

## Ad copy patterns (top patterns observed)

1. **Pricing-led:** "{N}% off — start at ${X}/mo" — used by {n} advertisers.
2. **Outcome-led:** "Get {specific outcome} in {time}" — used by {n}.
3. **Trust-led:** "Trusted by {n} {audience}" — used by {n}.
4. ...

## SERP feature inventory

| Keyword | Top ads | Shopping pack | PAA | Image pack |
|---|---|---|---|---|
| {kw} | {advertiser list} | {✓/✗} | {✓/✗} | {✓/✗} |
| ...

## Recommended bid-keyword shortlist

See `recommended-keywords.csv`. Top 10:

| Keyword | Volume | Est. CPC | Why |
|---|---|---|---|
| {kw} | {n} | ${n} | Question-intent variant; competitor X bids on head term but not this. |
| ...

## Constraints / caveats
- CPC and volume estimates are directional. Actual costs depend on Quality Score, time of day, audience, etc.
- {Note any ad-copy that's clearly seasonal / promotional and may not represent steady-state.}

## Recommended next step
Cross-reference these paid keywords with `seo-keyword-cluster` output to find under-served paid clusters. For organic content opportunities corresponding to these paid keywords, run `seo-keyword-niche`.
```

`recommended-keywords.csv` columns: `keyword,volume,cpc_estimate,position_target,intent,competitor_count,why_recommended`

## Tips

- DataForSEO allows up to 2,000 calls/min, 30 concurrent; pace sequentially. Domain mode: one SERP call per seed keyword plus a volume/CPC batch. Keyword mode: ~3 calls.
- Cost: DataForSEO bills per call; ~10–25 calls typical for domain mode (scales with seed-keyword count), ~5–10 for keyword mode. Cap large lists with `limit`/`ceiling`.
- **CPC estimates lag.** `kw_data_google_ads_search_volume` CPC is Google Ads aggregate data, not real-time auction data; treat as ±30% directional.
- Ad copy often reveals competitor positioning before product launches do — periodic review (quarterly) catches strategic shifts.
- Question-intent variants often have lower CPC and higher conversion than head terms. The shortlist in step 8 prioritises these.
- Pair with `seo-keyword-niche` for organic content opportunities derived from paid keyword research.
- Pair with `seo-competitor-pages` if the bidding landscape reveals "X vs Y" / "alternatives" intent — those keywords convert best as comparison pages, not paid ads.
- **The paid landscape is reconstructed from the live SERP, keyword by keyword.** There is no domain-level "all keywords a competitor bids on" tool here; the footprint is only as complete as the seed keyword set you probe. Widen the seed set to widen coverage. The mechanics: `mcp__dataforseo__serp_organic_live_advanced` reads the paid/ad and shopping blocks (top ads, bottom ads, shopping carousel) per keyword, and `mcp__dataforseo__kw_data_google_ads_search_volume` supplies CPC/competition/competition_index for the bidding landscape. *Optional accelerator:* a user who already has a paid-keyword database MCP can substitute it for the seed-set enumeration in domain mode — not required.
- Don't recommend paid keywords without context. The shortlist is a starting point for the PPC team, not an autopilot.
