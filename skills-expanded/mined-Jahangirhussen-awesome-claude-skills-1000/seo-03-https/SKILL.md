---
name: seo-03-https
description: HTTPS and security headers (SEO). Use when the request involves: https, ssl, mixed content, hsts, security headers. Not for topics owned by sibling SEO skills or other categories; routed by seo-master.
---

# HTTPS and security headers

ID: 03.10 | Level: child | Parent: [Technical SEO](../SKILL.md)

## Purpose
HTTPS and security headers within the seo-master tree: HTTPS checklist with status.

## When to use
Triggers: https, ssl, mixed content, hsts, security headers

## When NOT to use
- The topic is covered by a sibling skill: `../canonical`, `../core-web-vitals`, `../crawlability`, `../indexability`, `../javascript-seo`.
- The task is outside this SEO category; see `ROUTER.md` at the seo-master root.

## Inputs
- Target site/URL(s) or project files, platform (CMS/framework), and goal.
- Data access as available: Screaming Frog or Sitebulb, Google Search Console, Lighthouse, PageSpeed Insights, CrUX, WebPageTest, curl -I, server logs.

## Core workflow
1. Valid certificate, auto-renew, no mixed content
2. 301 all HTTP to HTTPS (single hop), preferred host (www/non-www)
3. Add HSTS after verifying; set basic security headers
4. Update canonicals, sitemap, internal links, GSC property

## Decision rules and checks
- Valid cert, HTTP->HTTPS 301
- No mixed content
- HSTS, CSP/X-Content-Type basics

## Edge cases and failure handling
- Mixed content warnings -> update asset URLs to HTTPS
- Redirect loop behind CDN -> fix origin protocol setting

## Validation
- Re-fetch or re-crawl changed URLs; confirm the fix is live (status, rendered HTML, canonical, schema validator, GSC URL Inspection as relevant).
- Compare with the baseline recorded before the change; check for regressions on neighbouring templates.

## Output requirements
HTTPS checklist with status. Report as a short DONE: what changed, evidence, remaining issues.

## Example
- Input/symptom: Mixed content warnings
- Action: update asset URLs to HTTPS
- Output: HTTPS checklist with status.

## References
`references/playbook.md`: detailed how-to, common problems and fixes, tools, verify steps. Read when executing.
