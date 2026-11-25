---
name: seo-30-technical-audit
description: Technical audit (SEO). Use when the request involves: technical audit, site health, crawl audit. Not for topics owned by sibling SEO skills or other categories; routed by seo-master.
---

# Technical audit

ID: 30.02 | Level: child | Parent: [SEO Audit](../SKILL.md)

## Purpose
Technical audit within the seo-master tree: Technical findings table.

## When to use
Triggers: technical audit, site health, crawl audit

## When NOT to use
- The topic is covered by a sibling skill: `../backlink-audit`, `../ecommerce-audit`, `../full-audit`, `../onpage-audit`.
- The task is outside this SEO category; see `ROUTER.md` at the seo-master root.

## Inputs
- Target site/URL(s) or project files, platform (CMS/framework), and goal.
- Data access as available: Screaming Frog, GSC, GA4, Lighthouse, Ahrefs/Semrush, schema validator, platform-specific plugins.

## Core workflow
1. Crawl + GSC indexing + CWV + log files if available
2. Triage by SEO impact (not by error count)
3. Group by root cause (template, plugin, server)

## Decision rules and checks
- Triage by SEO impact not severity count
- Crawl + GSC + CWV evidence

## Edge cases and failure handling
- Thousands of identical errors -> fix once at template

## Validation
- Re-fetch or re-crawl changed URLs; confirm the fix is live (status, rendered HTML, canonical, schema validator, GSC URL Inspection as relevant).
- Compare with the baseline recorded before the change; check for regressions on neighbouring templates.

## Output requirements
Technical findings table. Report as a short DONE: what changed, evidence, remaining issues.

## Example
- Input/symptom: Thousands of identical errors
- Action: fix once at template
- Output: Technical findings table.

## Dependencies (load only if needed)
- 03-technical-seo

## Merged from (read for deep method)
- `../../_source/seo-site-health-audit/SKILL.md`

## References
`references/playbook.md`: detailed how-to, common problems and fixes, tools, verify steps. Read when executing.
