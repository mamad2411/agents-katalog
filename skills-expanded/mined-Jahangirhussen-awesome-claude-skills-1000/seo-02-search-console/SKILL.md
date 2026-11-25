---
name: seo-02-search-console
description: Search Console (SEO). Use when the request involves: gsc, search console, performance report, url inspection, page indexing, manual action. Not for topics owned by sibling SEO skills or other categories; routed by seo-master.
---

# Search Console

ID: 02.01 | Level: child | Parent: [Google SEO](../SKILL.md)

## Purpose
Search Console within the seo-master tree: Opportunity sheet: query/page, impressions, CTR, position, action.

## When to use
Triggers: gsc, search console, performance report, url inspection, page indexing, manual action

## When NOT to use
- The topic is covered by a sibling skill: `../core-updates`, `../indexing`.
- The task is outside this SEO category; see `ROUTER.md` at the seo-master root.

## Inputs
- Target site/URL(s) or project files, platform (CMS/framework), and goal.
- Data access as available: Google Search Console (+API), GA4, URL Inspection tool, Search Status Dashboard, Looker Studio.

## Core workflow
1. Performance: filter by query/page/country/device, compare 3 months vs previous
2. Find striking-distance queries (position 8-20) and low-CTR high-impression pages
3. Page indexing: group 'not indexed' reasons, fix biggest group first
4. Sitemaps: submitted vs indexed counts
5. Export via API for large sites (1000-row UI limit)

## Decision rules and checks
- Performance: clicks/impressions/CTR/position by page + query
- Page indexing: reasons for not indexed
- URL Inspection on key URLs
- Sitemaps + CWV + Manual actions/Security reports

## Edge cases and failure handling
- CTR low at good position -> rewrite title/meta, check SERP features
- Brand queries inflate results -> filter brand terms with regex

## Validation
- Re-fetch or re-crawl changed URLs; confirm the fix is live (status, rendered HTML, canonical, schema validator, GSC URL Inspection as relevant).
- Compare with the baseline recorded before the change; check for regressions on neighbouring templates.

## Output requirements
Opportunity sheet: query/page, impressions, CTR, position, action. Report as a short DONE: what changed, evidence, remaining issues.

## Example
- Input/symptom: CTR low at good position
- Action: rewrite title/meta, check SERP features
- Output: Opportunity sheet: query/page, impressions, CTR, position, action.

## Dependencies (load only if needed)
- 28-seo-analytics/search-console

## References
`references/playbook.md`: detailed how-to, common problems and fixes, tools, verify steps. Read when executing.
