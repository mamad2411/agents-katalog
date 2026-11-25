---
name: seo-09-product-schema
description: Product schema in Woo (SEO). Use when the request involves: woocommerce schema. Not for topics owned by sibling SEO skills or other categories; routed by seo-master.
---

# Product schema in Woo

ID: 09.05 | Level: child | Parent: [WooCommerce SEO](../SKILL.md)

## Purpose
Product schema in Woo within the seo-master tree: Schema validation report.

## When to use
Triggers: woocommerce schema

## When NOT to use
- The topic is covered by a sibling skill: `../attributes`, `../categories`, `../filters`, `../products`, `../woocommerce-technical`.
- The task is outside this SEO category; see `ROUTER.md` at the seo-master root.

## Inputs
- Target site/URL(s) or project files, platform (CMS/framework), and goal.
- Data access as available: WooCommerce admin, Yoast/Rank Math, Query Monitor, Screaming Frog, WP-CLI, Rich Results Test.

## Core workflow
1. Use one schema source (Woo core, Yoast WooCommerce, or Rank Math)
2. Verify price, availability, reviews match page
3. Validate variations schema

## Decision rules and checks
- One schema source (plugin XOR theme)
- Validate Offer/price/availability

## Edge cases and failure handling
- Schema duplicates -> disable extra output
- Reviews missing -> enable verified-owner reviews

## Validation
- Re-fetch or re-crawl changed URLs; confirm the fix is live (status, rendered HTML, canonical, schema validator, GSC URL Inspection as relevant).
- Compare with the baseline recorded before the change; check for regressions on neighbouring templates.

## Output requirements
Schema validation report. Report as a short DONE: what changed, evidence, remaining issues.

## Example
- Input/symptom: Schema duplicates
- Action: disable extra output
- Output: Schema validation report.

## Dependencies (load only if needed)
- 27-schema-seo/product

## References
`references/playbook.md`: detailed how-to, common problems and fixes, tools, verify steps. Read when executing.
