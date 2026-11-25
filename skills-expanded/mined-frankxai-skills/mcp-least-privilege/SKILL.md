---
name: mcp-least-privilege
description: Use when building, auditing, or reviewing the authorization of an MCP server - "is my MCP server's OAuth set up right", "probe my remote MCP endpoint", "what scopes should my MCP server advertise", "protected resource metadata", "WWW-Authenticate for MCP", "can my MCP server pass the user's token to an upstream API", "should I cache MCP auth checks", or scoping an MCP server's tools and credentials before production. Do NOT use for deciding which tools an agent may call (use tool-allowlist), for building an OAuth authorization server, or for general MCP server design with no security question (use mcp-architecture).
argument-hint: "[url of the MCP endpoint to probe]"
metadata:
  version: "2.0.0"
---

# MCP least privilege

An MCP server is a privilege boundary: each tool gets only the access its function needs, each token is checked as issued for this server, and nothing is connected "because we might need it". This skill is the server owner's side; which tools an agent may call at all is `tool-allowlist`.

Quoted text is the MCP authorization spec, revision 2026-07-28, keywords as written. Unquoted guidance is engineering practice.

## Probe a server first

```bash
node scripts/probe-mcp-auth.mjs https://mcp.example.com/mcp          # human report
node scripts/probe-mcp-auth.mjs https://mcp.example.com/mcp --json   # machine report
node scripts/probe-mcp-auth.mjs http://127.0.0.1:3000/mcp --allow-http
```

Zero dependencies, Node 18+. Exit `0` all pass, `1` a check failed, `2` not probeable (connection error, non-HTTP URL, bad arguments). It sends an MCP `initialize` POST with no credentials, the same POST with the dummy bearer token `probe`, and the same POST with `?access_token=probe`. Metadata comes from the advertised `resource_metadata` URL, or from endpoint-path then origin-root well-known URIs when that parameter is absent. It refuses URLs that carry userinfo or a credential-like query parameter, never reads the environment, and does not follow redirects.

| Check | Passes when |
|---|---|
| `unauth-401` | the unauthenticated request gets 401 |
| `challenge-bearer` | the 401 carries a `WWW-Authenticate: Bearer` challenge |
| `challenge-resource-metadata` | the challenge has a usable `resource_metadata` URL; absence is informational and triggers well-known discovery |
| `challenge-scope` | info only: whether the challenge names `scope` (a SHOULD) |
| `challenge-no-offline-access` | the challenge scope omits `offline_access` |
| `metadata-json` | the metadata URL returns 200 and a JSON object |
| `metadata-resource` | it has an absolute http(s) `resource` |
| `resource-no-fragment` | `resource` has no `#fragment` |
| `resource-matches-endpoint` | `resource` equals the probed URL in canonical form, or is its path prefix (the spec lists both an origin and a path as canonical) |
| `authorization-servers` | `authorization_servers` is a non-empty array of https URLs |
| `scopes-supported-no-offline-access` | `scopes_supported`, if present, omits `offline_access` |
| `invalid-bearer-401` | the dummy bearer token gets 401 |
| `query-token-rejected` | the dummy token in the query string gets 400 or 401; this does not prove valid query tokens are rejected |

It cannot test, without a real token: token passthrough to upstream APIs, audience validation of a real token issued for another resource, acceptance of valid query tokens, and 403 `insufficient_scope` step-up. Review those in code with `references/server-owner-checklist.md`.

Judgment calls built into the probe: the canonical-URI rule the spec writes for the client's `resource` parameter is applied to the metadata `resource` field; https for authorization servers is the probe's bar. The discovery sub-page requires a header URL or well-known metadata; both routes are tested. Tests: `node --test` in `scripts/`.

## Scope: when the spec applies

- "Authorization is OPTIONAL." A deliberately public server can skip it; the probe then fails `unauth-401` and says so.
- "When supported: HTTP-based transports SHOULD conform to this spec."
- "STDIO transports SHOULD NOT follow it and instead retrieve credentials from the environment." Practice: stdio is a transport, not a sandbox. The process still runs with the user's OS permissions, so least privilege for a local server means a narrow credential in its environment and an OS-level sandbox, not OAuth.

## Server owner requirements

