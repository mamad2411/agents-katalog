---
name: seo-27-product
description: Product and Offer (SEO). Use when the request involves: product schema, offer, price. Not for topics owned by sibling SEO skills or other categories; routed by seo-master.
---

# Product and Offer

ID: 27.03 | Level: child | Parent: [Schema / Structured Data](../SKILL.md)

## Purpose
Product and Offer within the seo-master tree: Product JSON-LD.

## When to use
Triggers: product schema, offer, price

## When NOT to use
- The topic is covered by a sibling skill: `../article`, `../breadcrumb`, `../faq`, `../local-business`, `../organization`.
- The task is outside this SEO category; see `ROUTER.md` at the seo-master root.

## Inputs
- Target site/URL(s) or project files, platform (CMS/framework), and goal.
- Data access as available: Rich Results Test, Schema Markup Validator (validator.schema.org), GSC Enhancements, JSON-LD generator or code.

## Core workflow
1. Product: name, image, description, sku, brand; offers with price, priceCurrency, availability
2. Add gtin/mpn when available
3. AggregateRating only with real visible reviews

## Decision rules and checks
- name, image, sku/gtin, brand, offers(price,currency,availability)
- AggregateRating only with visible real reviews

## Edge cases and failure handling
- Price missing in page -> show it

## Validation
- Re-fetch or re-crawl changed URLs; confirm the fix is live (status, rendered HTML, canonical, schema validator, GSC URL Inspection as relevant).
- Compare with the baseline recorded before the change; check for regressions on neighbouring templates.

## Output requirements
Product JSON-LD. Report as a short DONE: what changed, evidence, remaining issues.

## Example
- Input/symptom: Price missing in page
- Action: show it
- Output: Product JSON-LD.

## References
`references/playbook.md`: detailed how-to, common problems and fixes, tools, verify steps. Read when executing.
