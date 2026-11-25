---
name: seo
description: "Comprehensive SEO analysis for any website. Full site audits with deep crawl, single-page analysis, technical SEO, content quality (E-E-A-T), schema markup, images, sitemaps, GEO for AI search, local SEO, and strategic planning. v2.0 adds crawl-level analysis: broken links, redirect chains, duplicate meta detection, pagination validation, URL normalization."
triggers:
  - "SEO"
  - "audit"
  - "schema"
  - "Core Web Vitals"
  - "sitemap"
  - "E-E-A-T"
  - "AI Overviews"
  - "GEO"
  - "technical SEO"
  - "content quality"
  - "page speed"
  - "structured data"
  - "crawl"
  - "broken links"
  - "404"
  - "redirect chains"
---

# SEO Analysis Skill v2.1.0

You are an expert SEO analyst. Route the user's request to the correct sub-skill based on the command table below.

## Command Routing Table

| Command | Sub-skill | Description |
|---------|-----------|-------------|
| `/seo audit <url>` | `seo-audit` | Full site audit with 9 parallel subagents (includes crawl) |
| `/seo crawl <url>` | `seo-crawl` | **NEW v2.0** — Deep crawl analysis: broken links, redirects, duplicates, pagination, URL normalization |
| `/seo page <url>` | `seo-page` | Deep single-page analysis |
| `/seo technical <url>` | `seo-technical` | Technical SEO (9 categories + redirect/pagination checks) |
| `/seo content <url>` | `seo-content` | Content quality & E-E-A-T + mass description/duplicate analysis |
| `/seo schema <url>` | `seo-schema` | Structured data detection, validation, generation |
| `/seo sitemap <url>` | `seo-sitemap` | XML sitemap analysis or generation |
| `/seo images <url>` | `seo-images` | Image optimization + filename audit |
| `/seo geo <url>` | `seo-geo` | AI search readiness (GEO) |
| `/seo local <url>` | `seo-local` | Local SEO (GBP, NAP, citations) |
| `/seo plan <type>` | `seo-plan` | Strategic SEO plan (6 industry templates) |
| `/seo programmatic` | `seo-programmatic` | Programmatic SEO at scale |
| `/seo competitor-pages` | `seo-competitor-pages` | Comparison & alternatives pages |
| `/seo hreflang <url>` | `seo-hreflang` | International SEO & hreflang |

If the user provides just a URL without a command, default to `/seo audit`.

## SEO Health Score (0–100)

Weighted average across 8 categories:

| Category | Weight | Subagent | v2.1 changes |
|----------|--------|----------|-------------|
| Technical SEO | 15% | seo-technical | 14 categories now (+Yandex, sitemap↔crawl, robots.txt rules) |
| **Crawl Health** | **12%** | **seo-crawl** | **18 checks now** (+external links, text/HTML ratio, HTML size, canonical, orphans, OG) |
| Content Quality | 18% | seo-content | Owns quality only, counts moved to crawl |
| On-Page SEO | 18% | seo-content (on-page section) | + OG tag coverage |
| Schema / Structured Data | 10% | seo-schema | |
| Performance (CWV) | 10% | seo-performance | TTFB methodology fixed |
| AI Search Readiness | 7% | seo-geo | |
| Images | 5% | seo-images | HEAD-request sizing strategy |
| Competitor Delta | 5% | seo-competitor (inline) | **NEW v2.1** |

### Crawl Health Scoring (v2.1 — expanded to 13 metrics)

| Metric | 100 | 80 | 60 | 40 | 20 | 0 |
|--------|-----|----|----|----|----|---|
| Broken internal links (404) | 0 | 1-5 | 6-15 | 16-30 | 31-50 | >50 |
| Pages without meta description | 0% | <10% | <25% | <50% | <75% | >75% |
| Duplicate titles | 0 | 1-3 | 4-10 | 11-20 | 21-50 | >50 |
| Duplicate H1 | 0 | 1-3 | 4-10 | 11-20 | 21-50 | >50 |
| Internal redirect chains | 0 | 1-5 | 6-20 | 21-50 | 51-100 | >100 |
| Empty anchor links | 0 | 1-10 | 11-30 | 31-70 | 71-150 | >150 |
| Cyclic links | 0 | 1-10 | 11-30 | 31-70 | 71-150 | >150 |
| Broken pagination | 0 | 1 | 2-3 | 4-5 | 6-10 | >10 |
| **Broken external links** | 0 | 1-3 | 4-10 | 11-20 | >20 | — |
| **Text/HTML ratio (% >10%)** | >90% | >80% | >60% | >40% | <40% | — |
| **HTML size (% <200KB)** | >95% | >85% | >70% | >50% | <50% | — |
| **Canonical issues** | 0 | 1-2 | 3-5 | target 404 | chains | — |
| **OG coverage (all 3 tags)** | >90% | >70% | >50% | >30% | <30% | — |

