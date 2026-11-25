---
name: seo-04-url-optimization
description: URL optimization (SEO). Use when the request involves: url, slug, permalink. Not for topics owned by sibling SEO skills or other categories; routed by seo-master.
---

# URL optimization

ID: 04.04 | Level: child | Parent: [On-Page SEO](../SKILL.md)

## Purpose
URL optimization within the seo-master tree: URL change map.

## When to use
Triggers: url, slug, permalink

## When NOT to use
- The topic is covered by a sibling skill: `../content-optimization`, `../entity-optimization`, `../headings`, `../internal-linking`, `../meta-descriptions`.
- The task is outside this SEO category; see `ROUTER.md` at the seo-master root.

## Inputs
- Target site/URL(s) or project files, platform (CMS/framework), and goal.
- Data access as available: Screaming Frog (titles/meta/H1), Google Search Console, SERP checks, SEO plugin or CMS fields, a text diff tool.

## Core workflow
1. Short, lowercase, hyphenated, descriptive slugs
2. Avoid params, dates, IDs when possible
3. On change: 301 old to new, update internal links and sitemap

## Decision rules and checks
- Short, lowercase, hyphens, keyword
- No dates/IDs/params when avoidable
- 301 on any change

## Edge cases and failure handling
- Changing URLs without redirects -> add 301 map
- Keyword-stuffed long URLs -> shorten

## Validation
- Re-fetch or re-crawl changed URLs; confirm the fix is live (status, rendered HTML, canonical, schema validator, GSC URL Inspection as relevant).
- Compare with the baseline recorded before the change; check for regressions on neighbouring templates.

## Output requirements
URL change map. Report as a short DONE: what changed, evidence, remaining issues.

## Example
- Input/symptom: Changing URLs without redirects
- Action: add 301 map
- Output: URL change map.

## References
`references/playbook.md`: detailed how-to, common problems and fixes, tools, verify steps. Read when executing.
