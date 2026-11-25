---
name: seo-06
description: 06. Content SEO (SEO). Use when the request involves: content seo, content strategy, topic cluster, pillar page, content gap, seo copywriting, content refresh, content audit, thin content, cannibalization. Not for topics owned by sibling SEO skills or other categories; routed by seo-master.
---

# 06. Content SEO

ID: 06 | Level: parent | Parent: SEO Master

## Purpose
Content planning, creation, refresh.

## When to use
Triggers: content seo, content strategy, topic cluster, pillar page, content gap, seo copywriting, content refresh, content audit, thin content, cannibalization

## When NOT to use
- The request belongs to another SEO category (see `../ROUTER.md`): e.g. core seo, google seo, technical seo, on page seo, off page seo, local seo.
- A more specific child skill already covers it: open that child instead of repeating its work.

## Inputs
- Target site/URL(s) or project files, platform (CMS/framework), and goal.
- Data access as available: Google Search Console, GA4, Ahrefs/Semrush content gap, SERP analysis, content brief template, CMS.

## Core workflow
1. Audit content: traffic, rankings, conversions per URL
2. Decide keep / update / merge / redirect / delete
3. Plan new content from keyword and gap research
4. Publish with briefs and internal links; refresh on schedule

## Decision rules
- Use evidence (crawl, GSC, rendered HTML, validators), not assumptions.
- Fix the highest-impact, lowest-risk items first; change only what the task needs.
- If a platform skill (WordPress, WooCommerce, Shopify) applies, its guidance overrides generic advice.

## Edge cases and failure handling
- Publishing volume over value -> raise quality bar
- Duplicate topics -> consolidate

## Validation
- Re-fetch or re-crawl changed URLs; confirm the fix is live (status, rendered HTML, canonical, schema validator, GSC URL Inspection as relevant).
- Compare with the baseline recorded before the change; check for regressions on neighbouring templates.

## Output requirements
Content plan and refresh queue. Report as a short DONE: what changed, evidence, remaining issues.

## Example
- Input/symptom: Publishing volume over value
- Action: raise quality bar
- Output: Content plan and refresh queue.

## Children
- [Content strategy](content-strategy/SKILL.md)
- [Topical authority](topical-authority/SKILL.md)
- [Content clusters](content-clusters/SKILL.md)
- [Content gap](content-gap/SKILL.md)
- [SEO copywriting](seo-copywriting/SKILL.md)
- [Content audit and refresh](content-refresh/SKILL.md)

## Merged from (read for deep method)
- `../_source/seo-content-audit/SKILL.md`

## Related installed skills (kept in place; invoke only if needed)
- `content-strategy`
- `pillar-content-architecture`
- `content-refresh-system`
- `stale-content-detector`

## References
`references/playbook.md`: detailed how-to, common problems and fixes, tools, verify steps. Read when executing.
