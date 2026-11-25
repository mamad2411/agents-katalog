---
name: seo-10-shopify-technical
description: Shopify technical (SEO). Use when the request involves: shopify sitemap, shopify robots, shopify speed, shopify duplicate. Not for topics owned by sibling SEO skills or other categories; routed by seo-master.
---

# Shopify technical

ID: 10.03 | Level: child | Parent: [Shopify SEO](../SKILL.md)

## Purpose
Shopify technical within the seo-master tree: Technical checklist.

## When to use
Triggers: shopify sitemap, shopify robots, shopify speed, shopify duplicate

## When NOT to use
- The topic is covered by a sibling skill: `../collections`, `../liquid-seo`, `../products`, `../shopify-migration`, `../structured-data`.
- The task is outside this SEO category; see `ROUTER.md` at the seo-master root.

## Inputs
- Target site/URL(s) or project files, platform (CMS/framework), and goal.
- Data access as available: Shopify admin (themes, redirects, navigation), Liquid editor, Screaming Frog, Rich Results Test, app list.

## Core workflow
1. Review theme.liquid canonical and meta robots
2. Edit robots.txt.liquid carefully (can add disallow rules)
3. Check sitemap.xml index structure
4. Speed: reduce apps, defer scripts, compress images

## Decision rules and checks
- robots.txt.liquid edits carefully
- Auto sitemap review
- Audit apps injecting scripts/schema

## Edge cases and failure handling
- Duplicate pages from /collections/x/products/y -> canonical
- Slow theme -> audit sections and app scripts

## Validation
- Re-fetch or re-crawl changed URLs; confirm the fix is live (status, rendered HTML, canonical, schema validator, GSC URL Inspection as relevant).
- Compare with the baseline recorded before the change; check for regressions on neighbouring templates.

## Output requirements
Technical checklist. Report as a short DONE: what changed, evidence, remaining issues.

## Example
- Input/symptom: Duplicate pages from /collections/x/products/y
- Action: canonical
- Output: Technical checklist.

## Dependencies (load only if needed)
- 03-technical-seo

## References
`references/playbook.md`: detailed how-to, common problems and fixes, tools, verify steps. Read when executing.
