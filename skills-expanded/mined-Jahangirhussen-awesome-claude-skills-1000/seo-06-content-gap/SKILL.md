---
name: seo-06-content-gap
description: Content gap (SEO). Use when the request involves: content gap, missing topics, decay. Not for topics owned by sibling SEO skills or other categories; routed by seo-master.
---

# Content gap

ID: 06.04 | Level: child | Parent: [Content SEO](../SKILL.md)

## Purpose
Content gap within the seo-master tree: Gap list with brief links.

## When to use
Triggers: content gap, missing topics, decay

## When NOT to use
- The topic is covered by a sibling skill: `../content-clusters`, `../content-refresh`, `../content-strategy`, `../seo-copywriting`, `../topical-authority`.
- The task is outside this SEO category; see `ROUTER.md` at the seo-master root.

## Inputs
- Target site/URL(s) or project files, platform (CMS/framework), and goal.
- Data access as available: Google Search Console, GA4, Ahrefs/Semrush content gap, SERP analysis, content brief template, CMS.

## Core workflow
1. Compare your ranking keywords with competitors' (keyword gap)
2. Find missing topics, thin pages, and outdated pages
3. Prioritize by intent fit, volume, difficulty, business value
4. Write briefs for the top gaps

## Decision rules and checks
- Compare vs competitors/GSC
- Prioritize by intent + value
- Brief new or expand existing

## Edge cases and failure handling
- Gap keywords off-brand -> exclude
- Too competitive -> target long-tail first

## Validation
- Re-fetch or re-crawl changed URLs; confirm the fix is live (status, rendered HTML, canonical, schema validator, GSC URL Inspection as relevant).
- Compare with the baseline recorded before the change; check for regressions on neighbouring templates.

## Output requirements
Gap list with brief links. Report as a short DONE: what changed, evidence, remaining issues.

## Example
- Input/symptom: Gap keywords off-brand
- Action: exclude
- Output: Gap list with brief links.

## Merged from (read for deep method)
- `../../_source/seo-content-gap-audit/SKILL.md`

## External sources merged (deep method)
- `../../_source/aaron__content-gap-analysis/SKILL.md`

## References
`references/playbook.md`: detailed how-to, common problems and fixes, tools, verify steps. Read when executing.
