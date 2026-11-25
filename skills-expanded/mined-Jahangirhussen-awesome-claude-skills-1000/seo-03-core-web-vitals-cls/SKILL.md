---
name: seo-03-core-web-vitals-cls
description: CLS (SEO). Use when the request involves: cls, layout shift. Not for topics owned by sibling SEO skills or other categories; routed by seo-master.
---

# CLS

ID: 03.08.3 | Level: grandchild | Parent: [Core Web Vitals and speed](../SKILL.md)

## Purpose
CLS within the seo-master tree: Shifting elements and fixes.

## When to use
Triggers: cls, layout shift

## When NOT to use
- The topic is covered by a sibling skill: `../inp`, `../lcp`.
- The task is outside this SEO category; see `ROUTER.md` at the seo-master root.

## Inputs
- Target site/URL(s) or project files, platform (CMS/framework), and goal.
- Data access as available: Screaming Frog or Sitebulb, Google Search Console, Lighthouse, PageSpeed Insights, CrUX, WebPageTest, curl -I, server logs.

## Core workflow
1. Record layout shifts (DevTools Layout Shift regions)
2. Set width/height or aspect-ratio on images, video, embeds
3. Reserve space for ads, banners, late widgets
4. Use font-display: swap with matched fallback metrics

## Decision rules and checks
- Set width/height on media
- Reserve space for ads/embeds
- font-display + size-adjust fallback

## Edge cases and failure handling
- Cookie banner pushes content -> overlay or reserved space
- Late-loading fonts -> preload and size-adjust

## Validation
- Re-fetch or re-crawl changed URLs; confirm the fix is live (status, rendered HTML, canonical, schema validator, GSC URL Inspection as relevant).
- Compare with the baseline recorded before the change; check for regressions on neighbouring templates.

## Output requirements
Shifting elements and fixes. Report as a short DONE: what changed, evidence, remaining issues.

## Example
- Input/symptom: Cookie banner pushes content
- Action: overlay or reserved space
- Output: Shifting elements and fixes.

## References
`references/playbook.md`: detailed how-to, common problems and fixes, tools, verify steps. Read when executing.
