---
name: seo-29-data-collection
description: Data collection (SEO). Use when the request involves: export data, crawl data, screaming frog. Not for topics owned by sibling SEO skills or other categories; routed by seo-master.
---

# Data collection

ID: 29.04 | Level: child | Parent: [SEO Tools and APIs](../SKILL.md)

## Purpose
Data collection within the seo-master tree: Data pipeline notes.

## When to use
Triggers: export data, crawl data, screaming frog

## When NOT to use
- The topic is covered by a sibling skill: `../backlink-tools`, `../keyword-tools`, `../scraping`, `../seo-apis`.
- The task is outside this SEO category; see `ROUTER.md` at the seo-master root.

## Inputs
- Target site/URL(s) or project files, platform (CMS/framework), and goal.
- Data access as available: GSC API, GA4 Data API, PageSpeed Insights API, DataForSEO, Ahrefs/Semrush APIs, Python or Node scripts.

## Core workflow
1. Crawl with Screaming Frog/Sitebulb or scripts; set limits
2. Store raw exports for diffing
3. Schedule regular pulls

## Decision rules and checks
- Crawl config + limits
- Store raw exports for diffing

## Edge cases and failure handling
- Crawl overload -> throttle

## Validation
- Re-fetch or re-crawl changed URLs; confirm the fix is live (status, rendered HTML, canonical, schema validator, GSC URL Inspection as relevant).
- Compare with the baseline recorded before the change; check for regressions on neighbouring templates.

## Output requirements
Data pipeline notes. Report as a short DONE: what changed, evidence, remaining issues.

## Example
- Input/symptom: Crawl overload
- Action: throttle
- Output: Data pipeline notes.

## References
`references/playbook.md`: detailed how-to, common problems and fixes, tools, verify steps. Read when executing.
