---
name: seo-07-local-keywords
description: Local keywords and pages (SEO). Use when the request involves: local keywords, location page, service area page. Not for topics owned by sibling SEO skills or other categories; routed by seo-master.
---

# Local keywords and pages

ID: 07.02 | Level: child | Parent: [Local SEO](../SKILL.md)

## Purpose
Local keywords and pages within the seo-master tree: Local keyword map to URLs.

## When to use
Triggers: local keywords, location page, service area page

## When NOT to use
- The topic is covered by a sibling skill: `../citations`, `../google-business-profile`, `../local-links`, `../local-schema`, `../reviews`.
- The task is outside this SEO category; see `ROUTER.md` at the seo-master root.

## Inputs
- Target site/URL(s) or project files, platform (CMS/framework), and goal.
- Data access as available: Google Business Profile, Local Falcon or geo-grid tool, BrightLocal/Whitespark, Google Maps, Rich Results Test.

## Core workflow
1. Combine service + city/neighborhood and 'near me' intent
2. Check local pack vs organic SERP for each term
3. One page per service-location combination only if genuinely distinct
4. Use local entities (landmarks, areas served) naturally

## Decision rules and checks
- One unique page per location/service
- Local proof: reviews, projects, map
- Avoid doorway pages

## Edge cases and failure handling
- Doorway pages -> add unique local proof or consolidate
- Wrong location targeting -> set geo in tools

## Validation
- Re-fetch or re-crawl changed URLs; confirm the fix is live (status, rendered HTML, canonical, schema validator, GSC URL Inspection as relevant).
- Compare with the baseline recorded before the change; check for regressions on neighbouring templates.

## Output requirements
Local keyword map to URLs. Report as a short DONE: what changed, evidence, remaining issues.

## Example
- Input/symptom: Doorway pages
- Action: add unique local proof or consolidate
- Output: Local keyword map to URLs.

## References
`references/playbook.md`: detailed how-to, common problems and fixes, tools, verify steps. Read when executing.
