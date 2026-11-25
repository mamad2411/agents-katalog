---
name: seo-07-local-schema
description: Local schema (SEO). Use when the request involves: localbusiness schema. Not for topics owned by sibling SEO skills or other categories; routed by seo-master.
---

# Local schema

ID: 07.06 | Level: child | Parent: [Local SEO](../SKILL.md)

## Purpose
Local schema within the seo-master tree: LocalBusiness JSON-LD per location.

## When to use
Triggers: localbusiness schema

## When NOT to use
- The topic is covered by a sibling skill: `../citations`, `../google-business-profile`, `../local-keywords`, `../local-links`, `../reviews`.
- The task is outside this SEO category; see `ROUTER.md` at the seo-master root.

## Inputs
- Target site/URL(s) or project files, platform (CMS/framework), and goal.
- Data access as available: Google Business Profile, Local Falcon or geo-grid tool, BrightLocal/Whitespark, Google Maps, Rich Results Test.

## Core workflow
1. Add LocalBusiness (or specific subtype) JSON-LD
2. Include name, address, geo, telephone, openingHours, url, sameAs
3. Match visible NAP exactly
4. Validate in Rich Results Test

## Decision rules and checks
- LocalBusiness + geo + openingHours
- Match visible NAP

## Edge cases and failure handling
- Multiple locations -> one entity per location page
- Schema differs from GBP -> align

## Validation
- Re-fetch or re-crawl changed URLs; confirm the fix is live (status, rendered HTML, canonical, schema validator, GSC URL Inspection as relevant).
- Compare with the baseline recorded before the change; check for regressions on neighbouring templates.

## Output requirements
LocalBusiness JSON-LD per location. Report as a short DONE: what changed, evidence, remaining issues.

## Example
- Input/symptom: Multiple locations
- Action: one entity per location page
- Output: LocalBusiness JSON-LD per location.

## Dependencies (load only if needed)
- 27-schema-seo/local-business

## References
`references/playbook.md`: detailed how-to, common problems and fixes, tools, verify steps. Read when executing.
