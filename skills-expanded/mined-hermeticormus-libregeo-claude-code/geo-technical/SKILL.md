---
name: geo-technical
description: "Technical SEO audit with GEO-specific checks: crawlability, AI crawler user agents, indexability, security headers, URL structure, mobile, Core Web Vitals (INP), and server-side rendering for crawlers that do not run JavaScript, scored by category with fixes. Use when the user asks about technical SEO, site speed, rendering, or why AI crawlers see an empty page."
version: 1.0.0
author: geo-seo-claude
tags: [geo, technical-seo, core-web-vitals, ssr, crawlability, security, performance]
---

# GEO Technical SEO Audit

## Purpose

Foundation audit for both traditional search and AI citation. Most critical GEO gates: **server-side rendering** (AI crawlers do not execute JavaScript) and **AI crawler access** (sites often inadvertently block AI bots in robots.txt). 8 categories, 100 points.

## How to Use This Skill

1. Collect target URL (homepage + 2-3 key inner pages)
2. Fetch each page using curl/WebFetch — get raw HTML + HTTP headers
3. Run through each of the 8 audit categories below
4. Score using the rubric
5. Generate GEO-TECHNICAL-AUDIT.md (template at end)

Sub-check details, fix lists, framework-specific SSR solutions, and the IndexNow protocol explainer are in **`checks.md`** alongside this file. Reference it as needed.

---

## Category 1: Crawlability (15 pts)

Sub-checks (detail in checks.md §1):
- **1.1 robots.txt validity** — syntactic correctness, sitemap reference
- **1.2 AI crawler access (CRITICAL)** — see table below
- **1.3 XML sitemaps** — valid XML, `<lastmod>` accurate, sample-verify 200s
- **1.4 Crawl depth** — important pages within 3 clicks of homepage
- **1.5 Noindex management** — no erroneous `noindex` on indexable pages

### AI Crawlers — User-Agent Reference

| Crawler | User-Agent | Platform |
|---|---|---|
| GPTBot | GPTBot | ChatGPT / OpenAI |
| Google-Extended | Google-Extended | Gemini / Google AI training |
| Googlebot | Googlebot | Google Search + AI Overviews |
| Bingbot | bingbot | Bing Copilot + ChatGPT (via Bing) |
| PerplexityBot | PerplexityBot | Perplexity AI |
| ClaudeBot | ClaudeBot | Anthropic Claude |
| Amazonbot | Amazonbot | Alexa / Amazon AI |
| CCBot | CCBot | Common Crawl (many AI models) |
| FacebookBot | FacebookExternalHit | Meta AI |
| Bytespider | Bytespider | TikTok / ByteDance AI |
| Applebot-Extended | Applebot-Extended | Apple Intelligence |

### Scoring

| Check | Points |
|---|---|
| robots.txt valid and complete | 3 |
| AI crawlers allowed | 5 |
| XML sitemap present and valid | 3 |
| Crawl depth within 3 clicks | 2 |
| No erroneous noindex directives | 2 |

---

## Category 2: Indexability (12 pts)

Sub-checks (detail in checks.md §2):
- **2.1 Canonical tags** — self-referencing, no conflicts, no chains
- **2.2 Duplicate content** — www/non-www, HTTP/HTTPS, trailing slash, params
- **2.3 Pagination** — `rel="next/prev"` or canonical-to-first
- **2.4 Hreflang** — reciprocal, x-default, valid ISO codes
- **2.5 Index bloat** — indexed pages vs valuable content pages

| Check | Points |
|---|---|
| Canonical tags correct on all pages | 3 |
| No duplicate content issues | 3 |
| Pagination handled correctly | 2 |
| Hreflang correct (if applicable) | 2 |
| No index bloat | 2 |

---

## Category 3: Security (10 pts)

