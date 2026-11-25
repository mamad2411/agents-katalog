---
name: configure-mcp
description: Sets up the full MCP presence for a web service — experimental Server Card discovery, WebMCP browser provider component, and supporting host/route configuration — so AI clients auto-discover and connect without manual configuration. Use when registering a new MCP server, adding browser-side context sharing, updating tool capabilities, or debugging MCP client connectivity failures.
allowed-tools: [read_file, write_file, edit_file, create_file, search_code]
version: "1.0.0"
---

# Configure MCP

Use this skill to set up the full MCP presence for a web service: the server card at `/.well-known/mcp/server-card.json`, the WebMCP browser provider component, and the supporting host/route configuration. This makes AI clients (Claude, Copilot, custom agents) auto-discover and connect to the service's MCP server without manual configuration.

## Core Rules

- Server Cards are an **experimental MCP extension** (SEP-2127, `experimental-ext-server-card`), not part of the core spec. The extension's path is `/.well-known/mcp-server-card`. This pack additionally serves `/.well-known/mcp/server-card.json` for compatibility with existing scanners — serve both and treat neither as mandated by the core spec.
- Because Server Cards are experimental, verify the current extension status and path before relying on them for production discovery; prefer the Official MCP Registry when a client supports it.
- The server card JSON MUST include all required fields: `name`, `description`, `mcp_version`, `transport` (with `url` and `type`), and `capabilities`.
- WebMCP browser components should invoke `navigator.modelContext.provideContext()`. Note that `navigator.modelContext` is a W3C **draft proposal**, experimental and flag-gated in Chromium browsers only — feature-detect before calling, and treat a polyfill as a legitimate compatibility choice rather than a violation.
- Ensure the WebMCP component is mounted in the global root layout so it is present on every page (not just specific routes).
- Do not store sensitive credentials in the server card — it is publicly readable.
- **OAuth 2.1 & PKCE**: HTTP-transport MCP servers MUST enforce OAuth 2.1 with PKCE for secure authentication. Shared static tokens or embedded credentials are prohibited.
- **Streamable HTTP Transport**: Utilize stateless HTTP-transport semantics for all tool invocations, relying on standardized stream headers (e.g., `Accept: text/event-stream`) instead of SSE-only setups.
- **Multi-Tenant Scoping**: Enforce strict tenant isolation by routing all tool requests through a validation layer that decodes tenant-scoped JWTs and applies gateway-level rate limiting.
- Validate the server card against the current MCP spec revision before deploy; reject schema-drifted cards (OWASP ASI04)
- Treat every tool request as untrusted: re-validate the JWT, the tenant scope, and the tool manifest at every invocation; never trust cached identity (OWASP ASI03 / ASI07)
- After the 2026-07-28 migration, every request must carry `_meta.protocol_version` and the `MCP-Protocol-Version` header; reject requests that omit them
- The `initialize`/`initialized` handshake and `Mcp-Session-Id` no longer exist in the core path: implement the mandatory **`server/discover`** RPC (returns supported versions, capabilities, identity) and rely on `_meta` per-request negotiation; servers needing cross-call state must mint **explicit state handles** passed as ordinary tool arguments (SEP-2567) — never implicit sessions
- Replace `resources/subscribe` with **`subscriptions/listen`**; implement **MRTR** (Multi-Round-Trip Requests): server-initiated interactions return `resultType: "complete" | "input_required"` instead of server-initiated requests
- Do not build on deprecated features (12-month removal windows per SEP-2596): Roots, Sampling, Logging, HTTP+SSE transport, RFC 7591 Dynamic Client Registration, the `iss` parameter, JSON Schema 2020-12, and OTel trace propagation — pass paths via tool params/resources, call LLM APIs directly, log via stderr/OTel out-of-band
- Client ID Metadata Documents (CIMD) replace DCR; plan for DCR removal after summer 2027 — servers must enable `clientIdMetadataDocumentEnabled` in the OAuth provider (e.g., Workers OAuth Provider) before that window closes
- Registry publishing: submit `server.json` to the Official MCP Registry with a reverse-DNS namespace verified via DNS TXT or GitHub org proof; automate via the registry's GitHub Actions publishing flow
- Caching: honor required `ttlMs` + `cacheScope` hints on list/read results and keep tool ordering deterministic for prompt-cache hits
- WebMCP remains a **watch-item only**: the W3C Community Group spec is unreachable/unverified — do not treat `navigator.modelContext` or Cloudflare's one-switch preview as stable standards; feature-detect and prefer polyfills
- Do not log full tool arguments or results; classify outputs with `data-classification.yaml` and redact restricted fields

