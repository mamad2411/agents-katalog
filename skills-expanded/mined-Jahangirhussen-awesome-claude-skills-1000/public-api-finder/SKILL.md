---
name: public-api-finder
description: Use when the user wants to find, compare, or recommend a public/free API — e.g. "find a free weather API", "API with no auth", "compare finance APIs", "API for sending emails". Searches a local knowledge base built from the official Public APIs repository.
---

# Public API Finder

Local knowledge base of every API in the official [Public APIs repository](https://github.com/public-apis/public-apis), organized by category under `references/`.

## Entry point

Always start at `references/INDEX.md`. It lists every category, its API count, and the file to open.

## Search strategy

1. Read `references/INDEX.md` to find the matching category (or categories) for the user's request.
2. Open the relevant category file(s) under `references/`.
3. Search the API Directory table using: API name, Description, Auth, HTTPS, CORS.
4. For broad/ambiguous requests, check multiple relevant category files. Do not load every file — target the search.
5. Return the strongest matches only.

## Response format

Present candidates as a table:

| API | Best For | Auth | HTTPS | CORS | Documentation |
| :-- | :-- | :--: | :--: | :--: | :-- |

Then a short **Recommendation** section: the best match and a bullet-point reason (auth type, HTTPS/CORS support, fit to the use case).

Keep responses concise — no unnecessary explanation.

## Data integrity rules

- Never invent API information (auth type, CORS, HTTPS, pricing, rate limits, status).
- `—` in a table cell means the source had no value — do not guess a replacement.
- The reference files are the primary discovery source. For questions the files don't answer (current status, pricing, rate limits, up-to-date auth requirements), say the reference data doesn't cover it and offer to check the API's official documentation — clearly label that as externally verified, not from the source list.
- The reference files are a snapshot from generation time (see `Last Generated` in each file and `references/INDEX.md`). The upstream repo updates continuously — mention this if the user needs guaranteed current data.

## Updating the knowledge base

Re-fetch `https://raw.githubusercontent.com/public-apis/public-apis/master/README.md`, re-parse category tables (`### <Category>` sections with `API | Description | Auth | HTTPS | CORS` tables), and regenerate `references/*.md` + `INDEX.md`. Do not hand-edit entries — always regenerate from source to keep data faithful.

## Purpose
Find, compare and recommend free/public APIs for a need.

## When NOT to use
- Paid enterprise API selection.

## Inputs
Need, auth constraints, rate limits.

## Edge cases and failure handling
- No public API fits -> say so and suggest scraping alternatives with caveats.

## Example
```text
"free weather API, no auth" -> Open-Meteo vs others.
```
