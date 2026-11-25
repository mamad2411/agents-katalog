---
name: seo-19-ai-citations
description: AI citations (SEO). Use when the request involves: ai citation, citability, source selection. Not for topics owned by sibling SEO skills or other categories; routed by seo-master.
---

# AI citations

ID: 19.03 | Level: child | Parent: [AI SEO](../SKILL.md)

## Purpose
AI citations within the seo-master tree: Citation gap list.

## When to use
Triggers: ai citation, citability, source selection

## When NOT to use
- The topic is covered by a sibling skill: `../ai-content`, `../ai-search`, `../ai-visibility`.
- The task is outside this SEO category; see `ROUTER.md` at the seo-master root.

## Inputs
- Target site/URL(s) or project files, platform (CMS/framework), and goal.
- Data access as available: Prompt tracking sheet, ChatGPT/Gemini/Perplexity/Claude/AI Overviews, GA4 referral reports, server logs for AI bots.

## Core workflow
1. Publish original research, benchmarks, definitions
2. Get listed on authoritative third-party sources (reviews, directories, press)
3. Use consistent brand/product descriptions everywhere
4. Make claims verifiable with sources

## Decision rules and checks
- Original data and primary sources
- Third-party mentions/reviews
- Consistent entity facts

## Edge cases and failure handling
- Only competitors cited -> create better primary source content

## Validation
- Re-fetch or re-crawl changed URLs; confirm the fix is live (status, rendered HTML, canonical, schema validator, GSC URL Inspection as relevant).
- Compare with the baseline recorded before the change; check for regressions on neighbouring templates.

## Output requirements
Citation gap list. Report as a short DONE: what changed, evidence, remaining issues.

## Example
- Input/symptom: Only competitors cited
- Action: create better primary source content
- Output: Citation gap list.

## References
`references/playbook.md`: detailed how-to, common problems and fixes, tools, verify steps. Read when executing.
