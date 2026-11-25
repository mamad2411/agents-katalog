---
name: seo-17-video-content
description: Video content on page (SEO). Use when the request involves: video page. Not for topics owned by sibling SEO skills or other categories; routed by seo-master.
---

# Video content on page

ID: 17.04 | Level: child | Parent: [Video SEO](../SKILL.md)

## Purpose
Video content on page within the seo-master tree: Page layout notes.

## When to use
Triggers: video page

## When NOT to use
- The topic is covered by a sibling skill: `../video-schema`, `../video-sitemap`, `../youtube-seo`.
- The task is outside this SEO category; see `ROUTER.md` at the seo-master root.

## Inputs
- Target site/URL(s) or project files, platform (CMS/framework), and goal.
- Data access as available: YouTube Studio, VideoObject validator (Rich Results Test), Google Search Console video report, sitemap generator.

## Core workflow
1. Place video near top, with H1 and written summary
2. Add transcript/captions for accessibility and indexing
3. One primary video per page

## Decision rules and checks
- Surrounding text, transcript, relevant H1

## Edge cases and failure handling
- Autoplay slowing page -> lazy-load player

## Validation
- Re-fetch or re-crawl changed URLs; confirm the fix is live (status, rendered HTML, canonical, schema validator, GSC URL Inspection as relevant).
- Compare with the baseline recorded before the change; check for regressions on neighbouring templates.

## Output requirements
Page layout notes. Report as a short DONE: what changed, evidence, remaining issues.

## Example
- Input/symptom: Autoplay slowing page
- Action: lazy-load player
- Output: Page layout notes.

## References
`references/playbook.md`: detailed how-to, common problems and fixes, tools, verify steps. Read when executing.
