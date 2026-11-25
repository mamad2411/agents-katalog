---
name: seo-29-seo-apis
description: SEO APIs (SEO). Use when the request involves: gsc api, ga4 api, pagespeed api, dataforseo. Not for topics owned by sibling SEO skills or other categories; routed by seo-master.
---

# SEO APIs

ID: 29.03 | Level: child | Parent: [SEO Tools and APIs](../SKILL.md)

## Purpose
SEO APIs within the seo-master tree: API client notes.

## When to use
Triggers: gsc api, ga4 api, pagespeed api, dataforseo

## When NOT to use
- The topic is covered by a sibling skill: `../backlink-tools`, `../data-collection`, `../keyword-tools`, `../scraping`.
- The task is outside this SEO category; see `ROUTER.md` at the seo-master root.

## Inputs
- Target site/URL(s) or project files, platform (CMS/framework), and goal.
- Data access as available: GSC API, GA4 Data API, PageSpeed Insights API, DataForSEO, Ahrefs/Semrush APIs, Python or Node scripts.

## Core workflow
1. GSC API (searchAnalytics.query), GA4 Data API, PageSpeed Insights API, URL Inspection API
2. Use minimal OAuth scopes/service accounts; paginate; cache
3. Log quotas

## Decision rules and checks
- OAuth/service account scopes minimal
- Respect quotas

## Edge cases and failure handling
- Quota errors -> batch and back off

## Validation
- Re-fetch or re-crawl changed URLs; confirm the fix is live (status, rendered HTML, canonical, schema validator, GSC URL Inspection as relevant).
- Compare with the baseline recorded before the change; check for regressions on neighbouring templates.

## Output requirements
API client notes. Report as a short DONE: what changed, evidence, remaining issues.

## Example
- Input/symptom: Quota errors
- Action: batch and back off
- Output: API client notes.

## References
`references/playbook.md`: detailed how-to, common problems and fixes, tools, verify steps. Read when executing.
