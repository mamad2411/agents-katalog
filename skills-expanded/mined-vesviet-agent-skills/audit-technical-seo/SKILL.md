---
name: audit-technical-seo
description: Audit crawl budgets, search and AI bot access in robots.txt (Googlebot, Bingbot, OAI-SearchBot, PerplexityBot, Applebot-Extended, and other AI search crawlers), XML sitemaps, canonical tags, HTTP status codes, redirect chains (301/404/410), and Core Web Vitals (LCP, INP, CLS) emitting structured audit reports. Use when diagnosing crawlability issues, auditing staging or production sites for technical health, resolving redirect loops or canonical errors, or preparing engineering escalation tickets for frontend and infrastructure teams.
allowed-tools: [read_file, write_file, edit_file, create_file, search_code, fetch]
---

# Audit Technical SEO

Use this skill with the **SEO Analyst** role to perform technical audits of crawlability, bot governance, URL canonicalization, redirect graphs, sitemap hygiene, and Core Web Vitals. While `optimize-seo` manages keyword intent and on-page content briefs, `audit-technical-seo` engineers technical health, crawler efficiency, and infrastructure readiness for traditional search engines and AI discovery bots.

## When to Use

- diagnosing crawl budget waste, server latency bottlenecks, or spider traps
- verifying `robots.txt` accessibility for AI search crawlers (OAI-SearchBot, PerplexityBot, ClaudeBot, Applebot-Extended, Bingbot) and Googlebot
- auditing XML sitemaps for syntax compliance, URL freshness, and non-200 exclusions
- resolving canonical loops, self-canonical errors, or cross-domain canonical mismatches
- detecting multi-hop redirect chains, 302 temporary redirect leaks, and 404/410 status codes
- assessing Core Web Vitals (LCP <= 2.5s, INP <= 200ms, CLS <= 0.1) and SSR/hydration overhead
- emitting machine-readable `contracts/schemas/seo-audit-report.json` with technical escalation tickets

## Core Rules

### Crawl Budget & Server Efficiency
- eliminate crawler traps caused by unconstrained faceted navigation, session IDs, search filters, and infinite date pickers per [`references/crawl-budget-and-bot-access-guide.md`](references/crawl-budget-and-bot-access-guide.md)
- audit Time to First Byte (TTFB); flag TTFB > 500ms as an infrastructure bottleneck requiring edge caching or compute optimization
- preserve crawl equity by directing search bots toward high-priority canonical content, product catalogs, and indexable pillars

### AI & Search Engine Bot Governance
- declare explicit user-agent directives in `robots.txt` for Googlebot, Bingbot, OAI-SearchBot, PerplexityBot, and ClaudeBot
- distinguish conversational/search discovery crawlers (OAI-SearchBot, PerplexityBot) from bulk training scrapers (GPTBot, CCBot)
- prohibit global wildcard blocks (`Disallow: /`) that cause total brand invisibility across emerging AI answer engines
- ensure valid `Sitemap:` declarations with absolute HTTPS URLs are present in `robots.txt`

### Canonical Tag & URL Normalization
- enforce self-referential canonical tags on all original canonical URLs; never omit canonical tags on indexable pages per [`references/redirects-canonicals-and-status-codes.md`](references/redirects-canonicals-and-status-codes.md)
- resolve circular canonical loops and eliminate canonical tags pointing to 3xx redirects, 4xx errors, or noindexed endpoints
- enforce strict URL normalization: consistent HTTPS protocol, canonical domain (non-www vs www), and uniform trailing slashes

### Redirect Hygiene & Status Codes
- enforce single-hop 301 permanent redirects; strictly ban redirect chains (> 1 hop) and circular redirect loops
- update internal site links to point directly to target canonical URLs rather than through intermediary 3xx hops
- return HTTP 410 Gone for intentionally removed content to expedite index de-allocation; reserve HTTP 404 for accidental missing resources
- detect and eliminate 302 temporary redirect leaks that dilute ranking equity

### XML Sitemap Hygiene
- validate XML schema against sitemaps.org standards; partition sitemaps at 50,000 URLs or 50MB per file with a sitemap index
- enforce strict inclusion of 200 OK canonical URLs only; ban noindexed, redirected, or error URLs from XML sitemaps
- require accurate ISO-8601 `lastmod` timestamps that update only when substantive content changes occur

### Core Web Vitals & Hydration Profiling
- audit 75th percentile Core Web Vitals thresholds per [`references/core-web-vitals-and-performance.md`](references/core-web-vitals-and-performance.md): Largest Contentful Paint (LCP <= 2.5s), Interaction to Next Paint (INP <= 200ms), Cumulative Layout Shift (CLS <= 0.1)
- diagnose JavaScript hydration bottlenecks, long tasks (> 50ms), and render-blocking CSS/fonts; dispatch actionable escalation tickets

## Suggested Process

