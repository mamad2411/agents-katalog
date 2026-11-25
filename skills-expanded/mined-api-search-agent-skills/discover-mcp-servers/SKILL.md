---
name: discover-mcp-servers
description: Find providers in the apis.io catalog that publish an MCP server, with the endpoint and install method, so you can plug real tools into an agent. Use when the user wants agent-ready tools rather than raw REST.
license: CC-BY-NC-SA-4.0
---

# discover-mcp-servers

Find the MCP servers a capability or a vendor already ships — the shortest path from catalog
to working agent tools.

## When to use this skill

Use when the user wants agent-ready tools: "which of these vendors has an MCP server",
"find MCP servers for payments", "what can I plug into my agent". For agent *skills* rather
than servers, use `discover-agent-skills`.

## The v1 API

Base `https://apis.io/api/v1`. All **free**. MCP is a first-class artifact type.

| Step | Call | Why |
|---|---|---|
| 1. Browse | `GET /mcp?q=<capability>` | Catalogued MCP servers, filterable by `q`, `tags`, `providers`. |
| 2. Per provider | `GET /mcp?providers={slug}` | Does this specific vendor ship one? |
| 3. Confirm | `GET /providers/{slug}/artifacts` | `artifact_types` will contain `MCP` and/or `MCPServer`. |

Standard envelope — `{ "meta": {...}, "data": [...] }`. Each record:

```json
{ "type": "MCP", "slug": "stripe", "name": "...", "provider_slug": "stripe",
  "provider_name": "Stripe", "description": "...", "tags": [...],
  "url": "https://mcp.stripe.com",
  "meta": { "install_method": "Hosted endpoint" } }
```

`url` is the endpoint or install target and `meta.install_method` tells you how to wire it —
those two fields are the payload. **`include=content` usually returns nothing** for MCP
records: most point at an HTML page, so the API sets `content_skipped: "not_machine_readable"`
and a `content_hint`. Fetch the `url` yourself if you need the manifest.

## Recipe

```bash
# 1. MCP servers for a capability
curl -s "https://apis.io/api/v1/mcp?q=payments&limit=10" \
  | jq '{n: .meta.total, servers: [.data[] | {provider_slug, name, url, install: .meta.install_method}]}'

# 2. Does this provider ship one?
curl -s "https://apis.io/api/v1/mcp?providers=stripe" \
  | jq '{n: .meta.total, servers: [.data[] | {name, url, install: .meta.install_method}]}'

# 3. Cross-check against everything the provider publishes
curl -s "https://apis.io/api/v1/providers/stripe/artifacts" \
  | jq '.artifact_types | map(select(. == "MCP" or . == "MCPServer"))'
```

MCP equivalents (`https://apis.io/mcp`): `find_mcp`, `get_provider_artifacts`,
`get_provider_tools`.

## Read the description before recommending

Not every record is a shipped, official server. The catalog also profiles **candidate** tool
surfaces derived from an API, and says so in the `description` — e.g. *"No official
hosted/remote MCP server was found … This is a CANDIDATE tool surface derived on…"*.

Check the description and `meta.install_method` before telling a user to connect. Report a
candidate as a candidate, not as an available server.

## Output format

For each server:
- Provider + server name
- The endpoint `url` and `meta.install_method` (hosted endpoint, npm package, registry entry…)
- Official vs candidate, per the description
- One line on wiring it in (transport, auth)

If the provider has no server, say so plainly and fall back to `integrate-provider` for raw
REST, or `discover-agent-skills` if a packaged skill exists instead.

## Errors

Free endpoint. HTTP 402 means you reached a Pro filter — body carries `error`, `detail`,
`tier`, `plans`. Don't retry.

## Related skills

- `find-api` — find the provider first.
- `discover-agent-skills` — packaged Agent Skills, the sibling of this.
- `agent-readiness-scan` — the full agent-readiness picture for one provider.
- `assemble-api-stack` — Pro, combine multiple providers into a toolset.
