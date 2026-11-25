---
name: configure-oauth-metadata
description: Configures well-known OAuth 2.0 and OpenID Connect discovery endpoints (`oauth-protected-resource`, `oauth-authorization-server`, `openid-configuration`) including the `agent_auth` block required for agentic registration flows. Use when setting up or correcting OAuth metadata for AI agent authentication, WorkOS agentic registration, or any service that exposes agent-accessible authorization endpoints.
allowed-tools: [read_file, write_file, edit_file, create_file, search_code, query_db, read_database, run_tests, execute_command]
version: "1.0.0"
---

# Configure OAuth Metadata

Use this skill when configuring `/.well-known/oauth-protected-resource`, `/.well-known/oauth-authorization-server`, or `/.well-known/openid-configuration` — especially the `agent_auth` block that enables agentic client registration and claim flows.

## Core Rules

- Ensure `authorization_servers` lists a fully resolvable, operational domain — do not use dummy subdomains that are not bound in DNS; a 530 Origin DNS Error means the URL is unreachable.
- The `agent_auth` block MUST exist in the `oauth-authorization-server` metadata file.
- The `agent_auth` block MUST include a `"skill"` attribute pointing to the absolute URL of root `/auth.md` (matching `manage-auth-md`, e.g., `https://yourdomain.com/auth.md`).
- Implement **RFC 9728** for `/.well-known/oauth-protected-resource`, and configure protected API `401` responses to emit `WWW-Authenticate: Bearer resource_metadata="https://yourdomain.com/.well-known/oauth-protected-resource"`.
- Prefer **Client ID Metadata Documents (CIMD)** (`client_id_metadata_document_supported: true` / `clientIdMetadataDocumentEnabled`) over legacy RFC 7591 Dynamic Client Registration (scheduled for deprecation in MCP 2026–2027).
- Use `"register_uri"` (not `identity_endpoint`) and `"claim_uri"` (not `claim_endpoint`) — the field names are exact; any deviation will fail scanner validation.
- Define `credential_types_supported` nested inside the identity type blocks (e.g., `anonymous.credential_types_supported`), NOT at the root of `agent_auth`.
- Both `anonymous` and `identity_assertion` credential paths must be documented if the service supports them.
- All endpoints must be served with `Content-Type: application/json` and appropriate CORS headers.
- enforce PKCE (Proof Key for Code Exchange) as mandatory for all agent OAuth flows, asserting `code_challenge_methods_supported: ["S256"]` in authorization metadata
- support OpenID Connect (OIDC) Dynamic Client Registration by exposing a POST endpoint that accepts the Agent Card JSON as input
- bind issued access tokens cryptographically to agent identities using the `azp` and agent DID claims in the JWT payload
- validate that the `agent_auth` configuration complies with isitagentready.com and WorkOS requirements
- Treat the OAuth metadata as a public, signed contract: do not include client secrets or sensitive callback URLs in the served JSON (OWASP ASI03)
- Verify every URL in `authorization_servers` resolves in public DNS before each deploy; a 530 error must fail the scanner run (OWASP ASI04)
- After the 2026-07-28 changes, every metadata file must assert `code_challenge_methods_supported: ["S256"]`; reject metadata that does not

## When to Use

- Setting up WorkOS Agentic Registration for the first time on a domain
- Correcting `agent_auth` field names after scanner validation failures
- Adding OAuth metadata endpoints to a Cloudflare Pages or Workers site
- Verifying that `isitagentready.com` or equivalent scanner passes the OAuth metadata checks
- Updating authorization server metadata after adding or changing credential types

## Suggested Process

1. **Locate or create metadata files**: Identify where `oauth-protected-resource.json` and `oauth-authorization-server.json` are served from. For Cloudflare Pages, these live under `public/.well-known/`. For Workers, serve them from dedicated route handlers.

2. **Structure the `oauth-authorization-server` payload**: Include the required top-level fields (`issuer`, `authorization_endpoint`, `token_endpoint`) and the `agent_auth` block:
   ```json
   {
     "issuer": "https://auth.yourdomain.com",
     "authorization_endpoint": "https://auth.yourdomain.com/authorize",
     "token_endpoint": "https://auth.yourdomain.com/token",
     "code_challenge_methods_supported": ["S256"],
     "client_id_metadata_document_supported": true,
     "agent_auth": {
       "skill": "https://yourdomain.com/auth.md",
       "register_uri": "https://auth.yourdomain.com/agent/register",
       "claim_uri": "https://auth.yourdomain.com/agent/claim",
       "anonymous": {
         "credential_types_supported": ["anonymous"]
       },
       "identity_assertion": {
         "credential_types_supported": ["jwt_bearer"]
       }
     }
   }
   ```

3. **Structure the `oauth-protected-resource` payload**: Include `resource` (the service URL) and `authorization_servers` (array of issuer URLs):
   ```json
   {
     "resource": "https://yourdomain.com",
     "authorization_servers": ["https://auth.yourdomain.com"]
   }
   ```

4. **Validate DNS**: Confirm every domain in `authorization_servers` resolves correctly in public DNS. A non-resolving domain causes 530 errors in scanners.

5. **Mount metadata endpoints**: Ensure each file is reachable at its standard path. Set `Content-Type: application/json` and CORS headers.

6. **Expose via Link headers**: Use `configure-agent-headers` to add Link headers pointing to both well-known files for passive agent discovery.