1. **Bot Access & Directive Audit**: Fetch and inspect `robots.txt`; evaluate allow/disallow directives for Googlebot, Bingbot, and AI bots (OAI-SearchBot, PerplexityBot, ClaudeBot, Applebot-Extended); verify sitemap index declaration.
2. **XML Sitemap Validation**: Extract declared sitemap URLs; verify schema validity, 200 OK HTTP status, canonical alignment, and genuine `lastmod` timestamps.
3. **Status Code & Redirect Traversal**: Trace HTTP response headers across core site paths; flag redirect chains (> 1 hop), 302 leaks, soft 404s, and un-pruned legacy URLs.
4. **Canonical & Header Inspection**: Inspect DOM `<link rel="canonical">` and HTTP `Link` headers; verify self-referential canonical tags, absolute HTTPS format, and absence of canonical loops.
5. **Crawl Budget & Architecture Profiling**: Identify faceted navigation parameters, internal query loops, and high-TTFB routes that deplete crawl allocation.
6. **Core Web Vitals Telemetry Analysis**: Evaluate field (CrUX) and lab (Lighthouse) telemetry for LCP, INP, and CLS; identify un-sized assets, layout shifts, and heavy hydration scripts.
7. **Escalation Ticket Authoring**: Generate structured technical escalation tickets assigned to `frontend-developer`, `devops-engineer`, or `cloudflare-engineer` with clear priority tags.
8. **Audit Contract Emission**: Compile all findings and severitized logs into `contracts/schemas/seo-audit-report.json`.

## Checklist

- [ ] `robots.txt` explicitly configures access for Googlebot, Bingbot, OAI-SearchBot, PerplexityBot, ClaudeBot, and Applebot-Extended
- [ ] global wildcard blocks (`Disallow: /`) verified absent for authorized search and discovery bots
- [ ] XML sitemap syntax validated against sitemaps.org schema with absolute HTTPS URLs and valid ISO-8601 `lastmod` dates
- [ ] XML sitemap contains exclusively 200 OK canonical URLs with zero redirected, noindexed, or 4xx targets
- [ ] canonical tags are self-referential on canonical pages, use absolute HTTPS URLs, and have zero circular loops
- [ ] redirect chains eliminated (strict 1-hop maximum for legacy redirects) and circular loops broken
- [ ] internal site links updated to point directly to final destination URLs without intermediary 3xx hops
- [ ] HTTP 410 Gone status code implemented for permanently retired pages to expedite index de-allocation
- [ ] faceted navigation parameters and session IDs restricted from search crawlers via robots directives or canonicals
- [ ] Core Web Vitals verified within thresholds: LCP <= 2.5s, INP <= 200ms, CLS <= 0.1
- [ ] render-blocking assets and JavaScript hydration bottlenecks documented with optimization remediation steps
- [ ] technical escalation tickets authored with explicit owners (`frontend-developer`, `devops-engineer`, `cloudflare-engineer`)
- [ ] audit findings and severitized issue logs compiled into `contracts/schemas/seo-audit-report.json`

## Output Contracts

When completing a technical SEO audit, emit:

- **`contracts/schemas/seo-audit-report.json`** — Populates `traditional_seo.issues` with `category: "technical_seo"` and severitized issues (`critical`, `high`, `medium`, `low`, `info`), `ai_extractability.ai_bot_crawlability` for crawler permissions, and `technical_escalations` defining explicit owners (`frontend-developer`, `devops-engineer`, `cloudflare-engineer`) and priorities (`must_do_before_publish`, `post_publish`, `next_sprint`).

## Failure Modes

- **AI engine blindness**: blanket `Disallow: /` directives in `robots.txt` block AI search bots. Mitigation: inspect user-agent blocks; grant explicit crawl access to authorized discovery bots.
- **Redirect chain latency**: multi-hop redirects degrade server TTFB and dilute link equity. Mitigation: rewrite edge redirect rules to route directly from source to target in a single 301 hop.
- **Canonical loop lock**: conflicting canonical declarations cause indexing paralysis. Mitigation: trace canonical pairs; ensure all canonical targets resolve to 200 OK self-canonical pages.
- **Sitemap index pollution**: including redirects, 404s, or noindexed URLs wastes crawl budget. Mitigation: automate sitemap generation from production route manifests; filter non-canonical paths.
- **Hydration INP degradation**: client-side JavaScript hydration delays main-thread input responsiveness. Mitigation: escalate to frontend engineer for islands architecture, code-splitting, or CSS transitions.

## Security Guardrails (OWASP ASI)

- **ASI01 Goal Hijack**: ensure crawler directives and audit queries cannot be subverted by untrusted query parameters or injected request headers.
- **ASI03 Identity & Privilege Abuse**: never expose internal staging URLs, administrative routes, secret tokens, or private endpoints in public `robots.txt` or XML sitemaps.
- **ASI04 Supply Chain**: verify external bot user-agent signatures and crawler IP verification mechanisms against official search engine documentation.
- **ASI07 Inter-Agent Communication**: emit machine-validated findings via `seo-audit-report.json` so engineering roles receive unambiguous technical tickets.
- **ASI09 Human-Agent Trust Exploitation**: report verified HTTP response headers, crawl traces, and CWV measurements without fabricating performance scores or crawl completion claims.

## Related Skills

- **optimize-seo**: Keyword intent mapping, on-page content briefs, and search visibility strategy
- **implement-schema-markup**: Connected Schema.org @graph JSON-LD architecture and rich results validation
- **performance-profiling**: Deep browser runtime profiling, flamegraphs, and main-thread execution diagnostics
- **add-page-route**: Frontend route creation, canonical tag implementation, and SSR rendering configurations
- **troubleshoot-service**: Infrastructure-level HTTP error investigation, edge routing, and server log analysis
