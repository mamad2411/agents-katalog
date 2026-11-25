---
name: search-apis
description: Search the apis.io catalog for APIs, providers, and tags by keyword, capability, tag, or provider. Use when the user asks what APIs exist for something, which providers offer a capability, or wants to filter the catalog.
license: CC-BY-NC-SA-4.0
---

# search-apis

Keyword search across the apis.io catalog, returning structured matches you can hand to the
user or feed to another skill.

## When to use this skill

Use when the user asks "what APIs are there for X", "find an API to do Y", "which providers
offer Z", or anything else that means filtering the catalog. For a single decisive
recommendation, use `find-api` instead — it wraps this with inspection and a pick.

## Two calls

Base `https://apis.io/api/v1`. Both are **free**, no key required.

| Call | Use when |
|---|---|
| `GET /search?q=<query>` | You don't know whether the answer is an API, a provider, or a tag. One call, three ranked sections. |
| `GET /apis?q=<query>` / `GET /providers?q=<query>` | You know which you want and need the full paginated list. |

### `/search` — the exception to the envelope

It returns **sections**, not a `data` array:

```json
{ "query": "sms", "per_section": 5,
  "apis":      { "total": 2548, "top": [ { "aid": "brevo:brevo-transactional-sms-api",
                                           "name": "brevo Transactional SMS API",
                                           "description": "...",
                                           "provider_slug": "brevo",
                                           "tags": ["Transactional SMS"],
                                           "artifact_types": ["OpenAPI","Documentation","GraphQL","AsyncAPI"],
                                           "baseURL": "...", "humanURL": "...",
                                           "artifact_count": 4 } ] },
  "providers": { "total": 46, "top": [ ... ] },
  "tags":      { "total": 12, "top": [ ... ] } }
```

`return=apis` narrows which sections are populated — it does **not** flatten the response
to `.data`. Read `.apis.top[]`, not `.data[]`.

### `/apis` and `/providers` — the standard envelope

```json
{ "meta": { "total": 2548, "page": 1, "limit": 25, "pages": 102, "query": {...} },
  "data": [ ... ] }
```

Both accept `q`, `tags`, `limit`, `page`. `/apis` also accepts `providers`.

## Recipe

```bash
# One-shot: what exists for this capability?
curl -s "https://apis.io/api/v1/search?q=send+sms" \
  | jq '{apis: [.apis.top[] | {aid, name, provider_slug, artifact_types}],
         providers: [.providers.top[] | {slug, name}],
         tags: [.tags.top[] | .name]}'

# Full ranked list of APIs, paginated
curl -s "https://apis.io/api/v1/apis?q=send+sms&limit=10" \
  | jq '.meta.total, [.data[] | {aid, name, provider_slug}]'

# Scope to one provider
curl -s "https://apis.io/api/v1/apis?providers=twilio&limit=10" | jq '.data[].aid'

# Inspect a tag before filtering on it (detail object, not the list envelope)
curl -s "https://apis.io/api/v1/tags/payments" \
  | jq '{name, band, composite, provider_count, api_count, neighbors: [.neighbors[].tag]}'

# Then filter by it
curl -s "https://apis.io/api/v1/apis?tags=payments&limit=10" | jq '.data[].aid'
```

MCP equivalents (`https://apis.io/mcp`): `apis_io_search`, `find_apis`, `find_providers`,
`find_tags`. Or start from the `find_api` prompt.

## Handling the input

Users search with domains and company names as often as keywords. If the query looks like a
domain, URL, or GitHub org, call `/resolve?identifier=<value>` first — it returns the exact
slug plus the quality band, free. See `resolve-provider`.

## Output format

For each match give: API name, provider slug, its apis.io URL
(`https://apis.io/apis/{provider_slug}/{slug}/`), and what it publishes (`artifact_types`).
Lead with `meta.total` so the user knows how deep the catalog goes on their query.

Prefer entries with a populated `artifact_types` and a non-zero `artifact_count` — an entry
with neither is a thin profile, not a consumable API.

## Errors

Free endpoints. If you get HTTP 402 you've reached for a Pro filter — the body carries
`error`, `detail`, `tier`, and a `plans` link. Surface it, don't retry.

## Related skills

- `discover-apis-io` — the conventions this skill assumes.
- `resolve-provider` — domain or company name to catalog slug.
- `find-api` — search, inspect, and recommend one.
- `fetch-api-spec` — pull the OpenAPI for a hit.
