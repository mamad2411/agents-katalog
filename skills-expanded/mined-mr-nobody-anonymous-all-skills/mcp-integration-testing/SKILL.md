---
name: mcp-integration-testing
description: "Test MCP servers and their integrations: tool-schema contracts, transport handshakes, failure and timeout behaviour, permission scoping and end-to-end agent runs."
type: procedural
category: agents
domain: agents
version: 1.0.0
author: Mr-Nobody-Anonymous
license: MIT
risk: medium
level: advanced
triggers:
  - test mcp server
  - mcp tool schema validation
  - mcp server timeout handling
  - mcp integration test harness
  - verify mcp connector works
aliases:
  - mcp-testing
keywords:
  - mcp
  - integration-testing
  - json-rpc
  - tool-schema
  - transport
  - stdio
mcp_servers:
  - filesystem
  - github
  - playwright
source: custom
enabled: true
---

# MCP Integration Testing

## Purpose

Test MCP servers and their integrations: tool-schema contracts, transport handshakes, failure and timeout behaviour, permission scoping and end-to-end agent runs.

## When to Use

- A new MCP server is about to be added to a catalog or an agent config.
- An agent works locally but fails when a connector is installed.
- A server upgrade may have changed a tool schema or transport behaviour.

## When NOT to Use

- Only the agent prompt is changing, with no connector involvement.
- The server requires credentials no test environment has.
- The failure is clearly in the model, not the tool boundary.

## Capabilities

- Handshake over stdio or HTTP and assert the protocol version and capabilities.
- Validate every advertised tool schema against the spec before use.
- Exercise success, error, timeout and malformed-response paths.
- Verify permission scoping and that destructive tools require approval.
- Run the installed configuration end to end, not just the server in isolation.

## Inputs

- The server's launch command or URL and its required environment.
- The tools the agent is expected to call, with sample arguments.
- The failure semantics the agent must handle.

## Workflow

1. Start the server exactly as the generated harness config would.
2. Send `initialize`, then `tools/list`; snapshot the schema and diff it on upgrade.
3. Call a read-only tool with valid and invalid arguments; assert structured errors.
4. Simulate a timeout and a server crash; confirm the agent degrades instead of hanging.
5. Re-run the same flow through the installed harness config file.
6. Record the transcript as the regression fixture.

## Tools

- mcp
- pytest
- node
- playwright

## Examples

- `A tool that returns `{"error": "..."}` with HTTP 200 breaks agents that only check status; assert on content.`
- `A server needing `uvx` fails silently when the harness config forgot the command — test the generated config, not the source.`

## Safety

- Never run destructive tools against real systems in tests; use a sandbox or a stub.
- Do not commit transcripts containing tokens or customer data.

## MCP Requirements

| Server | Transport | Tier | Risk | Required env |
| :--- | :--- | :--- | :--- | :--- |
| `filesystem` | stdio | core | low | — |
| `github` | http | standard | medium | `GITHUB_PERSONAL_ACCESS_TOKEN` |
| `playwright` | stdio | standard | medium | — |

Install the connectors above with `allskills mcp install --harness <harness> --profile full`,
or list the same ids in your harness config. Full detail per server: [`docs/MCP-CATALOG.md`](MCP-CATALOG.md) and [`mcp/registry.json`](../mcp/registry.json).

## Source

All-Skills canonical library (`skills/agents/mcp-integration-testing`). First-party skill, maintained in this repository.

## Notes

- Schema diffs catch breaking upgrades that version numbers do not.
- Test the installed config: the catalog and the written config can diverge.
- Pairs with: `agent-reliability`, `mcp-security-review`.
