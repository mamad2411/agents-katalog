---
name: seo-04-internal-linking
description: Internal linking (SEO). Use when the request involves: internal links, anchor text, orphan pages, link equity. Not for topics owned by sibling SEO skills or other categories; routed by seo-master.
---

# Internal linking

ID: 04.05 | Level: child | Parent: [On-Page SEO](../SKILL.md)

## Purpose
Internal linking within the seo-master tree: Link plan: source URL, target URL, anchor.

## When to use
Triggers: internal links, anchor text, orphan pages, link equity

## When NOT to use
- The topic is covered by a sibling skill: `../content-optimization`, `../entity-optimization`, `../headings`, `../meta-descriptions`, `../title-tags`.
- The task is outside this SEO category; see `ROUTER.md` at the seo-master root.

## Inputs
- Target site/URL(s) or project files, platform (CMS/framework), and goal.
- Data access as available: Screaming Frog (titles/meta/H1), Google Search Console, SERP checks, SEO plugin or CMS fields, a text diff tool.

## Core workflow
1. Crawl link graph; find orphans and pages with few inlinks
2. Link from high-authority, relevant pages to priority pages with descriptive anchors
3. Add contextual links in body, hubs, related blocks; fix broken internal links
4. Avoid sitewide footers/nav as the only links

## Decision rules and checks
- Link to money pages from relevant content
- Descriptive anchors
- Fix orphans; limit sitewide noise

## Edge cases and failure handling
- Generic anchors ('click here') -> descriptive
- Too many links per page -> prioritize relevance

## Validation
- Re-fetch or re-crawl changed URLs; confirm the fix is live (status, rendered HTML, canonical, schema validator, GSC URL Inspection as relevant).
- Compare with the baseline recorded before the change; check for regressions on neighbouring templates.

## Output requirements
Link plan: source URL, target URL, anchor. Report as a short DONE: what changed, evidence, remaining issues.

## Example
- Input/symptom: Generic anchors ('click here')
- Action: descriptive
- Output: Link plan: source URL, target URL, anchor.

## Dependencies (load only if needed)
- internal-link-builder (installed skill)

## External sources merged (deep method)
- `../../_source/aaron__internal-linking-optimizer/SKILL.md`

## References
`references/playbook.md`: detailed how-to, common problems and fixes, tools, verify steps. Read when executing.
