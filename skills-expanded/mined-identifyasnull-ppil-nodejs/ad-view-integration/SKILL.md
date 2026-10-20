---
name: ad-view-integration
description: Integrate generated SEO metadata into ad/profile rendering with language fallback, canonical URL behavior, and image alt assignment.
intent: >-
  Use when wiring search.seo fields into route/view rendering and ensuring metadata maps to head tags and media attributes.
type: workflow
---

# Ad View Integration

## Mapping Contract

- `seo.pageTitle` -> `<title>`
- `seo.h1` -> primary heading override
- `seo.pageDescription` -> `<meta name="description">`
- `seo.pageKeywords` -> `<meta name="keywords">`
- `seo.imageAlt[]` -> carousel image `alt`
- ad permalink -> `<link rel="canonical">`

## Checklist

1. Resolve SEO payload by language with fallback to English.
2. Normalize canonical URL for absolute and relative permalink inputs.
3. Ensure view template conditionally renders metadata tags.
4. Ensure image alt fallback exists if SEO alt array is short/empty.
5. Add helper tests for language fallback and canonical normalization.

## Anti-Patterns

- Hardcoding metadata in template without route model fields.
- Using only one language key with no fallback behavior.
