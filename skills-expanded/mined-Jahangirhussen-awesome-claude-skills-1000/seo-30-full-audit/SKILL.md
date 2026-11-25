---
name: seo-30-full-audit
description: Full audit (SEO). Use when the request involves: seo audit, full site audit, what is wrong with my seo. Not for topics owned by sibling SEO skills or other categories; routed by seo-master.
---

# Full audit

ID: 30.01 | Level: child | Parent: [SEO Audit](../SKILL.md)

## Purpose
Full audit within the seo-master tree: Full audit report.

## When to use
Triggers: seo audit, full site audit, what is wrong with my seo

## When NOT to use
- The topic is covered by a sibling skill: `../backlink-audit`, `../ecommerce-audit`, `../onpage-audit`, `../technical-audit`.
- The task is outside this SEO category; see `ROUTER.md` at the seo-master root.

## Inputs
- Target site/URL(s) or project files, platform (CMS/framework), and goal.
- Data access as available: Screaming Frog, GSC, GA4, Lighthouse, Ahrefs/Semrush, schema validator, platform-specific plugins.

## Core workflow
1. Crawl site; pull GSC/GA4
2. Run technical, on-page, content, link, schema, performance checks
3. Merge duplicates between modules
4. Deliver prioritized fix list

## Decision rules and checks
- Detect platform + site type
- Run only applicable modules in parallel
- Score + P0/P1/P2 fix list

## Edge cases and failure handling
- Huge sites -> sample by template

## Validation
- Re-fetch or re-crawl changed URLs; confirm the fix is live (status, rendered HTML, canonical, schema validator, GSC URL Inspection as relevant).
- Compare with the baseline recorded before the change; check for regressions on neighbouring templates.

## Output requirements
Full audit report. Report as a short DONE: what changed, evidence, remaining issues.

## Example
- Input/symptom: Huge sites
- Action: sample by template
- Output: Full audit report.

## Dependencies (load only if needed)
- 30-seo-audit/technical-audit
- 30-seo-audit/onpage-audit

## Merged from (read for deep method)
- `../../_source/seo-audit/SKILL.md`

## External sources merged (deep method)
- `../../_source/borghei__seo-audit/SKILL.md`

## References
`references/playbook.md`: detailed how-to, common problems and fixes, tools, verify steps. Read when executing.
