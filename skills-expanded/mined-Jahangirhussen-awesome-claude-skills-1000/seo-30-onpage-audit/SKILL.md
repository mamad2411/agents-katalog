---
name: seo-30-onpage-audit
description: On-page audit (SEO). Use when the request involves: on-page audit. Not for topics owned by sibling SEO skills or other categories; routed by seo-master.
---

# On-page audit

ID: 30.03 | Level: child | Parent: [SEO Audit](../SKILL.md)

## Purpose
On-page audit within the seo-master tree: On-page audit sheet.

## When to use
Triggers: on-page audit

## When NOT to use
- The topic is covered by a sibling skill: `../backlink-audit`, `../ecommerce-audit`, `../full-audit`, `../technical-audit`.
- The task is outside this SEO category; see `ROUTER.md` at the seo-master root.

## Inputs
- Target site/URL(s) or project files, platform (CMS/framework), and goal.
- Data access as available: Screaming Frog, GSC, GA4, Lighthouse, Ahrefs/Semrush, schema validator, platform-specific plugins.

## Core workflow
1. Evaluate titles, metas, headings, content, internal links per template
2. Compare to SERP intent
3. Fix patterns first

## Decision rules and checks
- Titles/meta/H1/internal links/content per template

## Edge cases and failure handling
- Per-page edits at scale -> template/pattern

## Validation
- Re-fetch or re-crawl changed URLs; confirm the fix is live (status, rendered HTML, canonical, schema validator, GSC URL Inspection as relevant).
- Compare with the baseline recorded before the change; check for regressions on neighbouring templates.

## Output requirements
On-page audit sheet. Report as a short DONE: what changed, evidence, remaining issues.

## Example
- Input/symptom: Per-page edits at scale
- Action: template/pattern
- Output: On-page audit sheet.

## Dependencies (load only if needed)
- 04-on-page-seo

## References
`references/playbook.md`: detailed how-to, common problems and fixes, tools, verify steps. Read when executing.
