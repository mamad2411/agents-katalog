---
name: seo-audit
description: "Full website SEO audit with 10 parallel subagents including deep crawl. v2.1: clear agent ownership, external links, text/HTML ratio, HTML size, canonical validation, robots.txt rule testing, Yandex checks, sitemap↔crawl cross-ref, competitor quick-glance, TTFB methodology fix, dependency checks."
triggers:
  - "audit"
  - "full SEO check"
  - "analyze my site"
  - "website health check"
  - "SEO audit"
---

# Full SEO Audit — v2.1

You are the audit orchestrator. Your job is to run a comprehensive SEO audit by delegating to 9 specialized subagents in parallel, then synthesizing their results into a unified report.

## Input

```
/seo audit <url> [--max-pages=500] [--skip-visual] [--skip-crawl]
```

## Process

### Phase 0: Dependency Check (NEW v2.1)

Before starting, verify Python dependencies:
```bash
python3 -c "import requests; from bs4 import BeautifulSoup; print('deps OK')" 2>&1
```

If dependencies are missing:
- Try: `pip install requests beautifulsoup4 lxml`
- If pip fails: proceed with **manual crawl mode** and add warning to report header:
  > ⚠️ Python dependencies unavailable — crawl data is approximate. Install `requests beautifulsoup4 lxml` for exact counts.

### Phase 1: Initial Discovery (sequential)

1. Fetch the homepage at `<url>`
2. Detect industry type (e-commerce, SaaS, local, publisher, agency, generic)
3. Detect CMS (WordPress, Shopify, Wix, custom, etc.)
4. Fetch robots.txt and sitemap.xml
5. Count approximate page count from sitemap
6. **NEW v2.1**: Identify top 3 competitors from:
   - Similar businesses found in search results for primary keywords
   - Competitors mentioned on the site itself
   - Known industry players for the detected business type

### Phase 2: Parallel Subagent Delegation

Launch **10 subagents** simultaneously (9 if `--skip-crawl`, 8 if also `--skip-visual`):

```
Agent 1:  seo-technical    → Technical SEO (14 categories: crawlability, robots.txt rules, security, mobile, CWV, JS, IndexNow, Yandex, sitemap↔crawl)
Agent 2:  seo-crawl        → Crawl Health (18 checks: broken links, redirects, duplicates, pagination, external links, text/HTML ratio, HTML size, canonical, orphans, OG tags)
Agent 3:  seo-content      → Content Quality (E-E-A-T, readability, thin content, meta tag quality, OG audit, content freshness)
Agent 4:  seo-schema       → Structured Data (detection, validation, generation recommendations)
Agent 5:  seo-sitemap      → Sitemap (structure, coverage, quality gates)
Agent 6:  seo-performance  → Core Web Vitals (LCP, INP, CLS, TTFB cached+uncached)
Agent 7:  seo-geo          → AI Search Readiness (llms.txt, AI crawlers, citability)
Agent 8:  seo-visual       → Visual Analysis (screenshots, above-fold, mobile rendering)
Agent 9:  seo-local        → Local SEO (only if local business detected in Phase 1)
Agent 10: seo-competitor   → NEW v2.1: Competitor Quick Glance (top 3 competitors, key metrics comparison)
```

### Agent Ownership Boundaries (NEW v2.1)

| Data type | Owner agent | Other agents must NOT duplicate |
|-----------|-------------|-------------------------------|
| HTTP status codes, broken links | seo-crawl | seo-technical |
| Meta tag counts & duplicates | seo-crawl | seo-content |
| Redirect chains & counts | seo-crawl | seo-technical |
| Pagination URL validation | seo-crawl | seo-technical |
| URL normalization counts | seo-crawl | seo-technical |
| robots.txt rule analysis | seo-technical | seo-crawl |
| Security headers | seo-technical | — |
| CWV measurements | seo-performance | seo-technical (only flags) |
| E-E-A-T assessment | seo-content | — |
| Meta tag quality & templates | seo-content | — |

Each agent receives:
- The URL
- Industry type
- CMS type
- robots.txt content
- Sitemap URL list (first 50 URLs)

### Phase 3: Synthesis

Collect all subagent results and produce the unified report.

#### Scoring

Calculate the SEO Health Score using v2.1 weights:

```
Health Score = (
    technical_score * 0.15 +
    crawl_score * 0.12 +
    content_score * 0.18 +
    onpage_score * 0.18 +
    schema_score * 0.10 +
    performance_score * 0.10 +
    geo_score * 0.07 +
    images_score * 0.05 +
    competitor_delta * 0.05
)
```

**v2.1 changes**: Crawl weight increased 8%→12% (it now covers 18 checks). Technical reduced 17%→15%. Content/On-Page reduced 20%→18% each. GEO reduced 10%→7%. Added 5% for competitor delta.

If local business → replace `geo_score * 0.07` with `(geo_score * 0.03 + local_score * 0.04)`.

#### Priority Consolidation

Merge all findings from all subagents into a single prioritized list:
1. CRITICAL — from any subagent
2. HIGH — from any subagent
3. MEDIUM — from any subagent
4. LOW — from any subagent

