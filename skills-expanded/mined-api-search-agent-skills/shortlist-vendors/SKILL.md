---
name: shortlist-vendors
description: Turn one capability into a scored, compared vendor shortlist from the apis.io catalog, with a clear recommendation. Use for a buy decision on a single capability. Pro tier.
license: CC-BY-NC-SA-4.0
---

# shortlist-vendors

**Description:** Turn a single capability into a scored, compared vendor shortlist with a clear recommendation.

> **Pro tier.** Ratings and comparison endpoints require an apis.io Pro API key. See https://apis.io/developer/plans/.

## When to use this skill

Use for a buy decision on one capability: "shortlist email delivery vendors", "who should we use for KYC", "compare SMS providers for EU". This produces a defensible 3–5 vendor shortlist with scores and tradeoffs.

## The v1 API

Base URL: `https://apis.io/api/v1`. Send `x-api-key: <key>` for the Pro calls.

| Step | Call | Tier | Why |
|---|---|---|---|
| 1. Candidates | `GET /search?q=<capability>&return=providers` | free | Gather providers for the capability. |
| 2. Alternatives | `GET /providers/{slug}/similar` | free | Round out the candidate set. |
| 3. Score | `GET /ratings?band=exemplar,strong` / `GET /providers/{slug}/rating` | pro | Quality bands + six facets. |
| 4. Compare | `GET /compare?providers=a,b,c` | pro | Side-by-side facet leaders + artifact matrix. |

MCP equivalents: `apis_io_search`, `find_similar_providers`, `find_ratings`, `get_provider_rating`, `compare_providers`. Or run the `vendor_shortlist` / `find_alternatives` prompts.

## Recipe

```bash
# 1-2. Build the candidate set.
# NOTE: /search returns SECTIONS, not `.data` — read `.providers.top[]`.
curl -s "https://apis.io/api/v1/search?q=email+delivery" \
  | jq -r '.providers.top[].slug'

# Or use the paginated list endpoint, which does use the standard {meta,data} envelope:
curl -s "https://apis.io/api/v1/providers?q=email+delivery&limit=8" | jq -r '.data[].slug'

# Free quality band per candidate, before spending a Pro call:
for s in sendgrid mailgun postmark; do
  curl -s "https://apis.io/api/v1/resolve?identifier=$s" | jq -c '{slug, band, composite}'
done

# 4. Compare the top candidates
curl -s -H "x-api-key: $APISIO_KEY" \
  "https://apis.io/api/v1/compare?providers=sendgrid,mailgun,postmark" \
  | jq '{best_overall,facet_leaders}'
```

## Output format (recommended)

A shortlist of 3–5, each with:
- Composite score + band
- Artifact coverage (OpenAPI, MCP, SDKs, pricing…)
- A one-line tradeoff

End with a single recommended pick and the reason. Honor stated constraints (region, compliance, must-use).

## Errors and tiering

Send the key as `x-api-key: <key>`. Without one, or on a lower tier, gated calls return
HTTP **402** with a machine-readable body:

```json
{ "error": "upgrade_required", "detail": "...", "tier": "pro",
  "plans": "https://apis.io/developer/plans/" }
```

Surface `detail` and the `plans` link — never retry a 402, and never fabricate the numbers
the gated call would have returned. Where a free fallback exists, take it and say you did:
`/resolve?identifier=<domain>` returns a provider's `band` and `composite` at no tier.

Response shapes for the gated endpoints are not pinned in the published OpenAPI. Inspect the
first response (`jq 'keys'`) before assuming a field path.

## Related skills

- `assemble-api-stack` — when you need multiple capabilities, not one.
- `audit-api-estate` — score/gap vendors you already use.
