---
name: seo-22
description: 22. ChatGPT SEO (SEO). Use when the request involves: chatgpt seo, chatgpt search, chatgpt citations, openai search, chatgpt referral. Not for topics owned by sibling SEO skills or other categories; routed by seo-master.
---

# 22. ChatGPT SEO

ID: 22 | Level: parent | Parent: SEO Master

## Purpose
ChatGPT-specific. Shared method in 19-ai-seo.

## When to use
Triggers: chatgpt seo, chatgpt search, chatgpt citations, openai search, chatgpt referral

## When NOT to use
- The request belongs to another SEO category (see `../ROUTER.md`): e.g. core seo, google seo, technical seo, on page seo, off page seo, content seo.
- A more specific child skill already covers it: open that child instead of repeating its work.

## Inputs
- Target site/URL(s) or project files, platform (CMS/framework), and goal.
- Data access as available: ChatGPT Search, Bing Webmaster Tools, robots.txt tester, GA4 referral reports.

## Core workflow
1. Allow OAI-SearchBot and ChatGPT-User in robots.txt (GPTBot controls training use)
2. Make pages indexable in Bing as well (ChatGPT Search draws on it)
3. Check ChatGPT answers for brand and category prompts
4. Track chatgpt.com referrals in GA4; add UTM where you control links

## Decision rules
- Use evidence (crawl, GSC, rendered HTML, validators), not assumptions.
- Fix the highest-impact, lowest-risk items first; change only what the task needs.
- If a platform skill (WordPress, WooCommerce, Shopify) applies, its guidance overrides generic advice.

## Edge cases and failure handling
- Not cited -> improve authority, passages, third-party mentions

## Validation
- Re-fetch or re-crawl changed URLs; confirm the fix is live (status, rendered HTML, canonical, schema validator, GSC URL Inspection as relevant).
- Compare with the baseline recorded before the change; check for regressions on neighbouring templates.

## Output requirements
ChatGPT visibility notes. Report as a short DONE: what changed, evidence, remaining issues.

## Example
- Input/symptom: Not cited
- Action: improve authority, passages, third-party mentions
- Output: ChatGPT visibility notes.

## Topics handled here (no separate child)
- Allow OAI-SearchBot and ChatGPT-User in robots.txt (GPTBot is training; decide separately)
- Strong Bing index + crawlable pages
- Track chatgpt.com referrals in GA4
- Visibility, citations, recommendations: see 19-ai-seo/ai-visibility and ai-citations

## References
`references/playbook.md`: detailed how-to, common problems and fixes, tools, verify steps. Read when executing.
