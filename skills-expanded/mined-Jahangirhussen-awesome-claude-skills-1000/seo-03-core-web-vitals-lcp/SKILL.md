---
name: seo-03-core-web-vitals-lcp
description: LCP (SEO). Use when the request involves: lcp, largest contentful paint. Not for topics owned by sibling SEO skills or other categories; routed by seo-master.
---

# LCP

ID: 03.08.1 | Level: grandchild | Parent: [Core Web Vitals and speed](../SKILL.md)

## Purpose
LCP within the seo-master tree: LCP element, before/after timing.

## When to use
Triggers: lcp, largest contentful paint

## When NOT to use
- The topic is covered by a sibling skill: `../cls`, `../inp`.
- The task is outside this SEO category; see `ROUTER.md` at the seo-master root.

## Inputs
- Target site/URL(s) or project files, platform (CMS/framework), and goal.
- Data access as available: Screaming Frog or Sitebulb, Google Search Console, Lighthouse, PageSpeed Insights, CrUX, WebPageTest, curl -I, server logs.

## Core workflow
1. Identify LCP element (Chrome DevTools Performance / Lighthouse)
2. Preload the LCP image or font; set fetchpriority=high; never lazy-load it
3. Cut TTFB (cache, CDN, edge), remove render-blocking CSS/JS, inline critical CSS
4. Serve right-sized WebP/AVIF

## Decision rules and checks
- Identify LCP element
- Preload + priority hint, no lazy-load on it
- Reduce TTFB and render-blocking CSS

## Edge cases and failure handling
- Hero is a CSS background image -> use <img> so it can be preloaded/discovered
- Slow TTFB -> full-page cache or edge rendering

## Validation
- Re-fetch or re-crawl changed URLs; confirm the fix is live (status, rendered HTML, canonical, schema validator, GSC URL Inspection as relevant).
- Compare with the baseline recorded before the change; check for regressions on neighbouring templates.

## Output requirements
LCP element, before/after timing. Report as a short DONE: what changed, evidence, remaining issues.

## Example
- Input/symptom: Hero is a CSS background image
- Action: use <img> so it can be preloaded/discovered
- Output: LCP element, before/after timing.

## References
`references/playbook.md`: detailed how-to, common problems and fixes, tools, verify steps. Read when executing.
