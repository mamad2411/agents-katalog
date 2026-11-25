---
name: permalink-ownership-gateway
description: Move SEO permalink fragments into seoPermalink documents and wire gateway lookup routes for operational SEO URLs.
intent: >-
  Use when implementing or validating SEO permalink ownership, deterministic ID generation, stale cleanup, and gateway document lookup mappings.
type: workflow
---

# Permalink Ownership and Gateway

## Ownership Model

- Store SEO-owned permalinks in `seoPermalink` docs.
- Set `owner = seo`.
- Keep `search.seo.<lang>` payload free of permalink fragments.

## Checklist

1. Define/validate `seoPermalink` documentType schema.
2. Ensure `generatePageSEO` builds desired permalink set per ad/lang.
3. Upsert changed/missing seo-owned permalink docs.
4. Delete stale seo-owned permalink docs not in desired set.
5. Register gateway `/seo/:${lang}/profile/...` mappings for expected segment depth.
6. Ensure mapping lookup uses `documentType = seoPermalink` and resolves to `ad_view`.

## Operational Notes

- Launch reload should rebuild permalink index.
- After destructive regen, compute/search repopulation is required before live permalink checks.
