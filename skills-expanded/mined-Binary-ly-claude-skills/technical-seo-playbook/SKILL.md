---
name: technical-seo-playbook
description: Implementation-ready technical SEO playbook (May 2026) with code, exact thresholds, and decision trees for crawl architecture, indexing, Core Web Vitals, structured data, E-E-A-T, hreflang, JavaScript SEO, AI Overviews / answer-engine optimization, and penalty recovery. Use whenever the user mentions SEO, Googlebot, robots.txt, sitemaps, indexation, crawl budget, Core Web Vitals, LCP, INP, CLS, page speed for ranking, structured data, JSON-LD, schema.org, rich results, GSC, Bing Webmaster, hreflang, AI Overviews, AEO, GEO, Perplexity/ChatGPT citations, llms.txt, Helpful Content / HCU, E-E-A-T, YMYL, manual actions, disavow, traffic decline, hydration, SSR/SSG/ISR/CSR, title tags, meta descriptions, internal linking, canonical, noindex, 404/410/301, pagination, faceted navigation, log analysis, BigQuery export, or site reputation abuse — even if they don't explicitly say "SEO". Stack-aware (WordPress, Shopify, Next.js, Astro, headless).
---

# Technical SEO Playbook — May 2026 Edition

This is a working engineering manual, not a marketing overview. Every recommendation is paired with code, an exact threshold, or a citation. Treat it like internal engineering documentation and reach for the reference files whenever the topic touches them — do not answer from memory on contested or recently-changed topics.

The playbook captures the state of search as of **May 2026**, with citations to Google Search Central, web.dev, IETF RFCs, and named practitioner research. Where Google's behavior is documented, the documentation URL is cited. Where the field has moved faster than docs (AI Overviews, llms.txt, the May 2026 FAQ rich-result deprecation), the playbook says so explicitly.

---

## When to use this skill

Use this skill any time the user asks about anything SEO-related, including:

- **Crawl & indexation**: robots.txt, sitemaps, Googlebot, log files, parameter handling, faceted navigation, soft 404s, "Discovered – currently not indexed", "Crawled – currently not indexed"
- **Performance for ranking**: Core Web Vitals, LCP/INP/CLS, PageSpeed, CrUX, preload, fetchpriority, hydration, scheduler.yield
- **On-page**: title tags, meta descriptions, headings, internal linking, canonical tags, pagination
- **Structured data**: JSON-LD, schema.org, Article, Product, Recipe, Event, VideoObject, LocalBusiness, Organization, BreadcrumbList, FAQ deprecation, HowTo deprecation
- **Content quality**: E-E-A-T, YMYL, Helpful Content System (HCU), author markup, site reputation abuse
- **Links**: disavow file, broken-link reclamation, digital PR templates
- **International**: hreflang (HTML/HTTP/sitemap), ccTLD vs subdomain vs subfolder
- **JavaScript SEO**: SSR/SSG/ISR/CSR tradeoffs, edge rendering, hydration mismatches, client-side routing
- **Answer engines**: AI Overviews, Perplexity, ChatGPT Search, Claude citations, GEO/AEO, llms.txt
- **Measurement**: GSC API, GSC bulk export to BigQuery, log-file analysis, rank tracking
- **Recovery**: manual actions, algorithmic suppression, HCU classifier, reconsideration requests

Stack guidance is included for WordPress, Shopify, Next.js / React, Astro / SSG, and headless setups — note where advice differs per stack.

**Do NOT use this skill for**: general copywriting that isn't ranking-driven, paid search / SEM strategy, social media marketing, conversion rate optimization that doesn't intersect with CWV, brand strategy.

---

## Working principles — read first

1. **Never give vague advice.** "Improve page speed" is not an answer. The answer is "Your LCP is 3.4s at p75; preload the hero image and add `fetchpriority='high'` (see Section 3)."
2. **Cite the source.** Google docs, web.dev, IETF, RFC 9309 for robots, named practitioner studies (Botify, Onely, BrightEdge, SearchPilot, Ahrefs, Profound). Cite the data, not the marketing copy.
3. **Code-first.** If the recommendation can be expressed as code, write the code. HTML, JSON-LD, Nginx config, Next.js patterns, Cloudflare Workers, DuckDB queries, Python scripts.
4. **Numbers, not adjectives.** Thresholds in ms, byte sizes in KB, character counts, exact HTTP status code behaviors.
5. **Show the diff.** Where there is a wrong pattern and a right pattern, show both side by side.
6. **Stack-aware.** WordPress, Shopify, Next.js, Astro, and headless setups differ — be explicit when advice diverges.

---

## Always-true thresholds (cheat sheet)

Memorize these. They drive most of the work.

