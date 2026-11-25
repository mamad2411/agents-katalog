---
name: seo-29-backlink-tools
description: Backlink tools (SEO). Use when the request involves: ahrefs backlinks, semrush backlinks. Not for topics owned by sibling SEO skills or other categories; routed by seo-master.
---

# Backlink tools

ID: 29.02 | Level: child | Parent: [SEO Tools and APIs](../SKILL.md)

## Purpose
Backlink tools within the seo-master tree: Backlink export.

## When to use
Triggers: ahrefs backlinks, semrush backlinks

## When NOT to use
- The topic is covered by a sibling skill: `../data-collection`, `../keyword-tools`, `../scraping`, `../seo-apis`.
- The task is outside this SEO category; see `ROUTER.md` at the seo-master root.

## Inputs
- Target site/URL(s) or project files, platform (CMS/framework), and goal.
- Data access as available: GSC API, GA4 Data API, PageSpeed Insights API, DataForSEO, Ahrefs/Semrush APIs, Python or Node scripts.

## Core workflow
1. Use Ahrefs/Semrush/Majestic or GSC Links
2. Export referring domains and anchors
3. Check lost/new links

## Decision rules and checks
- Use MCP/API if connected

## Edge cases and failure handling
- Tool index gaps -> combine sources

## Validation
- Re-fetch or re-crawl changed URLs; confirm the fix is live (status, rendered HTML, canonical, schema validator, GSC URL Inspection as relevant).
- Compare with the baseline recorded before the change; check for regressions on neighbouring templates.

## Output requirements
Backlink export. Report as a short DONE: what changed, evidence, remaining issues.

## Example
- Input/symptom: Tool index gaps
- Action: combine sources
- Output: Backlink export.

## References
`references/playbook.md`: detailed how-to, common problems and fixes, tools, verify steps. Read when executing.
