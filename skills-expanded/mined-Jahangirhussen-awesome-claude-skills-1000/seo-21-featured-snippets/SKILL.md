---
name: seo-21-featured-snippets
description: Featured snippets and PAA (SEO). Use when the request involves: featured snippet, people also ask, paa. Not for topics owned by sibling SEO skills or other categories; routed by seo-master.
---

# Featured snippets and PAA

ID: 21.02 | Level: child | Parent: [AEO](../SKILL.md)

## Purpose
Featured snippets and PAA within the seo-master tree: Snippet target list.

## When to use
Triggers: featured snippet, people also ask, paa

## When NOT to use
- The topic is covered by a sibling skill: `../answer-optimization`, `../faq`, `../voice-search`.
- The task is outside this SEO category; see `ROUTER.md` at the seo-master root.

## Inputs
- Target site/URL(s) or project files, platform (CMS/framework), and goal.
- Data access as available: Google SERP (PAA, snippets), GSC queries, AlsoAsked/AnswerThePublic, schema validator.

## Core workflow
1. Find queries where you rank 1-10 and a snippet exists
2. Match the snippet format (paragraph/list/table/video)
3. Structure with clear headings and ordered lists

## Decision rules and checks
- Match snippet format (paragraph/list/table)
- Target existing page-1 queries

## Edge cases and failure handling
- Snippet held by competitor -> provide clearer, more complete answer

## Validation
- Re-fetch or re-crawl changed URLs; confirm the fix is live (status, rendered HTML, canonical, schema validator, GSC URL Inspection as relevant).
- Compare with the baseline recorded before the change; check for regressions on neighbouring templates.

## Output requirements
Snippet target list. Report as a short DONE: what changed, evidence, remaining issues.

## Example
- Input/symptom: Snippet held by competitor
- Action: provide clearer, more complete answer
- Output: Snippet target list.

## References
`references/playbook.md`: detailed how-to, common problems and fixes, tools, verify steps. Read when executing.
