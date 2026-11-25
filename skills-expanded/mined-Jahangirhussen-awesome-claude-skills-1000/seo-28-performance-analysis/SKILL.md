---
name: seo-28-performance-analysis
description: Performance analysis (SEO). Use when the request involves: organic performance. Not for topics owned by sibling SEO skills or other categories; routed by seo-master.
---

# Performance analysis

ID: 28.05 | Level: child | Parent: [SEO Analytics](../SKILL.md)

## Purpose
Performance analysis within the seo-master tree: Analysis memo.

## When to use
Triggers: organic performance

## When NOT to use
- The topic is covered by a sibling skill: `../google-analytics`, `../keyword-tracking`, `../search-console`, `../seo-reporting`.
- The task is outside this SEO category; see `ROUTER.md` at the seo-master root.

## Inputs
- Target site/URL(s) or project files, platform (CMS/framework), and goal.
- Data access as available: GA4, Google Search Console, Looker Studio, GTM, BigQuery export, spreadsheet.

## Core workflow
1. Break down changes by page type and query class
2. Find cause: technical, content, SERP feature, competitor, seasonality
3. Recommend targeted action

## Decision rules and checks
- Trend not day-to-day
- Annotate releases/updates

## Edge cases and failure handling
- Correlation vs cause -> test

## Validation
- Re-fetch or re-crawl changed URLs; confirm the fix is live (status, rendered HTML, canonical, schema validator, GSC URL Inspection as relevant).
- Compare with the baseline recorded before the change; check for regressions on neighbouring templates.

## Output requirements
Analysis memo. Report as a short DONE: what changed, evidence, remaining issues.

## Example
- Input/symptom: Correlation vs cause
- Action: test
- Output: Analysis memo.

## References
`references/playbook.md`: detailed how-to, common problems and fixes, tools, verify steps. Read when executing.
