---
name: seo-07-citations
description: Citations / NAP (SEO). Use when the request involves: citations, nap, directories. Not for topics owned by sibling SEO skills or other categories; routed by seo-master.
---

# Citations / NAP

ID: 07.03 | Level: child | Parent: [Local SEO](../SKILL.md)

## Purpose
Citations / NAP within the seo-master tree: Citation sheet: site, status, URL.

## When to use
Triggers: citations, nap, directories

## When NOT to use
- The topic is covered by a sibling skill: `../google-business-profile`, `../local-keywords`, `../local-links`, `../local-schema`, `../reviews`.
- The task is outside this SEO category; see `ROUTER.md` at the seo-master root.

## Inputs
- Target site/URL(s) or project files, platform (CMS/framework), and goal.
- Data access as available: Google Business Profile, Local Falcon or geo-grid tool, BrightLocal/Whitespark, Google Maps, Rich Results Test.

## Core workflow
1. Audit NAP on top directories and data aggregators
2. Fix inconsistencies and duplicates; claim major listings
3. Add industry/local directories
4. Keep a master NAP sheet

## Decision rules and checks
- NAP identical everywhere
- Top directories + industry
- Fix duplicates

## Edge cases and failure handling
- Old address still live -> update or request removal
- Paid directory spam -> skip

## Validation
- Re-fetch or re-crawl changed URLs; confirm the fix is live (status, rendered HTML, canonical, schema validator, GSC URL Inspection as relevant).
- Compare with the baseline recorded before the change; check for regressions on neighbouring templates.

## Output requirements
Citation sheet: site, status, URL. Report as a short DONE: what changed, evidence, remaining issues.

## Example
- Input/symptom: Old address still live
- Action: update or request removal
- Output: Citation sheet: site, status, URL.

## References
`references/playbook.md`: detailed how-to, common problems and fixes, tools, verify steps. Read when executing.
