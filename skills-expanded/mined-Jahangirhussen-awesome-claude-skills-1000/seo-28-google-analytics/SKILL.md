---
name: seo-28-google-analytics
description: GA4 (SEO). Use when the request involves: ga4, google analytics. Not for topics owned by sibling SEO skills or other categories; routed by seo-master.
---

# GA4

ID: 28.01 | Level: child | Parent: [SEO Analytics](../SKILL.md)

## Purpose
GA4 within the seo-master tree: GA4 organic dashboard.

## When to use
Triggers: ga4, google analytics

## When NOT to use
- The topic is covered by a sibling skill: `../keyword-tracking`, `../performance-analysis`, `../search-console`, `../seo-reporting`.
- The task is outside this SEO category; see `ROUTER.md` at the seo-master root.

## Inputs
- Target site/URL(s) or project files, platform (CMS/framework), and goal.
- Data access as available: GA4, Google Search Console, Looker Studio, GTM, BigQuery export, spreadsheet.

## Core workflow
1. GA4: confirm key events and conversions
2. Explore organic landing pages, engagement, revenue
3. Link GA4 with GSC

## Decision rules and checks
- Organic channel, landing pages, conversions
- Key events defined

## Edge cases and failure handling
- Consent mode losing data -> note in reports

## Validation
- Re-fetch or re-crawl changed URLs; confirm the fix is live (status, rendered HTML, canonical, schema validator, GSC URL Inspection as relevant).
- Compare with the baseline recorded before the change; check for regressions on neighbouring templates.

## Output requirements
GA4 organic dashboard. Report as a short DONE: what changed, evidence, remaining issues.

## Example
- Input/symptom: Consent mode losing data
- Action: note in reports
- Output: GA4 organic dashboard.

## References
`references/playbook.md`: detailed how-to, common problems and fixes, tools, verify steps. Read when executing.
