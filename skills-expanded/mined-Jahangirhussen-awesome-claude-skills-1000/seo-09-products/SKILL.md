---
name: seo-09-products
description: Products (SEO). Use when the request involves: woocommerce product seo, variable product. Not for topics owned by sibling SEO skills or other categories; routed by seo-master.
---

# Products

ID: 09.01 | Level: child | Parent: [WooCommerce SEO](../SKILL.md)

## Purpose
Products within the seo-master tree: Product page checklist.

## When to use
Triggers: woocommerce product seo, variable product

## When NOT to use
- The topic is covered by a sibling skill: `../attributes`, `../categories`, `../filters`, `../product-schema`, `../woocommerce-technical`.
- The task is outside this SEO category; see `ROUTER.md` at the seo-master root.

## Inputs
- Target site/URL(s) or project files, platform (CMS/framework), and goal.
- Data access as available: WooCommerce admin, Yoast/Rank Math, Query Monitor, Screaming Frog, WP-CLI, Rich Results Test.

## Core workflow
1. Unique title/description; use short description for summary, long for detail
2. Set canonical for variations to the parent product
3. Images with alt; gallery optimized
4. Handle out-of-stock (keep page, show notice) and discontinued (301)

## Decision rules and checks
- Unique titles/descriptions, short vs long description
- Variations: canonical to parent
- Out-of-stock handling

## Edge cases and failure handling
- Product in multiple categories creating duplicate URLs -> primary category in SEO plugin
- Draft/private products leaking -> check status

## Validation
- Re-fetch or re-crawl changed URLs; confirm the fix is live (status, rendered HTML, canonical, schema validator, GSC URL Inspection as relevant).
- Compare with the baseline recorded before the change; check for regressions on neighbouring templates.

## Output requirements
Product page checklist. Report as a short DONE: what changed, evidence, remaining issues.

## Example
- Input/symptom: Product in multiple categories creating duplicate URLs
- Action: primary category in SEO plugin
- Output: Product page checklist.

## Dependencies (load only if needed)
- 08-ecommerce-seo/product-seo

## References
`references/playbook.md`: detailed how-to, common problems and fixes, tools, verify steps. Read when executing.
