---
name: seo-21-answer-optimization
description: Answer optimization (SEO). Use when the request involves: direct answer, answer-first. Not for topics owned by sibling SEO skills or other categories; routed by seo-master.
---

# Answer optimization

ID: 21.01 | Level: child | Parent: [AEO](../SKILL.md)

## Purpose
Answer optimization within the seo-master tree: Q&A blocks.

## When to use
Triggers: direct answer, answer-first

## When NOT to use
- The topic is covered by a sibling skill: `../faq`, `../featured-snippets`, `../voice-search`.
- The task is outside this SEO category; see `ROUTER.md` at the seo-master root.

## Inputs
- Target site/URL(s) or project files, platform (CMS/framework), and goal.
- Data access as available: Google SERP (PAA, snippets), GSC queries, AlsoAsked/AnswerThePublic, schema validator.

## Core workflow
1. Place 40-60 word answer directly under a question-style heading
2. Support with steps, examples, sources
3. Keep one answer per heading

## Decision rules and checks
- 40-60 word answer under question heading
- Definitions, steps, tables
- Cite sources

## Edge cases and failure handling
- Vague answers -> be specific

## Validation
- Re-fetch or re-crawl changed URLs; confirm the fix is live (status, rendered HTML, canonical, schema validator, GSC URL Inspection as relevant).
- Compare with the baseline recorded before the change; check for regressions on neighbouring templates.

## Output requirements
Q&A blocks. Report as a short DONE: what changed, evidence, remaining issues.

## Example
- Input/symptom: Vague answers
- Action: be specific
- Output: Q&A blocks.

## References
`references/playbook.md`: detailed how-to, common problems and fixes, tools, verify steps. Read when executing.
