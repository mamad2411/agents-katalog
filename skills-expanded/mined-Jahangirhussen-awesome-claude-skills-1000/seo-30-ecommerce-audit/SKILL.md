---
name: seo-30-ecommerce-audit
description: E-commerce audit (SEO). Use when the request involves: ecommerce audit, woocommerce audit, shopify audit. Not for topics owned by sibling SEO skills or other categories; routed by seo-master.
---

# E-commerce audit

ID: 30.05 | Level: child | Parent: [SEO Audit](../SKILL.md)

## Purpose
E-commerce audit within the seo-master tree: E-commerce audit sheet.

## When to use
Triggers: ecommerce audit, woocommerce audit, shopify audit

## When NOT to use
- The topic is covered by a sibling skill: `../backlink-audit`, `../full-audit`, `../onpage-audit`, `../technical-audit`.
- The task is outside this SEO category; see `ROUTER.md` at the seo-master root.

## Inputs
- Target site/URL(s) or project files, platform (CMS/framework), and goal.
- Data access as available: Screaming Frog, GSC, GA4, Lighthouse, Ahrefs/Semrush, schema validator, platform-specific plugins.

## Core workflow
1. Review categories, products, facets, variants, schema, feed
2. Platform specifics (Woo, Shopify)
3. Index bloat and duplicate content

## Decision rules and checks
- Facets, product schema, feed, index bloat

## Edge cases and failure handling
- Thin supplier copy -> rewrite top sellers first

## Validation
- Re-fetch or re-crawl changed URLs; confirm the fix is live (status, rendered HTML, canonical, schema validator, GSC URL Inspection as relevant).
- Compare with the baseline recorded before the change; check for regressions on neighbouring templates.

## Output requirements
E-commerce audit sheet. Report as a short DONE: what changed, evidence, remaining issues.

## Example
- Input/symptom: Thin supplier copy
- Action: rewrite top sellers first
- Output: E-commerce audit sheet.

## Dependencies (load only if needed)
- 08-ecommerce-seo
- 09-woocommerce-seo
- 10-shopify-seo

## References
`references/playbook.md`: detailed how-to, common problems and fixes, tools, verify steps. Read when executing.
