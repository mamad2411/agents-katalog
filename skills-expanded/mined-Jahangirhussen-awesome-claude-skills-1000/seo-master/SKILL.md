---
name: seo-master
description: Use automatically for ANY SEO-related request - audits, rankings, traffic drops, keywords, technical/on-page/off-page/content/local SEO, WordPress/WooCommerce/Shopify SEO, SaaS/ERP/POS SEO, programmatic, image, video, international, schema/structured data, AI search (GEO, AEO, ChatGPT/Claude/Gemini/Perplexity visibility), Search Console and analytics, migration, monitoring, automation. Autonomous router over 33 SEO categories (190+ skills); loads only the branch the task needs. Not for paid ads (use marketing skills) or general web development without an SEO goal.
---

# SEO Master

## Purpose
Single entry point for all SEO work. The user states the goal; this skill picks the category and child skills, runs the method, verifies, and reports. Nobody names a category or types a slash command.

## When to use
Any task about search visibility: why rankings or traffic dropped, what to rank for, technical crawl/index problems, page optimization, schema, local/e-commerce/platform SEO, AI-search citations, SEO migrations, reporting or automation.

## When NOT to use
- Paid search/social ads, email, social media management -> marketing skills.
- Pure development with no search goal -> development skills (SEO only as a dependency).
- Writing a non-SEO article with no ranking goal.

## Inputs
Site URL or repo, platform/CMS, target market and goal, and access to whatever exists: Search Console, GA4, crawl export, rank data. Infer the rest from the project; ask only if the site or goal cannot be found.

## Core workflow
1. Read `RULES.md`, then match the request in `ROUTER.md` (parent categories and combos).
2. Inspect the real site/project first (fetch pages, headers, robots, sitemap, rendered HTML, code).
3. Open only the matched parent `NN-*/SKILL.md`, then the one or two child skills needed (`REGISTRY.md` lists all). Open a child's `references/playbook.md` only when executing.
4. Follow `DEPENDENCIES.md` for cross-category links (e.g. WooCommerce product SEO -> technical, schema, image) only where needed.
5. Execute the smallest correct change set; platform skills (WordPress, WooCommerce, Shopify) override generic advice.
6. Verify, then report using `WORKFLOW.md`.

## Decision rules
- One clear skill -> use one. Several concerns -> chain in order: strategy -> technical -> platform -> on-page -> content -> schema -> off-page -> AI search -> analytics/monitoring.
- Broad request ("audit", "improve SEO") -> inspect first, then load only the modules the evidence points to; never load all 33.
- Prefer the most specific child (e.g. JavaScript SEO over general technical SEO).
- Merged external skills live in `_source/`; read one only when a child's "Merged from" says deeper method is needed.

## Edge cases and failure handling
- No Search Console/analytics access -> use crawl + SERP checks and state the limitation.
- Site blocked by login or robots -> test what is reachable, report what could not be verified.
- Conflicting platform plugins (two SEO plugins, duplicate schema) -> fix the conflict before optimizing.
- Large sites -> sample by template, fix patterns, not individual pages.

## Validation
Re-fetch changed URLs; check status, canonical, rendered HTML, schema validity, GSC URL Inspection where available; compare with the pre-change baseline; confirm no regressions on sibling templates.

## Output requirements
Short `DONE`: what changed, evidence, expected effect, remaining issues. White-hat only (no link schemes, fake reviews, cloaking). Never hard-code API keys.

## Example
Request: "WooCommerce products are not showing on Google." -> inspect product URLs (indexability, canonical, noindex, sitemap, schema) -> 09 WooCommerce -> 03 indexability -> 02 Search Console indexing -> 27 product schema -> fix -> re-inspect -> DONE listing the URLs now indexable.

## Related / dependencies
`ROUTER.md`, `REGISTRY.md`, `DEPENDENCIES.md`, `RULES.md`, `WORKFLOW.md`, `AUDIT.md`, `_source/` (merged original skills). Orchestrated by `master-auto-orchestrator`; analytics dashboards -> `erp-saas-analytics-visualization`.

## References
`NN-*/references/playbook.md` inside each skill; `CHANGELOG.md`.
