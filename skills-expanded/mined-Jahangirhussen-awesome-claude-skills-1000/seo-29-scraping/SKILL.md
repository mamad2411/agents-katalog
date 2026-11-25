---
name: seo-29-scraping
description: Scraping (compliant) (SEO). Use when the request involves: scrape serp, scraping. Not for topics owned by sibling SEO skills or other categories; routed by seo-master.
---

# Scraping (compliant)

ID: 29.05 | Level: child | Parent: [SEO Tools and APIs](../SKILL.md)

## Purpose
Scraping (compliant) within the seo-master tree: Scraper spec.

## When to use
Triggers: scrape serp, scraping

## When NOT to use
- The topic is covered by a sibling skill: `../backlink-tools`, `../data-collection`, `../keyword-tools`, `../seo-apis`.
- The task is outside this SEO category; see `ROUTER.md` at the seo-master root.

## Inputs
- Target site/URL(s) or project files, platform (CMS/framework), and goal.
- Data access as available: GSC API, GA4 Data API, PageSpeed Insights API, DataForSEO, Ahrefs/Semrush APIs, Python or Node scripts.

## Core workflow
1. Respect robots.txt and terms; rate-limit
2. Prefer APIs and official exports
3. Cache results; identify user agent

## Decision rules and checks
- Respect robots.txt/ToS, rate limits
- Prefer APIs

## Edge cases and failure handling
- Blocked -> do not evade; use API

## Validation
- Re-fetch or re-crawl changed URLs; confirm the fix is live (status, rendered HTML, canonical, schema validator, GSC URL Inspection as relevant).
- Compare with the baseline recorded before the change; check for regressions on neighbouring templates.

## Output requirements
Scraper spec. Report as a short DONE: what changed, evidence, remaining issues.

## Example
- Input/symptom: Blocked
- Action: do not evade; use API
- Output: Scraper spec.

## References
`references/playbook.md`: detailed how-to, common problems and fixes, tools, verify steps. Read when executing.
