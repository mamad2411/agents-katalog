---
name: seo-09-attributes
description: Attributes (SEO). Use when the request involves: product attributes, tags. Not for topics owned by sibling SEO skills or other categories; routed by seo-master.
---

# Attributes

ID: 09.03 | Level: child | Parent: [WooCommerce SEO](../SKILL.md)

## Purpose
Attributes within the seo-master tree: Attribute indexing policy.

## When to use
Triggers: product attributes, tags

## When NOT to use
- The topic is covered by a sibling skill: `../categories`, `../filters`, `../product-schema`, `../products`, `../woocommerce-technical`.
- The task is outside this SEO category; see `ROUTER.md` at the seo-master root.

## Inputs
- Target site/URL(s) or project files, platform (CMS/framework), and goal.
- Data access as available: WooCommerce admin, Yoast/Rank Math, Query Monitor, Screaming Frog, WP-CLI, Rich Results Test.

## Core workflow
1. Decide which attribute archives are useful (brand, size)
2. Noindex low-value attribute archives
3. Make useful ones real landing pages with content

## Decision rules and checks
- Index attribute pages only if useful
- Otherwise noindex

## Edge cases and failure handling
- Thousands of attribute URLs -> noindex or disable archives
- Duplicate content with filters -> canonicalize

## Validation
- Re-fetch or re-crawl changed URLs; confirm the fix is live (status, rendered HTML, canonical, schema validator, GSC URL Inspection as relevant).
- Compare with the baseline recorded before the change; check for regressions on neighbouring templates.

## Output requirements
Attribute indexing policy. Report as a short DONE: what changed, evidence, remaining issues.

## Example
- Input/symptom: Thousands of attribute URLs
- Action: noindex or disable archives
- Output: Attribute indexing policy.

## References
`references/playbook.md`: detailed how-to, common problems and fixes, tools, verify steps. Read when executing.
