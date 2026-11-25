---
name: seo-30
description: 30. SEO Audit (SEO). Use when the request involves: seo audit, site audit, technical audit, on-page audit, backlink audit, ecommerce audit, full audit, seo health check. Not for topics owned by sibling SEO skills or other categories; routed by seo-master.
---

# 30. SEO Audit

ID: 30 | Level: parent | Parent: SEO Master

## Purpose
Inspect first, run only applicable modules, prioritize, fix.

## When to use
Triggers: seo audit, site audit, technical audit, on-page audit, backlink audit, ecommerce audit, full audit, seo health check

## When NOT to use
- The request belongs to another SEO category (see `../ROUTER.md`): e.g. core seo, google seo, technical seo, on page seo, off page seo, content seo.
- A more specific child skill already covers it: open that child instead of repeating its work.

## Inputs
- Target site/URL(s) or project files, platform (CMS/framework), and goal.
- Data access as available: Screaming Frog, GSC, GA4, Lighthouse, Ahrefs/Semrush, schema validator, platform-specific plugins.

## Core workflow
1. Detect platform and site type first
2. Run applicable modules: technical, on-page, content, links, schema, speed, platform-specific, AI visibility
3. Score by impact and effort; P0/P1/P2
4. Fix in scope and re-test if asked

## Decision rules
- Use evidence (crawl, GSC, rendered HTML, validators), not assumptions.
- Fix the highest-impact, lowest-risk items first; change only what the task needs.
- If a platform skill (WordPress, WooCommerce, Shopify) applies, its guidance overrides generic advice.

## Edge cases and failure handling
- Everything critical -> rank by traffic/revenue impact

## Validation
- Re-fetch or re-crawl changed URLs; confirm the fix is live (status, rendered HTML, canonical, schema validator, GSC URL Inspection as relevant).
- Compare with the baseline recorded before the change; check for regressions on neighbouring templates.

## Output requirements
Audit report: findings, evidence, fix, priority. Report as a short DONE: what changed, evidence, remaining issues.

## Example
- Input/symptom: Everything critical
- Action: rank by traffic/revenue impact
- Output: Audit report: findings, evidence, fix, priority.

## Children
- [Full audit](full-audit/SKILL.md)
- [Technical audit](technical-audit/SKILL.md)
- [On-page audit](onpage-audit/SKILL.md)
- [Backlink audit](backlink-audit/SKILL.md)
- [E-commerce audit](ecommerce-audit/SKILL.md)

## Merged from (read for deep method)
- `../_source/seo-audit/SKILL.md`
- `../_source/seo-audit-orchestration/SKILL.md`

## Related installed skills (kept in place; invoke only if needed)
- `security-reviewer`

## References
`references/playbook.md`: detailed how-to, common problems and fixes, tools, verify steps. Read when executing.
