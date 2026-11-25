---
name: seo-21-voice-search
description: Voice and conversational (SEO). Use when the request involves: voice search, conversational. Not for topics owned by sibling SEO skills or other categories; routed by seo-master.
---

# Voice and conversational

ID: 21.04 | Level: child | Parent: [AEO](../SKILL.md)

## Purpose
Voice and conversational within the seo-master tree: Conversational query list.

## When to use
Triggers: voice search, conversational

## When NOT to use
- The topic is covered by a sibling skill: `../answer-optimization`, `../faq`, `../featured-snippets`.
- The task is outside this SEO category; see `ROUTER.md` at the seo-master root.

## Inputs
- Target site/URL(s) or project files, platform (CMS/framework), and goal.
- Data access as available: Google SERP (PAA, snippets), GSC queries, AlsoAsked/AnswerThePublic, schema validator.

## Core workflow
1. Use natural-language questions and short answers
2. Local intent: hours, near me, directions
3. Fast mobile pages

## Decision rules and checks
- Natural-language questions
- Local + concise answers

## Edge cases and failure handling
- No local data -> complete GBP

## Validation
- Re-fetch or re-crawl changed URLs; confirm the fix is live (status, rendered HTML, canonical, schema validator, GSC URL Inspection as relevant).
- Compare with the baseline recorded before the change; check for regressions on neighbouring templates.

## Output requirements
Conversational query list. Report as a short DONE: what changed, evidence, remaining issues.

## Example
- Input/symptom: No local data
- Action: complete GBP
- Output: Conversational query list.

## References
`references/playbook.md`: detailed how-to, common problems and fixes, tools, verify steps. Read when executing.
