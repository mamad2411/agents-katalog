---
name: google-search-console
description: "Google Search Console data analysis and API use. Use when interpreting search performance, indexing reports, queries, impressions, CTR or URL inspection."
metadata:
  version: 1.5.1
---

# Google Search Console

Interpret GSC data (performance, indexing, sitemaps, Core Web Vitals, rich results) and turn it into prioritized actions. On first use give 1-2 sentences on what this covers; on later use or when asked, go straight to the output.

## Reading the data

- One metric at a time: stacked charts hide fluctuation, so toggle the others off.
- Read the full trend, not two endpoints (end of month vs prior month misses mid-month drama).
- Look past the default top 10 rows.
- GSC keeps limited history: screenshot charts and export to a spreadsheet at month-end.
- Track release dates (join dev standups, read release notes) so shifts can be tied to deployments.

Investigation order: pinpoint the date the metric changed; correlate with releases, CMS changes, server maintenance and third-party code; decide to investigate, correct, overlook or monitor; loop in dev for root cause.

## Performance report

Metrics: clicks (traffic), impressions (visibility), CTR (does the result look like it answers the query), average position (ranking trend). Dimensions: query, page, country, device, date; filter by search type (web, image, video, news) and search appearance.

Expected CTR by position, undated third-party baselines (SERP features shift them; AI Overviews and other zero-click features lower organic CTR):

| Position | Baseline CTR | With AI Overviews |
|---|---|---|
| 1 | 25-35% | ~19% |
| 2 | 12-18% | ~12% |
| 3 | 8-12% | ~7% |
| 4-5 | 5-7% | ~5% |
| 6-10 | 2-5% | 2-5% |

CTR below the expected range for the position is the signal to optimize title and meta (`title-tag`, `meta-description`). Over 90% of first-page results sit under 10% CTR, so the upside is real.

**Low CTR, high impressions workflow:**
1. Sort by impressions, filter positions 1-10 and 1,000+ monthly impressions.
2. Compare actual CTR with the table (position 4 at 2% vs 5-7% expected is roughly 3-5 points of uplift).
3. Rewrite title and meta; add schema for rich results (review stars, FAQ and similar snippets are reported to add 10-20% clicks; `schema-markup`).

**AI Overviews:** GSC does not separate AI Overview clicks and impressions from organic. To estimate AI-driven visibility, filter queries that tend to trigger them:
```
(?i)^(who|what|where|when|why|how|which|is|are|can|does|should)|\b(vs|versus|compare|difference|pros and cons|guide|tutorial|best|top|list)\b
```
For GA4 AI traffic see `ai-traffic-tracking`.

## Other reports

- **Page indexing**: Indexed and Not indexed are complementary; not every page should be indexed, so investigate only when important pages are excluded or the not-indexed trend spikes. Reasons table, URL Inspection verdicts, Insights, Video indexing, Sitemaps, CWV (mobile first), Enhancements and Links/disavow: [references/reports.md](references/reports.md).
- **Search Console API** (`searchanalytics.query`, 25,000 rows per response, 50,000 rows per day per search type per property, data lags 2-3 days): [references/api.md](references/api.md).

The monthly audit checklist is at the end of reports.md.

## Output format

Summary (findings, trends, anomalies); metrics with date ranges; CTR analysis (actual vs expected, low-CTR high-impression pages); title/meta opportunities with specific rewrites; prioritized actions (indexing, CWV, sitemaps, enhancements, metadata); suspected correlations (releases, config); next steps and dev handoff.

## Related skills

`title-tag`, `meta-description`, `page-metadata`, `xml-sitemap`, `indexing`, `core-web-vitals`, `mobile-friendly`, `schema-markup`, `backlink-analysis`, `seo-monitoring`.
