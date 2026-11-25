---
name: seo-05
description: 05. Off-Page SEO (SEO). Use when the request involves: backlinks, link building, digital pr, guest post, brand mentions, citations, link audit, toxic links, disavow. Not for topics owned by sibling SEO skills or other categories; routed by seo-master.
---

# 05. Off-Page SEO

ID: 05 | Level: parent | Parent: SEO Master

## Purpose
Authority via links and mentions. White-hat only.

## When to use
Triggers: backlinks, link building, digital pr, guest post, brand mentions, citations, link audit, toxic links, disavow

## When NOT to use
- The request belongs to another SEO category (see `../ROUTER.md`): e.g. core seo, google seo, technical seo, on page seo, content seo, local seo.
- A more specific child skill already covers it: open that child instead of repeating its work.

## Inputs
- Target site/URL(s) or project files, platform (CMS/framework), and goal.
- Data access as available: Ahrefs, Semrush, Majestic, Google Search Console Links report, Google Alerts, outreach CRM or spreadsheet.

## Core workflow
1. Profile existing links (Ahrefs/Semrush/GSC Links)
2. Compare against 3-5 competitors: referring domains, link types, top linked pages
3. Choose white-hat tactics fitting the brand: assets, PR, partnerships, mentions

## Decision rules
- Use evidence (crawl, GSC, rendered HTML, validators), not assumptions.
- Fix the highest-impact, lowest-risk items first; change only what the task needs.
- If a platform skill (WordPress, WooCommerce, Shopify) applies, its guidance overrides generic advice.

## Edge cases and failure handling
- Low-quality outreach -> target relevance and real traffic
- Risky past links -> audit before disavow

## Validation
- Re-fetch or re-crawl changed URLs; confirm the fix is live (status, rendered HTML, canonical, schema validator, GSC URL Inspection as relevant).
- Compare with the baseline recorded before the change; check for regressions on neighbouring templates.

## Output requirements
Link plan: targets, tactic, asset, owner. Report as a short DONE: what changed, evidence, remaining issues.

## Example
- Input/symptom: Low-quality outreach
- Action: target relevance and real traffic
- Output: Link plan: targets, tactic, asset, owner.

## Children
- [Link building](link-building/SKILL.md)
- [Backlink analysis](backlinks/SKILL.md)
- [Digital PR](digital-pr/SKILL.md)
- [Guest posting](guest-posting/SKILL.md)
- [Brand mentions and citations](brand-mentions/SKILL.md)
- [Link audit](link-audit/SKILL.md)

## Merged from (read for deep method)
- `../_source/seo-offpage/SKILL.md`

## References
`references/playbook.md`: detailed how-to, common problems and fixes, tools, verify steps. Read when executing.
