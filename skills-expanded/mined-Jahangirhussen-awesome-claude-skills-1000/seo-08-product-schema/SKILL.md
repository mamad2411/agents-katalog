---
name: seo-08-product-schema
description: Product schema (SEO). Use when the request involves: product schema, offer, review schema. Not for topics owned by sibling SEO skills or other categories; routed by seo-master.
---

# Product schema

ID: 08.04 | Level: child | Parent: [E-commerce SEO](../SKILL.md)

## Purpose
Product schema within the seo-master tree: Product JSON-LD template.

## When to use
Triggers: product schema, offer, review schema

## When NOT to use
- The topic is covered by a sibling skill: `../category-seo`, `../ecommerce-content`, `../faceted-navigation`, `../merchant-center`, `../product-seo`.
- The task is outside this SEO category; see `ROUTER.md` at the seo-master root.

## Inputs
- Target site/URL(s) or project files, platform (CMS/framework), and goal.
- Data access as available: Screaming Frog, Google Search Console, Merchant Center, Rich Results Test, platform admin, feed validator.

## Core workflow
1. Product with name, image, description, sku, brand, offers
2. Offer: price, priceCurrency, availability, url; add gtin if available
3. AggregateRating/Review only if real, visible
4. Validate; compare to feed values

## Decision rules and checks
- Product + Offer + price/availability
- AggregateRating only with real reviews

## Edge cases and failure handling
- Price mismatch with page -> sync from same source
- Duplicate schema from plugin + theme -> keep one

## Validation
- Re-fetch or re-crawl changed URLs; confirm the fix is live (status, rendered HTML, canonical, schema validator, GSC URL Inspection as relevant).
- Compare with the baseline recorded before the change; check for regressions on neighbouring templates.

## Output requirements
Product JSON-LD template. Report as a short DONE: what changed, evidence, remaining issues.

## Example
- Input/symptom: Price mismatch with page
- Action: sync from same source
- Output: Product JSON-LD template.

## Dependencies (load only if needed)
- 27-schema-seo/product

## References
`references/playbook.md`: detailed how-to, common problems and fixes, tools, verify steps. Read when executing.
