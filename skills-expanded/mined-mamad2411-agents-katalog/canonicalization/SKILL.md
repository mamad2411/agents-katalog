---
name: canonicalization
description: Resolves duplicate URL signals with rel=canonical, redirects, and parameter handling. Use when duplicates, www/http variants, or conflicting canonicals appear.
---

# Canonicalization

## Overview

Consolidate indexing signals on the preferred URL.

## When to Use

- Duplicate content clusters, parameter URLs, mixed www/HTTPS

**Not for:** Writing new page copy.

## Official sources

- https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls
- https://developers.google.com/search/docs/crawling-indexing/canonicalization

## Process

1. List URL variants (slash, www, http/https, params, CMS duplicates).
2. Choose one canonical per document.
3. Implement self-referencing `rel=canonical` on the preferred URL.
4. Align internal links, sitemaps, and redirects (301/308 for permanent moves) with that choice.
5. Remove conflicting signals (canonical pointing at noindex/redirect loops).
6. Re-fetch and confirm the canonical href matches the preferred URL.

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "Canonical is optional if the sitemap is clean." | Conflicting URL variants still split signals; self-referencing canonicals matter. |
| "A 302 is fine for a permanent host move." | Use 301/308 for permanent consolidations. |
| "Parameters can all stay indexable." | Facets/sort params often create duplicates — consolidate or noindex carefully. |

## Red Flags

- Inventing ranking factors not documented by Google
- Skipping verification ("looks fine")
- Advising spammy shortcuts (cloaking, doorways, link schemes)

## Verification

- [ ] Preferred URL documented
- [ ] Self-referencing canonical present on preferred URL
- [ ] Sitemap and major internal links agree
