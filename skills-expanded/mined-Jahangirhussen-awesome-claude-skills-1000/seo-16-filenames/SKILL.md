---
name: seo-16-filenames
description: Filenames (SEO). Use when the request involves: image filename. Not for topics owned by sibling SEO skills or other categories; routed by seo-master.
---

# Filenames

ID: 16.02 | Level: child | Parent: [Image SEO](../SKILL.md)

## Purpose
Filenames within the seo-master tree: Rename map.

## When to use
Triggers: image filename

## When NOT to use
- The topic is covered by a sibling skill: `../alt-text`, `../image-compression`, `../image-schema`, `../image-sitemap`.
- The task is outside this SEO category; see `ROUTER.md` at the seo-master root.

## Inputs
- Target site/URL(s) or project files, platform (CMS/framework), and goal.
- Data access as available: Squoosh/ImageMagick/sharp, Lighthouse, Screaming Frog (images), Google Search Console, CDN image transforms.

## Core workflow
1. Use descriptive, hyphenated, lowercase filenames
2. Avoid IMG_1234 and spaces
3. Keep stable URLs; redirect if renamed

## Decision rules and checks
- Descriptive-hyphenated
- No camera defaults

## Edge cases and failure handling
- Bulk rename breaking links -> redirect or update references

## Validation
- Re-fetch or re-crawl changed URLs; confirm the fix is live (status, rendered HTML, canonical, schema validator, GSC URL Inspection as relevant).
- Compare with the baseline recorded before the change; check for regressions on neighbouring templates.

## Output requirements
Rename map. Report as a short DONE: what changed, evidence, remaining issues.

## Example
- Input/symptom: Bulk rename breaking links
- Action: redirect or update references
- Output: Rename map.

## References
`references/playbook.md`: detailed how-to, common problems and fixes, tools, verify steps. Read when executing.
