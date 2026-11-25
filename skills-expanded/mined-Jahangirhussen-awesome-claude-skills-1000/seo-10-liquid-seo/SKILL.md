---
name: seo-10-liquid-seo
description: Liquid / theme SEO (SEO). Use when the request involves: liquid, theme seo. Not for topics owned by sibling SEO skills or other categories; routed by seo-master.
---

# Liquid / theme SEO

ID: 10.04 | Level: child | Parent: [Shopify SEO](../SKILL.md)

## Purpose
Liquid / theme SEO within the seo-master tree: Liquid snippets reviewed.

## When to use
Triggers: liquid, theme seo

## When NOT to use
- The topic is covered by a sibling skill: `../collections`, `../products`, `../shopify-migration`, `../shopify-technical`, `../structured-data`.
- The task is outside this SEO category; see `ROUTER.md` at the seo-master root.

## Inputs
- Target site/URL(s) or project files, platform (CMS/framework), and goal.
- Data access as available: Shopify admin (themes, redirects, navigation), Liquid editor, Screaming Frog, Rich Results Test, app list.

## Core workflow
1. Ensure one H1 in templates
2. Output title/meta via {{ page_title }} patterns with fallbacks
3. Add JSON-LD in theme or via one app
4. Use image_url with width/height and loading attributes

## Decision rules and checks
- One H1 in theme
- Meta tags via Liquid
- Remove duplicate schema

## Edge cases and failure handling
- Hardcoded titles -> use Liquid variables
- Missing alt -> add image.alt filter fallback

## Validation
- Re-fetch or re-crawl changed URLs; confirm the fix is live (status, rendered HTML, canonical, schema validator, GSC URL Inspection as relevant).
- Compare with the baseline recorded before the change; check for regressions on neighbouring templates.

## Output requirements
Liquid snippets reviewed. Report as a short DONE: what changed, evidence, remaining issues.

## Example
- Input/symptom: Hardcoded titles
- Action: use Liquid variables
- Output: Liquid snippets reviewed.

## References
`references/playbook.md`: detailed how-to, common problems and fixes, tools, verify steps. Read when executing.
