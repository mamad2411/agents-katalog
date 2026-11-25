---
name: web-seo-performance
description: Prepare professional websites for technical SEO, structured content, indexing, migrations, Core Web Vitals, responsive assets, font loading, third parties, and real-user monitoring. Use before launch and after major content or code changes.
version: 1.0.0
---

# Web SEO & Performance

Make the service useful and technically understandable. SEO and performance are ongoing product constraints, not a final checklist or a single Lighthouse score.

## Technical SEO baseline

- Stable, descriptive, human-readable URLs;
- unique title, meta description, useful H1, and logical headings;
- canonical URL and intentional redirects;
- XML sitemap and robots.txt;
- Search Console or equivalent launch verification;
- structured data only when truthful and eligible;
- Open Graph/share metadata;
- useful 404, empty, and error pages;
- no accidental indexing of account pages, private data, duplicate filter URLs, staging, thin vendor wrappers, or search results;
- preserve old URLs during migration with a documented redirect map;
- correct locale, date, address, and business information;
- accessible, specific content rather than keyword stuffing or invented proof.

## Structured data

Select schema by content: `Organization`, `LocalBusiness`, `Event`, `Product`, `Article`, `BreadcrumbList`, or another truthful type. Validate it, keep it in sync with visible content, and do not use FAQ/review markup merely to win space in search.

## Core Web Vitals budget

Target:

- LCP ≤ 2.5s;
- INP < 200ms;
- CLS < 0.1.

Set a project budget for HTML, CSS, JavaScript, fonts, images, and third parties. Measure mobile in lab and real-user conditions. A score is evidence, not the goal; preserve completion of the primary task.

## Implementation rules

- Reserve image dimensions and use responsive AVIF/WebP where appropriate.
- Do not lazy-load the primary LCP asset; preload only truly critical assets.
- Self-host or deliberately select WOFF2 fonts, use `font-display: swap`, and load only used weights.
- Defer non-critical scripts and lazy-load below-fold media and optional embeds.
- Prefer static/server rendering for public content; isolate interactive widgets.
- Animate according to `motion-system.md`; avoid unbounded scroll handlers and expensive filters.
- Avoid large client libraries for one small interaction.
- Cache public content deliberately and never cache private per-user data as public.

## Migration and launch

Create a route inventory, redirect map, canonical plan, sitemap, robots policy, indexation rules, metadata matrix, structured-data test list, and rollback plan. Verify preview/staging cannot be indexed. Keep tracking consent compatible with privacy decisions.

## Monitoring

After launch monitor index coverage, crawl errors, broken links, search queries, server/client errors, latency, Core Web Vitals, image/font failures, and third-party regressions. Set owners and thresholds. Re-test after releases, migrations, template changes, and content model changes.

## Handoff

Use with `product-discovery-ux`, `brand-content-strategy`, `frontend-architecture`, `web-accessibility`, `web-privacy-security`, `qa-release`, and the relevant domain addendum such as `library-seo-performance.md`.

References:
- https://developers.google.com/search/docs/fundamentals/seo-starter-guide
- https://developers.google.com/search/docs/appearance/core-web-vitals
- https://developers.google.com/search/docs/appearance/structured-data/intro-structured-data
