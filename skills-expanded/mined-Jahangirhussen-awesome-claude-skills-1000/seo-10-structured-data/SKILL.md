---
name: seo-10-structured-data
description: Shopify structured data (SEO). Use when the request involves: shopify schema. Not for topics owned by sibling SEO skills or other categories; routed by seo-master.
---

# Shopify structured data

ID: 10.05 | Level: child | Parent: [Shopify SEO](../SKILL.md)

## Purpose
Shopify structured data within the seo-master tree: Schema validation results.

## When to use
Triggers: shopify schema

## When NOT to use
- The topic is covered by a sibling skill: `../collections`, `../liquid-seo`, `../products`, `../shopify-migration`, `../shopify-technical`.
- The task is outside this SEO category; see `ROUTER.md` at the seo-master root.

## Inputs
- Target site/URL(s) or project files, platform (CMS/framework), and goal.
- Data access as available: Shopify admin (themes, redirects, navigation), Liquid editor, Screaming Frog, Rich Results Test, app list.

## Core workflow
1. Use theme product JSON-LD or a single app
2. Validate Product/Offer/Review
3. Add Organization and WebSite schema

## Decision rules and checks
- Single schema source
- Validate Product/Offer

## Edge cases and failure handling
- Duplicate schema -> disable one source
- Rating without reviews -> remove

## Validation
- Re-fetch or re-crawl changed URLs; confirm the fix is live (status, rendered HTML, canonical, schema validator, GSC URL Inspection as relevant).
- Compare with the baseline recorded before the change; check for regressions on neighbouring templates.

## Output requirements
Schema validation results. Report as a short DONE: what changed, evidence, remaining issues.

## Example
- Input/symptom: Duplicate schema
- Action: disable one source
- Output: Schema validation results.

## Dependencies (load only if needed)
- 27-schema-seo/product

## References
`references/playbook.md`: detailed how-to, common problems and fixes, tools, verify steps. Read when executing.
