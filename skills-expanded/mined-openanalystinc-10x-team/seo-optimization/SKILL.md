---
name: seo-optimization
description: SEO audits, keyword research with ReviewWeb.site API (keyword ideas, difficulty, traffic, backlinks), on-page optimization, technical SEO, programmatic SEO (pSEO), JSON+LD schema, Google Search Console API integration. Activate for search optimization, meta tags, sitemap, Core Web Vitals. Used by seo-specialist, attraction-specialist, content-creator agents.
license: MIT
---

# SEO Optimization

Technical SEO, keyword research (ReviewWeb.site API), Google Search Console API, and programmatic SEO.

## When to Use

- Keyword research with real data (volume, difficulty, CPC)
- Competitor domain analysis (traffic, top keywords, backlinks)
- Google Search Console data (queries, pages, clicks, impressions, CTR, position)
- SEO audit or technical analysis
- JSON+LD schema generation
- Programmatic SEO (pSEO) templates
- Core Web Vitals measurement (browser-based or API)

## Quick Start: Google Search Console

**Prerequisites:**
- Node.js 18+ with `googleapis` package (`npm install googleapis`)
- [Enable Search Console API](https://console.cloud.google.com/apis/library/searchconsole.googleapis.com) in your Google Cloud project

**Setup (one-time):**

1. Create OAuth credentials at [Google Cloud Console](https://console.cloud.google.com/apis/credentials) (Desktop app type)
2. Download JSON → save as `.claude/secrets/google_client_secret.json` (project) or `~/.claude/secrets/` (global)
3. Authenticate:
```bash
node scripts/gsc-auth.cjs --auth
```

**Query data:**
```bash
node scripts/gsc-query.cjs --sites                                    # List sites
node scripts/gsc-query.cjs --top-queries -s https://example.com       # Top queries
node scripts/gsc-query.cjs --low-ctr -s https://example.com -o low-ctr.csv -f csv
```

See `google-search-console-api-guide.md` for full API reference.

## Scripts

### Google Search Console (OAuth2)

Config: `google_client_secret.json` in `.claude/secrets/` (project or `~/.claude/secrets/` global)

| Script | Purpose |
|--------|---------|
| `gsc-config-loader.cjs` | Cross-platform config/token resolution |
| `gsc-auth.cjs` | OAuth2 authentication flow |
| `gsc-query.cjs` | Query analytics, sitemaps, URL inspection |

```bash
node scripts/gsc-auth.cjs --auth                    # Authenticate
node scripts/gsc-auth.cjs --verify                  # Check token
node scripts/gsc-query.cjs --top-queries -s URL     # Top queries
node scripts/gsc-query.cjs --inspect -s URL -u /page  # Inspect URL
```

### Keyword Research (ReviewWeb.site API)

Requires: `REVIEWWEB_API_KEY` in `.env`

```bash
node scripts/analyze-keywords.cjs -k "react tutorial" -o report.md
node scripts/analyze-keywords.cjs -d "competitor.com" -o analysis.md
```

### Core Web Vitals (PageSpeed API)

```bash
node scripts/audit-core-web-vitals.cjs -u https://example.com
node scripts/audit-core-web-vitals.cjs -s sitemap.xml -f md -o report.md
```

### Other Scripts

| Script | Purpose |
|--------|---------|
| `generate-sitemap.cjs` | XML sitemap generation |
| `generate-schema.cjs` | JSON+LD schema generator |
| `validate-schema.cjs` | Validate JSON-LD |
| `pseo-generator.cjs` | pSEO page generation |

## References

**Search Console:** `google-search-console-api-guide.md`, `search-console-query-patterns.md`

**API:** `reviewweb-api.md`, `reviewweb-content-api.md`

**Audit Workflows:** `seo-audit-workflow.md`, `browser-seo-audit-workflow.md`

**Keyword Research:** `keyword-research-workflow.md`, `keyword-clustering-methodology.md`, `content-gap-analysis-framework.md`

**Technical SEO:** `technical-seo-checklist.md`, `core-web-vitals-remediation.md`, `sitemap-best-practices.md`, `robots-txt-best-practices-2025.md`, `canonical-url-strategy.md`, `mobile-seo-checklist.md`

**On-Page SEO:** `on-page-seo-checklist-2025.md`, `meta-tag-templates.md`, `semantic-seo-framework.md`, `readability-scoring-guide.md`, `internal-linking-automation.md`

**Programmatic SEO:** `pseo-templates.md`, `pseo-best-practices.md`, `pseo-template-syntax.md`, `pseo-url-structure-guide.md`, `pseo-scale-architecture.md`

**Link Building:** `backlink-analysis-framework.md`, `link-building-campaign-framework.md`, `outreach-email-templates.md`, `directory-submission-list.md`

**Schema:** `schema-generation.md`, `schema-templates/` (article, product, faq, howto, organization, localbusiness)

## MCP Server Guidelines

**SEO uses multiple MCPs for different tasks.**

### Primary MCPs for SEO

| MCP | Use For |
|-----|---------|
| Google Search Console | First-party ranking data, queries, pages |
| ReviewWeb.site API | Keyword research, domain analysis |
| Exa MCP | Quick competitor research |
| Websets MCP | Comprehensive backlink/competitor analysis |

### When to Use Exa MCP (`exa-mcp-server`)

Use for **quick SEO research**:

| Task | Example |
|------|---------|
| Quick keyword ideas | "Find keywords for SaaS pricing" |
| Competitor lookup | "What keywords does competitor.com rank for?" |
| Content gap analysis | "Quick gaps in our content vs competitors" |
| SERP research | "What's ranking for 'best CRM software'?" |

### When to Use Websets MCP (`websets-mcp-server`)

Use for **comprehensive SEO analysis**:

| Task | Example |
|------|---------|
| Full backlink audit | "All backlinks pointing to competitor.com" |
| Complete competitor analysis | "All SEO strategies of top 20 competitors" |
| Exhaustive keyword research | "All keyword opportunities in fintech" |
| Link building prospects | "Find 50 sites for guest posting in SaaS" |

### MCP Selection Matrix

| SEO Task | MCP | Reason |
|----------|-----|--------|
| Keyword volume lookup | ReviewWeb API | Accurate metrics |
| Quick competitor check | Exa | Fast research |
| Full backlink audit | Websets | Exhaustive list |
| SERP analysis | Exa | Quick SERP data |
| Link prospect list | Websets | Comprehensive list |
| Technical SEO audit | Browser/PageSpeed | First-party tools |
| Ranking tracking | Google Search Console | First-party data |

### Auto-Selection Logic

```python
def select_mcp_for_seo(task: str, result_count: int = 0) -> str:
    # Use specialized APIs first
    if 'ranking' in task or 'search console' in task:
        return 'gsc'  # Google Search Console
    if 'keyword volume' in task or 'keyword difficulty' in task:
        return 'reviewweb'  # ReviewWeb API

    # Websets for comprehensive tasks
    websets_tasks = ['backlink audit', 'link prospects', 'full analysis',
                     'all competitors', 'comprehensive']
    if any(t in task.lower() for t in websets_tasks) or result_count >= 20:
        return 'websets'

    # Default to Exa for quick research
    return 'exa'
```

## Report Output

**Activate:** `assets-organizing` skill for report file paths

| Report Type | Path |
|-------------|------|
| SEO Audits | `assets/reports/seo/{date}-{domain}-audit.md` |
| Keyword Research | `assets/reports/seo/{date}-{topic}-keywords.md` |
| Ranking Reports | `assets/reports/seo/{date}-{domain}-rankings.md` |
| CWV Reports | `assets/reports/seo/{date}-{domain}-cwv.md` |

## Cross-Skill Integration

**chrome-devtools:** Real browser CWV, screenshots, network analysis → `browser-seo-audit-workflow.md`

**assets-organizing:** Report file organization and naming conventions
