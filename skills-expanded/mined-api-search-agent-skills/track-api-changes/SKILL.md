---
name: track-api-changes
description: Monitor the apis.io catalog for providers added or updated and for rating movement, across a chosen set or the whole network. Use for ongoing vendor monitoring. Pro tier.
license: CC-BY-NC-SA-4.0
---

# track-api-changes

**Description:** Monitor the catalog for change — providers added/updated and rating movement — for a chosen set or the whole network.

> **Pro tier.** The changes, movers, and rating-history endpoints require an apis.io Pro API key. See https://apis.io/developer/plans/.

## When to use this skill

Use for ongoing monitoring: "what changed since last month", "which vendors are improving or slipping", "watch these providers for me". This produces a change digest — new, moved-up, moved-down, and anything worth acting on.

## The v1 API

Base URL: `https://apis.io/api/v1`. Send `x-api-key: <key>`.

| Step | Call | Why |
|---|---|---|
| 1. Changes | `GET /changes?since=YYYY-MM-DD` | Providers added/updated + rating up/down since a date. |
| 2. Movers | `GET /ratings/movers` | Biggest up/down movers vs the previous scoring build. |
| 3. Per provider | `GET /providers/{slug}/rating/history` | A watched provider's current vs previous-build score. |

MCP equivalents: `whats_changed`, `find_rating_movers`, `get_rating_history`. There's also the `apis://changes` resource (last-30-days feed). Or run the `track_provider_changes` prompt.

## Recipe

```bash
# 1. What changed
curl -s -H "x-api-key: $APISIO_KEY" \
  "https://apis.io/api/v1/changes?since=2026-06-01" | jq '.counts'

# 2. Biggest movers
curl -s -H "x-api-key: $APISIO_KEY" \
  "https://apis.io/api/v1/ratings/movers?limit=10" | jq '{up:[.up[].slug],down:[.down[].slug]}'

# 3. Trend for a watched provider
curl -s -H "x-api-key: $APISIO_KEY" \
  "https://apis.io/api/v1/providers/twilio/rating/history" | jq '{current,previous,delta}'
```

## Output format (recommended)

A change digest:
- **New** — providers/APIs added in the window.
- **Up / Down** — biggest rating movers, with the delta.
- **Watched** — per-provider trend for the user's set.
- **Act on** — anything that warrants attention (a dependency slipping a band, a new entrant).

Note: apis.io tracks the current score plus week-over-week movement, not a full time series — history is current vs the implied previous point.

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

- `audit-api-estate` — the point-in-time snapshot this skill watches over time.
- `shortlist-vendors` — when a provider slips and you need a replacement.
