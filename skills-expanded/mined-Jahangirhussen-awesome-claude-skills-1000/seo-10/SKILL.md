---
name: seo-10
description: 10. Shopify SEO (SEO). Use when the request involves: shopify seo, collection, liquid, shopify canonical, shopify app conflict, robots.txt.liquid. Not for topics owned by sibling SEO skills or other categories; routed by seo-master.
---

# 10. Shopify SEO

ID: 10 | Level: parent | Parent: SEO Master

## Purpose
Shopify specifics.

## When to use
Triggers: shopify seo, collection, liquid, shopify canonical, shopify app conflict, robots.txt.liquid

## When NOT to use
- The request belongs to another SEO category (see `../ROUTER.md`): e.g. core seo, google seo, technical seo, on page seo, off page seo, content seo.
- A more specific child skill already covers it: open that child instead of repeating its work.

## Inputs
- Target site/URL(s) or project files, platform (CMS/framework), and goal.
- Data access as available: Shopify admin (themes, redirects, navigation), Liquid editor, Screaming Frog, Rich Results Test, app list.

## Core workflow
1. Review theme (Liquid) for H1, meta, canonical, schema
2. Audit collections/products URL patterns and duplicates
3. Review apps injecting scripts/schema
4. Check robots.txt.liquid and sitemap

## Decision rules
- Use evidence (crawl, GSC, rendered HTML, validators), not assumptions.
- Fix the highest-impact, lowest-risk items first; change only what the task needs.
- If a platform skill (WordPress, WooCommerce, Shopify) applies, its guidance overrides generic advice.

## Edge cases and failure handling
- Duplicate product URLs via /collections/ path -> theme should use product canonical
- App bloat -> remove unused apps

## Validation
- Re-fetch or re-crawl changed URLs; confirm the fix is live (status, rendered HTML, canonical, schema validator, GSC URL Inspection as relevant).
- Compare with the baseline recorded before the change; check for regressions on neighbouring templates.

## Output requirements
Shopify SEO issue list. Report as a short DONE: what changed, evidence, remaining issues.

## Example
- Input/symptom: Duplicate product URLs via /collections/ path
- Action: theme should use product canonical
- Output: Shopify SEO issue list.

## Children
- [Products](products/SKILL.md)
- [Collections](collections/SKILL.md)
- [Shopify technical](shopify-technical/SKILL.md)
- [Liquid / theme SEO](liquid-seo/SKILL.md)
- [Shopify structured data](structured-data/SKILL.md)
- [Shopify migration](shopify-migration/SKILL.md)

## Related installed skills (kept in place; invoke only if needed)
- `shopify-expert`

## References
`references/playbook.md`: detailed how-to, common problems and fixes, tools, verify steps. Read when executing.
