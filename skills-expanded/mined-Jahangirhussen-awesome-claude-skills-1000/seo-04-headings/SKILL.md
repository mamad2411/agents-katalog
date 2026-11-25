---
name: seo-04-headings
description: Headings (SEO). Use when the request involves: h1, h2, heading structure. Not for topics owned by sibling SEO skills or other categories; routed by seo-master.
---

# Headings

ID: 04.03 | Level: child | Parent: [On-Page SEO](../SKILL.md)

## Purpose
Headings within the seo-master tree: Heading outline per page.

## When to use
Triggers: h1, h2, heading structure

## When NOT to use
- The topic is covered by a sibling skill: `../content-optimization`, `../entity-optimization`, `../internal-linking`, `../meta-descriptions`, `../title-tags`.
- The task is outside this SEO category; see `ROUTER.md` at the seo-master root.

## Inputs
- Target site/URL(s) or project files, platform (CMS/framework), and goal.
- Data access as available: Screaming Frog (titles/meta/H1), Google Search Console, SERP checks, SEO plugin or CMS fields, a text diff tool.

## Core workflow
1. Exactly one H1 reflecting the page topic
2. H2/H3 outline mirrors subtopics and questions users ask
3. Do not skip levels for styling; use CSS for appearance

## Decision rules and checks
- One H1 matching intent
- Logical H2/H3 outline
- Question headings for AEO where natural

## Edge cases and failure handling
- Logo is the H1 -> make page title the H1
- Multiple H1 from theme -> fix template

## Validation
- Re-fetch or re-crawl changed URLs; confirm the fix is live (status, rendered HTML, canonical, schema validator, GSC URL Inspection as relevant).
- Compare with the baseline recorded before the change; check for regressions on neighbouring templates.

## Output requirements
Heading outline per page. Report as a short DONE: what changed, evidence, remaining issues.

## Example
- Input/symptom: Logo is the H1
- Action: make page title the H1
- Output: Heading outline per page.

## References
`references/playbook.md`: detailed how-to, common problems and fixes, tools, verify steps. Read when executing.
