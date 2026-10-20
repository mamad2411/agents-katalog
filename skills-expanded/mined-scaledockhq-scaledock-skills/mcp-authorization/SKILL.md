---
name: mcp-authorization
description: "MCP authorization: secure MCP servers with OAuth 2.1 as resource servers, and build MCP clients that discover, register and request audience-bound tokens. Use when adding or reviewing authorization on an HTTP MCP server, client, gateway or authorization server: 401 and 403 WWW-Authenticate challenges with resource_metadata, RFC 9728 Protected Resource Metadata at /.well-known/oauth-protected-resource, authorization server discovery through RFC 8414 or OpenID Connect Discovery, RFC 8707 resource indicators and audience validation, Client ID Metadata Documents (CIMD), pre-registration and deprecated Dynamic Client Registration (DCR), PKCE S256, insufficient_scope step-up and scope accumulation, RFC 9207 iss validation and mix-up attacks, Enterprise-Managed Authorization (ID-JAG), OAuth Client Credentials (machine-to-machine), token passthrough, confused deputy, SSRF, and TypeScript SDK auth helpers. Targets MCP 2026-07-28; supports 2025-11-25 and 2025-06-18, upgrades from 2025-03-26, and tracks the MCP draft."
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.3.0"
  kind: standard
---

# MCP authorization

