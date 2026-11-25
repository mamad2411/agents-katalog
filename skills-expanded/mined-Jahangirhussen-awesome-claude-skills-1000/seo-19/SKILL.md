---
name: seo-19
description: 19. AI SEO (SEO). Use when the request involves: ai seo, ai search, ai visibility, ai citations, machine-readable content, ai referral traffic, ai content seo. Not for topics owned by sibling SEO skills or other categories; routed by seo-master.
---

# 19. AI SEO

ID: 19 | Level: parent | Parent: SEO Master

## Purpose
Shared foundation for AI-search visibility; engine pages (20-25) reuse these children.

## When to use
Triggers: ai seo, ai search, ai visibility, ai citations, machine-readable content, ai referral traffic, ai content seo

## When NOT to use
- The request belongs to another SEO category (see `../ROUTER.md`): e.g. core seo, google seo, technical seo, on page seo, off page seo, content seo.
- A more specific child skill already covers it: open that child instead of repeating its work.

## Inputs
- Target site/URL(s) or project files, platform (CMS/framework), and goal.
- Data access as available: Prompt tracking sheet, ChatGPT/Gemini/Perplexity/Claude/AI Overviews, GA4 referral reports, server logs for AI bots.

## Core workflow
1. Check AI crawler access in robots.txt per policy (OAI-SearchBot, GPTBot, ClaudeBot, Claude-SearchBot, PerplexityBot, Google-Extended, Applebot-Extended)
2. Make key pages crawlable, fast, server-rendered
3. Write quotable answer-first passages with sources and dates
4. Build entity and brand consistency; earn third-party mentions
5. Track mentions/citations and AI referrals

## Decision rules
- Use evidence (crawl, GSC, rendered HTML, validators), not assumptions.
- Fix the highest-impact, lowest-risk items first; change only what the task needs.
- If a platform skill (WordPress, WooCommerce, Shopify) applies, its guidance overrides generic advice.

## Edge cases and failure handling
- Blocked all AI bots -> decide training vs search access separately
- Content only behind JS/login -> make accessible

## Validation
- Re-fetch or re-crawl changed URLs; confirm the fix is live (status, rendered HTML, canonical, schema validator, GSC URL Inspection as relevant).
- Compare with the baseline recorded before the change; check for regressions on neighbouring templates.

## Output requirements
AI visibility plan and tracking sheet. Report as a short DONE: what changed, evidence, remaining issues.

## Example
- Input/symptom: Blocked all AI bots
- Action: decide training vs search access separately
- Output: AI visibility plan and tracking sheet.

## Children
- [AI search optimization](ai-search/SKILL.md)
- [AI-ready content](ai-content/SKILL.md)
- [AI citations](ai-citations/SKILL.md)
- [AI visibility tracking](ai-visibility/SKILL.md)

## Merged from (read for deep method)
- `../_source/ai-seo/SKILL.md`
- `../_source/seo-aeo-amplifier/SKILL.md`

## External sources merged (deep method)
- `../_source/borghei__ai-seo/SKILL.md`
- `../_source/attainmentlabs__ai-seo-skill/SKILL.md`

## References
`references/playbook.md`: detailed how-to, common problems and fixes, tools, verify steps. Read when executing.
