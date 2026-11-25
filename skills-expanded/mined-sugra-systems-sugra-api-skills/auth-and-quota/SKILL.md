---
name: auth-and-quota
description: Authenticate to Sugra over HTTPS and MCP and stay inside the daily quota. Use when setting up a client or when a call returns 401, 403, missing_api_key, missing_bearer_token, or 429.
license: MIT
---

# Auth and quota

One key. Two header shapes. Volume gating only: every plan sees every endpoint. Plans and errors on https://docs.sugra.ai (search Authentication, Rate limits).

Issue a key at https://app.sugra.ai/settings/billing. Prefix `sugra_...`. Do not log it.

| Plan | Requests / day |
|---|---|
| Free | 50 |
| Dev | 5,000 |
| Pro | 50,000 |

Some bulk endpoints cost more than 1 request. HTTP reports `X-RateLimit-Cost`. MCP `describe_endpoint` `agent_hints.bulk_cost` warns before the call.

## HTTPS API

```
x-api-key: sugra_...
```

Not `Authorization: Bearer` on `https://sugra.ai`.

Every data response also carries `X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset` (UTC), `X-RateLimit-Cost`.

## MCP

| Transport | Client auth | Process env |
|---|---|---|
| Hosted `https://mcp.sugra.ai/mcp` | `Authorization: Bearer` (raw key or OAuth JWT) | n/a |
| Local stdio | none on the wire | `SUGRA_API_KEY` in the server process |
| Self-hosted HTTP | client Bearer; process `SUGRA_API_KEY` is only a downstream fallback | |

OAuth JWT: audience `https://app.sugra.ai/mcp` on both MCP hosts, scope `sugra:read`. Hosted discovery is public. `tools/call` and `resources/read` return 401 `missing_bearer_token` without Bearer.

Stdio catalog tools (`search_endpoints`, `describe_endpoint`, `list_toolsets`, `list_sources`) work without a key. `call_endpoint`, `fetch_data`, and entity tools return `missing_api_key` until `SUGRA_API_KEY` is set.

MCP tool JSON does not forward `X-RateLimit-*`. On 429 wait for `retry_after` (seconds). Downstream MCP still calls the API with `x-api-key`.

## Errors

| Signal | Meaning | What to do |
|---|---|---|
| HTTP 401 / MCP `missing_api_key` / `missing_bearer_token` | missing or invalid credential | stop. Do not retry the same call. |
| HTTP 403 | key cannot use this route | stop. |
| HTTP 429 / MCP 429 | quota exhausted | wait until `X-RateLimit-Reset` or `retry_after`. |
| HTTP 5xx / MCP `upstream_*` | platform or upstream fault | retry once with backoff. Then report. |

Do not retry 4xx except 429 after the reset.