Required HTTP response headers (detail + values in checks.md §3): `Strict-Transport-Security`, `Content-Security-Policy`, `X-Content-Type-Options: nosniff`, `X-Frame-Options: DENY` or `SAMEORIGIN`, `Referrer-Policy: strict-origin-when-cross-origin` (or stricter), `Permissions-Policy`.

HTTPS: enforced, HTTP→HTTPS 301, no mixed content, valid unexpired cert.

| Check | Points |
|---|---|
| HTTPS enforced with valid cert | 4 |
| HSTS header present | 2 |
| X-Content-Type-Options | 1 |
| X-Frame-Options | 1 |
| Referrer-Policy | 1 |
| Content-Security-Policy | 1 |

---

## Category 4: URL Structure (8 pts)

Sub-checks (detail in checks.md §4):
- **4.1 Clean URLs** — human-readable, lowercase, hyphens, no session IDs
- **4.2 Logical hierarchy** — `/category/subcategory/page`, consistent
- **4.3 Redirect chains** — max 1 hop, all 301, no loops
- **4.4 Parameter handling** — canonical/Disallow, GSC + Bing WMT configured

| Check | Points |
|---|---|
| Clean, readable URLs | 2 |
| Logical hierarchy | 2 |
| No redirect chains (max 1 hop) | 2 |
| Parameter handling configured | 2 |

---

## Category 5: Mobile Optimization (10 pts)

**Critical**: As of July 2024, Google crawls ALL sites exclusively with mobile Googlebot. No desktop crawling.

Sub-checks (detail in checks.md §5):
- **5.1 Responsive design** — `<meta name="viewport" content="width=device-width, initial-scale=1">`, no horizontal scroll
- **5.2 Tap targets** — minimum 48x48 CSS px, 8px spacing
- **5.3 Font sizes** — base ≥ 16px, WCAG AA contrast (4.5:1 normal, 3:1 large)
- **5.4 Mobile content parity** — all desktop content visible on mobile

| Check | Points |
|---|---|
| Viewport meta tag correct | 3 |
| Responsive layout (no horizontal scroll) | 3 |
| Tap targets appropriately sized | 2 |
| Font sizes legible | 2 |

---

## Category 6: Core Web Vitals (15 pts)

Field data (75th percentile) is the ranking signal. Lab data is for debugging.

| Metric | Good | Needs Improvement | Poor | Notes |
|---|---|---|---|---|
| **LCP** (Largest Contentful Paint) | < 2.5s | 2.5s - 4.0s | > 4.0s | Time until largest visible element renders |
| **INP** (Interaction to Next Paint) | < 200ms | 200ms - 500ms | > 500ms | Replaced FID March 2024. Measures ALL interactions |
| **CLS** (Cumulative Layout Shift) | < 0.1 | 0.1 - 0.25 | > 0.25 | Unexpected layout movements |

Without CrUX data, estimate from page characteristics; common fixes for each metric in checks.md §6.

| Check | Points |
|---|---|
| LCP < 2.5s | 5 |
| INP < 200ms | 5 |
| CLS < 0.1 | 5 |

---

## Category 7: Server-Side Rendering (15 pts) — CRITICAL FOR GEO

AI crawlers (GPTBot, PerplexityBot, ClaudeBot, etc.) do **NOT execute JavaScript**. They fetch raw HTML. Client-rendered content = invisible to AI. Googlebot does execute JS but deprioritizes it (separate rendering queue, days/weeks delay).

### Detection Method
1. Fetch with curl (no JS): `curl -s [URL]`
2. Compare raw HTML to browser-rendered DOM
3. If key content (headings, paragraphs, product info, article text) is MISSING from curl output → client-side rendering

### What to Check in Raw HTML
Main content text, headings (H1/H2/H3), navigation, structured data (JSON-LD), meta tags (title/description/canonical/OG), internal links.

SSR solutions per framework + extended scoring detail in checks.md §7.

| Check | Points |
|---|---|
| Main content in raw HTML | 8 |
| Meta tags + structured data in raw HTML | 4 |
| Internal links in raw HTML | 3 |

