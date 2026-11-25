---
name: seo-04-title-tags
description: Title tags (SEO). Use when the request involves: title tag, seo title. Not for topics owned by sibling SEO skills or other categories; routed by seo-master.
---

# Title tags

ID: 04.01 | Level: child | Parent: [On-Page SEO](../SKILL.md)

## Purpose
Title tags within the seo-master tree: Title table: URL, current, proposed, reason.

## When to use
Triggers: title tag, seo title

## When NOT to use
- The topic is covered by a sibling skill: `../content-optimization`, `../entity-optimization`, `../headings`, `../internal-linking`, `../meta-descriptions`.
- The task is outside this SEO category; see `ROUTER.md` at the seo-master root.

## Inputs
- Target site/URL(s) or project files, platform (CMS/framework), and goal.
- Data access as available: Screaming Frog (titles/meta/H1), Google Search Console, SERP checks, SEO plugin or CMS fields, a text diff tool.

## Core workflow
1. Write unique title per URL, ~50-60 chars (pixel width ~580px)
2. Primary keyword near the start; add brand at the end; add differentiator (year, price, benefit)
3. Match search intent; avoid clickbait that mismatches the page

## Decision rules and checks
- Unique, ~50-60 chars, primary keyword early
- Match intent; add differentiator
- Do not duplicate across URLs

## Edge cases and failure handling
- Google rewrites title -> shorten, align with H1 and content
- Duplicate titles -> add unique attribute

## Validation
- Re-fetch or re-crawl changed URLs; confirm the fix is live (status, rendered HTML, canonical, schema validator, GSC URL Inspection as relevant).
- Compare with the baseline recorded before the change; check for regressions on neighbouring templates.

## Output requirements
Title table: URL, current, proposed, reason. Report as a short DONE: what changed, evidence, remaining issues.

## Example
- Input/symptom: Google rewrites title
- Action: shorten, align with H1 and content
- Output: Title table: URL, current, proposed, reason.

## References
`references/playbook.md`: detailed how-to, common problems and fixes, tools, verify steps. Read when executing.
