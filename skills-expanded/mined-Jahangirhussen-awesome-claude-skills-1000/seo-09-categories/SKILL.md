---
name: seo-09-categories
description: Categories (SEO). Use when the request involves: woocommerce category, shop page. Not for topics owned by sibling SEO skills or other categories; routed by seo-master.
---

# Categories

ID: 09.02 | Level: child | Parent: [WooCommerce SEO](../SKILL.md)

## Purpose
Categories within the seo-master tree: Category template.

## When to use
Triggers: woocommerce category, shop page

## When NOT to use
- The topic is covered by a sibling skill: `../attributes`, `../filters`, `../product-schema`, `../products`, `../woocommerce-technical`.
- The task is outside this SEO category; see `ROUTER.md` at the seo-master root.

## Inputs
- Target site/URL(s) or project files, platform (CMS/framework), and goal.
- Data access as available: WooCommerce admin, Yoast/Rank Math, Query Monitor, Screaming Frog, WP-CLI, Rich Results Test.

## Core workflow
1. Edit category descriptions and titles in SEO plugin
2. Control pagination and 'products per page'
3. Hide empty categories from nav
4. Link subcategories

## Decision rules and checks
- Category descriptions
- Pagination
- Shop page title/intro

## Edge cases and failure handling
- Shop page thin -> add intro and curated links
- Category base in URL causing duplicates -> pick one structure

## Validation
- Re-fetch or re-crawl changed URLs; confirm the fix is live (status, rendered HTML, canonical, schema validator, GSC URL Inspection as relevant).
- Compare with the baseline recorded before the change; check for regressions on neighbouring templates.

## Output requirements
Category template. Report as a short DONE: what changed, evidence, remaining issues.

## Example
- Input/symptom: Shop page thin
- Action: add intro and curated links
- Output: Category template.

## References
`references/playbook.md`: detailed how-to, common problems and fixes, tools, verify steps. Read when executing.
