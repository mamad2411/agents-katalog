---
name: seo-28
description: 28. SEO Analytics (SEO). Use when the request involves: seo analytics, ga4, search console data, seo reporting, keyword tracking, organic traffic analysis. Not for topics owned by sibling SEO skills or other categories; routed by seo-master.
---

# 28. SEO Analytics

ID: 28 | Level: parent | Parent: SEO Master

## Purpose
Measure and report.

## When to use
Triggers: seo analytics, ga4, search console data, seo reporting, keyword tracking, organic traffic analysis

## When NOT to use
- The request belongs to another SEO category (see `../ROUTER.md`): e.g. core seo, google seo, technical seo, on page seo, off page seo, content seo.
- A more specific child skill already covers it: open that child instead of repeating its work.

## Inputs
- Target site/URL(s) or project files, platform (CMS/framework), and goal.
- Data access as available: GA4, Google Search Console, Looker Studio, GTM, BigQuery export, spreadsheet.

## Core workflow
1. Verify GA4 and GSC tracking
2. Segment organic by landing page, brand vs non-brand, device
3. Report trends with annotations (releases, updates)

## Decision rules
- Use evidence (crawl, GSC, rendered HTML, validators), not assumptions.
- Fix the highest-impact, lowest-risk items first; change only what the task needs.
- If a platform skill (WordPress, WooCommerce, Shopify) applies, its guidance overrides generic advice.

## Edge cases and failure handling
- Unattributed traffic -> UTM/consent issues

## Validation
- Re-fetch or re-crawl changed URLs; confirm the fix is live (status, rendered HTML, canonical, schema validator, GSC URL Inspection as relevant).
- Compare with the baseline recorded before the change; check for regressions on neighbouring templates.

## Output requirements
SEO report template. Report as a short DONE: what changed, evidence, remaining issues.

## Example
- Input/symptom: Unattributed traffic
- Action: UTM/consent issues
- Output: SEO report template.

## Children
- [GA4](google-analytics/SKILL.md)
- [Search Console analysis](search-console/SKILL.md)
- [SEO reporting](seo-reporting/SKILL.md)
- [Keyword tracking](keyword-tracking/SKILL.md)
- [Performance analysis](performance-analysis/SKILL.md)

## Topics handled here (no separate child)
- GTM/GA4: verify tracking before analysis; segment brand vs non-brand

## Related installed skills (kept in place; invoke only if needed)
- `analytics-tracking`
- `metrics-dashboard`

## References
`references/playbook.md`: detailed how-to, common problems and fixes, tools, verify steps. Read when executing.
