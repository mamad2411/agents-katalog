---
name: seo-05-link-audit
description: Link audit (SEO). Use when the request involves: toxic links, disavow, link penalty, backlink audit. Not for topics owned by sibling SEO skills or other categories; routed by seo-master.
---

# Link audit

ID: 05.06 | Level: child | Parent: [Off-Page SEO](../SKILL.md)

## Purpose
Link audit within the seo-master tree: Audit sheet: domain, issue, decision.

## When to use
Triggers: toxic links, disavow, link penalty, backlink audit

## When NOT to use
- The topic is covered by a sibling skill: `../backlinks`, `../brand-mentions`, `../digital-pr`, `../guest-posting`, `../link-building`.
- The task is outside this SEO category; see `ROUTER.md` at the seo-master root.

## Inputs
- Target site/URL(s) or project files, platform (CMS/framework), and goal.
- Data access as available: Ahrefs, Semrush, Majestic, Google Search Console Links report, Google Alerts, outreach CRM or spreadsheet.

## Core workflow
1. Export links; flag patterns (exact-match anchors, link networks, foreign spam)
2. Review manually before action; most weird links are ignored by Google
3. Disavow only when manual action risk or clear manipulation
4. Document before/after

## Decision rules and checks
- Profile health + anchors
- Identify truly toxic patterns
- Disavow only for manual-action risk

## Edge cases and failure handling
- Mass-disavow harming good links -> be conservative
- Manual action present -> remove links, then reconsideration request

## Validation
- Re-fetch or re-crawl changed URLs; confirm the fix is live (status, rendered HTML, canonical, schema validator, GSC URL Inspection as relevant).
- Compare with the baseline recorded before the change; check for regressions on neighbouring templates.

## Output requirements
Audit sheet: domain, issue, decision. Report as a short DONE: what changed, evidence, remaining issues.

## Example
- Input/symptom: Mass-disavow harming good links
- Action: be conservative
- Output: Audit sheet: domain, issue, decision.

## Merged from (read for deep method)
- `../../_source/seo-backlink-audit/SKILL.md`

## References
`references/playbook.md`: detailed how-to, common problems and fixes, tools, verify steps. Read when executing.
