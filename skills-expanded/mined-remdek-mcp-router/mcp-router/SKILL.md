---
name: mcp-router
description: >-
  Use mcp-router to search and call downstream MCP tools without loading the
  full catalog. Triggers: search MCP tools, call a tool via router, large tool
  catalog, router status/health, search_servers, review/feedback after a call.
---

# mcp-router

Thin proxy: discover tools by query, then call them by `server_name` + `tool_name`.
Do **not** invent tool names — always search (or verify schema) first.

## When to use

- Prefer the router when many MCP servers/tools are registered and you need one capability.
- Skip the router for local file I/O (read/write/list in the workspace) — use native file tools.
- Do not dump every downstream tool into context; search is the index.

## Core loop

1. `search_tools(query, …)` → pick `server_name` + `tool_name`. Strong hits include
   `tool_schema`; weak hits set `schema_omitted=true` (identity + description only).
2. If the chosen hit omitted the schema → `get_tool_schema(server_name, tool_name)`
   (or re-search with `include_schema_for=["server:tool"]` / `include_schemas=true`).
3. `call_server_tool(server_name, tool_name, arguments)`.
4. If the call returns `output_guard.truncated=true`, use `full_output_path` /
   `artifact_id` (file under the router host’s `data/call_artifacts/`) for the
   full body — do not ask the model to re-fetch the whole payload inline.
5. If results look empty or degraded → `get_router_status`; to list servers → `search_servers`.

Keep `search_id` / `call_id` when you may `review` or `feedback` afterward.

## Which tool when

| Tool | Call when |
|------|-----------|
| `search_tools` | Need a capability; query in EN or RU; optional `limit`, weights, `max_per_server`, `include_schemas`, `include_schema_for` |
| `get_tool_schema` | Need full input schema for a weak search hit before calling |
| `call_server_tool` | After you know exact `server_name` + `tool_name` + args; huge results may be truncated (`output_guard`) |
| `search_servers` | Discover registered servers (not tools); quarantine marks `healthy=false`; backoff adds `failure_backoff="failed Ns ago: …"` |
| `get_router_status` | Empty/odd search, index not ready, reconnect / embedding / probe / failure_backoff questions |
| `review` | Rate one prior `call_id` **or** `search_id` (`useful` / `partly` / `not_useful` / `not_sure`) |
| `feedback` | Local quality/friction/other note; optional `call_ids` / `search_ids` |

`review` and `feedback` write locally only — they do **not** call downstream servers. Continue the task after sending them.

## Examples

Search then call:

```text
search_tools(query="web search current events", limit=5)
→ pick searxng:searxng_web_search
→ if schema_omitted: get_tool_schema("searxng", "searxng_web_search")

call_server_tool(
  server_name="searxng",
  tool_name="searxng_web_search",
  arguments={"query": "…"}
)
```

Health check after a miss:

```text
get_router_status()
→ check index_status, tool_count, failed / reconnect hints
```

## Failure hints

On failure (or degraded search), read typed fields — do not guess secrets or raw headers:

| Field | Meaning |
|-------|---------|
| `failure_kind` | e.g. `downstream_unreachable`, `auth_failed`, `index_degraded`, `tool_not_found`, `timeout`, `server_unhealthy`, `strict_denied`, `policy_denied` |
| `next_action` / `retry_hint` | Concrete next step |
| `reconnect_hint` | Where to look / what is wrong |

- Quarantined / unhealthy servers: skipped in `search_tools`; `call_server_tool` may return `server_unhealthy`.
- `policy_denied`: invoke-time policy blocked the call — finding a tool in search does **not** grant permission; check `permission.rule` / operator `INVOKE_POLICY`.
- Index pending/empty: follow `next_action`; often wait/reindex or check `get_router_status`.
- Never invent `server_name`/`tool_name` from memory if search disagreed.

## Out of scope

- No Docker/ops deep dive (see repo README / compose).
- No catalog of every downstream tool — use `search_tools`.
- Workspace Multica skill `mcp-tools` is separate (product-adjacent how-tos); this file is the **repo** skill for the router surface itself.
