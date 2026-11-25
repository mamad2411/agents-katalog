---
name: seo-02-indexing
description: Google indexing (SEO). Use when the request involves: not indexed, crawled currently not indexed, discovered not indexed, index coverage. Not for topics owned by sibling SEO skills or other categories; routed by seo-master.
---

# Google indexing

ID: 02.02 | Level: child | Parent: [Google SEO](../SKILL.md)

## Purpose
Google indexing within the seo-master tree: Per-URL status, cause, fix, re-check date.

## When to use
Triggers: not indexed, crawled currently not indexed, discovered not indexed, index coverage

## When NOT to use
- The topic is covered by a sibling skill: `../core-updates`, `../search-console`.
- The task is outside this SEO category; see `ROUTER.md` at the seo-master root.

## Inputs
- Target site/URL(s) or project files, platform (CMS/framework), and goal.
- Data access as available: Google Search Console (+API), GA4, URL Inspection tool, Search Status Dashboard, Looker Studio.

## Core workflow
1. Open URL Inspection for the URL: crawl, index, canonical (Google-selected vs user-declared)
2. Map status to cause: 'Discovered not indexed' (crawl/quality), 'Crawled not indexed' (quality/duplicate), 'Blocked by robots', 'Alternate with canonical'
3. Fix cause, then Request Indexing for a few key URLs only

## Decision rules and checks
- Read exact GSC status for the URL
- Check noindex, canonical, robots, soft-404, duplicate
- Improve internal links + content value
- Request indexing only after the fix

## Edge cases and failure handling
- Crawled-not-indexed at scale -> improve unique value, internal links, prune thin pages
- Google picks different canonical -> align content, canonicals, internal links, sitemap

## Validation
- Re-fetch or re-crawl changed URLs; confirm the fix is live (status, rendered HTML, canonical, schema validator, GSC URL Inspection as relevant).
- Compare with the baseline recorded before the change; check for regressions on neighbouring templates.

## Output requirements
Per-URL status, cause, fix, re-check date. Report as a short DONE: what changed, evidence, remaining issues.

## Example
- Input/symptom: Crawled-not-indexed at scale
- Action: improve unique value, internal links, prune thin pages
- Output: Per-URL status, cause, fix, re-check date.

## Dependencies (load only if needed)
- 03-technical-seo/indexability

## References
`references/playbook.md`: detailed how-to, common problems and fixes, tools, verify steps. Read when executing.
