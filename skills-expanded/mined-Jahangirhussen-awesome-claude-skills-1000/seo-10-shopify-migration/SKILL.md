---
name: seo-10-shopify-migration
description: Shopify migration (SEO). Use when the request involves: migrate to shopify. Not for topics owned by sibling SEO skills or other categories; routed by seo-master.
---

# Shopify migration

ID: 10.06 | Level: child | Parent: [Shopify SEO](../SKILL.md)

## Purpose
Shopify migration within the seo-master tree: Migration redirect map and QA.

## When to use
Triggers: migrate to shopify

## When NOT to use
- The topic is covered by a sibling skill: `../collections`, `../liquid-seo`, `../products`, `../shopify-technical`, `../structured-data`.
- The task is outside this SEO category; see `ROUTER.md` at the seo-master root.

## Inputs
- Target site/URL(s) or project files, platform (CMS/framework), and goal.
- Data access as available: Shopify admin (themes, redirects, navigation), Liquid editor, Screaming Frog, Rich Results Test, app list.

## Core workflow
1. Export URLs, redirects, and rankings from the old site
2. Match handles where possible; build 301 map via Online Store > Navigation > URL redirects
3. Migrate meta, content, images with alt
4. Monitor GSC after launch

## Decision rules and checks
- Redirect map to new handles
- Keep URL equity

## Edge cases and failure handling
- Traffic drop after launch -> compare crawl, fix missing redirects
- Blog URL structure change (/blogs/news/) -> map carefully

## Validation
- Re-fetch or re-crawl changed URLs; confirm the fix is live (status, rendered HTML, canonical, schema validator, GSC URL Inspection as relevant).
- Compare with the baseline recorded before the change; check for regressions on neighbouring templates.

## Output requirements
Migration redirect map and QA. Report as a short DONE: what changed, evidence, remaining issues.

## Example
- Input/symptom: Traffic drop after launch
- Action: compare crawl, fix missing redirects
- Output: Migration redirect map and QA.

## Dependencies (load only if needed)
- 31-seo-migration/platform-migration

## References
`references/playbook.md`: detailed how-to, common problems and fixes, tools, verify steps. Read when executing.