7. **Run scanner validation**: Test with `isitagentready.com` or the WorkOS scanner. Review the diagnostic output against specific rule names — e.g., "anonymous registration requires anonymous.credential_types_supported" maps to a specific nesting requirement.

### 2026: Mandatory PKCE and Token Binding

To secure machine-to-machine interactions and prevent authorization code interception, A2A OAuth flows require strict PKCE and cryptographic token binding:
- **Mandatory PKCE**: All client authorization requests must use PKCE with SHA-256 challenge. The authorization server metadata must declare `"code_challenge_methods_supported": ["S256"]`.
- **Authorized Presenter**: The token payload must contain the `azp` (Authorized Party) claim, which identifies the client agent that was issued the token.
- **DID Token Binding**: The token must bind the agent's DID. The JWT claims include the agent's public key identifier or DID URI in custom claims to ensure only the holder of the agent's private key can present the token.

### 2026: Client ID Metadata Documents (CIMD) & Legacy Registration

Prefer **Client ID Metadata Documents (CIMD)** so client agents identify via HTTPS URLs rather than stateful dynamic client registration:
- **CIMD Metadata URL**: Agent presents its HTTPS URL as `client_id`, and the authorization server fetches client metadata/JWKS cleanly (`client_id_metadata_document_supported: true`).
- **Legacy DCR Fallback (Transitional Only)**: Where older clients require `register_uri` / OIDC Dynamic Client Registration (RFC 7591), validate signed Agent Card payloads strictly and schedule removal once CIMD adoption completes.

## Checklist

- [ ] `authorization_servers` URLs are fully resolvable in public DNS (no 530 errors).
- [ ] `agent_auth` block exists in `oauth-authorization-server` metadata.
- [ ] `agent_auth.skill` points to the absolute URL of `auth.md`.
- [ ] Field names use `register_uri` and `claim_uri` (not `identity_endpoint`/`claim_endpoint`).
- [ ] `credential_types_supported` is nested inside credential type blocks, not at the `agent_auth` root.
- [ ] Both `anonymous` and `identity_assertion` paths are documented if supported.
- [ ] Metadata files are served with `Content-Type: application/json`.
- [ ] CORS headers allow agent clients to fetch the metadata cross-origin.
- [ ] Link headers via `configure-agent-headers` point to the well-known paths.
- [ ] Scanner validation passes without field-name or DNS errors.

## Related Skills

- **manage-auth-md**: Manage the `auth.md` discovery file that `agent_auth.skill` points to.
- **debug-identity-provider**: Diagnose and fix scanner validation failures after configuring metadata.
- **configure-agent-headers**: Expose OAuth metadata well-known paths via HTTP Link headers.
- **configure-mcp**: Wire up OAuth 2.1 + PKCE for the MCP server card.
- **manage-agent-identity**: Issue NHI credentials bound to the OAuth metadata scopes.

## Output Contracts

When the OAuth metadata configuration is recorded as a deployable artifact
(CI output, edge-config change, or handoff to an infra agent), emit:

- **`contracts/schemas/edge-deployment-spec.json`** listing the well-known paths, the served content types, the CORS headers, and the resolved DNS status of every `authorization_servers` entry.
- **`contracts/schemas/api-contract-spec.json`** describing the metadata JSON shapes (with required vs optional fields) so the deployment agent can validate before serving.
- For human-readable reports, a markdown summary of the scanner run output and any field-level failures.

Skip emission for ad-hoc local edits.

## Failure Modes

- **Field name drift**: a legacy field name (`identity_endpoint`, `claim_endpoint`) is used instead of `register_uri`/`claim_uri`. Mitigation: copy field names from the current spec; CI must reject the legacy names.
- **DNS dead link**: an `authorization_servers` URL does not resolve. Mitigation: CI must `dig` every URL and fail the deploy on NXDOMAIN or 530.
- **Nesting error**: `credential_types_supported` is at the `agent_auth` root instead of inside `anonymous` or `identity_assertion`. Mitigation: validate against the current schema; reject mis-nested structures.
- **`auth.md` H1 wrong**: the file starts with a different heading (case, BOM, or alternate phrasing). Mitigation: enforce `# Auth.md` exactly; lint on the first non-empty line.
- **PKCE not asserted**: metadata does not list `code_challenge_methods_supported: ["S256"]`. Mitigation: scanner must reject; CI must include the assertion.
- **OIDC registration endpoint unreachable**: `register_uri` returns non-200. Mitigation: e2e test the POST endpoint before each deploy; surface the failure in the scanner report.
- **CORS blocking agent clients**: cross-origin agent clients cannot fetch the metadata. Mitigation: set `Access-Control-Allow-Origin` per the deployment's CORS policy; verify with a preflight.

## Security Guardrails (OWASP ASI)

- **ASI03 Identity & Privilege Abuse**: the metadata defines the auth surface; do not include client secrets, signing keys, or unreleased callback URLs in the served JSON.
- **ASI04 Supply Chain**: the metadata must be schema-validated against the current `agent_auth` draft before every deploy; reject schema-drifted metadata.
- **ASI05 RCE Guard**: never construct metadata JSON from dynamic template strings derived from external content; build the JSON from a static schema and merge only allowlisted fields.
- **ASI07 Inter-Agent Communication**: the metadata is consumed by external agents and scanners; treat it as a public contract and review all changes before deploy.
- **ASI09 Human-Agent Trust Exploitation**: do not present a metadata set as "scanner-compliant" without a successful scanner run; surface the scanner output in the deploy record.
