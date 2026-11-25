---
name: seo-canonical-hreflang
description: >-
  Keep canonical and i18n hreflang correct on this Nuxt 4 site
  (@nuxtjs/i18n, de/en, prefix strategy). Use when adding routes or
  changing i18n/SEO config.
---

# Canonical & hreflang

Single topic: one canonical + correct hreflang pairs (CI-gated:
`canonical`, `hreflang`).

- Exactly one canonical per page; correct `de`/`en` `hreflang` pairs.
- The i18n `baseUrl` stays the production domain in every environment so
  emitted URLs are the real ones.

Verify: `pnpm seo:lighthouse` — `canonical`/`hreflang` gates green.
