---
name: seo-05-guest-posting
description: Guest posting (SEO). Use when the request involves: guest post, contributor. Not for topics owned by sibling SEO skills or other categories; routed by seo-master.
---

# Guest posting

ID: 05.04 | Level: child | Parent: [Off-Page SEO](../SKILL.md)

## Purpose
Guest posting within the seo-master tree: Pitch list and published posts.

## When to use
Triggers: guest post, contributor

## When NOT to use
- The topic is covered by a sibling skill: `../backlinks`, `../brand-mentions`, `../digital-pr`, `../link-audit`, `../link-building`.
- The task is outside this SEO category; see `ROUTER.md` at the seo-master root.

## Inputs
- Target site/URL(s) or project files, platform (CMS/framework), and goal.
- Data access as available: Ahrefs, Semrush, Majestic, Google Search Console Links report, Google Alerts, outreach CRM or spreadsheet.

## Core workflow
1. Choose relevant sites with real audience and editorial standards
2. Pitch useful topics tied to expertise; no spun/AI filler
3. One contextual link at most, brand-safe anchor
4. Skip pay-for-link farms

## Decision rules and checks
- Relevant, real-traffic sites only
- Editorial value, no spun content

## Edge cases and failure handling
- Site sells guest posts openly -> avoid
- Off-topic placements -> not worth it

## Validation
- Re-fetch or re-crawl changed URLs; confirm the fix is live (status, rendered HTML, canonical, schema validator, GSC URL Inspection as relevant).
- Compare with the baseline recorded before the change; check for regressions on neighbouring templates.

## Output requirements
Pitch list and published posts. Report as a short DONE: what changed, evidence, remaining issues.

## Example
- Input/symptom: Site sells guest posts openly
- Action: avoid
- Output: Pitch list and published posts.

## References
`references/playbook.md`: detailed how-to, common problems and fixes, tools, verify steps. Read when executing.
