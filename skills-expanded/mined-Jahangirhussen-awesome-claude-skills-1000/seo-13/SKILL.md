---
name: seo-13
description: 13. ERP SEO (SEO). Use when the request involves: erp seo, accounting software, inventory software, hr payroll software, crm module, manufacturing software. Not for topics owned by sibling SEO skills or other categories; routed by seo-master.
---

# 13. ERP SEO

ID: 13 | Level: parent | Parent: SEO Master

## Purpose
Use 12-saas-seo children with ERP matrix: module x industry x integration x comparison.

## When to use
Triggers: erp seo, accounting software, inventory software, hr payroll software, crm module, manufacturing software

## When NOT to use
- The request belongs to another SEO category (see `../ROUTER.md`): e.g. core seo, google seo, technical seo, on page seo, off page seo, content seo.
- A more specific child skill already covers it: open that child instead of repeating its work.

## Inputs
- Target site/URL(s) or project files, platform (CMS/framework), and goal.
- Data access as available: Keyword tools by module and industry, GSC, competitor pages, CRM data (win/loss reasons), case studies.

## Core workflow
1. Create module pages: accounting, inventory, HR, payroll, CRM, purchase, sales, manufacturing
2. Create industry pages and integration pages
3. Add comparison/alternative pages vs competing ERPs
4. Add demo CTA, case studies, implementation guides

## Decision rules
- Use evidence (crawl, GSC, rendered HTML, validators), not assumptions.
- Fix the highest-impact, lowest-risk items first; change only what the task needs.
- If a platform skill (WordPress, WooCommerce, Shopify) applies, its guidance overrides generic advice.

## Edge cases and failure handling
- Too generic ERP copy -> segment by industry and module
- Long sales cycle -> content for research and evaluation stages

## Validation
- Re-fetch or re-crawl changed URLs; confirm the fix is live (status, rendered HTML, canonical, schema validator, GSC URL Inspection as relevant).
- Compare with the baseline recorded before the change; check for regressions on neighbouring templates.

## Output requirements
ERP page matrix: module x industry. Report as a short DONE: what changed, evidence, remaining issues.

## Example
- Input/symptom: Too generic ERP copy
- Action: segment by industry and module
- Output: ERP page matrix: module x industry.

## Topics handled here (no separate child)
- Modules: accounting, inventory, HR, payroll, CRM, purchase, sales, manufacturing - one page each
- Industry pages: module x industry combos with real differentiation
- Long sales cycle: target research + comparison + implementation keywords; demo CTA, case studies

## Related installed skills (kept in place; invoke only if needed)
- `competitor-alternatives`
- `programmatic-seo`

## References
`references/playbook.md`: detailed how-to, common problems and fixes, tools, verify steps. Read when executing.
