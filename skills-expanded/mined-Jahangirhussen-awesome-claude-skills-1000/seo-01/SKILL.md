---
name: seo-01
description: 01. Core SEO (SEO). Use when the request involves: seo strategy, seo plan, roadmap, keyword research, search intent, ranking factors, topical authority, competitor analysis. Not for topics owned by sibling SEO skills or other categories; routed by seo-master.
---

# 01. Core SEO

ID: 01 | Level: parent | Parent: SEO Master

## Purpose
Foundation: goals, intent, keywords, strategy, competitors.

## When to use
Triggers: seo strategy, seo plan, roadmap, keyword research, search intent, ranking factors, topical authority, competitor analysis

## When NOT to use
- The request belongs to another SEO category (see `../ROUTER.md`): e.g. google seo, technical seo, on page seo, off page seo, content seo, local seo.
- A more specific child skill already covers it: open that child instead of repeating its work.

## Inputs
- Target site/URL(s) or project files, platform (CMS/framework), and goal.
- Data access as available: Google Search Console, GA4, Ahrefs/Semrush (keywords, competitors), Google Trends, AnswerThePublic, a spreadsheet.

## Core workflow
1. Clarify goal (leads, sales, signups), market, and site/URL
2. Pull baseline: GSC clicks/impressions, GA4 organic conversions, top pages
3. Choose the 3 levers with biggest impact (technical blockers, content gaps, authority)
4. Write a 30/60/90-day plan with owners and success metrics

## Decision rules
- Use evidence (crawl, GSC, rendered HTML, validators), not assumptions.
- Fix the highest-impact, lowest-risk items first; change only what the task needs.
- If a platform skill (WordPress, WooCommerce, Shopify) applies, its guidance overrides generic advice.

## Edge cases and failure handling
- No baseline data -> connect GSC/GA4 first, else use a crawl + SERP sample
- Too many ideas -> rank by impact x effort x confidence and cut to top 10

## Validation
- Re-fetch or re-crawl changed URLs; confirm the fix is live (status, rendered HTML, canonical, schema validator, GSC URL Inspection as relevant).
- Compare with the baseline recorded before the change; check for regressions on neighbouring templates.

## Output requirements
Prioritized plan: goal, KPIs, ranked actions, timeline. Report as a short DONE: what changed, evidence, remaining issues.

## Example
- Input/symptom: No baseline data
- Action: connect GSC/GA4 first, else use a crawl + SERP sample
- Output: Prioritized plan: goal, KPIs, ranked actions, timeline.

## Children
- [Keyword research](keyword-research/SKILL.md)
- [SEO strategy and roadmap](seo-strategy/SKILL.md)
- [Competitor SEO analysis](competitor-analysis/SKILL.md)

## Topics handled here (no separate child)
- Search intent: classify informational / commercial / transactional / navigational; map one intent per URL
- Fundamentals: crawl -> index -> rank; E-E-A-T; helpful content
- Ranking factors: relevance, content quality, links, UX/CWV, authority; no guessing about weights

## Merged from (read for deep method)
- `../_source/seo-specialist/SKILL.md`

## Related installed skills (kept in place; invoke only if needed)
- `content-strategy`
- `pillar-content-architecture`

## External sources merged (deep method)
- `../_source/aaron__serp-analysis/SKILL.md`

## References
`references/playbook.md`: detailed how-to, common problems and fixes, tools, verify steps. Read when executing.
