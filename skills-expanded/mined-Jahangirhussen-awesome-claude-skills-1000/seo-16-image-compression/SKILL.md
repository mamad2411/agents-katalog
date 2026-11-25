---
name: seo-16-image-compression
description: Compression and formats (SEO). Use when the request involves: image compression, webp, avif, lazy loading, responsive images. Not for topics owned by sibling SEO skills or other categories; routed by seo-master.
---

# Compression and formats

ID: 16.03 | Level: child | Parent: [Image SEO](../SKILL.md)

## Purpose
Compression and formats within the seo-master tree: Image pipeline settings.

## When to use
Triggers: image compression, webp, avif, lazy loading, responsive images

## When NOT to use
- The topic is covered by a sibling skill: `../alt-text`, `../filenames`, `../image-schema`, `../image-sitemap`.
- The task is outside this SEO category; see `ROUTER.md` at the seo-master root.

## Inputs
- Target site/URL(s) or project files, platform (CMS/framework), and goal.
- Data access as available: Squoosh/ImageMagick/sharp, Lighthouse, Screaming Frog (images), Google Search Console, CDN image transforms.

## Core workflow
1. Resize to display size (2x for retina max)
2. Convert to WebP/AVIF with fallback
3. Use srcset/sizes and width/height attributes
4. Lazy-load below the fold; never lazy-load the LCP image

## Decision rules and checks
- WebP/AVIF with fallback
- srcset/sizes, width/height
- Do not lazy-load LCP image

## Edge cases and failure handling
- CLS from missing dimensions -> set width/height
- Quality too low -> test visually

## Validation
- Re-fetch or re-crawl changed URLs; confirm the fix is live (status, rendered HTML, canonical, schema validator, GSC URL Inspection as relevant).
- Compare with the baseline recorded before the change; check for regressions on neighbouring templates.

## Output requirements
Image pipeline settings. Report as a short DONE: what changed, evidence, remaining issues.

## Example
- Input/symptom: CLS from missing dimensions
- Action: set width/height
- Output: Image pipeline settings.

## Dependencies (load only if needed)
- 03-technical-seo/core-web-vitals

## References
`references/playbook.md`: detailed how-to, common problems and fixes, tools, verify steps. Read when executing.
