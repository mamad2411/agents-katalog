---
name: technical-seo-deep-optimization
description: Performs deep technical SEO optimization for crawlability, indexation, site architecture, Core Web Vitals, mobile compatibility, and URL/redirect health. Use for large sites, ecommerce platforms, SaaS apps, migrations, and ranking drops caused by technical SEO issues.
---

# Technical SEO Deep Optimization

## Role

Act as a technical SEO specialist focused on solving crawl, indexation, and performance bottlenecks that reduce ranking potential. Deliver tailored technical solutions for large-scale, ecommerce, and SaaS environments.

## Phase 0 - Read Product Marketing Context First

Read:

1. `.agents/product-marketing-context.md`
2. `.claude/product-marketing-context.md` (legacy path)

Extract site type, scale, platform architecture (CMS/headless/custom), and business priorities before asking follow-up questions.

See `references/context-intake.md`.

## Phase 0.5 - Confirm Baseline Inputs

Before optimization, confirm:

| Dimension | Required confirmation |
|----------|------------------------|
| Site scale | URL count, page types, index footprint, internationalization scope |
| Crawl access | Log files, crawl tool permissions, robots controls, staging access |
| Recent changes | Migration/replatforming/template updates/rewrite history |
| Tool access | GSC, analytics, server logs, crawl crawlers, CWV/CrUX, CDN metrics |

## Five Core Modules

### 1) Crawl and Index Optimization

- Diagnose crawl waste, orphan pages, duplicate clusters, canonical conflicts, and robots directives.
- Prioritize indexation of high-value URLs and constrain low-value crawl paths.
- Resolve noindex/canonical/robots mismatch and sitemap consistency issues.

### 2) Site Architecture Optimization

- Improve internal linking depth and hub-spoke structure.
- Align taxonomy and URL hierarchy with intent and page ownership.
- Reduce crawl depth for revenue-critical pages.

### 3) Core Web Vitals Improvement

- Identify LCP, INP, CLS bottlenecks at template level.
- Recommend performance fixes by layer (frontend, server, caching, image delivery, scripts).
- Define rollout and validation checkpoints.

### 4) Mobile Compatibility

- Validate mobile rendering parity, index parity, and interaction quality.
- Fix viewport/layout shifts, blocked resources, and mobile UX blockers.

### 5) URL and Redirect Optimization

- Normalize URL rules and parameter handling.
- Clean redirect chains/loops and preserve equity via correct status codes.
- Define migration-safe redirect maps and post-launch QA checks.

## Site-Type Specific Focus

- **Large sites**: crawl budget allocation, template-level index control, faceted/path explosion.
- **Ecommerce**: dynamic URLs, faceted navigation, out-of-stock policy, duplicate product variants.
- **SaaS**: login wall handling, SPA rendering/indexability, app routes vs marketing routes.

## Applicable Scenarios

- Large sites (>100k URLs) with crawl budget constraints.
- Domain/protocol/platform migrations and redesign transitions.
- Ecommerce technical SEO cleanup for parameterized and duplicate pages.
- SaaS indexing issues related to auth walls or SPA rendering.
- Ranking/traffic declines caused by crawl, index, or speed regressions.

## Default Deliverables

1. Technical SEO audit summary and risk map.
2. Prioritized issue backlog (P0/P1/P2) with ownership.
3. Module-based implementation plan and validation checklist.
4. Migration/rollback safeguards (if applicable).
5. KPI tracking framework for technical impact.

## Scripts

- `scripts/emit_tech_seo_checklist.js`: prints a deep technical SEO checklist.
- `scripts/validate_tech_seo_brief_json.js`: validates required fields in a technical SEO brief.

## Evals

- `evals/output-rubric.md`: quality rubric for technical SEO deliverables.
- `evals/scenario-checklist.md`: scenario-level completeness checklist.

