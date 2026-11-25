---
name: seo-17
description: 17. Video SEO (SEO). Use when the request involves: video seo, youtube seo, video schema, video sitemap, transcript, thumbnail. Not for topics owned by sibling SEO skills or other categories; routed by seo-master.
---

# 17. Video SEO

ID: 17 | Level: parent | Parent: SEO Master

## Purpose
Video visibility on Google and YouTube.

## When to use
Triggers: video seo, youtube seo, video schema, video sitemap, transcript, thumbnail

## When NOT to use
- The request belongs to another SEO category (see `../ROUTER.md`): e.g. core seo, google seo, technical seo, on page seo, off page seo, content seo.
- A more specific child skill already covers it: open that child instead of repeating its work.

## Inputs
- Target site/URL(s) or project files, platform (CMS/framework), and goal.
- Data access as available: YouTube Studio, VideoObject validator (Rich Results Test), Google Search Console video report, sitemap generator.

## Core workflow
1. Host videos on a crawlable page with surrounding text
2. Add VideoObject schema, transcript, thumbnail
3. Submit video sitemap if many videos
4. Optimize YouTube separately

## Decision rules
- Use evidence (crawl, GSC, rendered HTML, validators), not assumptions.
- Fix the highest-impact, lowest-risk items first; change only what the task needs.
- If a platform skill (WordPress, WooCommerce, Shopify) applies, its guidance overrides generic advice.

## Edge cases and failure handling
- Video not indexed -> page quality and visibility; ensure video is main content
- Embed only via iframe without page text -> add transcript

## Validation
- Re-fetch or re-crawl changed URLs; confirm the fix is live (status, rendered HTML, canonical, schema validator, GSC URL Inspection as relevant).
- Compare with the baseline recorded before the change; check for regressions on neighbouring templates.

## Output requirements
Video SEO checklist. Report as a short DONE: what changed, evidence, remaining issues.

## Example
- Input/symptom: Video not indexed
- Action: page quality and visibility; ensure video is main content
- Output: Video SEO checklist.

## Children
- [YouTube SEO](youtube-seo/SKILL.md)
- [Video schema](video-schema/SKILL.md)
- [Video sitemap](video-sitemap/SKILL.md)
- [Video content on page](video-content/SKILL.md)

## Topics handled here (no separate child)
- Transcripts + captions on page
- Thumbnails: custom, high-res
- Video indexing: crawlable page hosts video, one primary video per page

## Related installed skills (kept in place; invoke only if needed)
- `youtube-full`

## References
`references/playbook.md`: detailed how-to, common problems and fixes, tools, verify steps. Read when executing.
