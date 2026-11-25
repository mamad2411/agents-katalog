---
name: seo-04-content-optimization
description: On-page content optimization (SEO). Use when the request involves: optimize content, content score, semantic keywords, readability. Not for topics owned by sibling SEO skills or other categories; routed by seo-master.
---

# On-page content optimization

ID: 04.06 | Level: child | Parent: [On-Page SEO](../SKILL.md)

## Purpose
On-page content optimization within the seo-master tree: Content change list per page.

## When to use
Triggers: optimize content, content score, semantic keywords, readability

## When NOT to use
- The topic is covered by a sibling skill: `../entity-optimization`, `../headings`, `../internal-linking`, `../meta-descriptions`, `../title-tags`.
- The task is outside this SEO category; see `ROUTER.md` at the seo-master root.

## Inputs
- Target site/URL(s) or project files, platform (CMS/framework), and goal.
- Data access as available: Screaming Frog (titles/meta/H1), Google Search Console, SERP checks, SEO plugin or CMS fields, a text diff tool.

## Core workflow
1. Compare against top-ranking pages for entities, subtopics, questions
2. Answer the main query in the first screen; add depth where competitors are thin
3. Add original value: data, examples, screenshots, expert quotes
4. Improve readability: short paragraphs, lists, tables

## Decision rules and checks
- Cover entities/subtopics from top SERPs
- Answer first, scannable structure
- Fresh facts, sources, author

## Edge cases and failure handling
- Matching competitors word-for-word -> add distinct value instead
- Outdated facts -> refresh with sources and date

## Validation
- Re-fetch or re-crawl changed URLs; confirm the fix is live (status, rendered HTML, canonical, schema validator, GSC URL Inspection as relevant).
- Compare with the baseline recorded before the change; check for regressions on neighbouring templates.

## Output requirements
Content change list per page. Report as a short DONE: what changed, evidence, remaining issues.

## Example
- Input/symptom: Matching competitors word-for-word
- Action: add distinct value instead
- Output: Content change list per page.

## References
`references/playbook.md`: detailed how-to, common problems and fixes, tools, verify steps. Read when executing.
