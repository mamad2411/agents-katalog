---
name: seo-competitor-gap-analysis
description: Compare a target domain to its top organic competitors and surface keywords the competitors rank for that the target does not, filtered by intent, volume, and difficulty. Use when the user asks for a competitor gap analysis, keyword gap, organic content gap, missing keyword opportunities, or wants to see what their competitors are ranking for that they are not.
---
> Example output: [examples/seo-competitor-gap-analysis-wix-com-20260514/REPORT.md](../../examples/seo-competitor-gap-analysis-wix-com-20260514/REPORT.md)

# Competitor Gap Analysis

Identify the specific keywords your competitors rank for in the top 20 that your domain does not, ranked by commercial value and realistic capture difficulty.

## Prerequisites

- DataForSEO MCP server connected.
- User provides: (a) target domain, (b) 3 to 5 competitor domains (or ask the skill to auto-discover them), (c) market country (default: `us`), and optionally filters (min volume, max KD, intent).

## Process

1. **Validate or discover competitors** `mcp__dataforseo__dataforseo_labs_google_competitors_domain`
   - If the user did not provide competitors, pull the top 5 organic competitors for the target in the target market.
   - Surface the list to the user and ask them to confirm or override before proceeding.
   - **Note:** large competitor lists can exceed the MCP inline limit. Cap with `limit` and filters; if the result is written to a file, read that path, parse the `{data: [...]}` JSON, sort by `common_keywords` desc, and take the top 5.

2. **Pull competitor keyword sets** `mcp__dataforseo__dataforseo_labs_google_ranked_keywords`
   - For each competitor, pull keywords where they rank in the top 20 of the target country.
   - Save per-competitor lists.

3. **Pull target keyword set** `mcp__dataforseo__dataforseo_labs_google_ranked_keywords`
   - For the target domain, pull all ranking keywords in the target country (any position).
   - This is the exclusion set.

4. **Compute the gap** `mcp__dataforseo__dataforseo_labs_google_domain_intersection` (cross-check)
   - Keywords ranked by at least one competitor in the top 20 but not ranked by the target domain at all.
   - Use the domain-intersection endpoint as a cross-check.

5. **Filter and segment**
   - Apply user-specified filters on volume, KD, and intent.
   - Segment by intent: informational, commercial, transactional, navigational.
   - Segment by competition: how many of the N competitors rank for each gap keyword.

6. **Score and prioritise**
   - Score each gap keyword: traffic potential (volume × CTR model) + intent weighting + inverse KD.
   - Surface the top 50 opportunities with reasoning per keyword.

7. **Map to content actions**
   - For each top opportunity, recommend: new article, expand existing page, refresh existing page, programmatic template.
   - Flag quick wins: competitors rank with thin content (detected by URL pattern and content-length heuristics).

## Output format

Create a folder `seo-competitor-gap-analysis-{target-slug}-{YYYYMMDD}/` with:

```
seo-competitor-gap-analysis-{target-slug}-{YYYYMMDD}/
├── REPORT.md                                (synthesised report — primary deliverable)
├── gaps.csv                                 (full gap list — load-bearing CSV the writers/planners paste into briefs)
└── evidence/
    ├── 01-competitors.md                    (competitor list / discovery — raw step output)
    ├── 02-competitor-keywords-{domain}.md   (one per competitor — raw step output)
    ├── 03-target-keywords.md                (target's existing ranking set — raw step output)
    └── 04-gap-raw.md                        (human-readable full gap list before filtering — raw step output)
```

Top-level: `REPORT.md` + `gaps.csv`. The numbered step files preserve the raw API outputs in `evidence/` for reproducibility.

`REPORT.md` follows this shape:

```markdown
# Competitor Gap: {target}
Market: {country}
Competitors analysed: {list}

## Summary
- Competitor keywords in top 20: {n}
- Target keywords overall: {n}
- Gap keywords (opportunities): {n}
- Gap traffic potential: ~{n}/mo

## Top 50 opportunities

### Informational intent
| # | Keyword | Volume | KD | Competitors ranking | Action | Score |
|---|---|---|---|---|---|---|
| 1 | {kw} | {n} | {n} | {3 of 5} | New article | {score} |
| 2 | ... | ... | ... | ... | ... | ... |

### Commercial intent
| # | Keyword | Volume | KD | Competitors ranking | Action | Score |
|---|---|---|---|---|---|---|
...

### Transactional intent
...

## Quick wins (top 10)
Keywords where competitors rank in positions 5 to 20 with thin content, low domain rank, or old dates.

| # | Keyword | Weakest competitor position | Suggested angle |
|---|---|---|---|
| 1 | {kw} | example.com at #14 (2022 article, 800 words) | Fresh, comprehensive guide |

## Recommended next steps
1. Run `content-brief` on the top 3 opportunities to generate writer-ready briefs.
2. Run `keyword-cluster-planner` on the full gap list to build a sequencing plan.
3. Track the gap keywords once content ships — for your own verified site use GSC (`mcp__gscServer__get_search_analytics`); for any-domain tracking, save dated `serp_organic_live_advanced` snapshots to local storage (the `seo-drift` pattern).

## Files
- gaps.csv: full gap list for spreadsheet analysis
- evidence/04-gap-raw.md: human-readable full gap list before filtering
```

`gaps.csv` columns:
`keyword,volume,kd,cpc,intent,competitors_ranking,top_competitor_position,target_position,action,score`

## Tips

- DataForSEO allows up to 2,000 calls/min, 30 concurrent. Skills pace sequentially. For large sites, `dataforseo_labs_google_ranked_keywords` may paginate heavily; set a ceiling (e.g., top 1,000 keywords per domain via `limit`) unless the user explicitly asks for the full set.
- DataForSEO bills per call; this run issues ~N calls (one ranked-keywords pull per seed plus the intersection cross-checks). Use the documented `limit`/`ceiling` params to cap.
- The `competitors_ranking` count is the best signal of realism. Keywords ranked by 4 of 5 competitors are validated opportunities; keywords ranked by only 1 may be noise.
- Do not recommend capturing branded competitor keywords unless the user explicitly asks. Pivoting to compete on "competitor brand review" is a viable strategy but only if the user opts in.
- When many gap keywords cluster around a theme, recommend a hub page plus cluster rather than 50 individual articles.
- Chain this skill with `content-brief` and `keyword-cluster-planner` naturally. Mention them in the Recommended next steps section of the output.