| Metric | Good threshold | Source |
|---|---|---|
| **LCP** (Largest Contentful Paint) | < 2.5s at p75 | Google Search Central, `developers.google.com/search/docs/appearance/core-web-vitals` |
| **INP** (Interaction to Next Paint) | < 200ms at p75 — replaced FID on March 12, 2024 | web.dev |
| **CLS** (Cumulative Layout Shift) | < 0.1 at p75 | web.dev |
| **CrUX measurement window** | 28-day rolling, p75 across all page loads | Google Chrome User Experience Report |
| **Critical CSS budget** | < 14 KB inlined (fits in TCP slow-start initial congestion window) | web.dev |
| **Sitemap URL limit** | 50,000 URLs OR 50 MB uncompressed per file | sitemaps.org / Google docs |
| **Sitemap recommended shard size** | 10,000 URLs per file for large sites | Barry Adams / Polemic Digital |
| **Disavow file** | Max 100,000 lines, max 2 MB | Google docs |
| **Title visible length** | ~600 px / ~60 chars desktop, ~50 chars mobile | Search Engine Land |
| **Meta description visible length** | ~155–160 chars desktop, ~120 mobile | observed SERP behavior |
| **Title rewrite rate** | ~61% (Cyrus Shepard / Zyppy, 2022) | Zyppy ranking study |
| **VideoObject minimum duration** | 30 seconds for rich-result eligibility | Google docs |
| **BreadcrumbList minimum** | At least 2 ListItems | Google docs |
| **Crawl ratio (healthy site)** | 60–80% of indexable URLs crawled per 30 days | Botify case data |
| **Click depth target** | ≤ 3 clicks from homepage for indexable URLs | practitioner consensus |

---

## Decision tree — noindex vs canonical vs disallow vs 410 vs 301

The most-confused area of technical SEO. The decision is mechanical:

```
Is the URL gone forever?
├── YES → Is there an equivalent replacement?
│   ├── YES → 301 to replacement (preserves PageRank)
│   └── NO  → 410 Gone (faster deindexing than 404 per Mueller)
└── NO (page exists but should not rank)
    ├── Is it a duplicate of another indexable page?
    │   └── YES → rel="canonical" to the master
    ├── Should crawlers see it at all? (e.g. /admin/)
    │   └── NO  → Disallow in robots.txt (for crawl waste, NOT for deindexing)
    └── Should it be crawlable but not indexable? (thank-you, faceted combos)
        └── YES → meta robots noindex (NOT robots.txt — Google must crawl to see noindex)
```

**The classic mistake**: `Disallow: /thank-you/` + `<meta name="robots" content="noindex">` — Googlebot never reaches the page to see the noindex, so the URL stays indexed with anchor-text-only snippets. Per Martin Splitt: "Use noindex meta tags or X-Robots-Tag for pages you want to be hidden from search results. Do not block those pages in robots.txt."

---

## Reference router — load the right file for the topic

When the user's question lands on one of these areas, **read the relevant reference file before answering**. Do not paraphrase from memory; the references contain the exact code, numbers, and citations that make answers credible.

| Topic | Reference file |
|---|---|
| robots.txt, crawl budget, log files, sitemaps, faceted nav, URL parameters | `references/01-crawl-and-log-files.md` |
| SSR/SSG/ISR/CSR, hydration, soft 404, GSC Index Coverage remediation, dynamic rendering | `references/02-indexing-and-rendering.md` |
| LCP, INP, CLS, preload, fetchpriority, scheduler.yield, PerformanceObserver, CDN config | `references/03-core-web-vitals.md` |
| Titles, meta descriptions, headings, internal linking, pagination, infinite scroll | `references/04-onpage-architecture.md` |
| JSON-LD examples for every type, FAQ/HowTo deprecation, CI validation, review-snippet eligibility | `references/05-structured-data.md` |
| Author markup, HCU audit checklist, first-hand experience signals, YMYL | `references/06-eeat.md` |
| Digital PR data assets, broken-link reclamation API code, disavow syntax | `references/07-link-acquisition.md` |
| hreflang in HTML/HTTP/sitemap, bidirectional validation, ccTLD vs subdomain vs subfolder | `references/08-international-seo.md` |
| Two-pass indexing reality, edge rendering with Cloudflare Workers, client-side routing | `references/09-javascript-seo.md` |
| AI Overviews citation patterns, Perplexity/ChatGPT/Claude data, passage optimization, llms.txt status | `references/10-aeo-geo.md` |
| GSC API Python code, BigQuery schema and queries, DuckDB log pipeline, rank tracking | `references/11-monitoring-and-measurement.md` |
| Manual action vs algorithmic vs HCU diagnosis, reconsideration requests, recovery timelines | `references/12-penalty-recovery.md` |
| 30/60/90-day plan for new site AND for declining established site | `references/action-plans.md` |

---

## Templates available

