---
name: discover-apis-io
description: Learn how to read the apis.io API catalog — the v1 REST API, the MCP server, and the markdown mirror of every page — so other skills can find APIs without scraping HTML. Use this first when the user mentions apis.io or asks to discover APIs across a catalog.
license: CC-BY-NC-SA-4.0
---

# discover-apis-io

Prime an agent with the three machine-readable ways into the apis.io catalog, so every
follow-on skill spends its tokens on answers instead of on HTML.

## When to use this skill

Use first when the user mentions apis.io, asks about API discovery, or wants to find APIs
across a catalog. Every other apis.io skill assumes the conventions below.

## Three ways in — pick one

| Path | Use when | Base |
|---|---|---|
| **MCP server** | The agent can connect to MCP. Best option — typed tools, no URL building. | `https://apis.io/mcp` |
| **v1 REST API** | No MCP, or you want raw JSON in a script. | `https://apis.io/api/v1` |
| **Markdown pages** | You already have a page URL and just want the prose. | append `index.md` to any page URL |

Never scrape the HTML pages, and never try to download the whole catalog — there is no
bulk dump to filter client-side. Query the API.

### MCP

Endpoint `https://apis.io/mcp`. Start with the `apis_io_search` tool, or one of the guided
prompts (`find_api`, `provider_overview`, `integrate_provider`, `agent_readiness_scan`,
`improve_my_score`). `prompts/list` shows every prompt including Pro ones.

### v1 REST API

Base `https://apis.io/api/v1`. No key needed for the free endpoints. Pass a Pro key as
`x-api-key: <key>`.

Collection endpoints all return the same envelope:

```json
{ "meta": { "total": 0, "page": 1, "limit": 25, "pages": 0, "query": {} },
  "data": [ ... ] }
```

Read `meta.total` for scale — never hardcode catalog counts, they move every build.

`/search` is the **one exception**. It returns sections, not `data`:

```json
{ "query": "sms", "per_section": 5,
  "apis":      { "total": 2548, "top": [ ... ] },
  "providers": { "total": 46,   "top": [ ... ] },
  "tags":      { "total": 12,   "top": [ ... ] } }
```

### Markdown pages

Append `index.md` to any catalog page URL for clean markdown:

```bash
curl -s https://apis.io/providers/twilio/index.md
curl -s https://apis.io/apis/twilio/twilio-a2p-api/index.md
```

An `Accept: text/markdown` header does **not** work — use the `index.md` suffix.

## Identifiers

- **Provider slug** — `twilio`, `stripe`. Used at `/providers/{slug}`.
- **aid** — `provider:api-slug`, e.g. `twilio:twilio-a2p-api`. Used at `/apis/{aid}`.
- Page URLs are `https://apis.io/providers/{slug}/` and `https://apis.io/apis/{slug}/{api-slug}/`.

**Always resolve first.** Users give you domains, URLs, and company names — not slugs.
`/resolve` is free and also hands back the quality band:

```bash
curl -s "https://apis.io/api/v1/resolve?identifier=twilio.com"
# {"slug":"twilio","name":"Twilio","website":"https://console.twilio.com",
#  "band":"exemplar","composite":73.8,"match":"identity_link"}
```

The parameter is `identifier`, not `q`. It accepts a domain, a URL, or a GitHub org.

## Free vs Pro

Discovery is free: search, apis, providers, artifacts, specs, onboarding, MCP servers,
skills, resolve. Ratings, comparison, gaps, scopes, security, insights and export are Pro.

A gated call returns HTTP 402 with a machine-readable body — surface the upgrade link, do
not retry:

```json
{ "error": "upgrade_required",
  "detail": "Provider ratings requires the Pro or Business tier.",
  "tier": "pro",
  "plans": "https://apis.io/developer/plans/" }
```

Errors use the same shape with `error` / `detail`. On 429, back off — don't hammer.

## What the catalog holds

Every provider is profiled across dozens of artifact types, not just OpenAPI:
OpenAPI, AsyncAPI, GraphQL, Postman, Arazzo, APIsJSON, JSONSchema, JSONStructure, JSONLD,
Rules, Scopes, Security, Authentication, Plans, Pricing, FinOps, RateLimits, Documentation,
ChangeLog, Lifecycle, LLMsTxt, MCP, MCPServer, AgentSkill, CLI, Packages, and more.

Ask a provider what it publishes rather than assuming:

```bash
curl -s "https://apis.io/api/v1/providers/twilio/artifacts" | jq '.artifact_types'
```

## Other discovery surfaces

- `https://apis.io/.well-known/api-catalog` — an RFC 9264 linkset **describing the network
  itself** (~14 entries: the API, the MCP server, the skills, the section indexes). It is a
  signpost, not a data dump. Do not try to filter it for individual APIs.
- `https://apis.io/sitemap_index.xml` — per-section sitemaps, for crawl-style discovery.
- `https://apis.io/robots.txt` — publishes `Content-Signal: search=yes, ai-input=yes, ai-train=yes`.

## Related skills

- `search-apis` — keyword search over the catalog.
- `resolve-provider` — turn a domain, URL, or company name into a catalog slug.
- `fetch-api-spec` — pull and parse an OpenAPI/AsyncAPI.
- `find-api` — turn a fuzzy need into one recommendation.
