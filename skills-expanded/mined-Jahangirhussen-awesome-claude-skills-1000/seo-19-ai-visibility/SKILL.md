---
name: seo-19-ai-visibility
description: AI visibility tracking (SEO). Use when the request involves: ai visibility, ai mention tracking, ai referral. Not for topics owned by sibling SEO skills or other categories; routed by seo-master.
---

# AI visibility tracking

ID: 19.04 | Level: child | Parent: [AI SEO](../SKILL.md)

## Purpose
AI visibility tracking within the seo-master tree: Visibility tracker: prompt, engine, mention?, cited URL, date.

## When to use
Triggers: ai visibility, ai mention tracking, ai referral

## When NOT to use
- The topic is covered by a sibling skill: `../ai-citations`, `../ai-content`, `../ai-search`.
- The task is outside this SEO category; see `ROUTER.md` at the seo-master root.

## Inputs
- Target site/URL(s) or project files, platform (CMS/framework), and goal.
- Data access as available: Prompt tracking sheet, ChatGPT/Gemini/Perplexity/Claude/AI Overviews, GA4 referral reports, server logs for AI bots.

## Core workflow
1. Define 20-50 prompts per topic (brand, category, comparison, problem)
2. Run them across ChatGPT, Gemini, Perplexity, Google AI Overviews, Claude; log mention, citation, position, sentiment
3. Repeat monthly; note variance (answers change run to run)
4. Track AI referral traffic in GA4 (referrers like chatgpt.com, perplexity.ai)

## Decision rules and checks
- Prompt set per topic
- Track mention/citation/position
- GA4 referrals from AI domains

## Edge cases and failure handling
- Single-run results are noisy -> average several runs

## Validation
- Re-fetch or re-crawl changed URLs; confirm the fix is live (status, rendered HTML, canonical, schema validator, GSC URL Inspection as relevant).
- Compare with the baseline recorded before the change; check for regressions on neighbouring templates.

## Output requirements
Visibility tracker: prompt, engine, mention?, cited URL, date. Report as a short DONE: what changed, evidence, remaining issues.

## Example
- Input/symptom: Single-run results are noisy
- Action: average several runs
- Output: Visibility tracker: prompt, engine, mention?, cited URL, date.

## References
`references/playbook.md`: detailed how-to, common problems and fixes, tools, verify steps. Read when executing.