The Model Context Protocol (MCP) authorization specification defines how an HTTP MCP server acts as an OAuth 2.1 resource server and how an MCP client finds the authorization server, registers, and obtains a token bound to that one server. This skill pins MCP revision 2026-07-28 and produces a server, client or review that meets its MUST-level rules.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources), with the page and heading it cites. MCP pages have no stable section numbers, so MCP rules cite the page and heading name; RFC and draft rules cite the section number. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: MCP server (resource server), MCP client, authorization server, or an MCP server that also calls upstream APIs (a proxy or gateway).
- Transport: Streamable HTTP or another HTTP transport (this skill applies), or STDIO (it does not; credentials come from the environment).
- Enterprise: whether an enterprise identity provider (IdP) must control access, which brings in Enterprise-Managed Authorization.
- User presence: whether a user authorizes access, or the client runs with no user (a service, pipeline or daemon), which brings in the Draft OAuth Client Credentials extension.
- Target version: MCP 2026-07-28 (current, the default; the revision the MCP Versioning page marks Current). MCP 2025-11-25 and MCP 2025-06-18 are supported: keep their behaviour only for a named peer on that revision. MCP 2025-03-26 is legacy: read it and upgrade from it, never author it. The MCP draft is a preview (posture: track): never emit it. OAuth 2.1 (draft-ietf-oauth-v2-1-16) and OAuth Client ID Metadata Document (draft-ietf-oauth-client-id-metadata-document-02) are previews (posture: track). Revision 2024-11-05 had no authorization. See [`references/versions.md`](references/versions.md).
- Sources: when refreshing this skill or when a rule looks out of date, re-read the MCP Versioning page for a newer Current revision, then the changelog and Deprecated Features page of that revision, then every URL in [Sources](#sources). Update the pins and bump the version.

## Invariants

1. **Authorization applies to HTTP transports only.** Authorization is OPTIONAL. HTTP-based implementations SHOULD conform to it, and STDIO implementations SHOULD NOT follow it and retrieve credentials from the environment instead (Authorization, Protocol Requirements).
2. **The server publishes Protected Resource Metadata.** MCP servers MUST implement RFC 9728, and the document MUST list at least one authorization server in `authorization_servers` (Authorization, Overview; Authorization Server Discovery, Authorization Server Location).
3. **The server says where the metadata is.** It MUST send `resource_metadata` in the `WWW-Authenticate` header of a 401 (RFC 9728 §5.1) or serve the metadata at a well-known URI. Clients MUST support both and use the header when present (Authorization Server Discovery, Protected Resource Metadata Discovery Requirements).
4. **Clients check the issuer of the metadata.** The `issuer` in the authorization server metadata MUST be identical to the issuer used to build the metadata URL, or the client rejects it (Authorization Server Discovery, Authorization Server Metadata Discovery; RFC 8414 §3.3).
5. **Every token request names the MCP server.** Clients MUST send `resource` in the authorization request and the token request, set to the canonical URI of the MCP server, whether or not the authorization server supports it (Authorization, Resource Parameter Implementation; RFC 8707 §2).
6. **The server accepts only its own tokens.** Servers MUST validate access tokens per OAuth 2.1 §5.2, MUST validate that the token was issued for them as the audience (RFC 8707 §2), and MUST answer invalid or expired tokens with 401 (Authorization, Token Handling).
7. **No token passthrough.** A server MUST NOT accept or transit any other token, and MUST NOT pass the client's token to an upstream API; it gets a separate token for the upstream (Authorization, Token Handling; Authorization Security Considerations, Access Token Privilege Restriction; Security Best Practices, Token Passthrough).
8. **Bearer header only.** Clients MUST send `Authorization: Bearer <token>` on every HTTP request, and the token MUST NOT be in the query string (Authorization, Token Requirements).
9. **PKCE with S256.** Clients MUST use PKCE, MUST use `S256` when technically capable, and MUST refuse to proceed when the authorization server metadata has no `code_challenge_methods_supported` (Authorization Security Considerations, Authorization Code Protection).
10. **Validate `iss` before using the code.** The client records the validated `issuer` with the PKCE verifier and applies RFC 9207 §2.4 to the authorization response before it sends the code to the token endpoint (Authorization, Authorization Response Validation).
11. **Credentials belong to one authorization server.** Clients MUST key client credentials by issuer and MUST NOT reuse them with a different authorization server (Client Registration, Authorization Server Binding).
12. **HTTPS and exact redirects.** Authorization server endpoints MUST use HTTPS; redirect URIs MUST be localhost or HTTPS, MUST be registered, and the authorization server MUST match them exactly (Authorization Security Considerations, Communication Security and Open Redirection).
13. **Proxies get consent per client.** An MCP proxy server that uses a static client ID with a third-party authorization server MUST obtain user consent for each dynamically registered client before forwarding to the third party (Authorization Security Considerations, Confused Deputy Problem).

## Workflow

1. **Scope the work and pick the version.** Confirm the role and transport from Inputs. For STDIO, stop: this skill does not apply. Target MCP 2026-07-28, and list any peers that still speak a supported older revision.
   -> [`references/versions.md`](references/versions.md)
   ✓ The design names the role, the HTTP transport, the canonical server URI and the target revision, and it is not a legacy or draft revision.
2. **Publish Protected Resource Metadata and challenges (server).** Serve RFC 9728 metadata, send `401` with `resource_metadata` and an initial `scope`, and send `403 insufficient_scope` for per-operation scopes.
   -> [`references/resource-server.md`](references/resource-server.md)
   ✓ An unauthenticated request gets a 401 whose header leads a client to the metadata, and the metadata lists an authorization server.
3. **Validate tokens (server).** Check signature or introspection, expiry, audience and scopes on every request; map failures to 401 or 403.
   -> [`references/resource-server.md`](references/resource-server.md)
   ✓ A token issued for another resource is rejected with 401, and no client token reaches an upstream API.
4. **Discover the authorization server (client).** Follow the header or the well-known probe order, pick an authorization server, fetch its metadata in the defined order and check `issuer`.
   -> [`references/client-flow.md`](references/client-flow.md)
   ✓ The client reaches the authorization server metadata from only the MCP server URL.
5. **Register the client.** Use pre-registered credentials, then CIMD, then DCR, then ask the user, and key the result by issuer.
   -> [`references/client-flow.md`](references/client-flow.md)
   ✓ The `client_id` in use was obtained for this issuer.
6. **Run the authorization code flow.** Send PKCE `S256`, `state`, `resource` and the selected scopes; validate `iss` and `state` on the callback; send `resource` again in the token request.
   -> [`references/client-flow.md`](references/client-flow.md)
   ✓ A callback with a wrong or missing `iss` is rejected according to the RFC 9207 table.
7. **Handle step-up.** On `403 insufficient_scope`, request the union of previously requested and newly challenged scopes, with a retry limit.
   -> [`references/client-flow.md`](references/client-flow.md)
   ✓ A second scope challenge does not drop the scopes from the first.
8. **Add Enterprise-Managed Authorization if the IdP must control access.** Exchange the IdP ID Token for an ID-JAG (RFC 8693), then the ID-JAG for an access token (RFC 7523).
   -> [`references/enterprise-managed-authorization.md`](references/enterprise-managed-authorization.md)
   ✓ The ID-JAG `aud` is the resource authorization server issuer and its `resource` is the MCP server.
9. **Use OAuth Client Credentials if no user is present.** Discover as in step 4, then run the `client_credentials` grant with a pre-registered client, authenticating with a JWT assertion (recommended) or a client secret, and send `resource` and `scope`.
   -> [`references/client-credentials.md`](references/client-credentials.md)
   ✓ The token request uses an authentication method listed in the authorization server's `token_endpoint_auth_methods_supported`, and no browser or DCR step runs.
10. **Review the attack surface.** Go through confused deputy, token passthrough, SSRF, session handles, URL validation, mix-up, localhost redirects and scope minimization.
    -> [`references/security.md`](references/security.md)
    ✓ Each item in the security reference has a mitigation or a reason it does not apply.
11. **Map to the TypeScript SDK if it is used.** Use the SDK's resource-server gate and client provider, and add the checks the SDK leaves to the app.
    -> [`references/typescript-sdk.md`](references/typescript-sdk.md)
    ✓ The app validates `state` itself and keys credentials by `ctx.issuer`.
12. **Upgrade** (only when asked). Follow the checklist for each step from the source revision to MCP 2026-07-28.
    -> [`references/versions.md`](references/versions.md)
    ✓ The upgraded server or client passes the Verify list below, and existing users keep the same grants.

## Verify before done

- [ ] `GET` on the metadata URL returns JSON with `resource` equal to the server's identifier and a non-empty `authorization_servers` (RFC 9728 §2, §3.3).
- [ ] A request without a token gets `401` with `WWW-Authenticate: Bearer resource_metadata="…"`.
- [ ] A token whose audience is a different resource gets `401`; a token without the needed scope gets `403` with `error="insufficient_scope"` and `scope`.
- [ ] Authorization and token requests both carry `resource` with the canonical server URI, without a fragment or trailing slash.
- [ ] The authorization request carries `code_challenge_method=S256`, and the client stops when the metadata lacks `code_challenge_methods_supported`.
- [ ] The callback handler checks `state` and `iss` before the code exchange, and does not show `error_description` after an `iss` mismatch.
- [ ] Client credentials are stored per issuer, and DCR is used only when neither pre-registration nor CIMD is available.
- [ ] No code path forwards the incoming access token to another service.
- [ ] A `client_credentials` client uses pre-registered credentials, sends `resource` in the token request, and prefers a JWT assertion over a client secret.
- [ ] Every outbound fetch of URLs taken from metadata or CIMD goes through the SSRF controls in the security reference.

## Reference index

- **`references/versions.md`**: every MCP revision with authorization, its status, what each changed, the upgrade checklists between adjacent revisions, and the draft. Load for steps 1 and 12.
- **`references/resource-server.md`**: Protected Resource Metadata, well-known URIs, 401 and 403 challenges, scope selection, token and audience validation, refresh token hints, error codes.
- **`references/client-flow.md`**: discovery order, authorization server selection, CIMD, pre-registration and DCR, PKCE, `resource`, `iss` validation, step-up and scope accumulation.
- **`references/enterprise-managed-authorization.md`**: the ext-auth Enterprise-Managed Authorization extension, ID-JAG token exchange, JWT bearer grant and discovery.
- **`references/client-credentials.md`**: the Draft ext-auth OAuth Client Credentials extension for machine-to-machine clients: when to use it, discovery, client authentication, authorization server metadata, negotiation, and how it differs from the authorization code flow.
- **`references/security.md`**: confused deputy, token passthrough, SSRF, session handles, local servers, URL validation, mix-up, localhost redirects, CIMD trust policies, scope minimization.
- **`references/typescript-sdk.md`**: what the MCP TypeScript SDK v2 provides for servers and clients, and what it leaves to the app.

## Related skills

- `mcp`, for the core Model Context Protocol, its transports and extension negotiation: `npx skills add ScaleDockHQ/scaledock-skills --skill mcp`
- `oauth`, for OAuth 2.1 and the RFCs this profile builds on, including the client credentials grant and client authentication: `npx skills add ScaleDockHQ/scaledock-skills --skill oauth`
- `jwt`, for validating JWT access tokens and ID-JAGs: `npx skills add ScaleDockHQ/scaledock-skills --skill jwt`
- `problem-details`, for error bodies next to 401 and 403 challenges: `npx skills add ScaleDockHQ/scaledock-skills --skill problem-details`
- `wimse`, for workload identity credentials of machine-to-machine clients: `npx skills add ScaleDockHQ/scaledock-skills --skill wimse`

## Sources

Status uses the publishing body's own maturity term. Checked is the date the source was last read.

- [MCP Versioning](https://modelcontextprotocol.io/specification/versioning): Specification page, lists 2026-07-28 as Current; names 2025-11-25 and earlier as handshake-based revisions, checked 2026-10-05.
- [MCP Authorization](https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization): Current, 2026-07-28, checked 2026-10-05.
- [MCP Authorization Server Discovery](https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization/authorization-server-discovery): Current, 2026-07-28, checked 2026-10-02.
- [MCP Client Registration](https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization/client-registration): Current, 2026-07-28, checked 2026-10-02.
- [MCP Authorization Security Considerations](https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization/security-considerations): Current, 2026-07-28, checked 2026-10-02.
- [MCP Key Changes](https://modelcontextprotocol.io/specification/2026-07-28/changelog): Current, 2026-07-28, checked 2026-10-05.
- [MCP Authorization (draft)](https://modelcontextprotocol.io/specification/draft/basic/authorization): Draft, draft as of 2026-10-05, same text as 2026-07-28, checked 2026-10-05. Draft posture: track.
- [MCP Changelog (draft)](https://modelcontextprotocol.io/specification/draft/changelog): Draft, no changes listed as of 2026-10-05, checked 2026-10-05. Draft posture: track.
- [MCP Authorization (2025-11-25)](https://modelcontextprotocol.io/specification/2025-11-25/basic/authorization): Final, 2025-11-25, checked 2026-10-05.
- [MCP Key Changes (2025-11-25)](https://modelcontextprotocol.io/specification/2025-11-25/changelog): Final, 2025-11-25, checked 2026-10-05.
- [MCP Authorization (2025-06-18)](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization): Final, 2025-06-18, checked 2026-10-05.
- [MCP Key Changes (2025-06-18)](https://modelcontextprotocol.io/specification/2025-06-18/changelog): Final, 2025-06-18, checked 2026-10-05.
- [MCP Authorization (2025-03-26)](https://modelcontextprotocol.io/specification/2025-03-26/basic/authorization): Final, 2025-03-26, checked 2026-10-05.
- [MCP Key Changes (2025-03-26)](https://modelcontextprotocol.io/specification/2025-03-26/changelog): Final, 2025-03-26, checked 2026-10-05.
- [MCP Deprecated Features](https://modelcontextprotocol.io/specification/2026-07-28/deprecated): Current, 2026-07-28, checked 2026-10-02.
- [MCP Security Best Practices](https://modelcontextprotocol.io/docs/2026-07-28/tutorials/security/security_best_practices): Documentation, 2026-07-28, checked 2026-10-02.
- [SEP-2350: Clarify client-side scope accumulation in step-up authorization](https://github.com/modelcontextprotocol/modelcontextprotocol/pull/2350): SEP, Final, merged 2026-03-28, checked 2026-10-02.
- [Enterprise-Managed Authorization](https://raw.githubusercontent.com/modelcontextprotocol/ext-auth/main/specification/stable/enterprise-managed-authorization.mdx): Stable extension, main at e5eef54 (2026-06-18), checked 2026-10-02.
- [OAuth Client Credentials Extension](https://raw.githubusercontent.com/modelcontextprotocol/ext-auth/main/specification/draft/oauth-client-credentials.mdx): Draft extension (Protocol Revision: draft), main at fb374c7 (2026-06-18; file last changed ce15435, 2025-10-14), checked 2026-10-05. Draft posture: build at fb374c7.
- [OAuth Client Credentials (MCP docs)](https://modelcontextprotocol.io/extensions/auth/oauth-client-credentials): Documentation, extension `io.modelcontextprotocol/oauth-client-credentials`, checked 2026-10-05.
- [Authorization Extensions (MCP docs)](https://modelcontextprotocol.io/extensions/auth/overview): Documentation, lists OAuth Client Credentials and Enterprise-Managed Authorization, checked 2026-10-05.
- [Extensions Overview (MCP docs)](https://modelcontextprotocol.io/extensions/overview): Documentation, extension identifiers and negotiation, checked 2026-10-05.
- [SEP-1046: Support OAuth client credentials flow in authorization](https://modelcontextprotocol.io/seps/1046-support-oauth-client-credentials-flow-in-authoriza): SEP, Final, created 2025-07-23, checked 2026-10-05.
- [MCP TypeScript SDK v2 documentation](https://ts.sdk.modelcontextprotocol.io/v2/): Released, v2 (packages 2.2.0, 2026-09-28), checked 2026-10-02.
- [TypeScript SDK: Authorization (server)](https://raw.githubusercontent.com/modelcontextprotocol/typescript-sdk/v2.2.0/docs/serving/authorization.md): Released, v2.2.0, checked 2026-10-02.
- [TypeScript SDK: OAuth (client)](https://raw.githubusercontent.com/modelcontextprotocol/typescript-sdk/v2.2.0/docs/clients/oauth.md): Released, v2.2.0, checked 2026-10-02.
- [TypeScript SDK: Machine authentication](https://raw.githubusercontent.com/modelcontextprotocol/typescript-sdk/v2.2.0/docs/clients/machine-auth.md): Released, v2.2.0, checked 2026-10-02.
- [TypeScript SDK: client auth source](https://raw.githubusercontent.com/modelcontextprotocol/typescript-sdk/v2.2.0/packages/client/src/client/auth.ts): Released, v2.2.0, checked 2026-10-02.
- [The OAuth 2.1 Authorization Framework](https://datatracker.ietf.org/doc/html/draft-ietf-oauth-v2-1-16): Internet-Draft (WG document), draft-ietf-oauth-v2-1-16, published 3 September 2026, checked 2026-10-06. MCP 2026-07-28 cited -13.
- [OAuth Client ID Metadata Document](https://datatracker.ietf.org/doc/html/draft-ietf-oauth-client-id-metadata-document-02): Internet-Draft (WG document), draft-ietf-oauth-client-id-metadata-document-02, published 6 July 2026, checked 2026-10-06. MCP 2026-07-28 cited -00.
- [Identity Assertion JWT Authorization Grant](https://datatracker.ietf.org/doc/html/draft-ietf-oauth-identity-assertion-authz-grant-04): Internet-Draft (WG document), draft-ietf-oauth-identity-assertion-authz-grant-04 (latest); Draft posture: build at -04 through the Stable extension, checked 2026-10-02.
- [RFC 9728: OAuth 2.0 Protected Resource Metadata](https://www.rfc-editor.org/rfc/rfc9728): RFC (Proposed Standard), RFC 9728, checked 2026-10-02.
- [RFC 8414: OAuth 2.0 Authorization Server Metadata](https://www.rfc-editor.org/rfc/rfc8414): RFC (Proposed Standard), RFC 8414, checked 2026-10-02.
- [OpenID Connect Discovery 1.0](https://openid.net/specs/openid-connect-discovery-1_0.html): Final, incorporating errata set 2, checked 2026-10-02.
- [RFC 8707: Resource Indicators for OAuth 2.0](https://www.rfc-editor.org/rfc/rfc8707): RFC (Proposed Standard), RFC 8707, checked 2026-10-02.
- [RFC 9207: OAuth 2.0 Authorization Server Issuer Identification](https://www.rfc-editor.org/rfc/rfc9207): RFC (Proposed Standard), RFC 9207, checked 2026-10-02.
- [RFC 6750: OAuth 2.0 Bearer Token Usage](https://www.rfc-editor.org/rfc/rfc6750): RFC (Proposed Standard, updated by RFC 8996 and RFC 9700), RFC 6750, checked 2026-10-02.
- [RFC 7591: OAuth 2.0 Dynamic Client Registration Protocol](https://www.rfc-editor.org/rfc/rfc7591): RFC (Proposed Standard), RFC 7591, checked 2026-10-02.
- [RFC 8693: OAuth 2.0 Token Exchange](https://www.rfc-editor.org/rfc/rfc8693): RFC (Proposed Standard), RFC 8693, checked 2026-10-02.
- [RFC 7523: JWT Profile for OAuth 2.0 Client Authentication and Authorization Grants](https://www.rfc-editor.org/rfc/rfc7523): RFC (Proposed Standard), RFC 7523, checked 2026-10-05.
