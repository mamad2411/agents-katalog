---
name: seo-31
description: 31. SEO Migration (SEO). Use when the request involves: seo migration, domain change, https migration, replatform, redirect map, relaunch, ranking recovery. Not for topics owned by sibling SEO skills or other categories; routed by seo-master.
---

# 31. SEO Migration

ID: 31 | Level: parent | Parent: SEO Master

## Purpose
Move without losing rankings.

## When to use
Triggers: seo migration, domain change, https migration, replatform, redirect map, relaunch, ranking recovery

## When NOT to use
- The request belongs to another SEO category (see `../ROUTER.md`): e.g. core seo, google seo, technical seo, on page seo, off page seo, content seo.
- A more specific child skill already covers it: open that child instead of repeating its work.

## Inputs
- Target site/URL(s) or project files, platform (CMS/framework), and goal.
- Data access as available: Screaming Frog (before/after crawls), redirect mapping sheet, GSC Change of Address, server config, log analysis.

## Core workflow
1. Crawl and snapshot old site (URLs, titles, canonicals, rankings, backlinks)
2. Map every old URL to a new URL 1:1 where possible
3. Stage and test; launch; monitor daily

## Decision rules
- Use evidence (crawl, GSC, rendered HTML, validators), not assumptions.
- Fix the highest-impact, lowest-risk items first; change only what the task needs.
- If a platform skill (WordPress, WooCommerce, Shopify) applies, its guidance overrides generic advice.

## Edge cases and failure handling
- Launching without redirect map -> do not launch

## Validation
- Re-fetch or re-crawl changed URLs; confirm the fix is live (status, rendered HTML, canonical, schema validator, GSC URL Inspection as relevant).
- Compare with the baseline recorded before the change; check for regressions on neighbouring templates.

## Output requirements
Migration plan and QA checklist. Report as a short DONE: what changed, evidence, remaining issues.

## Example
- Input/symptom: Launching without redirect map
- Action: do not launch
- Output: Migration plan and QA checklist.

## Children
- [Domain migration](domain-migration/SKILL.md)
- [Platform migration](platform-migration/SKILL.md)
- [URL migration](url-migration/SKILL.md)
- [Migration monitoring](migration-monitoring/SKILL.md)

## Related installed skills (kept in place; invoke only if needed)
- `migration-architect`

## References
`references/playbook.md`: detailed how-to, common problems and fixes, tools, verify steps. Read when executing.
