---
name: seo-09
description: 09. WooCommerce SEO (SEO). Use when the request involves: woocommerce seo, woo product not indexed, shop page, product attributes, variable product, cart noindex. Not for topics owned by sibling SEO skills or other categories; routed by seo-master.
---

# 09. WooCommerce SEO

ID: 09 | Level: parent | Parent: SEO Master

## Purpose
WooCommerce specifics; inherits 08 and 03.

## When to use
Triggers: woocommerce seo, woo product not indexed, shop page, product attributes, variable product, cart noindex

## When NOT to use
- The request belongs to another SEO category (see `../ROUTER.md`): e.g. core seo, google seo, technical seo, on page seo, off page seo, content seo.
- A more specific child skill already covers it: open that child instead of repeating its work.

## Inputs
- Target site/URL(s) or project files, platform (CMS/framework), and goal.
- Data access as available: WooCommerce admin, Yoast/Rank Math, Query Monitor, Screaming Frog, WP-CLI, Rich Results Test.

## Core workflow
1. Check Settings > Permalinks, SEO plugin, cart/checkout noindex
2. Audit product/category/attribute archives and tags
3. Check variations, filters, sitemap, speed, schema duplication

## Decision rules
- Use evidence (crawl, GSC, rendered HTML, validators), not assumptions.
- Fix the highest-impact, lowest-risk items first; change only what the task needs.
- If a platform skill (WordPress, WooCommerce, Shopify) applies, its guidance overrides generic advice.

## Edge cases and failure handling
- Cart/checkout indexed -> noindex
- Duplicate schema (theme + Yoast/Rank Math + WooCommerce) -> keep one

## Validation
- Re-fetch or re-crawl changed URLs; confirm the fix is live (status, rendered HTML, canonical, schema validator, GSC URL Inspection as relevant).
- Compare with the baseline recorded before the change; check for regressions on neighbouring templates.

## Output requirements
Woo SEO issue list. Report as a short DONE: what changed, evidence, remaining issues.

## Example
- Input/symptom: Cart/checkout indexed
- Action: noindex
- Output: Woo SEO issue list.

## Children
- [Products](products/SKILL.md)
- [Categories](categories/SKILL.md)
- [Attributes](attributes/SKILL.md)
- [Filters](filters/SKILL.md)
- [Product schema in Woo](product-schema/SKILL.md)
- [Woo technical](woocommerce-technical/SKILL.md)

## Topics handled here (no separate child)
- Cart/checkout/my-account: noindex
- Permalinks: strip /product-category/ base only if safe; no duplicate product URLs
- Sitemap: product, category, no attribute/tag junk
- Speed: object cache, image sizes, remove unused plugins/scripts

## Related installed skills (kept in place; invoke only if needed)
- `woocommerce-health-check`
- `woo-catalog-perfection`
- `wp-performance-review`
- `wordpress-pro`

## References
`references/playbook.md`: detailed how-to, common problems and fixes, tools, verify steps. Read when executing.
