---
name: architect-mcp-server
description: Architect enterprise-grade Model Context Protocol (MCP) servers, tool surfaces, schemas, transport protocols, and security perimeters. Use when designing MCP server contracts, selecting streamable HTTP or stdio transports, standardizing Zod/Pydantic schemas, externalizing state handles (SEP-2567), configuring OAuth 2.1 RFC 8707 Resource Indicators, or establishing Shadow MCP governance.
allowed-tools: [read_file, write_file, edit_file, create_file, search_code, run_build, run_tests]
version: "1.0.0"
---

# Architect MCP Server

Architect enterprise-grade Model Context Protocol (MCP) servers, tool surfaces, schemas, transport protocols, and security perimeters. This skill establishes architectural boundaries, ergonomics, and governance before code implementation.

## Core Rules

- **Stateless HTTP Architecture (MCP Revision 2026-07-28)**: Default to Stateless HTTP transport. Completely abolish all legacy session header identifiers and session handshakes (`initialize`, `notifications/initialized`). Every HTTP POST request is connectionless, standalone, and self-contained; reserve stdio strictly for local CLI development.
- **Client Metadata Injection (`params._meta`)**: Mandate per-request client metadata injected via JSON-RPC `params._meta`:
  - `trace_parent`: W3C distributed trace context (`traceparent` header / metadata).
  - `auth_context`: Authenticated caller identity, tenant ID, or SPIFFE SVID token.
  - `idempotency_key`: Client-generated UUIDv7/hash preventing duplicate execution of mutating tools.
- **Multi-Route Tool Routing (MRTR SEP-2322)**: Mandate `Mcp-Tool-Route: <domain>_<action>` (or `Mcp-Name`) HTTP headers so API gateways route individual tools directly to microservices without parsing JSON bodies. For interactive workflows, servers return `resultType: "input_required"` with `stateHandle` and `expectedFields`.
- **State Externalization (SEP-2567)**: Externalize multi-turn state, continuation tokens, and pagination cursors to durable remote storage (Redis, Cloudflare D1/KV) keyed by opaque `stateHandle` with 900s TTL. Zero in-memory server session affinity.
- **Stateless Gateway Routing Headers**:
  `Mcp-Protocol-Version: 2026-07-28`, `Mcp-Method: tools/call`, `Mcp-Name: <domain>_<action>`, `Mcp-Tool-Route: <domain>_<action>`, `Accept: text/event-stream, application/json`.
- **Action-Oriented Domain Prefixes**: Name tools with explicit verb-noun domain syntax (`<domain>_<action>`, e.g., `fs_read_file`, `billing_issue_refund`).
- **Strict Schema Validation**: Define strict input parameters and return types using Zod or Pydantic v2; prohibit untyped JSON blobs or generic string inputs.
- **OutputSchema & Structured Content**: Constrain returned payloads with `outputSchema` and emit `structuredContent` separating structured JSON from textual explanations.
- **Actionable Error Ergonomics**: Error responses MUST return typed error categories, machine-readable error codes, and explicit remediation hints enabling autonomous recovery.
- **OAuth 2.1 RFC 8707 Resource Indicators**: Require clients to specify target MCP server URIs in authorization requests to prevent token forwarding and replay attacks.
- **Registry Allowlisting & Supply Chain**: Production MCP servers must originate from vetted registries with publisher verification, code-signing, and SBOM audits (`MCP-REGISTRY LOCK`).
- **Shadow MCP Governance**: Enforce gateway inspection to detect and block unregistered, rogue MCP servers (`MCP-GATEWAY LOCK`).

## When to Use

- Architecting enterprise MCP server boundaries, tool surfaces, and input/output contracts
- Specifying MCP Revision 2026-07-28 Stateless HTTP transport and gateway routing headers
- Standardizing per-request client metadata injection (`params._meta`)
- Configuring Multi-Route Tool Routing (MRTR SEP-2322) and SEP-2567 external state handles
- Designing OAuth 2.1 RFC 8707 Resource Indicators and Enterprise-Managed Authorization
- Establishing Shadow MCP discovery, gateway routing, and supply-chain allowlisting

## Suggested Process

