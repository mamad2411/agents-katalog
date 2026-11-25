---
name: seo-19-ai-content
description: AI-ready content (SEO). Use when the request involves: ai readable content, machine readable. Not for topics owned by sibling SEO skills or other categories; routed by seo-master.
---

# AI-ready content

ID: 19.02 | Level: child | Parent: [AI SEO](../SKILL.md)

## Purpose
AI-ready content within the seo-master tree: Passage-level rewrite list.

## When to use
Triggers: ai readable content, machine readable

## When NOT to use
- The topic is covered by a sibling skill: `../ai-citations`, `../ai-search`, `../ai-visibility`.
- The task is outside this SEO category; see `ROUTER.md` at the seo-master root.

## Inputs
- Target site/URL(s) or project files, platform (CMS/framework), and goal.
- Data access as available: Prompt tracking sheet, ChatGPT/Gemini/Perplexity/Claude/AI Overviews, GA4 referral reports, server logs for AI bots.

## Core workflow
1. Use semantic HTML and short self-contained passages (50-150 words)
2. Lead with the answer, then support
3. Include named entities, numbers, citations
4. Add author and last-updated

## Decision rules and checks
- Clean semantic HTML
- Clear definitions, stats, lists, tables
- Dates + authorship

## Edge cases and failure handling
- Wall-of-text -> break into scannable sections

## Validation
- Re-fetch or re-crawl changed URLs; confirm the fix is live (status, rendered HTML, canonical, schema validator, GSC URL Inspection as relevant).
- Compare with the baseline recorded before the change; check for regressions on neighbouring templates.

## Output requirements
Passage-level rewrite list. Report as a short DONE: what changed, evidence, remaining issues.

## Example
- Input/symptom: Wall-of-text
- Action: break into scannable sections
- Output: Passage-level rewrite list.

## References
`references/playbook.md`: detailed how-to, common problems and fixes, tools, verify steps. Read when executing.
