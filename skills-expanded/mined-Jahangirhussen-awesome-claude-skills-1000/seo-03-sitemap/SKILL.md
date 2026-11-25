---
name: seo-03-sitemap
description: XML sitemaps (SEO). Use when the request involves: sitemap, xml sitemap, image sitemap, video sitemap, sitemap index. Not for topics owned by sibling SEO skills or other categories; routed by seo-master.
---

# XML sitemaps

ID: 03.05 | Level: child | Parent: [Technical SEO](../SKILL.md)

## Purpose
XML sitemaps within the seo-master tree: Sitemap spec: files, URL rules, update trigger.

## When to use
Triggers: sitemap, xml sitemap, image sitemap, video sitemap, sitemap index

## When NOT to use
- The topic is covered by a sibling skill: `../canonical`, `../core-web-vitals`, `../crawlability`, `../https`, `../indexability`.
- The task is outside this SEO category; see `ROUTER.md` at the seo-master root.

## Inputs
- Target site/URL(s) or project files, platform (CMS/framework), and goal.
- Data access as available: Screaming Frog or Sitebulb, Google Search Console, Lighthouse, PageSpeed Insights, CrUX, WebPageTest, curl -I, server logs.

## Core workflow
1. Generate only canonical, 200, indexable URLs
2. Split at 50k URLs/50MB; use sitemap index; set accurate lastmod
3. Add image/video/news sitemaps where relevant
4. Submit in GSC; compare submitted vs indexed

## Decision rules and checks
- Only canonical, 200, indexable URLs
- <50k URLs / 50MB per file; use index
- Accurate lastmod
- Submitted in GSC; image/video sitemaps if relevant

## Edge cases and failure handling
- Sitemap contains redirects/404 -> regenerate from live indexable URLs
- lastmod always 'now' -> use real modification dates or omit

## Validation
- Re-fetch or re-crawl changed URLs; confirm the fix is live (status, rendered HTML, canonical, schema validator, GSC URL Inspection as relevant).
- Compare with the baseline recorded before the change; check for regressions on neighbouring templates.

## Output requirements
Sitemap spec: files, URL rules, update trigger. Report as a short DONE: what changed, evidence, remaining issues.

## Example
- Input/symptom: Sitemap contains redirects/404
- Action: regenerate from live indexable URLs
- Output: Sitemap spec: files, URL rules, update trigger.

## References
`references/playbook.md`: detailed how-to, common problems and fixes, tools, verify steps. Read when executing.
