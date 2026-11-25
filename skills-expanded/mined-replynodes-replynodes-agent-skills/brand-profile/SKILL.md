---
name: brand-profile
description: "Internal: brand profile guidance, merged into brand-kit. For a known domain, use brand-kit's free, read-only brand host; this slug is not a separate public successor."
license: MIT
compatibility: "The free one-domain brand host needs only network access; the optional authenticated MCP route requires an MCP-capable agent and REPLYNODES_API_KEY in a secret store."
metadata:
  internal: true
  author: ReplyNodes
  version: "1.1.0"
  endpoint: https://brand.replynodes.com
  mcp_endpoint: https://mcp.replynodes.com/mcp
  keywords: [brand profile, brand identity, internal, merged, brand-kit]
---

# ReplyNodes brand profile (internal)

This is an internal compatibility skill. Agent-skills issue #57 (canonical
taxonomy #56) merged `brand-profile` guidance into the canonical
[`brand-kit`](../brand-kit/SKILL.md) skill. The public successor is
**`brand-kit`**.

## What to do instead

For a single known domain, request the free, zero-auth brand host — no API key,
account, signup, MCP server, or credits are required:

```bash
curl --fail-with-body https://brand.replynodes.com/replynodes.com
```

Send a bare public domain only — no scheme, port, path, query, or credentials.
`www.` and a trailing slash are normalized. `GET https://brand.replynodes.com/`
returns a small usage document. Append `.json` for the machine-readable
readback. The canonical contract is the
[Brand intelligence guide](https://docs.replynodes.com/docs/guides/brand-intelligence),
and the full response shape and field list live in
[`brand-kit`](../brand-kit/SKILL.md).

## Anonymous limits and errors (reconciled to production)

The brand host shares the anonymous quota with the Markdown host: **20 admitted
requests per trusted client-IP bucket per UTC day**, with `X-RateLimit-Limit`,
`X-RateLimit-Remaining`, and `X-RateLimit-Reset` on every anonymous response.
Over the limit the response is HTTP `429 anonymous_limit_reached` with a
`Retry-After` header and a `continuation` object pointing at
<https://docs.replynodes.com/docs/auth> (an existing authenticated free account
has 500 credits). Standard outcomes are `400 invalid_request`,
`405 method_not_allowed`, `502 upstream_unavailable`, `503 degraded`
(fail-closed), and `504 gateway_timeout`. Earlier guidance describing a
per-minute IP limit and a `429 rate_limited` envelope was superseded by the
shared anonymous daily quota shipped in fetcher #715/#727.

## Optional authenticated continuation

The same upstream capability backs the keyed `/v1/brand/*` routes. Use
`https://mcp.replynodes.com/mcp` with `Authorization: Bearer ${REPLYNODES_API_KEY}`
in a secret store, or the REST origin `https://api.replynodes.com` with the same
bearer key, for authentication, billing, bulk, or programmatic access. Never
paste, expose, or log the key; run `initialize` and `tools/list` on MCP.

## Migration

`brand-profile` is not a public successor and is not deleted in issue #57; it is
retained as internal migration guidance pointing to `brand-kit`. Registry-side
unpublish/redirect and readback are owned by issue #58.
