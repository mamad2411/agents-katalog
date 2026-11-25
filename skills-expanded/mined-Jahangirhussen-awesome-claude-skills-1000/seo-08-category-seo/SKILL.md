---
name: seo-08-category-seo
description: Category SEO (SEO). Use when the request involves: category page, collection page. Not for topics owned by sibling SEO skills or other categories; routed by seo-master.
---

# Category SEO

ID: 08.02 | Level: child | Parent: [E-commerce SEO](../SKILL.md)

## Purpose
Category SEO within the seo-master tree: Category template and copy brief.

## When to use
Triggers: category page, collection page

## When NOT to use
- The topic is covered by a sibling skill: `../ecommerce-content`, `../faceted-navigation`, `../merchant-center`, `../product-schema`, `../product-seo`.
- The task is outside this SEO category; see `ROUTER.md` at the seo-master root.

## Inputs
- Target site/URL(s) or project files, platform (CMS/framework), and goal.
- Data access as available: Screaming Frog, Google Search Console, Merchant Center, Rich Results Test, platform admin, feed validator.

## Core workflow
1. Target the commercial head term; one category per intent
2. Short unique intro above products, optional deeper copy below
3. Link to subcategories and top products; keep pagination crawlable
4. Unique titles/meta

## Decision rules and checks
- Intro copy above products, short
- Subcategory links
- Unique titles

## Edge cases and failure handling
- Long text pushing products down -> move below the grid
- Category and tag overlap -> merge

## Validation
- Re-fetch or re-crawl changed URLs; confirm the fix is live (status, rendered HTML, canonical, schema validator, GSC URL Inspection as relevant).
- Compare with the baseline recorded before the change; check for regressions on neighbouring templates.

## Output requirements
Category template and copy brief. Report as a short DONE: what changed, evidence, remaining issues.

## Example
- Input/symptom: Long text pushing products down
- Action: move below the grid
- Output: Category template and copy brief.

## References
`references/playbook.md`: detailed how-to, common problems and fixes, tools, verify steps. Read when executing.
