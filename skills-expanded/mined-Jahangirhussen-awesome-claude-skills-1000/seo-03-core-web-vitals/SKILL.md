---
name: seo-03-core-web-vitals
description: Core Web Vitals and speed (SEO). Use when the request involves: core web vitals, lcp, inp, cls, pagespeed, lighthouse, slow site, ttfb, cdn, caching. Not for topics owned by sibling SEO skills or other categories; routed by seo-master.
---

# Core Web Vitals and speed

ID: 03.08 | Level: child | Parent: [Technical SEO](../SKILL.md)

## Purpose
Core Web Vitals and speed within the seo-master tree: CWV table: metric, p75, cause, fix, owner.

## When to use
Triggers: core web vitals, lcp, inp, cls, pagespeed, lighthouse, slow site, ttfb, cdn, caching

## When NOT to use
- The topic is covered by a sibling skill: `../canonical`, `../crawlability`, `../https`, `../indexability`, `../javascript-seo`.
- The task is outside this SEO category; see `ROUTER.md` at the seo-master root.

## Inputs
- Target site/URL(s) or project files, platform (CMS/framework), and goal.
- Data access as available: Screaming Frog or Sitebulb, Google Search Console, Lighthouse, PageSpeed Insights, CrUX, WebPageTest, curl -I, server logs.

## Core workflow
1. Use field data first: CrUX/GSC CWV; then lab (Lighthouse, WebPageTest)
2. Targets at p75: LCP <= 2.5s, INP <= 200ms, CLS <= 0.1
3. Fix server (TTFB, cache, CDN, compression), then assets (images, fonts, JS)
4. Re-measure after deploy; field data lags ~28 days

## Decision rules and checks
- Use field data (CrUX/GSC) first, lab second
- Targets: LCP<=2.5s, INP<=200ms, CLS<=0.1
- Server: TTFB, cache, CDN, compression
- Assets: image size/format, defer JS, critical CSS, fonts

## Edge cases and failure handling
- Lab good but field bad -> real-user conditions (mobile, slow CPU); test throttled
- Third-party scripts dominate -> defer, facade, or remove

## Validation
- Re-fetch or re-crawl changed URLs; confirm the fix is live (status, rendered HTML, canonical, schema validator, GSC URL Inspection as relevant).
- Compare with the baseline recorded before the change; check for regressions on neighbouring templates.

## Output requirements
CWV table: metric, p75, cause, fix, owner. Report as a short DONE: what changed, evidence, remaining issues.

## Example
- Input/symptom: Lab good but field bad
- Action: real-user conditions (mobile, slow CPU); test throttled
- Output: CWV table: metric, p75, cause, fix, owner.

## Grandchildren
- [LCP](lcp/SKILL.md)
- [INP](inp/SKILL.md)
- [CLS](cls/SKILL.md)

## Dependencies (load only if needed)
- 16-image-seo

## References
`references/playbook.md`: detailed how-to, common problems and fixes, tools, verify steps. Read when executing.
