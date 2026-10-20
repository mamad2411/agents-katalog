---
name: wp-abilities-mcp-development-mcp-exposure
description: Designs WordPress MCP Adapter exposure and transport. Use when choosing the default server, a custom server, tools/resources/prompts, HTTP or STDIO, dependency setup, or client configuration.
---

# MCP Exposure

## Process

1. Confirm the Ability contract and permission tests are complete.
2. Decide whether MCP exposure is necessary.
3. Choose default layered server or custom curated server.
4. Choose tool, resource, or prompt based on semantics.
5. Choose local STDIO or remote HTTPS transport.
6. Choose dedicated user and minimum capabilities.
7. Configure dependencies and autoloading without version conflicts.
8. Keep secrets and environment-specific values outside the plugin repository.
9. Test discovery, invocation, permissions, output, and transport failure.
10. Follow `workflows/expose-ability-via-mcp-workflow.md`.
11. Use `resources/mcp-exposure-decision-matrix.md`.

Examples:

- `examples/custom-mcp-server.md`
- `examples/client-configuration.md`
