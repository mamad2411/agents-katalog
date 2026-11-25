---
name: seo-06-content-refresh
description: Content audit and refresh (SEO). Use when the request involves: content audit, refresh, prune, thin content, duplicate content, cannibalization. Not for topics owned by sibling SEO skills or other categories; routed by seo-master.
---

# Content audit and refresh

ID: 06.06 | Level: child | Parent: [Content SEO](../SKILL.md)

## Purpose
Content audit and refresh within the seo-master tree: Refresh queue with actions and results.

## When to use
Triggers: content audit, refresh, prune, thin content, duplicate content, cannibalization

## When NOT to use
- The topic is covered by a sibling skill: `../content-clusters`, `../content-gap`, `../content-strategy`, `../seo-copywriting`, `../topical-authority`.
- The task is outside this SEO category; see `ROUTER.md` at the seo-master root.

## Inputs
- Target site/URL(s) or project files, platform (CMS/framework), and goal.
- Data access as available: Google Search Console, GA4, Ahrefs/Semrush content gap, SERP analysis, content brief template, CMS.

## Core workflow
1. List pages with declining clicks or outdated facts
2. Decide: update, merge, redirect, or delete
3. Refresh facts, examples, screenshots, links; improve intro and structure
4. Update modified date honestly; resubmit in GSC if needed

## Decision rules and checks
- Keep / update / merge / redirect / delete decision
- Refresh by traffic decay + opportunity
- Fix cannibalization via merge/301

## Edge cases and failure handling
- Merging pages without 301 -> add redirects
- Cosmetic date bumps -> do real updates

## Validation
- Re-fetch or re-crawl changed URLs; confirm the fix is live (status, rendered HTML, canonical, schema validator, GSC URL Inspection as relevant).
- Compare with the baseline recorded before the change; check for regressions on neighbouring templates.

## Output requirements
Refresh queue with actions and results. Report as a short DONE: what changed, evidence, remaining issues.

## Example
- Input/symptom: Merging pages without 301
- Action: add redirects
- Output: Refresh queue with actions and results.

## Dependencies (load only if needed)
- content-refresh-system (installed skill)

## Merged from (read for deep method)
- `../../_source/seo-content-audit/SKILL.md`

## External sources merged (deep method)
- `../../_source/aaron__content-quality-auditor/SKILL.md`
- `../../_source/aaron__content-refresher/SKILL.md`

## References
`references/playbook.md`: detailed how-to, common problems and fixes, tools, verify steps. Read when executing.
