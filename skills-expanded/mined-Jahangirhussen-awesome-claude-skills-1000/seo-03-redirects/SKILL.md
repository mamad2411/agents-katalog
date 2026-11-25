---
name: seo-03-redirects
description: Redirects and status codes (SEO). Use when the request involves: 301, 302, redirect chain, 404, soft 404, status code. Not for topics owned by sibling SEO skills or other categories; routed by seo-master.
---

# Redirects and status codes

ID: 03.06 | Level: child | Parent: [Technical SEO](../SKILL.md)

## Purpose
Redirects and status codes within the seo-master tree: Redirect map: from, to, type, status.

## When to use
Triggers: 301, 302, redirect chain, 404, soft 404, status code

## When NOT to use
- The topic is covered by a sibling skill: `../canonical`, `../core-web-vitals`, `../crawlability`, `../https`, `../indexability`.
- The task is outside this SEO category; see `ROUTER.md` at the seo-master root.

## Inputs
- Target site/URL(s) or project files, platform (CMS/framework), and goal.
- Data access as available: Screaming Frog or Sitebulb, Google Search Console, Lighthouse, PageSpeed Insights, CrUX, WebPageTest, curl -I, server logs.

## Core workflow
1. Crawl and list all 3xx/4xx/5xx internal URLs
2. Use single-hop 301 for permanent moves; 302/307 only for temporary
3. Update internal links to final URLs; remove chains and loops
4. Serve 404/410 for gone pages; redirect to closest relevant page, not homepage

## Decision rules and checks
- Single-hop 301 for permanent moves
- No chains/loops
- Fix internal links to final URLs
- Meaningful 404 / 410 handling

## Edge cases and failure handling
- Redirect chains of 3+ hops -> collapse to one
- Soft 404s -> return real 404/410 or restore content

## Validation
- Re-fetch or re-crawl changed URLs; confirm the fix is live (status, rendered HTML, canonical, schema validator, GSC URL Inspection as relevant).
- Compare with the baseline recorded before the change; check for regressions on neighbouring templates.

## Output requirements
Redirect map: from, to, type, status. Report as a short DONE: what changed, evidence, remaining issues.

## Example
- Input/symptom: Redirect chains of 3+ hops
- Action: collapse to one
- Output: Redirect map: from, to, type, status.

## References
`references/playbook.md`: detailed how-to, common problems and fixes, tools, verify steps. Read when executing.
