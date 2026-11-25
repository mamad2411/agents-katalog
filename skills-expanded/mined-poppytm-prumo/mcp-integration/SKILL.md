# MCP Integration

## Purpose
Expose semantic, bounded tools and resources over Model Context Protocol: well-named tools with JSON Schema I/O, paginated resources, typed error envelopes, and least-privilege scopes — never arbitrary shell or unrestricted filesystem access by default.

## Use when
- Adding an MCP server surface to an existing product (docs search, issue tracker, project data) for AI clients.
- Defining tool/resource naming, input schemas, pagination, and error contracts for an MCP integration.
- Scoping an MCP server's authority with OAuth scopes, per-tool permissions, and audit logging.
- Reviewing a third-party MCP server for over-broad tools before enabling it in a workspace.

## Do not use when
- Building the MCP server SDK, transports, or client toolkits themselves (use `mcp-tooling`).
- Designing a general plugin system without the MCP wire protocol (use `plugin-architecture`).
- Wiring raw REST/webhook integrations with no MCP layer involved (use `backend-api`).

## Required context
- MCP protocol version under test (e.g., `2025-06-18`) and client set (e.g., Harbor Desktop 3.1, CI agent runner).
- Domain operations to expose (e.g., 6 issue-tracker reads, 3 writes) with their current auth model and rate limits.
- Data-sensitivity map: which fields are internal-only and must never cross the tool boundary.
- Deployment topology: stdio-local vs remote Streamable HTTP, and the OAuth provider issuing scopes.

## Procedure
1. **Inventory candidate operations**: List every domain operation, then exclude by default anything executing code, opening shells, or writing outside the product database; the Harbor issue-tracker integration kept 9 of 23 candidates.
2. **Name tools semantically with schemas**: Register `issue_search`, `issue_get`, `issue_create` (verb-first, snake_case) each with strict JSON Schema I/O (`additionalProperties: false`, `maxItems: 50` on list inputs); resources use stable URIs (`tracker://issues/8821`) with `ETag` pagination cursors.
3. **Bound authority per tool**: Map each tool to minimal OAuth scopes (`tracker:read` for reads, `tracker:write` for creates); destructive tools require explicit `confirm: true` parameters and human-in-the-loop approval in the client policy.
4. **Return typed errors, never traces**: Emit MCP error envelopes `{ code: -32001, message: 'issue not found', data: { issueId: 8821 } }`; assert no stack traces, SQL, or internal hostnames leak by running the 40-case error-probe battery.
5. **Load-test and audit**: Drive 200 tool calls/min for 15 minutes asserting p95 latency under 800 ms and zero scope violations; enable per-call audit logs (tool, principal, args hash, 2026-09-16 sample retained 90 days).
6. **Document and verify**: Publish the tool catalog with examples and rate limits, complete `templates/mcp-integration-spec.md`, and run `scripts/verify.sh` to confirm artifact completeness.

## Decision rules
- **Deny by default**: New operations ship unexposed until reviewed; exposure is an explicit allow-list entry, never inheritance.
- **No god tools**: `execute_sql`, `run_shell`, or full-filesystem tools are forbidden on shared servers; split into narrow semantic tools.
- **Schemas are strict**: `additionalProperties: false` on all tool inputs; unknown fields reject rather than ignore.
- **Destructive calls confirm**: Writes that delete, publish, or spend require `confirm: true` plus client-side approval policy.
- **Errors carry no internals**: Any stack trace, SQL fragment, or internal hostname in a tool response fails the security gate.

## Evidence required
- Tool catalog document with names, JSON Schemas, scopes, and rate limits.
- Error-probe battery log: 40 cases, zero internal-detail leaks.
- Load-test report: 200 calls/min for 15 min, p95 under 800 ms, zero scope violations.
- Audit-log sample with tool, principal, and args-hash fields verified present.
- Completed `templates/mcp-integration-spec.md` with surface and verdicts.
- Passing execution log from `scripts/verify.sh`.

## Output contract
- MCP integration specification with tool catalog, schemas, scopes, and error contracts.
- Scoped server implementation with strict schemas, confirm gates, and audit logging.
- Probe, load, and audit evidence archived with the release under test.

## Stop conditions
- All exposed tools pass schema-strictness, scope, error-probe, and load gates with evidence.
- Zero god tools on the surface; every destructive tool carries a confirm gate.
- Token budget exhausted.
- Blocked on external dependency.

## Escalation rules
- Escalate to the security owner if a requested tool cannot be scoped safely (e.g., arbitrary query language); do not ship it unscoped.
- Escalate to product when client demand (e.g., bulk delete) conflicts with the confirm-gate policy; resolve in policy, not in code shortcuts.
- Escalate immediately on discovery of prompt-injection paths where tool descriptions or resource content could hijack client behavior.
