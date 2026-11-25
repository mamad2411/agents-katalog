---
name: seo-03-robots
description: robots.txt (SEO). Use when the request involves: robots.txt, disallow, blocked resources. Not for topics owned by sibling SEO skills or other categories; routed by seo-master.
---

# robots.txt

ID: 03.04 | Level: child | Parent: [Technical SEO](../SKILL.md)

## Purpose
robots.txt within the seo-master tree: robots.txt diff with reasons.

## When to use
Triggers: robots.txt, disallow, blocked resources

## When NOT to use
- The topic is covered by a sibling skill: `../canonical`, `../core-web-vitals`, `../crawlability`, `../https`, `../indexability`.
- The task is outside this SEO category; see `ROUTER.md` at the seo-master root.

## Inputs
- Target site/URL(s) or project files, platform (CMS/framework), and goal.
- Data access as available: Screaming Frog or Sitebulb, Google Search Console, Lighthouse, PageSpeed Insights, CrUX, WebPageTest, curl -I, server logs.

## Core workflow
1. Fetch /robots.txt (200, text/plain, <500KB)
2. Test key URLs with the GSC robots tester or a parser
3. Ensure CSS/JS/images needed for rendering are not blocked
4. Add Sitemap: line; use noindex (not Disallow) to remove pages from the index

## Decision rules and checks
- Do not block CSS/JS/needed assets
- Do not use robots to deindex (use noindex)
- Sitemap line present
- Test critical URLs

## Edge cases and failure handling
- Disallow: / left from staging -> remove immediately
- Blocked page still indexed -> allow crawl and add noindex

## Validation
- Re-fetch or re-crawl changed URLs; confirm the fix is live (status, rendered HTML, canonical, schema validator, GSC URL Inspection as relevant).
- Compare with the baseline recorded before the change; check for regressions on neighbouring templates.

## Output requirements
robots.txt diff with reasons. Report as a short DONE: what changed, evidence, remaining issues.

## Example
- Input/symptom: Disallow: / left from staging
- Action: remove immediately
- Output: robots.txt diff with reasons.

## References
`references/playbook.md`: detailed how-to, common problems and fixes, tools, verify steps. Read when executing.
