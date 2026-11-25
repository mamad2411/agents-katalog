---
name: seo-28-seo-reporting
description: SEO reporting (SEO). Use when the request involves: seo report. Not for topics owned by sibling SEO skills or other categories; routed by seo-master.
---

# SEO reporting

ID: 28.03 | Level: child | Parent: [SEO Analytics](../SKILL.md)

## Purpose
SEO reporting within the seo-master tree: Monthly report.

## When to use
Triggers: seo report

## When NOT to use
- The topic is covered by a sibling skill: `../google-analytics`, `../keyword-tracking`, `../performance-analysis`, `../search-console`.
- The task is outside this SEO category; see `ROUTER.md` at the seo-master root.

## Inputs
- Target site/URL(s) or project files, platform (CMS/framework), and goal.
- Data access as available: GA4, Google Search Console, Looker Studio, GTM, BigQuery export, spreadsheet.

## Core workflow
1. Pick KPIs: organic clicks, conversions, revenue, non-brand growth, rankings, visibility
2. Show wins, risks, next actions
3. Keep report to one page for executives

## Decision rules and checks
- KPI deltas, wins, risks, next actions
- Revenue attribution where possible

## Edge cases and failure handling
- Vanity metrics -> tie to revenue

## Validation
- Re-fetch or re-crawl changed URLs; confirm the fix is live (status, rendered HTML, canonical, schema validator, GSC URL Inspection as relevant).
- Compare with the baseline recorded before the change; check for regressions on neighbouring templates.

## Output requirements
Monthly report. Report as a short DONE: what changed, evidence, remaining issues.

## Example
- Input/symptom: Vanity metrics
- Action: tie to revenue
- Output: Monthly report.

## External sources merged (deep method)
- `../../_source/aaron__performance-reporter/SKILL.md`

## References
`references/playbook.md`: detailed how-to, common problems and fixes, tools, verify steps. Read when executing.
