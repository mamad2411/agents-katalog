# AGENTS.md — src/providers/search/kagi/

## Purpose
Kagi search adapter. High-signal curated index — fewer results, generally higher quality.

## Vendor

- **Vendor**: Kagi
- **Endpoint**: `GET https://kagi.com/api/v0/search?q=...`
- **Auth**: `Authorization: Bot <KAGI_API_KEY>` (note: `Bot`, not `Bearer`)
- **Env var**: `KAGI_API_KEY` (shared with `../../ai_response/kagi_fastgpt/`)
- **Returns**: `{ title, url, snippet, source_provider: "kagi" }[]`
- **Default limit**: 20 results.

## Conventions / Invariants

- Implements `SearchProvider`.
- Uses the shared search-operator parser so `site:`, `filetype:`, `intitle:` etc. are encoded into the `q` string.
- Filters Kagi's response shape `data: [{ t: 0, ... }]` to type-`0` web results (Kagi also returns related-search and feature blocks at other type values).

## Related

- Registered as `kagi` in `../../unified/web_search.ts`.
- Sister module: `../../ai_response/kagi_fastgpt/`.
