---
name: seo-10-collections
description: Collections (SEO). Use when the request involves: shopify collection seo. Not for topics owned by sibling SEO skills or other categories; routed by seo-master.
---

# Collections

ID: 10.02 | Level: child | Parent: [Shopify SEO](../SKILL.md)

## Purpose
Collections within the seo-master tree: Collection template.

## When to use
Triggers: shopify collection seo

## When NOT to use
- The topic is covered by a sibling skill: `../liquid-seo`, `../products`, `../shopify-migration`, `../shopify-technical`, `../structured-data`.
- The task is outside this SEO category; see `ROUTER.md` at the seo-master root.

## Inputs
- Target site/URL(s) or project files, platform (CMS/framework), and goal.
- Data access as available: Shopify admin (themes, redirects, navigation), Liquid editor, Screaming Frog, Rich Results Test, app list.

## Core workflow
1. Add unique intro and meta; keep filters crawlable only where wanted
2. Avoid thin duplicate collections
3. Link subcollections; use pagination links

## Decision rules and checks
- Intro copy, filters via crawlable links
- Pagination
- Merge thin collections

## Edge cases and failure handling
- Tag-filter URLs indexed -> noindex or canonical
- Automated collections overlapping -> consolidate

## Validation
- Re-fetch or re-crawl changed URLs; confirm the fix is live (status, rendered HTML, canonical, schema validator, GSC URL Inspection as relevant).
- Compare with the baseline recorded before the change; check for regressions on neighbouring templates.

## Output requirements
Collection template. Report as a short DONE: what changed, evidence, remaining issues.

## Example
- Input/symptom: Tag-filter URLs indexed
- Action: noindex or canonical
- Output: Collection template.

## References
`references/playbook.md`: detailed how-to, common problems and fixes, tools, verify steps. Read when executing.
