---
name: find-api
description: Find the right API for a task — search the apis.io catalog, inspect the strongest candidates, and recommend one with its spec and links. Use when the user asks what API to use for something, or whether an API exists for a job.
license: CC-BY-NC-SA-4.0
---

# find-api

Turn a fuzzy need into one concrete, defensible recommendation grounded in the catalog —
not a web guess, and not a link dump.

## When to use this skill

Use when the user says "find an API to do X", "what should I use for Y", or "is there an API
for Z". If they only want a list, use `search-apis`.

## The v1 API

Base `https://apis.io/api/v1`. Every call below is **free**, no key required.

| Step | Call | Why |
|---|---|---|
| 1. Search | `GET /search?q=<task>` | Ranked APIs, providers, and tags in one call. |
| 2. Inspect | `GET /apis/{aid}` | Full record for a candidate. aid = `provider:api-slug`. |
| 3. Artifacts | `GET /apis/{aid}/artifacts` | What it actually publishes — spec, auth, pricing, MCP. |
| 4. Alternatives | `GET /apis/{aid}/similar` | Round out the comparison before committing. |
| 5. Band | `GET /resolve?identifier=<domain>` | Free quality band + composite for the provider. |

### Reading the search response

`/search` returns **sections**, not a `data` array. This is the one endpoint that breaks the
standard envelope:

```bash
curl -s "https://apis.io/api/v1/search?q=send+sms" \
  | jq '[.apis.top[] | {aid, name, provider_slug, artifact_types, artifact_count}]'
```

`.data[]` is empty here — use `.apis.top[]`, `.providers.top[]`, `.tags.top[]`. Every other
endpoint in this skill does use `{meta, data}`.

## Recipe

```bash
# 1. Candidates
curl -s "https://apis.io/api/v1/search?q=send+sms" \
  | jq '{n: .apis.total, top: [.apis.top[] | {aid, name, provider_slug, artifact_count}]}'

# 2. Inspect the leading pick
curl -s "https://apis.io/api/v1/apis/brevo:brevo-transactional-sms-api" \
  | jq '{name, description, tags, artifacts: [.properties[].type]}'

# 3. Alternatives before committing
curl -s "https://apis.io/api/v1/apis/brevo:brevo-transactional-sms-api/similar?limit=5" \
  | jq '.data[] | {aid, name}'
# `similar` is tag-based — thinly-tagged APIs return meta.total 0. Fall back to
# /search on the same capability, or /providers/{slug}/similar.

# 4. How good is the provider? (free — resolve returns the band)
curl -s "https://apis.io/api/v1/resolve?identifier=brevo.com" \
  | jq '{slug, band, composite}'
```

MCP equivalents (`https://apis.io/mcp`): `apis_io_search`, `get_api`, `get_api_artifacts`,
`find_similar_apis`, `resolve`. Or start from the `find_api` prompt.

## How to pick

Rank on evidence you can see, in this order:

1. **Does it publish a spec?** `properties[]` or `artifact_types` containing `OpenAPI`,
   `AsyncAPI`, or `GraphQL`. An entry with no machine-readable description is a profile, not
   an adoptable API.
2. **Quality band** from `/resolve` — `exemplar` beats `strong` beats the rest.
3. **Artifact depth** — `artifact_count`, and whether auth, pricing, and rate limits are
   documented. A provider that publishes `Plans`, `RateLimits`, and `Authentication` is one
   you can actually budget and ship against.
4. **Agent-readiness**, if that's the job — look for `MCP`, `MCPServer`, `AgentSkill`,
   `LLMsTxt` in `artifact_types`.
5. **Stated constraints** — region, compliance, must-use vendors. These override the above.

## Output format

Recommend **one** API, then list two alternatives:
- Name + provider, one line on what it does
- Its apis.io URL (`https://apis.io/apis/{provider_slug}/{slug}/`) and its spec URL
- Band/composite if you fetched it
- Why it beat the alternatives, in one sentence

Be decisive. The point of this skill is a pick, not a menu.

## Errors

All free. HTTP 402 means you reached a Pro endpoint (`/ratings`, `/compare`, `/gaps`) — the
body carries `error`, `detail`, `tier`, `plans`. Fall back to `/resolve` for a free band, or
surface the upgrade link. Don't retry a 402.

## Related skills

- `search-apis` — the broader list this narrows from.
- `resolve-provider` — when the user names a company or URL rather than a capability.
- `integrate-provider` — once picked, onboard end-to-end.
- `fetch-api-spec` — read the chosen spec.
- `shortlist-vendors` — Pro, when the decision needs scored comparison.
