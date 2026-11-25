---
name: seo-17-video-sitemap
description: Video sitemap (SEO). Use when the request involves: video sitemap. Not for topics owned by sibling SEO skills or other categories; routed by seo-master.
---

# Video sitemap

ID: 17.03 | Level: child | Parent: [Video SEO](../SKILL.md)

## Purpose
Video sitemap within the seo-master tree: Video sitemap file.

## When to use
Triggers: video sitemap

## When NOT to use
- The topic is covered by a sibling skill: `../video-content`, `../video-schema`, `../youtube-seo`.
- The task is outside this SEO category; see `ROUTER.md` at the seo-master root.

## Inputs
- Target site/URL(s) or project files, platform (CMS/framework), and goal.
- Data access as available: YouTube Studio, VideoObject validator (Rich Results Test), Google Search Console video report, sitemap generator.

## Core workflow
1. List video pages with title, description, thumbnail, content/player loc
2. Keep updated; submit in GSC

## Decision rules and checks
- List video pages with metadata

## Edge cases and failure handling
- Pages blocked -> allow crawl

## Validation
- Re-fetch or re-crawl changed URLs; confirm the fix is live (status, rendered HTML, canonical, schema validator, GSC URL Inspection as relevant).
- Compare with the baseline recorded before the change; check for regressions on neighbouring templates.

## Output requirements
Video sitemap file. Report as a short DONE: what changed, evidence, remaining issues.

## Example
- Input/symptom: Pages blocked
- Action: allow crawl
- Output: Video sitemap file.

## References
`references/playbook.md`: detailed how-to, common problems and fixes, tools, verify steps. Read when executing.
