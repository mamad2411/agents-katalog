---
name: seo-16-image-sitemap
description: Image sitemap (SEO). Use when the request involves: image sitemap. Not for topics owned by sibling SEO skills or other categories; routed by seo-master.
---

# Image sitemap

ID: 16.04 | Level: child | Parent: [Image SEO](../SKILL.md)

## Purpose
Image sitemap within the seo-master tree: Image sitemap file.

## When to use
Triggers: image sitemap

## When NOT to use
- The topic is covered by a sibling skill: `../alt-text`, `../filenames`, `../image-compression`, `../image-schema`.
- The task is outside this SEO category; see `ROUTER.md` at the seo-master root.

## Inputs
- Target site/URL(s) or project files, platform (CMS/framework), and goal.
- Data access as available: Squoosh/ImageMagick/sharp, Lighthouse, Screaming Frog (images), Google Search Console, CDN image transforms.

## Core workflow
1. Include important images (esp. JS-loaded) in sitemap
2. Use image extension tags with canonical page URL
3. Make image URLs crawlable

## Decision rules and checks
- Include key images
- Crawlable image URLs

## Edge cases and failure handling
- Blocked image folder -> allow in robots.txt

## Validation
- Re-fetch or re-crawl changed URLs; confirm the fix is live (status, rendered HTML, canonical, schema validator, GSC URL Inspection as relevant).
- Compare with the baseline recorded before the change; check for regressions on neighbouring templates.

## Output requirements
Image sitemap file. Report as a short DONE: what changed, evidence, remaining issues.

## Example
- Input/symptom: Blocked image folder
- Action: allow in robots.txt
- Output: Image sitemap file.

## References
`references/playbook.md`: detailed how-to, common problems and fixes, tools, verify steps. Read when executing.
