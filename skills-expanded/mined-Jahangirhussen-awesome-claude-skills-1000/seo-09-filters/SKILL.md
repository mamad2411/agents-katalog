---
name: seo-09-filters
description: Filters (SEO). Use when the request involves: woocommerce filter, layered nav. Not for topics owned by sibling SEO skills or other categories; routed by seo-master.
---

# Filters

ID: 09.04 | Level: child | Parent: [WooCommerce SEO](../SKILL.md)

## Purpose
Filters within the seo-master tree: Filter URL rules.

## When to use
Triggers: woocommerce filter, layered nav

## When NOT to use
- The topic is covered by a sibling skill: `../attributes`, `../categories`, `../product-schema`, `../products`, `../woocommerce-technical`.
- The task is outside this SEO category; see `ROUTER.md` at the seo-master root.

## Inputs
- Target site/URL(s) or project files, platform (CMS/framework), and goal.
- Data access as available: WooCommerce admin, Yoast/Rank Math, Query Monitor, Screaming Frog, WP-CLI, Rich Results Test.

## Core workflow
1. Identify filter plugin URL params (e.g. ?filter_color=, ?min_price=)
2. Canonical to base category; noindex combos
3. Block heavy param crawling
4. Ensure AJAX filters do not break back button/URLs

## Decision rules and checks
- Param URLs canonical to base
- robots/noindex for combos

## Edge cases and failure handling
- Crawl waste on filters -> rules above
- Filtered pages indexed -> remove from sitemap and noindex

## Validation
- Re-fetch or re-crawl changed URLs; confirm the fix is live (status, rendered HTML, canonical, schema validator, GSC URL Inspection as relevant).
- Compare with the baseline recorded before the change; check for regressions on neighbouring templates.

## Output requirements
Filter URL rules. Report as a short DONE: what changed, evidence, remaining issues.

## Example
- Input/symptom: Crawl waste on filters
- Action: rules above
- Output: Filter URL rules.

## Dependencies (load only if needed)
- 08-ecommerce-seo/faceted-navigation

## References
`references/playbook.md`: detailed how-to, common problems and fixes, tools, verify steps. Read when executing.
