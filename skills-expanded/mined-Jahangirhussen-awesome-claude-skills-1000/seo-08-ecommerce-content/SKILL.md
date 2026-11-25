---
name: seo-08-ecommerce-content
description: E-commerce content (SEO). Use when the request involves: buying guide, ecommerce blog. Not for topics owned by sibling SEO skills or other categories; routed by seo-master.
---

# E-commerce content

ID: 08.06 | Level: child | Parent: [E-commerce SEO](../SKILL.md)

## Purpose
E-commerce content within the seo-master tree: Content calendar tied to categories.

## When to use
Triggers: buying guide, ecommerce blog

## When NOT to use
- The topic is covered by a sibling skill: `../category-seo`, `../faceted-navigation`, `../merchant-center`, `../product-schema`, `../product-seo`.
- The task is outside this SEO category; see `ROUTER.md` at the seo-master root.

## Inputs
- Target site/URL(s) or project files, platform (CMS/framework), and goal.
- Data access as available: Screaming Frog, Google Search Console, Merchant Center, Rich Results Test, platform admin, feed validator.

## Core workflow
1. Create buying guides, comparisons, how-tos linked to categories/products
2. Use real expertise and product testing
3. Add FAQs and size/fit/spec info
4. Link back to money pages

## Decision rules and checks
- Buying guides linking to categories
- Comparison + how-to

## Edge cases and failure handling
- Blog does not convert -> add contextual product links
- Duplicate guides -> consolidate

## Validation
- Re-fetch or re-crawl changed URLs; confirm the fix is live (status, rendered HTML, canonical, schema validator, GSC URL Inspection as relevant).
- Compare with the baseline recorded before the change; check for regressions on neighbouring templates.

## Output requirements
Content calendar tied to categories. Report as a short DONE: what changed, evidence, remaining issues.

## Example
- Input/symptom: Blog does not convert
- Action: add contextual product links
- Output: Content calendar tied to categories.

## References
`references/playbook.md`: detailed how-to, common problems and fixes, tools, verify steps. Read when executing.
