---
name: build-mcp-server
description: Scaffolds and implements a new Model Context Protocol (MCP) server. Use when exposing new backend tools or resources to AI agents.
version: 1.0.0
allowed-tools: [read_file, write_file, edit_file, create_file, search_code, mcp_call, run_tests, execute_command]
---

# Build MCP Server

Use this skill to create standard-compliant MCP servers that expose system capabilities securely to AI agents.

## Core Rules

- **Schema-First**: Define all tool inputs and outputs using Zod or Pydantic schemas as the absolute source of truth; generate JSON Schema 2020-12 from these definitions for protocol compliance
- **Stateless Server Guarantee** (July 2026 MCP spec): MCP server instances must not store in-memory session state — all context must be passed in the request or persisted externally (Redis, Durable Objects); this enables deployment on serverless edge runtimes (Cloudflare Workers, AWS Lambda)
- **Transport Selection**: Use **Streamable HTTP** for remote/cloud deployments; use **stdio** exclusively for local IDE/CLI tools — in stdio mode, `stdout` is strictly reserved for JSON-RPC 2.0 frames; all logs must route to `stderr`
- **Header-Based Routing**: Pass tool method and name in HTTP headers (`Mcp-Method: tools/call`, `Mcp-Name: create_invoice`) to enable API gateway rate limiting and authorization without body parsing
- **Versioning**: Apply SemVer 2.0 to tool names; treat tool names as immutable public contracts — breaking schema changes require major version increments with dual-version deprecation windows
- **Security**: Implement OAuth 2.1 with PKCE Bearer token validation for HTTP-transport servers; apply tenant scoping and **least-privilege mutation gating** — destructive tools (write, delete, send) require explicit authorization and confirmation tokens; read-only tools may be open by default
- **Telemetry**: Emit an OTel span for every `tools/call` execution with `mcp.tool_name`, `mcp.transport_type`, duration, and outcome; never log sensitive payload data or auth credentials in trace attributes

## Suggested Process

### 1. Define Server Scope & Tool Contracts

Identify the capabilities, resources, and tools the MCP server will provide. For each tool:
- Define strict input schemas using Zod (TypeScript) or Pydantic (Python).
- Document clear, unambiguous tool descriptions so AI agents choose tools accurately.
- Specify returned output schemas and error response shapes.

### 2. Scaffold Server Runtime & Transport

Initialize the MCP server using the official SDK (`@modelcontextprotocol/sdk` or `mcp` Python package):
- Configure standard transports: stdio for local agent execution, streamable HTTP with SSE headers (`Accept: text/event-stream`) for remote service deployment.
- Declare server metadata (`name`, `version`) and capabilities (`tools`, `resources`, `prompts`).

### 3. Implement Tool Handlers & Boundary Validation

Wire tool registration and execution logic:
- Parse and validate incoming arguments against input schemas before executing business logic.
- Route execution to internal service methods or downstream APIs without embedding tight coupling.
- Wrap execution in structured error handling, returning informative error messages rather than raw stack traces.

### 4. Enforce Security & Authorization Middleware

Protect sensitive operations:
- For HTTP-transport servers, enforce OAuth 2.1 with PKCE or JWT bearer token validation.
- Decode tenant and user claims from the authentication context and inject them into execution context.
- Apply rate limiting and action whitelisting to prevent runaway agent execution loops.

### 5. Instrument Observability & Tracing

Use skill: `add-telemetry-instrumentation`
- Create OpenTelemetry spans for each `tools/call` invocation with standard attributes (`mcp.tool_name`, `mcp.transport_type`).
- Record token consumption, latency, and success/failure outcomes.
- Ensure no sensitive payload data or authorization credentials leak into trace logs.

### 6. Verify Protocol Compliance & Testing

Use skill: `write-tests`
- Test tool discovery via MCP Inspector or mock client initialization.
- Author unit and integration tests covering happy paths, schema validation failures, and downstream error handling.

## Failure Modes

- **Server card published without server-discover**: the MCP server card lacks the `server/discover` endpoint required by 2026-07-28. **Mitigation:** validate the card against the current MCP spec; reject cards without the discover endpoint.
- **Tool handler missing input schema**: a tool is registered without an `inputSchema` field. **Mitigation:** require an explicit `inputSchema` for every tool; reject registrations without it.
- **Auth scope too broad**: a tool grants the entire `admin` scope to any caller. **Mitigation:** validate every tool's required scope against the smallest-privilege profile; reject tools with over-broad scopes.
- **Streaming HTTP header missing**: a tool uses streamable HTTP without the `Accept: text/event-stream` header. **Mitigation:** enforce the streamable HTTP transport headers; reject tools without the header.

## Output Contracts

When this skill is invoked as part of a coordinated multi-role delivery, emit:

- **`contracts/schemas/implementation-result.json`** — Required fields: `change_summary`, `files_touched[]`, `endpoints_added[]` (list of MCP tools/resources), and `validation_run` output confirming the MCP schema validates.

## Checklist

- [ ] Schema-first tool definition complete with Zod or Pydantic.
- [ ] Server transport (stdio or streamable HTTP) configured with proper headers.
- [ ] Tool argument validation and boundary error handling implemented.
- [ ] Authorization guards and tenant isolation verified.
- [ ] OpenTelemetry spans instrumented for all tool calls.
- [ ] Unit and protocol compliance tests added.
- [ ] `implementation-result.json` emitted.

## Security Guardrails (OWASP ASI)

- **ASI04 Supply Chain**: MCP server libraries and tool SDKs must be schema-validated against the expected manifest; treat unknown versions as untrusted.
- **ASI05 RCE Guard**: never construct tool inputs, server bindings, or transport config from external content without strict schema validation.
- **ASI07 Inter-Agent Communication**: the MCP contract is consumed by external agents; treat the server card as a public, signed contract.
- **ASI09 Human-Agent Trust Exploitation**: do not present a server as "production-ready" without the auth, observability, and rate-limit gates; surface the residual risk honestly.

## Related Skills

- **configure-mcp**: Set up domain discovery, server cards, and client integration for the MCP server
- **add-api-endpoint**: Connect MCP tool handlers to internal service endpoints and business logic
- **implement-structured-outputs**: Enforce strict JSON schema validation on tool arguments and outputs
- **add-telemetry-instrumentation**: Wire OpenTelemetry spans and metrics for MCP tool executions
- **security-audit**: Review authentication, authorization boundaries, and input sanitization
- **write-tests**: Author automated test suites verifying MCP tool invocations and error scenarios