The `templates/` directory contains ready-to-use files. Reference them directly when the user asks for a starting point.

```
templates/
├── robots/
│   ├── wordpress.txt              # Canonical WP pattern with AI-crawler blocks
│   ├── shopify.liquid             # Online Store 2.0 robots.txt.liquid
│   ├── nextjs.ts                  # App Router app/robots.ts
│   └── astro.txt                  # Static public/robots.txt
├── schema/
│   ├── article.json               # Article / NewsArticle / BlogPosting
│   ├── product.json               # Merchant Listing with all 2026 requirements
│   ├── recipe.json                # Recipe with ISO 8601 durations
│   ├── event.json                 # Offline event (post-deprecation)
│   ├── video-object.json          # VideoObject with Clip markup
│   ├── local-business.json        # Use most specific subtype
│   ├── breadcrumb-list.json       # Minimum 2 ListItems
│   ├── organization.json          # Wikidata sameAs for KG disambiguation
│   └── profile-page-author.json   # E-E-A-T author page
└── code/
    ├── hreflang-sitemap.xml       # Sitemap with hreflang annotations
    ├── ci-validation.yml          # GitHub Actions for schema validation
    ├── gsc-api-python.py          # 90-day GSC API extraction
    └── duckdb-log-analysis.sql    # Googlebot log parser
```

---

## Common cross-cutting mistakes

These mistakes appear across multiple sections; flag them whenever the user describes the symptom:

- **Blocking rendering resources in robots.txt** (e.g. `/wp-content/`, `/_next/static/`). Per Google's December 2024 "Crawling December" post: "If WRS cannot fetch a rendering-critical resource, Google Search may have trouble extracting content."
- **Using `Disallow` to deindex** — disallow blocks crawling, not indexing. Google will still index the URL with anchor-text-only snippets.
- **Trusting Lighthouse for the ranking signal** — only CrUX field data feeds the Page Experience ranking signal. Lab metrics are diagnostic only.
- **Including non-canonical URLs in sitemaps** — degrades trust in your sitemap and confuses Google's canonical selection.
- **Bumping `lastmod` on every nightly cron** — Google will eventually ignore your `lastmod` entirely.
- **Canonicalizing paginated pages to page 1** — strips the content on pages 2+ from the index.
- **`loading="lazy"` on the LCP image** — never. It defers the most important asset.
- **Long-term `noindex,follow`** — per Mueller (2019, repeated since), Google eventually treats it as `noindex,nofollow`.
- **Mass-deleting "low-quality" content to recover from HCU** — per Mueller, mass-improvement is the right play, not mass-deletion.
- **Adding `llms.txt` and expecting AI Overview/Perplexity/ChatGPT citation lift** — as of May 2026, no answer engine has confirmed using it; Mueller (Dec 2025) noted server logs show AI services don't fetch it. See `references/10-aeo-geo.md` for the nuance.

---

## Authoritative sources to cite

Whenever answering, prefer citations from this set (in roughly descending order of weight):

1. **Google Search Central docs** — `developers.google.com/search/docs/*`
2. **Search Central Blog** — `developers.google.com/search/blog/*`
3. **web.dev** — performance and Core Web Vitals canonical documentation
4. **schema.org** — vocabulary definitions
5. **IETF RFCs** — RFC 9309 for robots.txt, HTTP RFCs for status codes
6. **Google Search Central YouTube** — Martin Splitt's Lightning Talks, John Mueller AMAs, Gary Illyes
7. **Named practitioners with documented research**: Aleyda Solís (hreflang), Barry Adams / Polemic Digital (sitemaps), Botify, Onely, SearchPilot, BrightEdge, Ahrefs research, Profound, OtterlyAI, Glenn Gabe / GSQi, Marie Haynes (penalties), Brian Dean / Backlinko (ranking studies), Cyrus Shepard / Zyppy (titles)
8. **Sistrix, Semrush, AccuRanker** — for SERP-level data, with the caveat that ranks are non-personalized

---

## How to deliver answers

When a user asks an SEO question, the response pattern is:

1. **Identify the topic and load the reference file** (use the router table above).
2. **Answer with code or a number first**, then explain why it works.
3. **Cite the source** for any non-obvious fact, dating it where the field moves fast (CWV thresholds, AIO behavior, FAQ deprecation).
4. **Show wrong vs right** where the user is describing an existing setup.
5. **Stack-callout**: if the user is on WordPress, give the WP-specific pattern, not a generic one. Same for Shopify, Next.js, Astro.
6. **Flag uncertainty honestly** — for AIO behavior, llms.txt adoption, and unconfirmed Google updates, say so explicitly rather than asserting.

Keep responses focused on what the user actually asked. Don't dump the whole reference — pull the exact piece that answers their question, and tell them which reference file to read for the surrounding context.