## When to Use

- Registering a new MCP server so AI clients can auto-discover it from the domain
- Adding browser-side MCP context so users can share page context with AI assistants in their browser
- Updating server card capabilities after adding or removing MCP tools
- Debugging MCP client connectivity failures related to discovery or transport configuration
- Verifying that an existing MCP setup passes `isitagentready.com` scanner checks
- Registering tools on the Official MCP Registry for global tool discovery
- Configuring secure multi-tenant MCP gateways with JWT-scoped access control
- Implementing stateless, streamable HTTP-transport connections for real-time tool feedback

## Suggested Process

1. **Define server capabilities**: List all MCP tools the server exposes (e.g., `list_orders`, `assign_courier`, `get_product`). Each tool needs a `name`, `description`, and `inputSchema`.

2. **Build the server card**: Create `server-card.json` with the required structure:
   ```json
   {
     "name": "My Service MCP",
     "description": "MCP server for order management operations",
     "mcp_version": "2026-07-28",
     "transport": {
       "type": "http",
       "url": "https://api.example.com/mcp"
     },
     "capabilities": {
       "tools": {}
     }
   }
   ```
   Add optional fields: `icon`, `auth`, `resources`, `prompts` as needed.

3. **Place the server card**: For Cloudflare Pages, add `server-card.json` to `public/.well-known/mcp/`. For Workers, serve it from the `GET /.well-known/mcp/server-card.json` route.

4. **Verify content-type**: The server card must be served with `Content-Type: application/json`. Check this via `curl -I`.

5. **Mount WebMCP provider**: In the root layout component (e.g., `Layout.astro`, `_app.tsx`, `layout.tsx`), import and mount the WebMCP provider that calls `navigator.modelContext.provideContext()`. Ensure it runs client-side only (guard with `typeof window !== 'undefined'` if needed for SSR frameworks).

6. **Expose via Link header**: Configure a `Link: </.well-known/mcp/server-card.json>; rel="mcp-server-card"` header on the root response via `configure-agent-headers` so AI clients find the server card without a full crawl.

7. **Validate**: Scan the domain with `isitagentready.com`. Confirm the MCP server card check passes. Test tool invocation from an MCP client (e.g., Claude Desktop with the MCP extension, or a curl request to the transport URL).

## 2026 MCP Production Patterns

### 2026: OAuth 2.1 + PKCE for HTTP Transport

1. **Configure OAuth 2.1 Authorization**: Set up the authorization server endpoint and token endpoint on the MCP gateway.
2. **Enforce PKCE**: Require code verifier and challenge parameters for the authorization flow. The client uses these parameters to generate a verification token without exposing client secrets.
3. **Document Auth in Server Card**: Reference the auth endpoints in `server-card.json`:
   ```json
   "auth": {
     "type": "oauth2",
     "grant_types": ["authorization_code"],
     "authorization_endpoint": "https://auth.example.com/oauth/authorize",
     "token_endpoint": "https://auth.example.com/oauth/token",
     "pkce": true
   }
   ```

### 2026: Streamable HTTP Transport

