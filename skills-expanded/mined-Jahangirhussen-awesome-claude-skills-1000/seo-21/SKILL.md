---
name: seo-21
description: 21. AEO (SEO). Use when the request involves: aeo, answer engine optimization, featured snippet, faq, people also ask, voice search, direct answer. Not for topics owned by sibling SEO skills or other categories; routed by seo-master.
---

# 21. AEO

ID: 21 | Level: parent | Parent: SEO Master

## Purpose
Direct-answer formatting.

## When to use
Triggers: aeo, answer engine optimization, featured snippet, faq, people also ask, voice search, direct answer

## When NOT to use
- The request belongs to another SEO category (see `../ROUTER.md`): e.g. core seo, google seo, technical seo, on page seo, off page seo, content seo.
- A more specific child skill already covers it: open that child instead of repeating its work.

## Inputs
- Target site/URL(s) or project files, platform (CMS/framework), and goal.
- Data access as available: Google SERP (PAA, snippets), GSC queries, AlsoAsked/AnswerThePublic, schema validator.

## Core workflow
1. Identify question queries from PAA, GSC, forums
2. Answer concisely first, detail after
3. Use matching format (paragraph, list, table)
4. Mark up FAQ only when visible and eligible

## Decision rules
- Use evidence (crawl, GSC, rendered HTML, validators), not assumptions.
- Fix the highest-impact, lowest-risk items first; change only what the task needs.
- If a platform skill (WordPress, WooCommerce, Shopify) applies, its guidance overrides generic advice.

## Edge cases and failure handling
- Answer buried -> move up

## Validation
- Re-fetch or re-crawl changed URLs; confirm the fix is live (status, rendered HTML, canonical, schema validator, GSC URL Inspection as relevant).
- Compare with the baseline recorded before the change; check for regressions on neighbouring templates.

## Output requirements
Answer-ready content list. Report as a short DONE: what changed, evidence, remaining issues.

## Example
- Input/symptom: Answer buried
- Action: move up
- Output: Answer-ready content list.

## Children
- [Answer optimization](answer-optimization/SKILL.md)
- [Featured snippets and PAA](featured-snippets/SKILL.md)
- [FAQ](faq/SKILL.md)
- [Voice and conversational](voice-search/SKILL.md)

## Merged from (read for deep method)
- `../_source/aeo/SKILL.md`

## External sources merged (deep method)
- `../_source/borghei__aeo/SKILL.md`

## References
`references/playbook.md`: detailed how-to, common problems and fixes, tools, verify steps. Read when executing.
