---
name: seo-03-crawlability
description: Crawlability (SEO). Use when the request involves: crawl budget, crawl depth, crawl errors, blocked, googlebot. Not for topics owned by sibling SEO skills or other categories; routed by seo-master.
---

# Crawlability

ID: 03.01 | Level: child | Parent: [Technical SEO](../SKILL.md)

## Purpose
Crawlability within the seo-master tree: Crawl report: depth distribution, waste sources, fixes.

## When to use
Triggers: crawl budget, crawl depth, crawl errors, blocked, googlebot

## When NOT to use
- The topic is covered by a sibling skill: `../canonical`, `../core-web-vitals`, `../https`, `../indexability`, `../javascript-seo`.
- The task is outside this SEO category; see `ROUTER.md` at the seo-master root.

## Inputs
- Target site/URL(s) or project files, platform (CMS/framework), and goal.
- Data access as available: Screaming Frog or Sitebulb, Google Search Console, Lighthouse, PageSpeed Insights, CrUX, WebPageTest, curl -I, server logs.

## Core workflow
1. Check robots.txt, response time, status codes for Googlebot (log files or GSC Crawl stats)
2. Measure click depth; important pages within 3 clicks
3. Find crawl traps: infinite params, calendars, session IDs, faceted combos
4. Reduce waste: block or canonicalize traps, fix redirect chains

## Decision rules and checks
- Server returns 200 fast for Googlebot
- Key pages within 3 clicks
- No crawl traps (params, calendars, faceted)
- Log/GSC crawl stats review

## Edge cases and failure handling
- Googlebot gets 429/5xx -> raise capacity, cache, CDN
- Crawl budget wasted on params -> param handling via robots/noindex/canonical

## Validation
- Re-fetch or re-crawl changed URLs; confirm the fix is live (status, rendered HTML, canonical, schema validator, GSC URL Inspection as relevant).
- Compare with the baseline recorded before the change; check for regressions on neighbouring templates.

## Output requirements
Crawl report: depth distribution, waste sources, fixes. Report as a short DONE: what changed, evidence, remaining issues.

## Example
- Input/symptom: Googlebot gets 429/5xx
- Action: raise capacity, cache, CDN
- Output: Crawl report: depth distribution, waste sources, fixes.

## References
`references/playbook.md`: detailed how-to, common problems and fixes, tools, verify steps. Read when executing.
