---
name: seo-03-mobile-seo
description: Mobile SEO (SEO). Use when the request involves: mobile friendly, responsive, mobile first indexing. Not for topics owned by sibling SEO skills or other categories; routed by seo-master.
---

# Mobile SEO

ID: 03.09 | Level: child | Parent: [Technical SEO](../SKILL.md)

## Purpose
Mobile SEO within the seo-master tree: Mobile issue list by template.

## When to use
Triggers: mobile friendly, responsive, mobile first indexing

## When NOT to use
- The topic is covered by a sibling skill: `../canonical`, `../core-web-vitals`, `../crawlability`, `../https`, `../indexability`.
- The task is outside this SEO category; see `ROUTER.md` at the seo-master root.

## Inputs
- Target site/URL(s) or project files, platform (CMS/framework), and goal.
- Data access as available: Screaming Frog or Sitebulb, Google Search Console, Lighthouse, PageSpeed Insights, CrUX, WebPageTest, curl -I, server logs.

## Core workflow
1. Test with Mobile-Friendly checks and real devices
2. Confirm same content, metadata, structured data on mobile and desktop
3. Viewport meta, readable font sizes, tap targets >= 48px, no intrusive interstitials
4. Check mobile CWV separately

## Decision rules and checks
- Same content + structured data on mobile
- Viewport meta, tap targets, no intrusive interstitials
- Mobile CWV

## Edge cases and failure handling
- Content hidden/cut on mobile -> include it (mobile-first indexing)
- Separate m. site -> migrate to responsive

## Validation
- Re-fetch or re-crawl changed URLs; confirm the fix is live (status, rendered HTML, canonical, schema validator, GSC URL Inspection as relevant).
- Compare with the baseline recorded before the change; check for regressions on neighbouring templates.

## Output requirements
Mobile issue list by template. Report as a short DONE: what changed, evidence, remaining issues.

## Example
- Input/symptom: Content hidden/cut on mobile
- Action: include it (mobile-first indexing)
- Output: Mobile issue list by template.

## References
`references/playbook.md`: detailed how-to, common problems and fixes, tools, verify steps. Read when executing.
