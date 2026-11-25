---
name: seo-25
description: 25. Perplexity SEO (SEO). Use when the request involves: perplexity seo, perplexity citations. Not for topics owned by sibling SEO skills or other categories; routed by seo-master.
---

# 25. Perplexity SEO

ID: 25 | Level: parent | Parent: SEO Master

## Purpose
Perplexity-specific. Shared method in 19-ai-seo.

## When to use
Triggers: perplexity seo, perplexity citations

## When NOT to use
- The request belongs to another SEO category (see `../ROUTER.md`): e.g. core seo, google seo, technical seo, on page seo, off page seo, content seo.
- A more specific child skill already covers it: open that child instead of repeating its work.

## Inputs
- Target site/URL(s) or project files, platform (CMS/framework), and goal.
- Data access as available: Perplexity, robots.txt tester, citation tracking sheet, GA4 referrals.

## Core workflow
1. Allow PerplexityBot
2. Publish original, well-sourced content with clear structure
3. Check which sources Perplexity cites for your topics and match/exceed them
4. Keep pages fast

## Decision rules
- Use evidence (crawl, GSC, rendered HTML, validators), not assumptions.
- Fix the highest-impact, lowest-risk items first; change only what the task needs.
- If a platform skill (WordPress, WooCommerce, Shopify) applies, its guidance overrides generic advice.

## Edge cases and failure handling
- Competitor sources always cited -> create more authoritative resource

## Validation
- Re-fetch or re-crawl changed URLs; confirm the fix is live (status, rendered HTML, canonical, schema validator, GSC URL Inspection as relevant).
- Compare with the baseline recorded before the change; check for regressions on neighbouring templates.

## Output requirements
Perplexity visibility notes. Report as a short DONE: what changed, evidence, remaining issues.

## Example
- Input/symptom: Competitor sources always cited
- Action: create more authoritative resource
- Output: Perplexity visibility notes.

## Topics handled here (no separate child)
- Allow PerplexityBot
- Original data, clear sourcing, fast crawlable pages
- Citations/visibility: see 19-ai-seo

## References
`references/playbook.md`: detailed how-to, common problems and fixes, tools, verify steps. Read when executing.
