---
name: mcp-stateless-core-2026
description: Applies the 2026-07-28 MCP specification's stateless protocol core, MRTR, header-based routing, cacheable lists, authorization hardening, and extension framework. Use when designing or upgrading MCP servers for enterprise scale, implementing elicitation/multi-round-trip requests, configuring OAuth/EMA, or migrating from stateful MCP.
---

# MCP Stateless Core 2026-07-28

## When to Use

- Upgrading MCP servers to the stateless protocol core (session removal)
- Implementing multi-round-trip requests (MRTR) for elicitation/sampling/roots
- Configuring header-based routing (`Mcp-Method`, `Mcp-Name`)
- Adding cacheable tool/resource lists (`ttlMs`, `cacheScope`)
- Hardening OAuth: RFC 9207 issuer validation, CIMD replacing DCR
- Adopting MCP Apps or Tasks extensions
- Migrating from `initialize`/`initialized` handshake
- Enterprise MCP deployment behind standard load balancers

## The Core Change: Stateless Protocol

The 2026-07-28 specification removes the `initialize`/`initialized` handshake and the `Mcp-Session-Id` header (SEP-2575, SEP-2567). Every request is now self-describing, carrying protocol version, client identity, and client capabilities in `_meta`.

### What This Means

- **Any request can land on any server instance** behind a plain round-robin load balancer
- No shared session store needed between server instances
- No sticky routing required
- Standard Kubernetes/cloud-native DevOps tooling works directly

### Migration Pattern

If your server needs state across calls, mint an explicit handle from a tool and have the model pass it back as an argument. This works better than hidden session state — the model can see the handle and thread it between tools.

```json
// Old: stateful
POST /mcp  (with Mcp-Session-Id: abc-123)

// New: stateless
POST /mcp HTTP/1.1
MCP-Protocol-Version: 2026-07-28
Mcp-Method: tools/call
Mcp-Name: search

{"jsonrpc":"2.0","id":1,"method":"tools/call",
 "params":{"name":"search","arguments":{"q":"otters"},
 "_meta":{"io.modelcontextprotocol/clientInfo":{"name":"my-app","version":"1.0"}}}}
```

## Key New Features

### 1. Multi Round-Trip Requests (MRTR)

Replaces server-initiated `elicitation/create`, `sampling/createMessage`, and `roots/list` requests that required held-open streams. The server returns `resultType: "input_required"` with the requests it needs answered; the client retries the original call with answers in `inputResponses`.

```
Client → Server: tools/call
Server → Client: resultType: "input_required", needs: [confirmation]
Client → Server: tools/call (with inputResponses: {confirmation: true})
Server → Client: result
```

### 2. Header-Based Routing (SEP-2243)

Streamable HTTP requests must include `Mcp-Method` and `Mcp-Name` headers. Gateways, rate limiters, and WAFs can route and meter on these headers instead of parsing JSON bodies.

### 3. Cacheable Lists (SEP-2549)

Responses from `tools/list`, `prompts/list`, `resources/list`, and `resources/read` carry `ttlMs` and `cacheScope`. Clients can cache tool catalogs and keep upstream prompt caches stable across reconnects.

### 4. Authorization Hardening

- RFC 9207 `iss` parameter validation (closes OAuth mix-up attacks)
- Client credentials bound to issuer (no reuse across authorization servers)
- Dynamic Client Registration (DCR) deprecated → Client ID Metadata Documents (CIMD)
- Enterprise Managed Authorization (EMA) extension for corporate IdP as gatekeeper

### 5. Tasks Extension

`tasks/get` (poll-based) and `tasks/update` for long-running async operations. Change notifications move to `subscriptions/listen` stream.

### 6. MCP Apps Extension

Server-rendered interactive UIs inside AI clients (dashboards, forms, visualizations).

## Deprecation Policy

- Formal 12-month minimum window between deprecation and removal
- Deprecated: Roots, Sampling, Logging (SEP-2577)
- Deprecated: Legacy HTTP+SSE transport (year-long offramp)
- Deprecated: Dynamic Client Registration (replaced by CIMD)

## Ecosystem Scale (July 2026)

- ~250M weekly SDK downloads (doubled in 6 months)
- 10K+ active public MCP servers (17K in registries)
- Core maintainers span Anthropic, Microsoft, OpenAI, Google, Amazon
- AAIF (Linux Foundation): 40 → 240 members in 7 months
- Anthropic contribution share below 50%

## Design Principles for Builders

1. **Keep MCP a discovery protocol, not an ESB.** If your server gets "smarter" with each integration (adding if/else routing logic), you're building an enterprise service bus. New integrations should add descriptions (schemas, guidance), not logic.

2. **Use MRTR for user input, not for orchestration.** Multi-round-trip is for getting missing parameters or confirmations — not for complex server-side workflows.

3. **Cache aggressively.** List responses now carry TTL hints. Use them to reduce re-fetching and keep prompt caches stable.

4. **Header routing enables security.** Route on `Mcp-Method`/`Mcp-Name` at the gateway layer for authz and rate-limiting without body parsing.

5. **State belongs in arguments, not sessions.** If the model needs to pass a handle, it should be an explicit tool argument — not hidden transport state.

## A-Tech Applications

- **A-Coder:** Stateless MCP servers for developer tools behind standard k8s; MRTR for destructive-action confirmations; header routing for per-tool authz
- **Be Practical:** MCP migration curriculum; stateless architecture as core teaching unit
- **Builder's Club:** Open-source MCP server templates using 2026-07-28 spec; community governance alignment with AAIF

## Cross-References

- `mcp-enterprise-adoption-2026` — enterprise MCP adoption patterns (updated)
- `mcp-security-trust` — MCP security model and tool poisoning defense
- `mcp-dual-identity-problem` — dual-identity resolution patterns
- `mcp-payment-support-specification` — payment extension specification
- `agentic-commerce-2026` — agentic commerce infrastructure

## A-Tech Alignment

- **Open-source:** MCP is now under Linux Foundation AAIF governance; spec, SDKs (TypeScript, Python, Go, C#, Rust beta) all open
- **Data privacy:** EMA enables corporate IdP as gatekeeper; RFC 9207 closes mix-up attacks; stateless reduces data exposure surface
- **Financial freedom:** Stateless core eliminates infrastructure overhead (session stores, sticky routing) — lowers deployment cost
- **Practical implementation:** 250M weekly downloads, 10K+ servers, production-proven at AWS/Cloudflare/Microsoft/Google scale