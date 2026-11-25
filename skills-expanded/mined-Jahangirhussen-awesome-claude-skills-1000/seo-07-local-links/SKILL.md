---
name: seo-07-local-links
description: Local links (SEO). Use when the request involves: local backlinks, sponsorships. Not for topics owned by sibling SEO skills or other categories; routed by seo-master.
---

# Local links

ID: 07.04 | Level: child | Parent: [Local SEO](../SKILL.md)

## Purpose
Local links within the seo-master tree: Local link targets and status.

## When to use
Triggers: local backlinks, sponsorships

## When NOT to use
- The topic is covered by a sibling skill: `../citations`, `../google-business-profile`, `../local-keywords`, `../local-schema`, `../reviews`.
- The task is outside this SEO category; see `ROUTER.md` at the seo-master root.

## Inputs
- Target site/URL(s) or project files, platform (CMS/framework), and goal.
- Data access as available: Google Business Profile, Local Falcon or geo-grid tool, BrightLocal/Whitespark, Google Maps, Rich Results Test.

## Core workflow
1. Find local sponsorships, chambers, partners, local press
2. Create local resources/events worth linking
3. Reclaim mentions without links

## Decision rules and checks
- Chambers, sponsorships, local press
- Partner pages

## Edge cases and failure handling
- No local relevance -> pursue regional sites only
- Link exchanges -> avoid

## Validation
- Re-fetch or re-crawl changed URLs; confirm the fix is live (status, rendered HTML, canonical, schema validator, GSC URL Inspection as relevant).
- Compare with the baseline recorded before the change; check for regressions on neighbouring templates.

## Output requirements
Local link targets and status. Report as a short DONE: what changed, evidence, remaining issues.

## Example
- Input/symptom: No local relevance
- Action: pursue regional sites only
- Output: Local link targets and status.

## References
`references/playbook.md`: detailed how-to, common problems and fixes, tools, verify steps. Read when executing.
