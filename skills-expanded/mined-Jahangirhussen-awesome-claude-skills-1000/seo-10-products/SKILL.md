---
name: seo-10-products
description: Products (SEO). Use when the request involves: shopify product seo. Not for topics owned by sibling SEO skills or other categories; routed by seo-master.
---

# Products

ID: 10.01 | Level: child | Parent: [Shopify SEO](../SKILL.md)

## Purpose
Products within the seo-master tree: Product page checklist.

## When to use
Triggers: shopify product seo

## When NOT to use
- The topic is covered by a sibling skill: `../collections`, `../liquid-seo`, `../shopify-migration`, `../shopify-technical`, `../structured-data`.
- The task is outside this SEO category; see `ROUTER.md` at the seo-master root.

## Inputs
- Target site/URL(s) or project files, platform (CMS/framework), and goal.
- Data access as available: Shopify admin (themes, redirects, navigation), Liquid editor, Screaming Frog, Rich Results Test, app list.

## Core workflow
1. Unique title/description; handle slugs set early
2. Use product canonical (/products/handle)
3. Optimize images and alt; variants share one URL with ?variant=
4. Add reviews and FAQs

## Decision rules and checks
- Canonical = /products/handle (not /collections/x/products/y)
- Unique titles/descriptions
- Image alt

## Edge cases and failure handling
- Auto-generated meta -> write manually for top products
- Handle changed -> auto 301 exists; update internal links

## Validation
- Re-fetch or re-crawl changed URLs; confirm the fix is live (status, rendered HTML, canonical, schema validator, GSC URL Inspection as relevant).
- Compare with the baseline recorded before the change; check for regressions on neighbouring templates.

## Output requirements
Product page checklist. Report as a short DONE: what changed, evidence, remaining issues.

## Example
- Input/symptom: Auto-generated meta
- Action: write manually for top products
- Output: Product page checklist.

## References
`references/playbook.md`: detailed how-to, common problems and fixes, tools, verify steps. Read when executing.
