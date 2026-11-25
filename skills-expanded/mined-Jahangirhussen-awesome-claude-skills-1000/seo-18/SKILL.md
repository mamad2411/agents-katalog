---
name: seo-18
description: 18. International SEO (SEO). Use when the request involves: international seo, hreflang, multilingual, country targeting, translation seo, cctld, subdirectory. Not for topics owned by sibling SEO skills or other categories; routed by seo-master.
---

# 18. International SEO

ID: 18 | Level: parent | Parent: SEO Master

## Purpose
Multi-language / multi-region.

## When to use
Triggers: international seo, hreflang, multilingual, country targeting, translation seo, cctld, subdirectory

## When NOT to use
- The request belongs to another SEO category (see `../ROUTER.md`): e.g. core seo, google seo, technical seo, on page seo, off page seo, content seo.
- A more specific child skill already covers it: open that child instead of repeating its work.

## Inputs
- Target site/URL(s) or project files, platform (CMS/framework), and goal.
- Data access as available: hreflang validator or Screaming Frog hreflang tab, GSC international targeting data, localization team, sitemap.

## Core workflow
1. Decide structure (subfolders default, ccTLD, subdomain)
2. Localize content (not just translate)
3. Implement hreflang and locale canonicals
4. Check geotargeting and local signals

## Decision rules
- Use evidence (crawl, GSC, rendered HTML, validators), not assumptions.
- Fix the highest-impact, lowest-risk items first; change only what the task needs.
- If a platform skill (WordPress, WooCommerce, Shopify) applies, its guidance overrides generic advice.

## Edge cases and failure handling
- Auto-redirect by IP blocks bots -> use banners instead
- Mixed language pages -> separate URLs per language

## Validation
- Re-fetch or re-crawl changed URLs; confirm the fix is live (status, rendered HTML, canonical, schema validator, GSC URL Inspection as relevant).
- Compare with the baseline recorded before the change; check for regressions on neighbouring templates.

## Output requirements
International SEO plan. Report as a short DONE: what changed, evidence, remaining issues.

## Example
- Input/symptom: Auto-redirect by IP blocks bots
- Action: use banners instead
- Output: International SEO plan.

## Children
- [Hreflang](hreflang/SKILL.md)
- [Multilingual content](multilingual/SKILL.md)
- [Country targeting](country-targeting/SKILL.md)
- [International architecture](international-architecture/SKILL.md)

## Topics handled here (no separate child)
- Regional keywords: research per market, do not machine-translate keywords

## Related installed skills (kept in place; invoke only if needed)
- `internationalization`

## References
`references/playbook.md`: detailed how-to, common problems and fixes, tools, verify steps. Read when executing.
