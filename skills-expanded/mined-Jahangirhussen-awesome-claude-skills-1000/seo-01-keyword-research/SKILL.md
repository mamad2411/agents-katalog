---
name: seo-01-keyword-research
description: Keyword research (SEO). Use when the request involves: keyword research, keyword clustering, keyword mapping, intent, keyword gap. Not for topics owned by sibling SEO skills or other categories; routed by seo-master.
---

# Keyword research

ID: 01.01 | Level: child | Parent: [Core SEO](../SKILL.md)

## Purpose
Keyword research within the seo-master tree: Keyword map table: keyword, intent, volume, difficulty, target URL, priority.

## When to use
Triggers: keyword research, keyword clustering, keyword mapping, intent, keyword gap

## When NOT to use
- The topic is covered by a sibling skill: `../competitor-analysis`, `../seo-strategy`.
- The task is outside this SEO category; see `ROUTER.md` at the seo-master root.

## Inputs
- Target site/URL(s) or project files, platform (CMS/framework), and goal.
- Data access as available: Google Search Console, GA4, Ahrefs/Semrush (keywords, competitors), Google Trends, AnswerThePublic, a spreadsheet.

## Core workflow
1. Seed terms from offer, product pages, GSC queries, competitor URLs, People Also Ask
2. Expand with autocomplete, related searches, competitor ranking keywords (Ahrefs/Semrush if available)
3. Label intent: informational / commercial / transactional / navigational
4. Cluster by SERP overlap (same top-10 URLs = same page)
5. Score: volume x business value / difficulty; assign 1 primary keyword per URL

## Decision rules and checks
- Seed from product/offer, GSC queries, competitors
- Classify intent; cluster by SERP overlap
- Prioritize: volume x difficulty x business value
- Map 1 primary keyword -> 1 URL

## Edge cases and failure handling
- Cannibalization (two URLs for one intent) -> merge or differentiate intent
- High volume but wrong intent -> drop or create the right page type

## Validation
- Re-fetch or re-crawl changed URLs; confirm the fix is live (status, rendered HTML, canonical, schema validator, GSC URL Inspection as relevant).
- Compare with the baseline recorded before the change; check for regressions on neighbouring templates.

## Output requirements
Keyword map table: keyword, intent, volume, difficulty, target URL, priority. Report as a short DONE: what changed, evidence, remaining issues.

## Example
- Input/symptom: Cannibalization (two URLs for one intent)
- Action: merge or differentiate intent
- Output: Keyword map table: keyword, intent, volume, difficulty, target URL, priority.

## Merged from (read for deep method)
- `../../_source/seo-keyword/SKILL.md`
- `../../_source/seo-keyword-gap-audit/SKILL.md`

## External sources merged (deep method)
- `../../_source/aaron__keyword-research/SKILL.md`

## References
`references/playbook.md`: detailed how-to, common problems and fixes, tools, verify steps. Read when executing.
