---
name: mcp-docs-and-implement
description: Implement using up-to-date docs or APIs via MCP. Use when the user wants to build something with current library/API docs (e.g. Context7, Stripe) and MCP is available.
---

# MCP Docs → Plan → Implement

This skill runs a workflow that uses **MCP** (Model Context Protocol) to fetch current documentation or API schemas, then plans and implements. Use when the project depends on external APIs or libraries and you want up-to-date references without pasting docs manually.

## MCP best practice: check tool schema first

Before calling any MCP tool, read the tool’s descriptor/schema (e.g. under `mcps/<server>/tools/<tool>.json`) so you use correct parameters and required fields. Do not guess; check the schema.

## Steps

1. **Fetch docs or schema via MCP**
   - Use MCP **tools** or **resources** to get current docs or API schema for the library/API the user asked about (e.g. Context7 for library docs, Stripe MCP for payments).
   - Use **resources** for read-only docs/data; use **tools** when you need to perform an action (query, API call). Check each tool’s schema before calling.

2. **Plan (optional)**
   - Optionally invoke the **planner** subagent with the fetched context to refine scope and steps (e.g. “what endpoints exist?”). Planner inherits MCP; it can call the same servers if needed.

3. **Implement**
   - Implement using the retrieved docs. Call MCP again during implementation if you need finer-grained details (signatures, options, examples).
   - Follow project rules. Prefer checking tool schema before each MCP call.

4. **Verify (optional)**
   - Optionally invoke the **verifier** subagent to confirm the implementation matches the docs or passes tool-based checks. Verifier can use MCP for compliance checks.

## Notes

- If the user only asked for docs lookup, stop after step 1 and present what was fetched.
- **MCP rule:** Use `@mcp-patterns` for server setup, check-tool-schema, and MCP hooks. See [.cursor/rules/mcp-patterns.mdc](../../rules/mcp-patterns.mdc).
- **Optional agent:** You can invoke the **mcp-docs-helper** subagent to fetch and summarize docs via MCP, then use the summary for planning or implementation.
- Subagents (planner, verifier, mcp-docs-helper) inherit MCP from the parent.
- **MCP hooks:** For audit or gate, use [.cursor/hooks/examples/mcp-hooks.example.json](../../hooks/examples/mcp-hooks.example.json) and [.cursor/hooks/advanced/mcp-audit.sh](../../hooks/advanced/mcp-audit.sh). See the mcp-patterns rule.
- Written workflow: [examples/agent-frameworks/mcp-docs-and-implement.md](../../../examples/agent-frameworks/mcp-docs-and-implement.md).
