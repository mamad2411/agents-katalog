---
name: seo-16-alt-text
description: Alt text (SEO). Use when the request involves: alt text, image alt. Not for topics owned by sibling SEO skills or other categories; routed by seo-master.
---

# Alt text

ID: 16.01 | Level: child | Parent: [Image SEO](../SKILL.md)

## Purpose
Alt text within the seo-master tree: Alt text table.

## When to use
Triggers: alt text, image alt

## When NOT to use
- The topic is covered by a sibling skill: `../filenames`, `../image-compression`, `../image-schema`, `../image-sitemap`.
- The task is outside this SEO category; see `ROUTER.md` at the seo-master root.

## Inputs
- Target site/URL(s) or project files, platform (CMS/framework), and goal.
- Data access as available: Squoosh/ImageMagick/sharp, Lighthouse, Screaming Frog (images), Google Search Console, CDN image transforms.

## Core workflow
1. Describe image content and purpose concisely
2. Include keyword only when natural
3. Empty alt for decorative images; do not stuff

## Decision rules and checks
- Describe the image, context-aware
- No keyword stuffing
- Empty alt for decorative

## Edge cases and failure handling
- Alt = filename -> rewrite
- Missing alt on product images -> template from product name + attribute

## Validation
- Re-fetch or re-crawl changed URLs; confirm the fix is live (status, rendered HTML, canonical, schema validator, GSC URL Inspection as relevant).
- Compare with the baseline recorded before the change; check for regressions on neighbouring templates.

## Output requirements
Alt text table. Report as a short DONE: what changed, evidence, remaining issues.

## Example
- Input/symptom: Alt = filename
- Action: rewrite
- Output: Alt text table.

## References
`references/playbook.md`: detailed how-to, common problems and fixes, tools, verify steps. Read when executing.
