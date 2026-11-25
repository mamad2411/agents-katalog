---
name: seo-08
description: 08. E-commerce SEO (SEO). Use when the request involves: ecommerce seo, product page seo, category page, faceted navigation, product schema, merchant center, out of stock. Not for topics owned by sibling SEO skills or other categories; routed by seo-master.
---

# 08. E-commerce SEO

ID: 08 | Level: parent | Parent: SEO Master

## Purpose
Product/category SEO independent of platform.

## When to use
Triggers: ecommerce seo, product page seo, category page, faceted navigation, product schema, merchant center, out of stock

## When NOT to use
- The request belongs to another SEO category (see `../ROUTER.md`): e.g. core seo, google seo, technical seo, on page seo, off page seo, content seo.
- A more specific child skill already covers it: open that child instead of repeating its work.

## Inputs
- Target site/URL(s) or project files, platform (CMS/framework), and goal.
- Data access as available: Screaming Frog, Google Search Console, Merchant Center, Rich Results Test, platform admin, feed validator.

## Core workflow
1. Crawl categories, products, filters; compare to GSC indexing
2. Check duplicate/thin product pages and param URLs
3. Validate product schema and feed
4. Review internal linking from categories to products

## Decision rules
- Use evidence (crawl, GSC, rendered HTML, validators), not assumptions.
- Fix the highest-impact, lowest-risk items first; change only what the task needs.
- If a platform skill (WordPress, WooCommerce, Shopify) applies, its guidance overrides generic advice.

## Edge cases and failure handling
- Index bloat from filters -> control facets
- Thin manufacturer copy -> write unique descriptions

## Validation
- Re-fetch or re-crawl changed URLs; confirm the fix is live (status, rendered HTML, canonical, schema validator, GSC URL Inspection as relevant).
- Compare with the baseline recorded before the change; check for regressions on neighbouring templates.

## Output requirements
E-commerce SEO audit by template. Report as a short DONE: what changed, evidence, remaining issues.

## Example
- Input/symptom: Index bloat from filters
- Action: control facets
- Output: E-commerce SEO audit by template.

## Children
- [Product SEO](product-seo/SKILL.md)
- [Category SEO](category-seo/SKILL.md)
- [Faceted navigation](faceted-navigation/SKILL.md)
- [Product schema](product-schema/SKILL.md)
- [Merchant Center and Shopping](merchant-center/SKILL.md)
- [E-commerce content](ecommerce-content/SKILL.md)

## Topics handled here (no separate child)
- Variants and out-of-stock: keep URL live if returning; 301/410 if discontinued
- Pagination/internal linking: crawlable paginated links, hub category links

## Related installed skills (kept in place; invoke only if needed)
- `ecommerce-advisor`
- `woo-catalog-perfection`

## References
`references/playbook.md`: detailed how-to, common problems and fixes, tools, verify steps. Read when executing.
