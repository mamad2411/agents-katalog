---
name: seo-17-video-schema
description: Video schema (SEO). Use when the request involves: videoobject. Not for topics owned by sibling SEO skills or other categories; routed by seo-master.
---

# Video schema

ID: 17.02 | Level: child | Parent: [Video SEO](../SKILL.md)

## Purpose
Video schema within the seo-master tree: VideoObject JSON-LD.

## When to use
Triggers: videoobject

## When NOT to use
- The topic is covered by a sibling skill: `../video-content`, `../video-sitemap`, `../youtube-seo`.
- The task is outside this SEO category; see `ROUTER.md` at the seo-master root.

## Inputs
- Target site/URL(s) or project files, platform (CMS/framework), and goal.
- Data access as available: YouTube Studio, VideoObject validator (Rich Results Test), Google Search Console video report, sitemap generator.

## Core workflow
1. VideoObject: name, description, thumbnailUrl, uploadDate, duration, contentUrl/embedUrl
2. Add transcript and key moments (Clip/SeekToAction) if applicable
3. Validate

## Decision rules and checks
- name, description, thumbnailUrl, uploadDate, contentUrl/embedUrl
- Validate

## Edge cases and failure handling
- Missing thumbnail -> provide stable URL
- Wrong dates -> use ISO 8601

## Validation
- Re-fetch or re-crawl changed URLs; confirm the fix is live (status, rendered HTML, canonical, schema validator, GSC URL Inspection as relevant).
- Compare with the baseline recorded before the change; check for regressions on neighbouring templates.

## Output requirements
VideoObject JSON-LD. Report as a short DONE: what changed, evidence, remaining issues.

## Example
- Input/symptom: Missing thumbnail
- Action: provide stable URL
- Output: VideoObject JSON-LD.

## Dependencies (load only if needed)
- 27-schema-seo/schema-validation

## References
`references/playbook.md`: detailed how-to, common problems and fixes, tools, verify steps. Read when executing.
