---
name: seo-07-reviews
description: Reviews (SEO). Use when the request involves: reviews, reputation. Not for topics owned by sibling SEO skills or other categories; routed by seo-master.
---

# Reviews

ID: 07.05 | Level: child | Parent: [Local SEO](../SKILL.md)

## Purpose
Reviews within the seo-master tree: Review request and response templates.

## When to use
Triggers: reviews, reputation

## When NOT to use
- The topic is covered by a sibling skill: `../citations`, `../google-business-profile`, `../local-keywords`, `../local-links`, `../local-schema`.
- The task is outside this SEO category; see `ROUTER.md` at the seo-master root.

## Inputs
- Target site/URL(s) or project files, platform (CMS/framework), and goal.
- Data access as available: Google Business Profile, Local Falcon or geo-grid tool, BrightLocal/Whitespark, Google Maps, Rich Results Test.

## Core workflow
1. Ask happy customers at the right moment via direct review link
2. Respond to every review, politely and specifically
3. Do not gate reviews or offer incentives
4. Display reviews on site (visible only; schema rules apply)

## Decision rules and checks
- Ask consistently, respond to all
- No fake/gated reviews

## Edge cases and failure handling
- Fake/competitor review -> flag through GBP
- Few reviews -> add review request step to workflow

## Validation
- Re-fetch or re-crawl changed URLs; confirm the fix is live (status, rendered HTML, canonical, schema validator, GSC URL Inspection as relevant).
- Compare with the baseline recorded before the change; check for regressions on neighbouring templates.

## Output requirements
Review request and response templates. Report as a short DONE: what changed, evidence, remaining issues.

## Example
- Input/symptom: Fake/competitor review
- Action: flag through GBP
- Output: Review request and response templates.

## References
`references/playbook.md`: detailed how-to, common problems and fixes, tools, verify steps. Read when executing.
