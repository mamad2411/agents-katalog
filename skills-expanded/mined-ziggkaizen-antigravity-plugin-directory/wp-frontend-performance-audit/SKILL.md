---
name: wp-frontend-performance-audit
description: Audits WordPress frontend delivery, Core Web Vitals, network waterfalls, assets, main-thread work, caching, and third-party impact under representative conditions.
---

# WordPress frontend performance audit

Use this skill for user-perceived loading and interaction performance.

## Measure

- TTFB and response/cache headers;
- LCP, INP, and CLS;
- document and asset waterfalls;
- render-blocking CSS and JavaScript;
- image dimensions, formats, responsive sources, and priority;
- font requests and rendering;
- JavaScript execution and main-thread tasks;
- third-party scripts and embeds;
- compression, cacheability, CDN behavior;
- logged-out versus authenticated/personalized behavior;
- mobile and desktop conditions.

Run [audit-frontend-performance-workflow.md](workflows/audit-frontend-performance-workflow.md) and use [frontend-performance-checklist.md](resources/frontend-performance-checklist.md).

Do not treat one lab score as field performance. Keep lab diagnostics, synthetic benchmarks, and real-user/field data separate.
