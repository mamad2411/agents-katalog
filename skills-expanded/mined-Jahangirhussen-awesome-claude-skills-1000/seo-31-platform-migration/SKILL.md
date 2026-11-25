---
name: seo-31-platform-migration
description: Platform migration (SEO). Use when the request involves: replatform, wordpress to shopify. Not for topics owned by sibling SEO skills or other categories; routed by seo-master.
---

# Platform migration

ID: 31.02 | Level: child | Parent: [SEO Migration](../SKILL.md)

## Purpose
Platform migration within the seo-master tree: Platform migration QA.

## When to use
Triggers: replatform, wordpress to shopify

## When NOT to use
- The topic is covered by a sibling skill: `../domain-migration`, `../migration-monitoring`, `../url-migration`.
- The task is outside this SEO category; see `ROUTER.md` at the seo-master root.

## Inputs
- Target site/URL(s) or project files, platform (CMS/framework), and goal.
- Data access as available: Screaming Frog (before/after crawls), redirect mapping sheet, GSC Change of Address, server config, log analysis.

## Core workflow
1. Preserve URLs/structure when possible
2. Migrate titles, metas, schema, content, images with alt
3. Test staging with crawler vs old crawl
4. Check speed and rendering

## Decision rules and checks
- Crawl + snapshot old site
- Preserve URLs/titles/content
- Test on staging

## Edge cases and failure handling
- URL changes unavoidable -> complete 301 map

## Validation
- Re-fetch or re-crawl changed URLs; confirm the fix is live (status, rendered HTML, canonical, schema validator, GSC URL Inspection as relevant).
- Compare with the baseline recorded before the change; check for regressions on neighbouring templates.

## Output requirements
Platform migration QA. Report as a short DONE: what changed, evidence, remaining issues.

## Example
- Input/symptom: URL changes unavoidable
- Action: complete 301 map
- Output: Platform migration QA.

## References
`references/playbook.md`: detailed how-to, common problems and fixes, tools, verify steps. Read when executing.
