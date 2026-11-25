---
name: seo-29-keyword-tools
description: Keyword tools (SEO). Use when the request involves: keyword planner, google trends, ahrefs keywords. Not for topics owned by sibling SEO skills or other categories; routed by seo-master.
---

# Keyword tools

ID: 29.01 | Level: child | Parent: [SEO Tools and APIs](../SKILL.md)

## Purpose
Keyword tools within the seo-master tree: Keyword data sheet.

## When to use
Triggers: keyword planner, google trends, ahrefs keywords

## When NOT to use
- The topic is covered by a sibling skill: `../backlink-tools`, `../data-collection`, `../scraping`, `../seo-apis`.
- The task is outside this SEO category; see `ROUTER.md` at the seo-master root.

## Inputs
- Target site/URL(s) or project files, platform (CMS/framework), and goal.
- Data access as available: GSC API, GA4 Data API, PageSpeed Insights API, DataForSEO, Ahrefs/Semrush APIs, Python or Node scripts.

## Core workflow
1. GSC queries, Google Trends, Keyword Planner, paid tools for volume/difficulty
2. Cross-check numbers across tools; treat as estimates

## Decision rules and checks
- State source per datapoint
- Cross-check volumes

## Edge cases and failure handling
- Volume mismatch -> use ranges

## Validation
- Re-fetch or re-crawl changed URLs; confirm the fix is live (status, rendered HTML, canonical, schema validator, GSC URL Inspection as relevant).
- Compare with the baseline recorded before the change; check for regressions on neighbouring templates.

## Output requirements
Keyword data sheet. Report as a short DONE: what changed, evidence, remaining issues.

## Example
- Input/symptom: Volume mismatch
- Action: use ranges
- Output: Keyword data sheet.

## References
`references/playbook.md`: detailed how-to, common problems and fixes, tools, verify steps. Read when executing.
