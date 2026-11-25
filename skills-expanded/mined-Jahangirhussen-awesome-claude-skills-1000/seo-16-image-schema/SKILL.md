---
name: seo-16-image-schema
description: Image structured data (SEO). Use when the request involves: image schema, imageobject. Not for topics owned by sibling SEO skills or other categories; routed by seo-master.
---

# Image structured data

ID: 16.05 | Level: child | Parent: [Image SEO](../SKILL.md)

## Purpose
Image structured data within the seo-master tree: Image JSON-LD example.

## When to use
Triggers: image schema, imageobject

## When NOT to use
- The topic is covered by a sibling skill: `../alt-text`, `../filenames`, `../image-compression`, `../image-sitemap`.
- The task is outside this SEO category; see `ROUTER.md` at the seo-master root.

## Inputs
- Target site/URL(s) or project files, platform (CMS/framework), and goal.
- Data access as available: Squoosh/ImageMagick/sharp, Lighthouse, Screaming Frog (images), Google Search Console, CDN image transforms.

## Core workflow
1. Use ImageObject with contentUrl, license, creator when relevant
2. Set primaryImageOfPage; ensure article image sizes meet guidelines
3. Validate

## Decision rules and checks
- ImageObject/primaryImageOfPage
- License metadata if relevant

## Edge cases and failure handling
- Wrong image ratios for Article -> provide 16:9, 4:3, 1:1 variants

## Validation
- Re-fetch or re-crawl changed URLs; confirm the fix is live (status, rendered HTML, canonical, schema validator, GSC URL Inspection as relevant).
- Compare with the baseline recorded before the change; check for regressions on neighbouring templates.

## Output requirements
Image JSON-LD example. Report as a short DONE: what changed, evidence, remaining issues.

## Example
- Input/symptom: Wrong image ratios for Article
- Action: provide 16:9, 4:3, 1:1 variants
- Output: Image JSON-LD example.

## References
`references/playbook.md`: detailed how-to, common problems and fixes, tools, verify steps. Read when executing.
