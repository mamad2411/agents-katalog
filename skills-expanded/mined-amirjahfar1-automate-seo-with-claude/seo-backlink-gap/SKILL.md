---
name: seo-backlink-gap
description: Find referring domains that link to multiple competitors but not to your site, then enrich with authority, anchor samples, and outreach angle per row. Produces a prospect list an outreach team can start emailing tomorrow. Use when the user asks for backlink gap analysis, link building opportunities, competitor backlink intersection, link prospecting, or wants referring domains they are missing.
---

> Example output: [examples/seo-backlink-gap-linear-app-20260514/REPORT.md](../../examples/seo-backlink-gap-linear-app-20260514/REPORT.md)

# Backlink Gap

Produce an actionable link-prospecting list: domains linking to your top competitors but not to you, filtered by authority and relevance, enriched with anchor samples and a suggested outreach angle.

## Prerequisites

- DataForSEO MCP server connected.
- Claude's `WebFetch` tool available (used for prospect scoring and topical relevance checks).
- User provides: (a) target domain, (b) 3 to 5 competitor domains, and optionally (c) minimum referring-domain rank (default: 250 on the 0–1000 scale), (d) dofollow-only filter (default: true), (e) minimum intersection count (default: linked by at least 2 of the N competitors).

## Process

1. **Baseline target backlinks** `mcp__dataforseo__backlinks_referring_domains`, `mcp__dataforseo__backlinks_summary`
   - Pull the target domain's existing referring domains to build an exclusion set.
   - Save count and summary metrics for the report.

2. **Competitor intersection** `mcp__dataforseo__backlinks_domain_intersection` (with `mcp__dataforseo__backlinks_competitors` to validate competitor set)
   - Use `backlinks_domain_intersection` to pull referring domains that link to the competitors. Apply a dofollow `filters` clause and a `rank` floor of `{threshold}` to narrow.
   - Collect as a dict keyed by referring domain with the list of competitors linking to it.

3. **Intersection**
   - Retain referring domains that link to at least the minimum number of competitors.
   - Exclude any domain already in the target's backlink set.

4. **Enrichment** `mcp__dataforseo__backlinks_bulk_ranks`, `mcp__dataforseo__backlinks_anchors`
   - For each candidate, pull: domain rank, page rank of the linking page, linking-to-competitor anchor samples (top 3 anchors), and country if available.
   - Classify by link type: editorial, resource list, directory, forum/UGC.

5. **Relevance scoring**
   - Score each candidate on: (a) topical overlap (use domain homepage title/meta via WebFetch), (b) rank, (c) intersection count, (d) link-type preference.
   - Suggest an outreach angle per row: local fit, topical fit, competitive parity, resource-list inclusion, broken link, etc.

6. **Produce the prospect list** (see Output Format).

## Output format

Create a folder `seo-backlink-gap-{target-slug}-{YYYYMMDD}/` with:

```
seo-backlink-gap-{target-slug}-{YYYYMMDD}/
├── 01-target-baseline.md
├── 02-competitor-{domain}-refs.md   # one per competitor
├── 03-intersection-raw.md
├── prospects.csv                     # machine-readable output
└── REPORT.md
```

`REPORT.md` follows this shape:

```markdown
# Backlink Gap: {target} vs {competitors}

## Filters applied
- Dofollow only: yes
- Min referring-domain rank: {n}
- Min intersection: links to at least {n} of {total} competitors

## Top 25 prospects

| # | Referring domain | Rank | Links to | Sample anchor | Link type | Angle | Score |
|---|---|---|---|---|---|---|---|
| 1 | example.com | 680 | {3 of 5} | "best yoga studios" | Resource list | Topical fit | 92 |
| 2 | ... | ... | ... | ... | ... | ... | ... |

## Outreach brief
- Segment these prospects into 3 batches by link type and pitch each batch with a tailored template.
- For editorial links: pitch a unique-angle comparison or original research.
- For resource lists: suggest inclusion with a specific anchor.
- For directories: apply directly.
- For forums/UGC: engage before pitching; these are not cold-outreachable.

## Counts
- Total unique referring domains across competitors: {n}
- Passed filters: {n}
- Already linking to {target}: {n} (excluded)
- Final prospects: {n}

## Files
- prospects.csv: import to Hunter.io, Pitchbox, or your outreach tool
- Per-competitor raw data: 02-competitor-*.md
```

`prospects.csv` columns:
`rank,referring_domain,domain_rank,links_to_count,links_to_competitors,sample_anchor,link_type,outreach_angle,score`

## Tips

- DataForSEO allows up to 2,000 calls/min, 30 concurrent. Skills pace sequentially. With 5 competitors, expect a handful of intersection + enrichment calls. DataForSEO bills per call; use `limit`/filters to cap large referring-domain lists.
- Do not include subdomains of already-linked domains in the prospect list. If news.example.com links to the target but blog.example.com links only to competitors, treat as already-linked unless the user asks otherwise.
- The "Angle" column is the most important output for outreach. Keep it specific: "Their 'best X tools' list from 2024 is out of date and doesn't include you" beats "topical fit".
- Exclude obvious spam/low-quality domains even if they pass rank thresholds (cross-check with `mcp__dataforseo__backlinks_bulk_spam_score`). Use the WebFetch step to sanity-check any prospect scoring above 80.
- If the target already outranks all competitors for branded terms, prioritise non-branded editorial placements over parity directories.
