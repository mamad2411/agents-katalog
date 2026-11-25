---
name: seo-21-faq
description: FAQ (SEO). Use when the request involves: faq, faq schema. Not for topics owned by sibling SEO skills or other categories; routed by seo-master.
---

# FAQ

ID: 21.03 | Level: child | Parent: [AEO](../SKILL.md)

## Purpose
FAQ within the seo-master tree: FAQ block and JSON-LD.

## When to use
Triggers: faq, faq schema

## When NOT to use
- The topic is covered by a sibling skill: `../answer-optimization`, `../featured-snippets`, `../voice-search`.
- The task is outside this SEO category; see `ROUTER.md` at the seo-master root.

## Inputs
- Target site/URL(s) or project files, platform (CMS/framework), and goal.
- Data access as available: Google SERP (PAA, snippets), GSC queries, AlsoAsked/AnswerThePublic, schema validator.

## Core workflow
1. Use real user questions
2. Visible Q&A on the page; keep answers short
3. FAQPage schema only when allowed (rich results are limited for most sites)

## Decision rules and checks
- Visible Q&A, real questions
- FAQ schema only if eligible/visible

## Edge cases and failure handling
- Hidden FAQ markup -> remove or make visible

## Validation
- Re-fetch or re-crawl changed URLs; confirm the fix is live (status, rendered HTML, canonical, schema validator, GSC URL Inspection as relevant).
- Compare with the baseline recorded before the change; check for regressions on neighbouring templates.

## Output requirements
FAQ block and JSON-LD. Report as a short DONE: what changed, evidence, remaining issues.

## Example
- Input/symptom: Hidden FAQ markup
- Action: remove or make visible
- Output: FAQ block and JSON-LD.

## Dependencies (load only if needed)
- 27-schema-seo/faq

## References
`references/playbook.md`: detailed how-to, common problems and fixes, tools, verify steps. Read when executing.
