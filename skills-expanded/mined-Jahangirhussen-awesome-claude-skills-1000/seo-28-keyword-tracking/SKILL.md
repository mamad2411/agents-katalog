---
name: seo-28-keyword-tracking
description: Keyword tracking (SEO). Use when the request involves: keyword tracking. Not for topics owned by sibling SEO skills or other categories; routed by seo-master.
---

# Keyword tracking

ID: 28.04 | Level: child | Parent: [SEO Analytics](../SKILL.md)

## Purpose
Keyword tracking within the seo-master tree: Rank tracker sheet.

## When to use
Triggers: keyword tracking

## When NOT to use
- The topic is covered by a sibling skill: `../google-analytics`, `../performance-analysis`, `../search-console`, `../seo-reporting`.
- The task is outside this SEO category; see `ROUTER.md` at the seo-master root.

## Inputs
- Target site/URL(s) or project files, platform (CMS/framework), and goal.
- Data access as available: GA4, Google Search Console, Looker Studio, GTM, BigQuery export, spreadsheet.

## Core workflow
1. Track by segment: brand, non-brand, money pages, locations
2. Use consistent device/location settings
3. Annotate algorithm updates

## Decision rules and checks
- Track by segment/intent
- Compare vs competitors

## Edge cases and failure handling
- Daily noise -> weekly averages

## Validation
- Re-fetch or re-crawl changed URLs; confirm the fix is live (status, rendered HTML, canonical, schema validator, GSC URL Inspection as relevant).
- Compare with the baseline recorded before the change; check for regressions on neighbouring templates.

## Output requirements
Rank tracker sheet. Report as a short DONE: what changed, evidence, remaining issues.

## Example
- Input/symptom: Daily noise
- Action: weekly averages
- Output: Rank tracker sheet.

## Dependencies (load only if needed)
- 32-seo-monitoring/rankings

## References
`references/playbook.md`: detailed how-to, common problems and fixes, tools, verify steps. Read when executing.
