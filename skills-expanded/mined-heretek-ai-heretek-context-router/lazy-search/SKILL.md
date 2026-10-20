# Lazy Search Skill

> Task-scoped skill for Goal 3a: discover backend MCP tools lazily through the
> 3 meta-tool broker (`mcp_search_tools`, `mcp_inspect_schema`, `mcp_call_tool`)
> instead of loading all 262,500 schema tokens upfront.

## When to mount

Mount this skill when the agent must find a backend capability (Android, Ghidra,
Godot, research) without dumping full schemas into context.

## Protocol

1. Call `mcp_search_tools` with a keyword query and optional profile filter
   (`core`, `appsec`, `android`, `game`, `research`).
2. Take only the top-K name/profile/one-line-summary hits.
3. Call `mcp_inspect_schema` for the single chosen tool.
4. Call `mcp_call_tool` with validated args; honor the circuit breaker
   (open 60s after 3 consecutive failures) and the role authorization gate
   (`qa-adversary` and `director` never call mutating tools).

## Invariants

- Never inline more than one full tool schema per turn.
- Never bypass the broker by addressing backend MCP servers directly.
- Fail closed: unknown tool names and unreachable backends are errors,
  never silent fallbacks.
