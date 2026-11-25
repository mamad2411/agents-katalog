---
name: seo-19-ai-search
description: AI search optimization (SEO). Use when the request involves: ai search optimization, ai overviews. Not for topics owned by sibling SEO skills or other categories; routed by seo-master.
---

# AI search optimization

ID: 19.01 | Level: child | Parent: [AI SEO](../SKILL.md)

## Purpose
AI search optimization within the seo-master tree: AI-search optimization checklist.

## When to use
Triggers: ai search optimization, ai overviews

## When NOT to use
- The topic is covered by a sibling skill: `../ai-citations`, `../ai-content`, `../ai-visibility`.
- The task is outside this SEO category; see `ROUTER.md` at the seo-master root.

## Inputs
- Target site/URL(s) or project files, platform (CMS/framework), and goal.
- Data access as available: Prompt tracking sheet, ChatGPT/Gemini/Perplexity/Claude/AI Overviews, GA4 referral reports, server logs for AI bots.

## Core workflow
1. Rank well in traditional search first (AI answers retrieve from the web)
2. Structure pages with clear headings, definitions, steps, tables
3. Cover query fan-out subtopics on one page or cluster
4. Keep facts current with dates

## Decision rules and checks
- Allow AI crawlers per policy (robots.txt)
- Answer-first, quotable passages
- Strong traditional rankings still feed AI

## Edge cases and failure handling
- Thin content never cited -> add original data and expertise

## Validation
- Re-fetch or re-crawl changed URLs; confirm the fix is live (status, rendered HTML, canonical, schema validator, GSC URL Inspection as relevant).
- Compare with the baseline recorded before the change; check for regressions on neighbouring templates.

## Output requirements
AI-search optimization checklist. Report as a short DONE: what changed, evidence, remaining issues.

## Example
- Input/symptom: Thin content never cited
- Action: add original data and expertise
- Output: AI-search optimization checklist.

## References
`references/playbook.md`: detailed how-to, common problems and fixes, tools, verify steps. Read when executing.
