---
name: seo-28-search-console
description: Search Console analysis (SEO). Use when the request involves: gsc analysis, queries, pages. Not for topics owned by sibling SEO skills or other categories; routed by seo-master.
---

# Search Console analysis

ID: 28.02 | Level: child | Parent: [SEO Analytics](../SKILL.md)

## Purpose
Search Console analysis within the seo-master tree: GSC analysis sheet.

## When to use
Triggers: gsc analysis, queries, pages

## When NOT to use
- The topic is covered by a sibling skill: `../google-analytics`, `../keyword-tracking`, `../performance-analysis`, `../seo-reporting`.
- The task is outside this SEO category; see `ROUTER.md` at the seo-master root.

## Inputs
- Target site/URL(s) or project files, platform (CMS/framework), and goal.
- Data access as available: GA4, Google Search Console, Looker Studio, GTM, BigQuery export, spreadsheet.

## Core workflow
1. Queries x pages x countries x devices
2. Compare periods; find striking-distance and low-CTR items
3. Use Looker Studio or API for history beyond 16 months

## Decision rules and checks
- Queries x pages x devices x countries
- CTR vs position curve outliers

## Edge cases and failure handling
- Sampling/limits -> API export

## Validation
- Re-fetch or re-crawl changed URLs; confirm the fix is live (status, rendered HTML, canonical, schema validator, GSC URL Inspection as relevant).
- Compare with the baseline recorded before the change; check for regressions on neighbouring templates.

## Output requirements
GSC analysis sheet. Report as a short DONE: what changed, evidence, remaining issues.

## Example
- Input/symptom: Sampling/limits
- Action: API export
- Output: GSC analysis sheet.

## References
`references/playbook.md`: detailed how-to, common problems and fixes, tools, verify steps. Read when executing.
