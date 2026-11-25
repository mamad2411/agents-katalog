---
name: connectors
description: Discover and invoke deferred connector tools through tool_search, tool_describe, and tool_call; use code only for fan-out or local result reduction.
allowed-tools:
  - tool_search
  - tool_describe
  - tool_call
  - tool_run_code
---

## Deferred connector workflow

Connector tools are deliberately absent from the normal tool list: this keeps the
prompt cache-stable even while MCP servers connect or reconnect. Discover their
live catalog at runtime; never assume a configured source or tool name exists.

```text
tool_search()                         → sources currently ready to call
tool_search(source="<source>")        → names + short descriptions, no schema
tool_describe(names=["<tool>", ...])  → schemas for selected tools, batched
tool_call(name="<tool>", arguments={}) → invoke one selected tool
```

Use `tool_search(query="<keywords>")` when you know the capability but not its
source. The returned catalog is the only live truth. The following is merely a
shape example, not a claim that Playwright is configured:

```text
tool_search(source="playwright")
  → mcp__playwright__browser_click
tool_describe(names=["mcp__playwright__browser_click"])
  → inputSchema
tool_call(name="mcp__playwright__browser_click", arguments={ ...schema fields... })
```

Always describe a tool before its first call in the current task. Batch the
schemas for a small related workflow in one `tool_describe` call. A result may
contain an image; it is automatically returned as visual input in the following
message, so inspect it rather than asking for its base64 data.

## When to use code

Use individual `tool_call` calls for a short sequential workflow. Use
`tool_run_code` only when repeatedly calling tools over many objects (fan-out),
filtering a large result, or aggregating a long chain. Keep raw intermediate
results inside code and return a compact final value. If code returns an image
result, preserve its structured content; do not stringify image base64.
