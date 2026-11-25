---
name: seo-08-faceted-navigation
description: Faceted navigation (SEO). Use when the request involves: filters, facets, parameters. Not for topics owned by sibling SEO skills or other categories; routed by seo-master.
---

# Faceted navigation

ID: 08.03 | Level: child | Parent: [E-commerce SEO](../SKILL.md)

## Purpose
Faceted navigation within the seo-master tree: Facet policy table: facet, index?, URL pattern.

## When to use
Triggers: filters, facets, parameters

## When NOT to use
- The topic is covered by a sibling skill: `../category-seo`, `../ecommerce-content`, `../merchant-center`, `../product-schema`, `../product-seo`.
- The task is outside this SEO category; see `ROUTER.md` at the seo-master root.

## Inputs
- Target site/URL(s) or project files, platform (CMS/framework), and goal.
- Data access as available: Screaming Frog, Google Search Console, Merchant Center, Rich Results Test, platform admin, feed validator.

## Core workflow
1. List all filter parameters and combos
2. Index only combos with demand (e.g. brand + category); canonical/noindex the rest
3. Block infinite combos from crawl (robots / nofollow / JS)
4. Keep clean URLs for indexable facets

## Decision rules and checks
- Index only high-demand facet combos
- noindex/canonical others
- Block infinite combos from crawl

## Edge cases and failure handling
- Millions of param URLs -> robots rules + noindex + canonical strategy
- Faceted pages in sitemap -> remove non-indexable

## Validation
- Re-fetch or re-crawl changed URLs; confirm the fix is live (status, rendered HTML, canonical, schema validator, GSC URL Inspection as relevant).
- Compare with the baseline recorded before the change; check for regressions on neighbouring templates.

## Output requirements
Facet policy table: facet, index?, URL pattern. Report as a short DONE: what changed, evidence, remaining issues.

## Example
- Input/symptom: Millions of param URLs
- Action: robots rules + noindex + canonical strategy
- Output: Facet policy table: facet, index?, URL pattern.

## References
`references/playbook.md`: detailed how-to, common problems and fixes, tools, verify steps. Read when executing.
