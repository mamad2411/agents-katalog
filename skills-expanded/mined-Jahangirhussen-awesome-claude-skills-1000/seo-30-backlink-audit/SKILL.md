---
name: seo-30-backlink-audit
description: Backlink audit (SEO). Use when the request involves: backlink audit. Not for topics owned by sibling SEO skills or other categories; routed by seo-master.
---

# Backlink audit

ID: 30.04 | Level: child | Parent: [SEO Audit](../SKILL.md)

## Purpose
Backlink audit within the seo-master tree: Backlink audit sheet.

## When to use
Triggers: backlink audit

## When NOT to use
- The topic is covered by a sibling skill: `../ecommerce-audit`, `../full-audit`, `../onpage-audit`, `../technical-audit`.
- The task is outside this SEO category; see `ROUTER.md` at the seo-master root.

## Inputs
- Target site/URL(s) or project files, platform (CMS/framework), and goal.
- Data access as available: Screaming Frog, GSC, GA4, Lighthouse, Ahrefs/Semrush, schema validator, platform-specific plugins.

## Core workflow
1. Profile referring domains, anchors, toxicity patterns
2. Compare to competitors
3. Plan reclaim and acquisition

## Decision rules and checks
- Profile, anchors, toxic, gap

## Edge cases and failure handling
- Over-trusting toxicity scores -> manual review

## Validation
- Re-fetch or re-crawl changed URLs; confirm the fix is live (status, rendered HTML, canonical, schema validator, GSC URL Inspection as relevant).
- Compare with the baseline recorded before the change; check for regressions on neighbouring templates.

## Output requirements
Backlink audit sheet. Report as a short DONE: what changed, evidence, remaining issues.

## Example
- Input/symptom: Over-trusting toxicity scores
- Action: manual review
- Output: Backlink audit sheet.

## Dependencies (load only if needed)
- 05-off-page-seo/link-audit

## References
`references/playbook.md`: detailed how-to, common problems and fixes, tools, verify steps. Read when executing.