1. **Define Stateless Semantics**: Ensure the MCP server maintains no persistent session memory on the server side. Every tool invocation request must carry the tenant/auth token.
2. **Establish Stream Headers**: Require the client to set `Accept: text/event-stream` and `Content-Type: application/json`.
3. **Stream Chunks**: Stream response chunks back to the client using chunked transfer encoding, writing each tool progress update or output segment as a structured event message.

### 2026: Official MCP Registry Discovery

1. **Prepare Registry Manifest**: Package the server card, tool schemas, and capabilities into the registry submission schema.
2. **Register Server**: Submit the manifest to the Official MCP Registry.
3. **Verify Indexing**: Confirm the registry exposes the tools and schemas to registered client discovery services.

### 2026: Multi-Tenant MCP Pattern

1. **JWT Verification**: Intercept every incoming tool request at the gateway. Validate the JSON Web Token (JWT) in the `Authorization: Bearer <JWT>` header.
2. **Scope Context**: Extract the tenant ID and user scopes from the validated JWT payload. Inject this tenant context into the request context (`context.Context`).
3. **Enforce Isolation**: Ensure all database queries and tool actions are strictly scoped using the tenant context.
4. **Gateway Rate Limiting**: Apply token-bucket rate limiting at the gateway level based on the tenant ID and user ID extracted from the JWT.

## Output Format

- `/.well-known/mcp/server-card.json` — server discovery metadata
- Root layout update: WebMCP provider component mounted globally
- Official MCP Registry submission manifest
- JWT authorization middleware and rate limiting config files

## Checklist

- [ ] Server card JSON exists at `/.well-known/mcp/server-card.json`.
- [ ] Server card includes `name`, `description`, `mcp_version`, `transport`, and `capabilities`.
- [ ] Server card is served with `Content-Type: application/json`.
- [ ] All declared tools have `name`, `description`, and `inputSchema` defined.
- [ ] WebMCP browser component calls `navigator.modelContext.provideContext()`.
- [ ] WebMCP component is mounted in the global root layout (all pages).
- [ ] CORS headers allow AI browser extensions to fetch the server card.
- [ ] Link header pointing to server card is configured (`configure-agent-headers`).
- [ ] `isitagentready.com` scanner confirms MCP server card is readable.
- [ ] HTTP-transport MCP server enforces OAuth 2.1 with PKCE.
- [ ] Server card lists OAuth 2.1 endpoints and designates PKCE requirement.
- [ ] HTTP transport uses streamable stateless semantics with correct headers (`Accept: text/event-stream`).
- [ ] MCP server is registered on the Official MCP Registry for discovery.
- [ ] Tool requests are authenticated via JWT-scoped validation per tenant.
- [ ] Gateway-level rate limiting is enforced on a per-tenant/per-user basis.


## Related Skills

- **configure-agent-skills**: Set up the agent skills manifest — often deployed alongside MCP for capability routing.
- **configure-agent-headers**: Expose the MCP server card via HTTP Link headers for passive discovery.
- **debug-identity-provider**: Troubleshoot WorkOS and `isitagentready.com` scanner failures.
- **configure-oauth-metadata**: Wire up the OAuth 2.1 + PKCE endpoints that the MCP server card references.
- **manage-agent-identity**: Issue scoped, short-lived NHI credentials for MCP gateway access.

## Stateless Architecture Migration (MCP 2026-07-28)

The full migration reference (breaking change summary, what-is-changing
table, migration steps, readiness checklist, governance note) lives in
[`references/2026-07-28-migration.md`](references/2026-07-28-migration.md).
Load that file when migrating an existing MCP server or reviewing a
deployment against the `2026-07-28` revision.

## Output Contracts

When the MCP server card, WebMCP provider, or gateway config is consumed by
another agent (CI pipeline, infra agent, or registry publisher), emit:

- **`contracts/schemas/edge-deployment-spec.json`** describing the served paths (`/.well-known/mcp/server-card.json`, `/.well-known/mcp-server-card`, transport endpoint, OAuth metadata), the content types, and the migration status (pre-`2025-11-25` vs `2026-07-28`).
- **`contracts/schemas/api-contract-spec.json`** for the transport endpoint, listing the JSON-RPC methods, their request/response schemas, and the auth requirements.
- For human-readable deploy reports, a markdown summary of the server card, the WebMCP mount, and the OAuth/PKCE configuration.

