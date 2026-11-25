---
name: seo-03-indexability
description: Indexability (SEO). Use when the request involves: noindex, index bloat, orphan page, duplicate url, thin page. Not for topics owned by sibling SEO skills or other categories; routed by seo-master.
---

# Indexability

ID: 03.02 | Level: child | Parent: [Technical SEO](../SKILL.md)

## Purpose
Indexability within the seo-master tree: Indexability matrix: URL group, intended, actual, fix.

## When to use
Triggers: noindex, index bloat, orphan page, duplicate url, thin page

## When NOT to use
- The topic is covered by a sibling skill: `../canonical`, `../core-web-vitals`, `../crawlability`, `../https`, `../javascript-seo`.
- The task is outside this SEO category; see `ROUTER.md` at the seo-master root.

## Inputs
- Target site/URL(s) or project files, platform (CMS/framework), and goal.
- Data access as available: Screaming Frog or Sitebulb, Google Search Console, Lighthouse, PageSpeed Insights, CrUX, WebPageTest, curl -I, server logs.

## Core workflow
1. List indexable URLs (200, no noindex, self-canonical) vs sitemap vs GSC indexed
2. Find accidental noindex (meta, X-Robots-Tag, staging leftovers)
3. Orphans: pages with no internal links (compare crawl to sitemap/GSC)
4. Consolidate duplicates; remove or noindex low-value URLs

## Decision rules and checks
- Compare indexed vs intended pages
- Find accidental noindex / X-Robots-Tag
- Orphans: add internal links or remove
- Consolidate duplicates

## Edge cases and failure handling
- Important page noindexed -> remove directive, resubmit
- Index bloat from tags/params -> noindex + remove from sitemap

## Validation
- Re-fetch or re-crawl changed URLs; confirm the fix is live (status, rendered HTML, canonical, schema validator, GSC URL Inspection as relevant).
- Compare with the baseline recorded before the change; check for regressions on neighbouring templates.

## Output requirements
Indexability matrix: URL group, intended, actual, fix. Report as a short DONE: what changed, evidence, remaining issues.

## Example
- Input/symptom: Important page noindexed
- Action: remove directive, resubmit
- Output: Indexability matrix: URL group, intended, actual, fix.

## References
`references/playbook.md`: detailed how-to, common problems and fixes, tools, verify steps. Read when executing.
