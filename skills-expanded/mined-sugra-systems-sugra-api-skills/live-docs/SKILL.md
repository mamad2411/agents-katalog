---
name: live-docs
description: Find current Sugra documentation. Use when an endpoint, parameter, count, or version might be stale. Canonical docs are https://docs.sugra.ai (search and Ask AI). Also OpenAPI, /sources, /stats, the blog, and MCP tools/list.
license: MIT
---

# Live docs

https://docs.sugra.ai is the external documentation truth. It has search and Ask AI. Per-endpoint parameters, schemas, and examples live in its API Reference sidebar. This skill pack does not copy that catalog.

Entry on the API host: https://sugra.ai/docs (same site). Do not use `https://sugra.ai/doc`.

## How to read docs.sugra.ai

1. Open https://docs.sugra.ai (Welcome: directions, key, envelope, plans, MCP).
2. Search the docs site, or use Ask AI, for the operation or topic.
3. Open the endpoint page in API Reference before calling. Confirm method, path, parameters, and body.
4. If a page offers a Markdown view or `.md` URL, prefer that for a compact read.

Do not invent a path. Do not treat this SKILL.md, a README, or a cookbook recipe as the operation list.

## Machine companions (not a second docs site)

| URL | Role |
|---|---|
| `GET https://sugra.ai/openapi.json` | HTTP contract for the call |
| `GET https://sugra.ai/sources` | live source families |
| `GET https://sugra.ai/services` | service list |
| `GET https://sugra.ai/about` | product surface |
| `GET https://sugra.ai/health` | liveness |
| `GET https://sugra.ai/stats` | live counts |

Public copy still uses hedges (1,500+ / 160+ / 36). `/stats` is the live counter. The MCP wheel catalog can lag OpenAPI. If MCP search misses, search docs.sugra.ai, then OpenAPI, then say whether the operation exists.

MCP after connect: `initialize` (`serverInfo.version`), `tools/list`, `prompts/list`, `resources/list`.

## Other public surfaces (search these, not the open web first)

| Where | What |
|---|---|
| https://sugra.ai | product |
| https://sugra.systems | company, legal, API marketing, direction pages |
| https://sugra.systems/blog | blog index; article also as `/{slug}.md`; `llms.txt` |
| https://app.sugra.ai | keys, billing, playground |
| https://app.sugra.ai/settings/billing | issue a key |
| https://pypi.org/project/sugra-api-mcp/ | MCP package version |
| https://github.com/Sugra-Systems/sugra-api-mcp | MCP server |
| https://github.com/Sugra-Systems/sugra-api-cookbook | HTTP recipes |
| https://github.com/Sugra-Systems/openbb-sugra | OpenBB provider |

Legal: https://sugra.systems/terms-of-service and sibling policy pages. Contacts: `support@`, `legal@`, `privacy@`, `abuse@` sugra.systems.

Source names: live `/sources`. Sovereign, intergovernmental, and academic names are open. Commercial upstreams appear as Sugra Finance, Sugra News, Sugra Crypto, Sugra Forex, Sugra Weather.
