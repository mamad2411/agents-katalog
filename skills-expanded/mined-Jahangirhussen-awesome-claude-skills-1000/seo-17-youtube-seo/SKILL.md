---
name: seo-17-youtube-seo
description: YouTube SEO (SEO). Use when the request involves: youtube seo. Not for topics owned by sibling SEO skills or other categories; routed by seo-master.
---

# YouTube SEO

ID: 17.01 | Level: child | Parent: [Video SEO](../SKILL.md)

## Purpose
YouTube SEO within the seo-master tree: Video metadata sheet.

## When to use
Triggers: youtube seo

## When NOT to use
- The topic is covered by a sibling skill: `../video-content`, `../video-schema`, `../video-sitemap`.
- The task is outside this SEO category; see `ROUTER.md` at the seo-master root.

## Inputs
- Target site/URL(s) or project files, platform (CMS/framework), and goal.
- Data access as available: YouTube Studio, VideoObject validator (Rich Results Test), Google Search Console video report, sitemap generator.

## Core workflow
1. Keyword-research titles; hook in first 30 seconds; custom thumbnail
2. Descriptions with links, chapters, key terms
3. Playlists, cards, end screens; pin comment
4. Track CTR and retention in YouTube Studio

## Decision rules and checks
- Title/description/chapters
- Retention + CTR
- Playlists + cards

## Edge cases and failure handling
- Low CTR -> test titles/thumbnails
- Low retention -> tighten intro

## Validation
- Re-fetch or re-crawl changed URLs; confirm the fix is live (status, rendered HTML, canonical, schema validator, GSC URL Inspection as relevant).
- Compare with the baseline recorded before the change; check for regressions on neighbouring templates.

## Output requirements
Video metadata sheet. Report as a short DONE: what changed, evidence, remaining issues.

## Example
- Input/symptom: Low CTR
- Action: test titles/thumbnails
- Output: Video metadata sheet.

## References
`references/playbook.md`: detailed how-to, common problems and fixes, tools, verify steps. Read when executing.