1. **Define Domain Boundary & Tool Surface**: Inventory operations, apply `<domain>_<action>` naming, calibrate granularity (single-action atomic vs. composite), and describe disambiguating triggers.
2. **Specify Strict Input & Output Schemas**: Author Zod or Pydantic schemas with field descriptions, validation constraints, enum values, and explicit `outputSchema` declarations.
3. **Design Actionable Error Envelopes**: Format error returns with `is_error`, `error_code`, `message`, `remediation_hint`, and `is_retriable` flags for agent self-correction.
4. **Configure Stateless HTTP & Routing**: Specify stateless HTTP headers (`Mcp-Protocol-Version: 2026-07-28`, `Mcp-Tool-Route`), inject `params._meta` (`trace_parent`, `auth_context`, `idempotency_key`), and externalize state via SEP-2567 handles (900s TTL).
5. **Architect Resources & Prompts**: Declare URI-addressable resources (`system://metrics/{host}`) and reusable prompt workflows (`prompts/get`) with parameter validation.
6. **Enforce Auth & RFC 8707 Scoping**: Configure OAuth 2.1 authorization servers with PKCE, audience-restricted Resource Indicators, and Enterprise-Managed Authorization policies.
7. **Establish Governance & Emit Contracts**: Validate against OWASP ASI and MCP Top 10 guardrails, define gateway telemetry, and emit `mcp-server-card.json`, `adr-spec.json`, and `architecture-options.json`.

## Checklist

- [ ] Production transport adheres to MCP Revision 2026-07-28 Stateless HTTP (zero session IDs, zero handshakes).
- [ ] Tool names adhere to action-oriented domain prefix naming (`<domain>_<action>`).
- [ ] Every tool defines strict Zod/Pydantic input schemas and explicit `outputSchema` contracts.
- [ ] Per-request client metadata injected via `params._meta` (`trace_parent`, `auth_context`, `idempotency_key`).
- [ ] Multi-Route Tool Routing (MRTR SEP-2322) configured with `Mcp-Tool-Route` HTTP headers.
- [ ] Multi-turn session handles and pagination cursors externalized via SEP-2567 to Redis/D1 (900s TTL).
- [ ] Output responses separate typed JSON from natural language via `structuredContent`.
- [ ] Error responses supply machine-readable error codes and self-correction remediation hints.
- [ ] OAuth 2.1 RFC 8707 Resource Indicators bound to target MCP server URI.
- [ ] Architecture decision record emitted conforming to `contracts/schemas/mcp-server-card.json` and `adr-spec.json`.

## Output Contracts

When architectural design is complete or ready for downstream implementation slices:

- **`contracts/schemas/mcp-server-card.json`**: Primary stateless server card discovery contract defining transports, MRTR support, tools, and auth schemes.
- **`contracts/schemas/adr-spec.json`**: Architectural decision record detailing MCP server contracts, transport choices, state externalization, and trust boundaries.
- **`contracts/schemas/architecture-options.json`**: Comparative options evaluation documenting trade-offs between transport modes, schema strategies, and authorization patterns.

## Failure Modes

- **Session Affinity Regression**: Relying on legacy session headers or server memory causes failure on serverless edge runtimes. Mitigation: Enforce connectionless HTTP POST with SEP-2567 external state handles.
- **Gateway Routing Failure**: Omitting `Mcp-Tool-Route` header forces API gateways to parse request bodies. Mitigation: Mandate `Mcp-Tool-Route: <domain>_<action>` header on every tool call.
- **Expired State Handle**: Client supplies expired continuation token. Mitigation: Return typed `HANDLE_EXPIRED` (`is_retriable: false`) with hint to restart flow.
- **Vague Tool Naming**: Tools with overlapping names cause model confusion. Mitigation: Mandate `<domain>_<action>` naming with explicit negative triggers.
- **Token Replay Vulnerability**: Forwarding caller tokens without audience restriction. Mitigation: Enforce OAuth 2.1 RFC 8707 Resource Indicators.

## Security Guardrails (OWASP ASI + MCP Top 10)

- **ASI02 Tool Misuse & Exploitation**: Limit tool capabilities to minimal required privilege; require human approval for irreversible write operations.
- **ASI04 Agentic Supply Chain**: Verify MCP server packages against signed provenance manifests; prohibit unvetted registries.
- **ASI05 Unexpected Code Execution**: Validate every input parameter against declared schemas; sanitize inputs before SQL, shell, or API dispatch.
- **ASI07 Insecure Inter-Agent Communication**: Enforce mutual authentication and RFC 8707 audience restriction on all inter-service MCP calls.
- **ASI08 Cascading Failures**: Implement circuit breakers, bulkhead isolation, and rate limiting across MCP gateways.
- **ASI09 Over-Reliance**: Provide deterministic schema validation and error hints to prevent blind acceptance of incorrect tool outputs.
- **ASI10 Rogue Agent Misbehavior**: Monitor tool call anomalies at gateway proxies and revoke access tokens upon abnormal call patterns.

## Related Skills

- **build-mcp-server**: Implement the backend code, handlers, and tests specified by this architectural design.
- **configure-mcp**: Publish server discovery cards and browser WebMCP provider components.
- **system-design**: Plan overall system topologies, compute sizing, and infrastructure resilience.
- **agent-tool-orchestration**: Orchestrate tool call sequences, fallback chains, and parameter injection.
- **security-audit**: Audit MCP authentication flows, token scopes, and transport encryption.
