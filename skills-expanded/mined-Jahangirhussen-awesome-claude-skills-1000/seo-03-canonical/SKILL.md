---
name: seo-03-canonical
description: Canonicals (SEO). Use when the request involves: canonical, duplicate content, rel canonical. Not for topics owned by sibling SEO skills or other categories; routed by seo-master.
---

# Canonicals

ID: 03.03 | Level: child | Parent: [Technical SEO](../SKILL.md)

## Purpose
Canonicals within the seo-master tree: Canonical audit: URL, declared canonical, Google-selected, issue.

## When to use
Triggers: canonical, duplicate content, rel canonical

## When NOT to use
- The topic is covered by a sibling skill: `../core-web-vitals`, `../crawlability`, `../https`, `../indexability`, `../javascript-seo`.
- The task is outside this SEO category; see `ROUTER.md` at the seo-master root.

## Inputs
- Target site/URL(s) or project files, platform (CMS/framework), and goal.
- Data access as available: Screaming Frog or Sitebulb, Google Search Console, Lighthouse, PageSpeed Insights, CrUX, WebPageTest, curl -I, server logs.

## Core workflow
1. Read rel=canonical in rendered HTML and HTTP header
2. Verify self-referencing on indexable pages; absolute URLs; one tag per page
3. Check canonical target returns 200, indexable, not redirected
4. Align protocol/www/trailing-slash across canonical, sitemap, internal links

## Decision rules and checks
- Self-referencing canonical on indexable pages
- Absolute URLs, one canonical per page
- No canonical to redirected/noindex URL
- Params/trailing-slash/www consistency

## Edge cases and failure handling
- Canonical points to noindex/redirect -> point to final indexable URL
- Param URLs indexed -> canonical to clean URL

## Validation
- Re-fetch or re-crawl changed URLs; confirm the fix is live (status, rendered HTML, canonical, schema validator, GSC URL Inspection as relevant).
- Compare with the baseline recorded before the change; check for regressions on neighbouring templates.

## Output requirements
Canonical audit: URL, declared canonical, Google-selected, issue. Report as a short DONE: what changed, evidence, remaining issues.

## Example
- Input/symptom: Canonical points to noindex/redirect
- Action: point to final indexable URL
- Output: Canonical audit: URL, declared canonical, Google-selected, issue.

## References
`references/playbook.md`: detailed how-to, common problems and fixes, tools, verify steps. Read when executing.