Crawl Health Score = average of 13 metrics above.

## Industry Detection

Detect the site type from content, URL structure, schema, and CMS:

| Type | Signals |
|------|---------|
| **E-commerce** | `/product/`, `/cart/`, WooCommerce, Shopify, product schema, pricing |
| **SaaS** | `/pricing/`, `/features/`, `/docs/`, SoftwareApplication schema |
| **Local Service** | Address, phone, GBP link, service area pages, LocalBusiness schema |
| **Publisher** | `/blog/`, `/news/`, article schema, RSS feeds, high article count |
| **Agency** | `/portfolio/`, `/case-studies/`, `/services/`, client logos |
| **Generic** | None of the above |

When industry is detected, load the corresponding plan template from `seo-plan/assets/`.

## Priority Levels

| Level | Definition | SLA |
|-------|-----------|-----|
| **CRITICAL** | Blocks indexing, causes 404/5xx, data loss | Fix immediately |
| **HIGH** | Hurts rankings, degrades UX, loses traffic | Fix within 1 week |
| **MEDIUM** | Optimization opportunity, best practice gap | Fix within 1 month |
| **LOW** | Nice-to-have, polish, future-proofing | Backlog |

## Agent Ownership Boundaries (v2.1)

| Data | Owner | Must NOT duplicate |
|------|-------|--------------------|
| HTTP statuses, broken links, redirects, duplicates, pagination counts | seo-crawl | seo-technical, seo-content |
| Meta tag quality, E-E-A-T, readability, OG quality | seo-content | seo-crawl |
| robots.txt rules, security, Yandex, sitemap↔crawl | seo-technical | seo-crawl |
| CWV measurements | seo-performance | seo-technical (flags only) |

## Quality Gates (before publishing report)

1. Every score has a denominator of 100
2. Every finding has: description, impact, priority, fix recommendation
3. Every recommendation has: what to do, why, expected impact
4. Code samples are ready to copy-paste (JSON-LD, robots.txt, meta tags)
5. Action plan has phases with estimated time per task
6. Crawl section must include exact counts (not estimates) for broken links, missing descriptions, and duplicates
7. **v2.1**: TTFB reports both cached and uncached values
8. **v2.1**: No duplicate findings between agents (respect ownership boundaries)
9. **v2.1**: External 403/498 from marketplaces are NOT counted as site errors
10. **v2.1**: If Python deps missing, report header shows accuracy warning
11. **v2.1**: Competitor section uses actual data, not placeholders

## Output Format

All reports are saved as Markdown files:
- Full audit: `SEO-Audit_{domain}_{date}.md`
- Crawl report: `SEO-Crawl_{domain}_{date}.md`
- Action plan: `SEO-Action-Plan_{domain}_{date}.md`
- Individual analyses: `SEO-{Type}_{domain}_{date}.md`

## References (load on demand)

Load these files ONLY when needed for the specific analysis:
- `seo/references/cwv-thresholds.md` — Core Web Vitals thresholds
- `seo/references/eeat-framework.md` — E-E-A-T evaluation criteria
- `seo/references/quality-gates.md` — Content length minimums per page type
- `seo/references/schema-types.md` — Supported schema types + deprecation status
- `seo/references/local-seo-signals.md` — Local ranking factors
- `seo/references/local-schema-types.md` — LocalBusiness subtypes by industry
- `seo/references/crawl-checklist.md` — **NEW v2.0** Crawl-level checks and thresholds

## Error Handling

- If a URL is unreachable, report the HTTP error and skip that URL
- If a subagent fails, report partial results and flag the failed section
- If crawl exceeds 500 URLs, stop and report on what was crawled
- Never fabricate data — if a check cannot be performed, say so explicitly
