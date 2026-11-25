---
name: seo-03-javascript-seo
description: JavaScript and rendering SEO (SEO). Use when the request involves: javascript seo, rendering, ssr, csr, hydration, spa. Not for topics owned by sibling SEO skills or other categories; routed by seo-master.
---

# JavaScript and rendering SEO

ID: 03.07 | Level: child | Parent: [Technical SEO](../SKILL.md)

## Purpose
JavaScript and rendering SEO within the seo-master tree: Rendering report: route, raw vs rendered diff, fix.

## When to use
Triggers: javascript seo, rendering, ssr, csr, hydration, spa

## When NOT to use
- The topic is covered by a sibling skill: `../canonical`, `../core-web-vitals`, `../crawlability`, `../https`, `../indexability`.
- The task is outside this SEO category; see `ROUTER.md` at the seo-master root.

## Inputs
- Target site/URL(s) or project files, platform (CMS/framework), and goal.
- Data access as available: Screaming Frog or Sitebulb, Google Search Console, Lighthouse, PageSpeed Insights, CrUX, WebPageTest, curl -I, server logs.

## Core workflow
1. Compare 'view source' vs rendered DOM; use URL Inspection live test
2. Ensure content, titles, canonicals and links exist in rendered HTML (links as <a href>)
3. Prefer SSR/SSG/ISR for indexable pages; hydrate after
4. Avoid content that needs clicks/scroll events to appear

## Decision rules and checks
- Compare raw vs rendered HTML
- Critical content/links in rendered DOM as <a href>
- SSR/SSG for indexable pages
- No content behind user events

## Edge cases and failure handling
- Content missing in rendered HTML -> SSR the route or prerender
- Links are onClick handlers -> use real anchors

## Validation
- Re-fetch or re-crawl changed URLs; confirm the fix is live (status, rendered HTML, canonical, schema validator, GSC URL Inspection as relevant).
- Compare with the baseline recorded before the change; check for regressions on neighbouring templates.

## Output requirements
Rendering report: route, raw vs rendered diff, fix. Report as a short DONE: what changed, evidence, remaining issues.

## Example
- Input/symptom: Content missing in rendered HTML
- Action: SSR the route or prerender
- Output: Rendering report: route, raw vs rendered diff, fix.

## References
`references/playbook.md`: detailed how-to, common problems and fixes, tools, verify steps. Read when executing.
