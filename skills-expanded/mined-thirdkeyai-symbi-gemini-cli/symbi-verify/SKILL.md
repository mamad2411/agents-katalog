---
name: symbi-verify
description: Verify MCP tool schemas using SchemaPin cryptographic verification. Use when adding new MCP servers, auditing existing tool integrations, or checking tool integrity.
---

# SchemaPin Verification

Verify the cryptographic integrity of MCP tool schemas to ensure they haven't been tampered with.

## Verification Process

1. Identify the MCP server to verify (from the extension manifest or the user's request)
2. Use the `symbi__verify_schema` tool to check the schema
3. Report the verification result:
   - **Verified**: Schema signature matches the publisher's key
   - **TOFU**: First-time use, key has been pinned for future verification
   - **Failed**: Schema has been modified since signing -- DO NOT USE
   - **No signature**: Schema is unsigned -- warn the user about risks

## When to Verify

- Before first use of any new MCP tool
- After updating MCP server configurations
- When security audit is requested
- When a tool returns unexpected results

## Note on Tool Names

In Gemini CLI, MCP tools are prefixed with the server alias and double underscore.
The symbi MCP tools are accessed as `symbi__verify_schema`, `symbi__list_agents`, etc.
