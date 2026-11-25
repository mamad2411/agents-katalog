---
name: seo-07
description: 07. Local SEO (SEO). Use when the request involves: local seo, google business profile, gbp, map pack, nap, citations, reviews, location page, service area. Not for topics owned by sibling SEO skills or other categories; routed by seo-master.
---

# 07. Local SEO

ID: 07 | Level: parent | Parent: SEO Master

## Purpose
Local pack and location pages.

## When to use
Triggers: local seo, google business profile, gbp, map pack, nap, citations, reviews, location page, service area

## When NOT to use
- The request belongs to another SEO category (see `../ROUTER.md`): e.g. core seo, google seo, technical seo, on page seo, off page seo, content seo.
- A more specific child skill already covers it: open that child instead of repeating its work.

## Inputs
- Target site/URL(s) or project files, platform (CMS/framework), and goal.
- Data access as available: Google Business Profile, Local Falcon or geo-grid tool, BrightLocal/Whitespark, Google Maps, Rich Results Test.

## Core workflow
1. Confirm business model: storefront, service-area, or hybrid
2. Audit GBP, NAP consistency, citations, reviews, location pages
3. Check local pack rankings from target locations (geo-grid if available)

## Decision rules
- Use evidence (crawl, GSC, rendered HTML, validators), not assumptions.
- Fix the highest-impact, lowest-risk items first; change only what the task needs.
- If a platform skill (WordPress, WooCommerce, Shopify) applies, its guidance overrides generic advice.

## Edge cases and failure handling
- Duplicate GBP listings -> merge/remove via Google support
- Address mismatch across web -> standardize NAP

## Validation
- Re-fetch or re-crawl changed URLs; confirm the fix is live (status, rendered HTML, canonical, schema validator, GSC URL Inspection as relevant).
- Compare with the baseline recorded before the change; check for regressions on neighbouring templates.

## Output requirements
Local audit with priority fixes. Report as a short DONE: what changed, evidence, remaining issues.

## Example
- Input/symptom: Duplicate GBP listings
- Action: merge/remove via Google support
- Output: Local audit with priority fixes.

## Children
- [Google Business Profile](google-business-profile/SKILL.md)
- [Local keywords and pages](local-keywords/SKILL.md)
- [Citations / NAP](citations/SKILL.md)
- [Local links](local-links/SKILL.md)
- [Reviews](reviews/SKILL.md)
- [Local schema](local-schema/SKILL.md)

## Merged from (read for deep method)
- `../_source/local-seo-manager/SKILL.md`

## References
`references/playbook.md`: detailed how-to, common problems and fixes, tools, verify steps. Read when executing.
