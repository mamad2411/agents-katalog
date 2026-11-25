---
name: seo-23
description: 23. Claude SEO (SEO). Use when the request involves: claude seo, claude visibility, anthropic search. Not for topics owned by sibling SEO skills or other categories; routed by seo-master.
---

# 23. Claude SEO

ID: 23 | Level: parent | Parent: SEO Master

## Purpose
Claude-specific. Shared method in 19-ai-seo.

## When to use
Triggers: claude seo, claude visibility, anthropic search

## When NOT to use
- The request belongs to another SEO category (see `../ROUTER.md`): e.g. core seo, google seo, technical seo, on page seo, off page seo, content seo.
- A more specific child skill already covers it: open that child instead of repeating its work.

## Inputs
- Target site/URL(s) or project files, platform (CMS/framework), and goal.
- Data access as available: Claude with web search, robots.txt tester, server logs, schema validator.

## Core workflow
1. Decide policy for ClaudeBot (training), Claude-User, Claude-SearchBot in robots.txt
2. Provide clean semantic, factual pages
3. Test brand/category prompts in Claude with web search enabled

## Decision rules
- Use evidence (crawl, GSC, rendered HTML, validators), not assumptions.
- Fix the highest-impact, lowest-risk items first; change only what the task needs.
- If a platform skill (WordPress, WooCommerce, Shopify) applies, its guidance overrides generic advice.

## Edge cases and failure handling
- Inconsistent brand facts -> standardize

## Validation
- Re-fetch or re-crawl changed URLs; confirm the fix is live (status, rendered HTML, canonical, schema validator, GSC URL Inspection as relevant).
- Compare with the baseline recorded before the change; check for regressions on neighbouring templates.

## Output requirements
Claude visibility notes. Report as a short DONE: what changed, evidence, remaining issues.

## Example
- Input/symptom: Inconsistent brand facts
- Action: standardize
- Output: Claude visibility notes.

## Topics handled here (no separate child)
- Bots: ClaudeBot (training), Claude-User, Claude-SearchBot - set robots.txt per policy
- Clean semantic HTML, factual sourced content
- Discoverability/citations: see 19-ai-seo

## References
`references/playbook.md`: detailed how-to, common problems and fixes, tools, verify steps. Read when executing.
