---
name: seo-03
description: 03. Technical SEO (SEO). Use when the request involves: technical seo, crawl, index, robots, canonical, sitemap, redirect, javascript seo, core web vitals, lcp, inp, cls, page speed, https, mobile, site architecture, seo technical audit. Not for topics owned by sibling SEO skills or other categories; routed by seo-master.
---

# 03. Technical SEO

ID: 03 | Level: parent | Parent: SEO Master

## Purpose
Crawlability, indexability, rendering, speed, security, architecture.

## When to use
Triggers: technical seo, crawl, index, robots, canonical, sitemap, redirect, javascript seo, core web vitals, lcp, inp, cls, page speed, https, mobile, site architecture, seo technical audit

## When NOT to use
- The request belongs to another SEO category (see `../ROUTER.md`): e.g. core seo, google seo, on page seo, off page seo, content seo, local seo.
- A more specific child skill already covers it: open that child instead of repeating its work.

## Inputs
- Target site/URL(s) or project files, platform (CMS/framework), and goal.
- Data access as available: Screaming Frog or Sitebulb, Google Search Console, Lighthouse, PageSpeed Insights, CrUX, WebPageTest, curl -I, server logs.

## Core workflow
1. Crawl with Screaming Frog/Sitebulb or a script: status codes, canonicals, noindex, titles, depth
2. Compare against GSC indexing and sitemap lists
3. Test rendered HTML for JS sites (URL Inspection live test)
4. Run Lighthouse/PageSpeed and CrUX for CWV

## Decision rules
- Use evidence (crawl, GSC, rendered HTML, validators), not assumptions.
- Fix the highest-impact, lowest-risk items first; change only what the task needs.
- If a platform skill (WordPress, WooCommerce, Shopify) applies, its guidance overrides generic advice.

## Edge cases and failure handling
- Crawler finds 5xx -> server/log review first
- Mixed signals (canonical vs sitemap vs internal links) -> make all three agree

## Validation
- Re-fetch or re-crawl changed URLs; confirm the fix is live (status, rendered HTML, canonical, schema validator, GSC URL Inspection as relevant).
- Compare with the baseline recorded before the change; check for regressions on neighbouring templates.

## Output requirements
Technical issue list ranked by SEO impact with URLs and fix. Report as a short DONE: what changed, evidence, remaining issues.

## Example
- Input/symptom: Crawler finds 5xx
- Action: server/log review first
- Output: Technical issue list ranked by SEO impact with URLs and fix.

## Children
- [Crawlability](crawlability/SKILL.md)
- [Indexability](indexability/SKILL.md)
- [Canonicals](canonical/SKILL.md)
- [robots.txt](robots/SKILL.md)
- [XML sitemaps](sitemap/SKILL.md)
- [Redirects and status codes](redirects/SKILL.md)
- [JavaScript and rendering SEO](javascript-seo/SKILL.md)
- [Core Web Vitals and speed](core-web-vitals/SKILL.md)
- [Mobile SEO](mobile-seo/SKILL.md)
- [HTTPS and security headers](https/SKILL.md)
- [Website architecture](website-architecture/SKILL.md)

## Merged from (read for deep method)
- `../_source/seo-technical/SKILL.md`

## Related installed skills (kept in place; invoke only if needed)
- `site-architecture`
- `performance-optimization`

## External sources merged (deep method)
- `../_source/aaron__technical-seo-checker/SKILL.md`

## References
`references/playbook.md`: detailed how-to, common problems and fixes, tools, verify steps. Read when executing.
