---
name: connect
description: Attach a client to Sugra over HTTPS or MCP. Use when setting up Claude Desktop, Claude Code, ChatGPT, claude.ai, Cursor, VS Code, Gemini CLI, Grok, OpenBB, a custom HTTP agent, or self-hosted MCP.
license: MIT
---

# Connect

Same key for every path: https://app.sugra.ai/settings/billing, prefix `sugra_...`. Do not log it. Client JSON blocks: [references/clients.md](references/clients.md).

## 1. HTTPS API

```
GET https://sugra.ai/api/v1/...
x-api-key: sugra_...
```

System endpoints (`/health`, `/about`, `/services`, `/sources`, `/openapi.json`) need no key. Recipes: https://github.com/Sugra-Systems/sugra-api-cookbook. Endpoint detail: https://docs.sugra.ai.

## 2. Hosted MCP

Canonical: `https://mcp.sugra.ai/mcp`
Permanent alias: `https://app.sugra.ai/mcp`

Auth: `Authorization: Bearer sugra_...` or OAuth (audience `https://app.sugra.ai/mcp`, scope `sugra:read`). Discovery is public. `tools/call` and `resources/read` need Bearer.

claude.ai: Settings -> Connectors -> Add custom connector.
ChatGPT: install skills from the Plugins Directory (https://chatgpt.com/plugins/plugins_6aa4f7db79848191a81e4048990545ef). Hosted MCP tools: Settings -> Connectors -> Add MCP server.

Hosted tools: 8 gateway plus 3 composed (`resolve_entity`, `get_snapshot`, `get_timeseries`). Confirm with live `tools/list`.

## 3. Local MCP stdio

```bash
pip install sugra-api-mcp
export SUGRA_API_KEY=sugra_...
```

Eight gateway tools. Catalog search works without the key; `call_endpoint` / `fetch_data` / entity tools return `missing_api_key` until it is set. If the console script is not on PATH: `"command": "python", "args": ["-m", "sugra_api_mcp"]`.

Package CLI: `sugra-api-mcp doctor`, `search`, `describe`, `call`.

Claude Desktop, Claude Code, Gemini CLI, Cursor, VS Code, and similar IDEs use the stdio block in [references/clients.md](references/clients.md), or the hosted URL with Bearer.

## 4. Self-hosted MCP HTTP

```bash
sugra-api-mcp --transport streamable-http --port 8001
```

Eight tools, not the hosted-only three. Operator CORS/host/OAuth: `docs/self-hosting.md` in `sugra-api-mcp`. Do not put `INTERNAL_API_TOKEN` or JWKS URLs in a skill or chat.

## 5. OpenBB

Public extension `openbb-sugra` uses the HTTPS API, not MCP.

## Pick

| Host | Typical attach |
|---|---|
| Script, custom agent, OpenBB | HTTPS `x-api-key` |
| ChatGPT | Plugins Directory listing plus hosted MCP |
| claude.ai | Hosted MCP connector |
| Claude Desktop / Code, Cursor, VS Code, Gemini CLI, Grok | stdio package or hosted MCP |
| Own HTTP MCP process | self-host |