De-duplicate findings that appear in multiple subagents (e.g., broken links may appear in both seo-technical and seo-crawl).

### Phase 4: Report Generation

Save two files:

#### File 1: `SEO-Audit_{domain}_{date}.md`

```markdown
# SEO Audit Report: {domain}

> **Date:** {date}
> **Score:** {score}/100
> **Industry:** {type}
> **CMS:** {cms}
> **Pages crawled:** {N}

## Executive Summary
{2-3 sentences: overall health, biggest wins, critical issues}

## Score Breakdown
| Category | Score | Weight | Weighted |
|----------|-------|--------|----------|
| Technical SEO | {}/100 | 15% | {} |
| Crawl Health | {}/100 | 12% | {} |
| Content Quality | {}/100 | 18% | {} |
| On-Page SEO | {}/100 | 18% | {} |
| Schema | {}/100 | 10% | {} |
| Performance | {}/100 | 10% | {} |
| AI Search | {}/100 | 7% | {} |
| Images | {}/100 | 5% | {} |
| Competitor Delta | {}/100 | 5% | {} |
| **Total** | | | **{}/100** |

## Critical Issues ({N})
{list with fix recommendations}

## High Priority ({N})
{list}

## Medium Priority ({N})
{list}

## Low Priority ({N})
{list}

## 1. Technical SEO
{subagent report}

## 2. Crawl Health (18 checks — v2.1)
{subagent report — must include exact counts:}
- Broken internal links: {N} (top 5 with inlink counts)
- Broken external links: {N} (excluding bot-blocks) — NEW v2.1
- Missing descriptions: {N}/{total} ({%})
- Duplicate titles: {N} groups
- Duplicate H1: {N} groups
- Redirect chains: {N}
- Empty anchors: {N}
- Cyclic links: {N}
- Broken pagination: {list}
- URL issues: {N} uppercase, {N} cyrillic, {N} encoded
- Text/HTML ratio: {N} pages below 10% — NEW v2.1
- Large HTML: {N} pages over 200KB — NEW v2.1
- Canonical issues: {N} — NEW v2.1
- Orphan pages: {N} — NEW v2.1
- OG tag coverage: {X}% — NEW v2.1

## 3. Content Quality & E-E-A-T
{subagent report}

## 4. On-Page SEO
{subagent report}

## 5. Schema / Structured Data
{subagent report + ready-to-use JSON-LD code}

## 6. Performance (Core Web Vitals)
{subagent report}

## 7. AI Search Readiness (GEO)
{subagent report}

## 8. Images
{subagent report}

## 9. Sitemap
{subagent report}

## 10. Local SEO (if applicable)
{subagent report}

## 11. Competitor Quick Glance (NEW v2.1)
{top 3 competitors — for each:}
- Domain authority / visibility estimate
- Schema types implemented
- Content volume (blog posts, product count if e-commerce)
- CWV status (from CrUX or PageSpeed Insights)
- Key differentiators (what they do that this site doesn't)
- Competitor Delta Score: how far behind/ahead on the 5 biggest gaps

## 12. Yandex-Specific (NEW v2.1, if RU-market)
{Yandex verification, Metrika, turbo pages, product feed, Host directive}
```

#### File 2: `SEO-Action-Plan_{domain}_{date}.md`

```markdown
# SEO Action Plan: {domain}

## Phase 0: Emergency Fixes (Day 1)
{CRITICAL items only — broken links, 404 redirects, missing descriptions}

## Phase 1: Foundation (Week 1-2)
{HIGH items — schema, robots.txt, sitemap cleanup, redirect chains}

## Phase 2: Growth (Week 3-6)
{MEDIUM items — content, images, CWV optimization}

## Phase 3: Authority (Month 2-3)
{LOW items + content strategy + link building}

## Expected Impact
| Metric | Current | After Phase 1 | After Phase 2 | After Phase 3 |
|--------|---------|--------------|--------------|--------------|
| SEO Score | {}/100 | ~{}/100 | ~{}/100 | ~{}/100 |
| Indexed pages | {} | {} | {} | {} |
| Estimated organic traffic | {} | {} | {} | {} |
```

## Quality Gate Checklist (before saving report)

- [ ] Every score is 0-100
- [ ] Crawl section has exact counts (not estimates like "~50")
- [ ] Every CRITICAL issue has a specific fix with code/config example
- [ ] JSON-LD code is valid and ready to paste
- [ ] No fabricated data — if a check failed, say "could not check"
- [ ] Action plan has time estimates per task
- [ ] Report uses the site's actual data, not generic advice
- [ ] **v2.1**: TTFB reports both cached and uncached values
- [ ] **v2.1**: No duplicate findings between seo-crawl and seo-technical/seo-content
- [ ] **v2.1**: External link 403/498 from marketplaces are NOT counted as site errors
- [ ] **v2.1**: If manual crawl used, report header has accuracy warning
- [ ] **v2.1**: Competitor section has actual data, not placeholder text