---

## Category 8: Page Speed & Server Performance (15 pts)

Sub-checks (detail in checks.md §8):
- **8.1 TTFB** — target **< 800ms** (ideal < 200ms). Measure: `curl -o /dev/null -s -w 'TTFB: %{time_starttransfer}s\n' [URL]`
- **8.2 Resource optimization** — total page weight **< 2MB** (critical pages < 1MB), gzip/brotli on, minified, unused CSS/JS
- **8.3 Image optimization** — WebP/AVIF, correctly sized, `loading="lazy"` below fold (NOT above), explicit width/height
- **8.4 Code splitting** — JS bundles < 200KB compressed (warning), < 500KB (critical), `async`/`defer` third-party, no render-blocking in `<head>`
- **8.5 Caching** — static assets `max-age=31536000` with content-hashed filenames; HTML short cache or `no-cache` with ETag/Last-Modified
- **8.6 CDN** — `CF-Ray` (Cloudflare), `X-Cache` (CloudFront), `X-Served-By` (Fastly)

| Check | Points |
|---|---|
| TTFB < 800ms | 3 |
| Page weight < 2MB | 2 |
| Images optimized (format, size, lazy) | 3 |
| JS bundles reasonable (< 200KB compressed) | 2 |
| Compression enabled (gzip/brotli) | 2 |
| Cache headers on static resources | 2 |
| CDN in use | 1 |

---

## IndexNow Protocol

Bing/Yandex/Seznam/Naver instant-indexing protocol. Google does NOT support but monitors. **GEO relevance**: ChatGPT and Bing Copilot both use Bing's index — faster Bing indexing = faster AI visibility.

Check for `https://[domain]/.well-known/indexnow-key.txt` or CMS plugin. Full explainer in checks.md.

---

## Overall Scoring

| Category | Max Points | Weight |
|---|---|---|
| Crawlability | 15 | Core foundation |
| Indexability | 12 | Core foundation |
| Security | 10 | Trust signal |
| URL Structure | 8 | Crawl efficiency |
| Mobile Optimization | 10 | Google requirement |
| Core Web Vitals | 15 | Ranking signal |
| Server-Side Rendering | 15 | GEO critical |
| Page Speed & Server | 15 | Performance |
| **Total** | **100** | |

Score interpretation bands in checks.md (90-100 Excellent, 70-89 Good, 50-69 Needs Work, 30-49 Poor, 0-29 Critical).

---

## Output Format

Generate **GEO-TECHNICAL-AUDIT.md** with:

```markdown
# GEO Technical SEO Audit — [Domain]
Date: [Date]

## Technical Score: XX/100

## Score Breakdown
| Category | Score | Status |
|---|---|---|
| Crawlability | XX/15 | Pass/Warn/Fail |
| Indexability | XX/12 | Pass/Warn/Fail |
| Security | XX/10 | Pass/Warn/Fail |
| URL Structure | XX/8 | Pass/Warn/Fail |
| Mobile Optimization | XX/10 | Pass/Warn/Fail |
| Core Web Vitals | XX/15 | Pass/Warn/Fail |
| Server-Side Rendering | XX/15 | Pass/Warn/Fail |
| Page Speed & Server | XX/15 | Pass/Warn/Fail |

Status: Pass = 80%+ of category points, Warn = 50-79%, Fail = <50%

## AI Crawler Access
| Crawler | User-Agent | Status | Recommendation |
|---|---|---|---|
| GPTBot | GPTBot | Allowed/Blocked | [Action] |
| Googlebot | Googlebot | Allowed/Blocked | [Action] |
[Continue for all AI crawlers]

## Critical Issues (fix immediately)
[List with specific page URLs and what is wrong]

## Warnings (fix this month)
[List with details]

## Recommendations (optimize this quarter)
[List with details]

## Detailed Findings
[Per-category breakdown with evidence]
```