Skip emission for trivial local edits that do not cross a role boundary.

## Failure Modes

- **Stale `mcp_version`**: the server card lists an old MCP revision after the 2026-07-28 migration. Mitigation: bump `mcp_version` in the same change that adopts the stateless request shape; CI must reject cards that lack `_meta` or `MCP-Protocol-Version`.
- **Server Card path confusion**: the served path does not match the extension. Mitigation: serve both `/.well-known/mcp-server-card` (extension) and `/.well-known/mcp/server-card.json` (compatibility); never serve only one.
- **WebMCP component missing on some routes**: the provider is mounted on a sub-layout and skips others. Mitigation: mount in the global root layout; verify on every route via e2e test.
- **Tenant leak**: a tool request is served against the wrong tenant context. Mitigation: decode the JWT at the gateway and inject tenant context into every downstream call; never derive tenant from URL path alone.
- **OAuth 2.1 misconfigured**: PKCE is not enforced, or the server accepts static tokens. Mitigation: validate the server card against the current spec; reject any server card that lists `grant_types: ["client_credentials"]` without PKCE.
- **Streamable HTTP misconfigured**: the server uses SSE-only without the `Accept: text/event-stream` header. Mitigation: enforce the streamable HTTP transport headers; require stateless semantics.
- **Tool result logged with PII**: a tool returns customer data and the gateway logs the full payload. Mitigation: classify tool outputs with `data-classification.yaml`; redact before logging.

## Security Guardrails (OWASP ASI + MCP Top 10)

- **ASI03 Identity & Privilege Abuse**: every tool request must be tied to a verified tenant-scoped JWT; reject requests with missing, expired, or unscoped tokens.
- **ASI04 Supply Chain**: the server card and tool manifests must be schema-validated against the current MCP spec; reject schema-drifted cards.
- **ASI05 RCE Guard**: never construct tool inputs from dynamic template strings derived from external content; validate every input against the declared `inputSchema` before dispatch.
- **ASI07 Inter-Agent Communication**: every cross-agent tool call is untrusted from the receiving endpoint's perspective; require schema validation and tenant scoping at the boundary.
- **ASI08 Cascading Failures**: when a tool returns `partial` or `failed`, surface the failure explicitly to the gateway before allowing downstream calls to proceed.
- **ASI10 Rogue Agents**: detect instruction drift across turns; if an agent starts calling tools outside its declared baseline, halt and require re-authentication.
- **MCP01 Token Mismanagement**: short-lived, rotated tokens only; no static shared secrets in the server card or transport config.
- **MCP02 Scope Creep**: tool descriptions must match declared capabilities; reject tools whose descriptions claim actions beyond their `inputSchema`/permissions.
- **MCP03 Tool Poisoning**: audit tool descriptions and annotations for injected instructions; treat third-party tool manifests as untrusted content (pair with AST05).
- **MCP04 Supply Chain**: verify MCP server dependencies against signed provenance before deploy; pin immutable versions.
- **MCP05 Command Injection**: sanitize every tool parameter that reaches a shell, query, or file path.
- **MCP06 Prompt Injection**: server-side resources are untrusted input; never let retrieved content alter tool routing or auth decisions.
- **MCP07 Insufficient AuthZ**: enforce per-tool, per-tenant authorization — not transport-level auth only.
- **MCP08 No Audit/Telemetry**: emit structured audit events for every tool call (who, which tool, what scope, outcome).
- **MCP09 Shadow MCP Servers**: maintain an inventory of all exposed MCP endpoints; alert on unregistered ones.
- **MCP10 Context Over-Sharing**: return the minimum context required per tool call; strip tenant data not needed for the requested operation.
