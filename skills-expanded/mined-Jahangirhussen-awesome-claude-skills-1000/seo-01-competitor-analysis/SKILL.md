---
name: seo-01-competitor-analysis
description: Competitor SEO analysis (SEO). Use when the request involves: competitor, serp overlap, competitive seo, content gap vs competitor. Not for topics owned by sibling SEO skills or other categories; routed by seo-master.
---

# Competitor SEO analysis

ID: 01.03 | Level: child | Parent: [Core SEO](../SKILL.md)

## Purpose
Competitor SEO analysis within the seo-master tree: Gap table: keyword/topic, competitor URL, your URL (or none), action.

## When to use
Triggers: competitor, serp overlap, competitive seo, content gap vs competitor

## When NOT to use
- The topic is covered by a sibling skill: `../keyword-research`, `../seo-strategy`.
- The task is outside this SEO category; see `ROUTER.md` at the seo-master root.

## Inputs
- Target site/URL(s) or project files, platform (CMS/framework), and goal.
- Data access as available: Google Search Console, GA4, Ahrefs/Semrush (keywords, competitors), Google Trends, AnswerThePublic, a spreadsheet.

## Core workflow
1. Pick true SERP competitors (who ranks for your target queries), not business rivals
2. Compare: keywords they win, top pages by traffic, content depth, backlinks, technical speed
3. Find gaps (they rank, you do not) and weaknesses (thin pages you can beat)
4. Choose angles you can defend with better data, UX, or expertise

## Decision rules and checks
- Pick 3-5 true SERP competitors
- Compare keywords, content, links, technical
- List gaps + defensible angles

## Edge cases and failure handling
- Comparing against giants -> include 2-3 sites of similar authority
- Copying topics blindly -> verify the intent matches your offer

## Validation
- Re-fetch or re-crawl changed URLs; confirm the fix is live (status, rendered HTML, canonical, schema validator, GSC URL Inspection as relevant).
- Compare with the baseline recorded before the change; check for regressions on neighbouring templates.

## Output requirements
Gap table: keyword/topic, competitor URL, your URL (or none), action. Report as a short DONE: what changed, evidence, remaining issues.

## Example
- Input/symptom: Comparing against giants
- Action: include 2-3 sites of similar authority
- Output: Gap table: keyword/topic, competitor URL, your URL (or none), action.

## Merged from (read for deep method)
- `../../_source/seo-competitor/SKILL.md`

## External sources merged (deep method)
- `../../_source/aaron__competitor-analysis/SKILL.md`

## References
`references/playbook.md`: detailed how-to, common problems and fixes, tools, verify steps. Read when executing.
