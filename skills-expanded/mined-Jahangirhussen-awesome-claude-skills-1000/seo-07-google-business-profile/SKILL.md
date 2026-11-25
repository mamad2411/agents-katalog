---
name: seo-07-google-business-profile
description: Google Business Profile (SEO). Use when the request involves: gbp, google business profile, google maps. Not for topics owned by sibling SEO skills or other categories; routed by seo-master.
---

# Google Business Profile

ID: 07.01 | Level: child | Parent: [Local SEO](../SKILL.md)

## Purpose
Google Business Profile within the seo-master tree: GBP completeness checklist.

## When to use
Triggers: gbp, google business profile, google maps

## When NOT to use
- The topic is covered by a sibling skill: `../citations`, `../local-keywords`, `../local-links`, `../local-schema`, `../reviews`.
- The task is outside this SEO category; see `ROUTER.md` at the seo-master root.

## Inputs
- Target site/URL(s) or project files, platform (CMS/framework), and goal.
- Data access as available: Google Business Profile, Local Falcon or geo-grid tool, BrightLocal/Whitespark, Google Maps, Rich Results Test.

## Core workflow
1. Claim/verify the profile; set primary category and relevant secondary categories
2. Complete services, attributes, hours, description, photos, products
3. Post updates, answer Q&A, add UTM to website link
4. Never keyword-stuff the business name

## Decision rules and checks
- Primary category, services, hours, photos
- Posts + Q&A
- Verify and keep NAP identical

## Edge cases and failure handling
- Suspended profile -> follow reinstatement flow with proof of business
- Wrong category -> change to the most specific accurate one

## Validation
- Re-fetch or re-crawl changed URLs; confirm the fix is live (status, rendered HTML, canonical, schema validator, GSC URL Inspection as relevant).
- Compare with the baseline recorded before the change; check for regressions on neighbouring templates.

## Output requirements
GBP completeness checklist. Report as a short DONE: what changed, evidence, remaining issues.

## Example
- Input/symptom: Suspended profile
- Action: follow reinstatement flow with proof of business
- Output: GBP completeness checklist.

## References
`references/playbook.md`: detailed how-to, common problems and fixes, tools, verify steps. Read when executing.
