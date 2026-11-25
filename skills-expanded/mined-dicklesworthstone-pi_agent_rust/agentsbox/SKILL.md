---
name: agentsbox
description: >-
  Discovers and executes MCP tools on-demand via agentsbox_* tools.
  Use when you need to find the right tool, when a user asks to use a tool
  you don’t have in context, or when troubleshooting MCP/tool availability.
license: MIT
metadata:
  author: agentsbox
  version: "0.1"
---

# agentsbox

Minimize context bloat by using a small, stable tool surface:

- `agentsbox_search_bm25` (natural language)
- `agentsbox_search_regex` (pattern search)
- `agentsbox_execute` (run discovered tool)
- `agentsbox_status` (health/status)
- `agentsbox_perf` (performance)
- `agentsbox_test` (tool verification)

## Workflow

1. **Search first**
   - If you don’t know the exact tool name: `agentsbox_search_bm25`.
   - If you know server prefix / partial name: `agentsbox_search_regex`.

2. **Inspect schema**
   - From search results, read `schema` and required fields.

3. **Execute**
   - Call `agentsbox_execute({ toolId, arguments })`.
   - `toolId` format: `{serverName}_{toolName}`.
   - `arguments` is a JSON string (or omit / `{}` when none required).

4. **Troubleshoot**
   - If tool not found: widen search, verify server prefix, try BM25.
   - If execution fails: run `agentsbox_status({})` and include server diagnostics.

## Examples

### Search the web with tavily

1) Search:

```text
agentsbox_search_bm25({ "text": "search the web for information", "limit": 5 })
```

2) Execute:

```text
agentsbox_execute({
  "toolId": "tavily_tavily_search",
  "arguments": "{\"query\":\"latest AI news\",\"max_results\":5}"
})
```

## Edge cases

- **Empty or missing servers**: `agentsbox_status` will show zero configured servers.
- **Schema mismatch**: prefer passing only required fields first.
- **Server name/tool name ambiguity**: use regex to list server tools: `"server_.*"`.
