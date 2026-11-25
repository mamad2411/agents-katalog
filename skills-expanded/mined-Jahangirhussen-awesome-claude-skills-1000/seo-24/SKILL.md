---
name: seo-24
description: 24. Gemini SEO (SEO). Use when the request involves: gemini seo, google ai ecosystem, gemini visibility. Not for topics owned by sibling SEO skills or other categories; routed by seo-master.
---

# 24. Gemini SEO

ID: 24 | Level: parent | Parent: SEO Master

## Purpose
Gemini-specific. Shared method in 19-ai-seo.

## When to use
Triggers: gemini seo, google ai ecosystem, gemini visibility

## When NOT to use
- The request belongs to another SEO category (see `../ROUTER.md`): e.g. core seo, google seo, technical seo, on page seo, off page seo, content seo.
- A more specific child skill already covers it: open that child instead of repeating its work.

## Inputs
- Target site/URL(s) or project files, platform (CMS/framework), and goal.
- Data access as available: Gemini, Google AI Overviews, GSC, Business Profile, Knowledge Graph search, schema validator.

## Core workflow
1. Strengthen Google indexing, Business Profile, Knowledge Graph signals
2. Organization schema with sameAs
3. Quality images and video for multimodal answers
4. Test prompts in Gemini and AI Overviews

## Decision rules
- Use evidence (crawl, GSC, rendered HTML, validators), not assumptions.
- Fix the highest-impact, lowest-risk items first; change only what the task needs.
- If a platform skill (WordPress, WooCommerce, Shopify) applies, its guidance overrides generic advice.

## Edge cases and failure handling
- No Knowledge Panel -> build entity signals

## Validation
- Re-fetch or re-crawl changed URLs; confirm the fix is live (status, rendered HTML, canonical, schema validator, GSC URL Inspection as relevant).
- Compare with the baseline recorded before the change; check for regressions on neighbouring templates.

## Output requirements
Gemini visibility notes. Report as a short DONE: what changed, evidence, remaining issues.

## Example
- Input/symptom: No Knowledge Panel
- Action: build entity signals
- Output: Gemini visibility notes.

## Topics handled here (no separate child)
- Strong Google indexing + Business Profile
- Organization schema + sameAs, Knowledge Graph presence
- Quality images/video for multimodal

## References
`references/playbook.md`: detailed how-to, common problems and fixes, tools, verify steps. Read when executing.
