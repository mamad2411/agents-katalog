---
name: seo-16
description: 16. Image SEO (SEO). Use when the request involves: image seo, alt text, image filename, webp, avif, image compression, image sitemap, google images. Not for topics owned by sibling SEO skills or other categories; routed by seo-master.
---

# 16. Image SEO

ID: 16 | Level: parent | Parent: SEO Master

## Purpose
Image discoverability and speed.

## When to use
Triggers: image seo, alt text, image filename, webp, avif, image compression, image sitemap, google images

## When NOT to use
- The request belongs to another SEO category (see `../ROUTER.md`): e.g. core seo, google seo, technical seo, on page seo, off page seo, content seo.
- A more specific child skill already covers it: open that child instead of repeating its work.

## Inputs
- Target site/URL(s) or project files, platform (CMS/framework), and goal.
- Data access as available: Squoosh/ImageMagick/sharp, Lighthouse, Screaming Frog (images), Google Search Console, CDN image transforms.

## Core workflow
1. Audit image count, size, format, alt, dimensions, lazy-loading
2. Compress and convert; set responsive images
3. Add image sitemap/schema where useful

## Decision rules
- Use evidence (crawl, GSC, rendered HTML, validators), not assumptions.
- Fix the highest-impact, lowest-risk items first; change only what the task needs.
- If a platform skill (WordPress, WooCommerce, Shopify) applies, its guidance overrides generic advice.

## Edge cases and failure handling
- Huge hero images -> resize/serve WebP/AVIF
- Missing alt -> write meaningful alt

## Validation
- Re-fetch or re-crawl changed URLs; confirm the fix is live (status, rendered HTML, canonical, schema validator, GSC URL Inspection as relevant).
- Compare with the baseline recorded before the change; check for regressions on neighbouring templates.

## Output requirements
Image optimization list. Report as a short DONE: what changed, evidence, remaining issues.

## Example
- Input/symptom: Huge hero images
- Action: resize/serve WebP/AVIF
- Output: Image optimization list.

## Children
- [Alt text](alt-text/SKILL.md)
- [Filenames](filenames/SKILL.md)
- [Compression and formats](image-compression/SKILL.md)
- [Image sitemap](image-sitemap/SKILL.md)
- [Image structured data](image-schema/SKILL.md)

## Related installed skills (kept in place; invoke only if needed)
- `performance-optimization`

## References
`references/playbook.md`: detailed how-to, common problems and fixes, tools, verify steps. Read when executing.