1. Metadata. "MCP servers MUST implement OAuth 2.0 Protected Resource Metadata (RFC 9728). MCP clients MUST use it for authorization server discovery."
2. Challenge. "MCP servers SHOULD include a `scope` parameter in the `WWW-Authenticate` header (RFC 6750 section 3) to indicate required scopes." The spec's example: `WWW-Authenticate: Bearer resource_metadata="https://mcp.example.com/.well-known/oauth-protected-resource", scope="files:read"`.
3. Status codes. "401 authorization required or token invalid; 403 invalid scopes or insufficient permissions; 400 malformed request." And: "Invalid or expired tokens MUST receive HTTP 401."
4. Audience. "MCP servers MUST validate access tokens per OAuth 2.1 section 5.2 and MUST validate that tokens were issued specifically for them as the intended audience (RFC 8707 section 2)."
5. No token passthrough. "MCP servers MUST only accept tokens that are valid for use with their own resources." "MCP servers MUST NOT accept or transit any other tokens." Practice: when the server calls an upstream API, it uses its own credential for that API, never the token the client sent.
6. Canonical resource. Of the RFC 8707 `resource` parameter that names this server, the spec says it "MUST identify the MCP server the token is for; MUST use the canonical URI of the server." Canonical: `https://mcp.example.com/mcp`, `https://mcp.example.com`. Invalid: no scheme, "anything with a fragment". "Prefer no trailing slash."
7. Minimal scopes. `scopes_supported` is "intended to represent the minimal set of scopes necessary for basic functionality". "Servers SHOULD NOT include `offline_access` in the WWW-Authenticate scope or in `scopes_supported`."
8. Insufficient scope at runtime. "servers SHOULD respond `403 Forbidden` with `WWW-Authenticate: Bearer error="insufficient_scope", scope="<needed scopes>", resource_metadata="...", error_description="..."`." "Servers SHOULD include all scopes required for the current operation in a single challenge, not one at a time." "Servers MUST account for scope hierarchies (a broader scope implies narrower ones)."

## Client rules, briefly

- "The client MUST use the `Authorization: Bearer <access-token>` header on every HTTP request. Access tokens MUST NOT be included in the URI query string."
- "MCP clients MUST NOT send tokens to the MCP server other than ones issued by the MCP server's authorization server."
- Clients "MUST generate PKCE parameters, include the `resource` parameter, and record the expected issuer before redirecting", and the resource parameter "MUST be included in both authorization and token requests". "Clients MUST send it regardless of whether authorization servers support it."
- "Clients MUST treat the challenge scopes as authoritative for the current operation."
- "Authorization servers and MCP clients SHOULD support OAuth Client ID Metadata Documents." Dynamic Client Registration "is deprecated and retained for backwards compatibility with authorization servers that do not support Client ID Metadata Documents". Details live in the unread client-registration sub-page.

## Should authorization decisions be cached?

- Scope checks: run them at every tool dispatch, against the scopes on the token presented with that request. A session that authenticated once does not carry a permission forward to a later, more powerful call. This is what makes requirement 8 possible.
- Token validation: caching the result of an introspection call or a fetched signing key for a short TTL is normal practice and not forbidden by the spec text read here. The cache must never outlive the token's own expiry, because "Invalid or expired tokens MUST receive HTTP 401." Keep the TTL short enough that revocation lands within a window you can defend.

## Least privilege inside the server (practice, not spec text)

- Narrow tools. No `execute` or `run` tool that takes a free-form command; one tool per audited operation. When a tool shells out, pass an argument array to `execFile`, never a string to `exec`. The corrected `git diff` example is in the checklist.
- One scope per capability tier, checked at the tool, for example `files:read` versus `files:write`. A read-only tool never inherits a write credential because it shares a pool.
- Bind the user. Authorize the action for the user behind the token, not for the server's own service account, or the server becomes a confused deputy.
- Sandbox local servers: container or OS sandbox, no network unless a tool needs it, read-only filesystem by default.
- Audit every call: caller identity, tool, sanitized arguments, scopes, decision, outcome. Never log tokens.

## Stop conditions

Do not ship the server if any of these hold:

1. The probe exits 1 on an endpoint that is meant to require authorization.
2. A tool accepts a free-form command or builds a shell string from input.
3. The server forwards the client's token upstream or accepts a token issued for another resource.
4. One scope grants every tool, or `scopes_supported` lists more than basic functionality needs.
5. Scope is checked once per session instead of per call.
6. No audit log exists for tool calls.

## Sources and limits

Verified against modelcontextprotocol.io/specification/2026-07-28/basic/authorization and its authorization-server-discovery sub-page on 2026-10-05.

Client-registration and security-considerations remain outside this probe. Read those pages and validate real token flows before treating an endpoint as production-ready. A passing dummy-token probe is evidence for its listed checks, not a complete OAuth security review.
