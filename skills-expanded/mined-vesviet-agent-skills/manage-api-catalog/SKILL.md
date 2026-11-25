---
name: manage-api-catalog
description: Use when publishing and maintaining RFC 9727 API Catalog registries for automated API discovery by agents, developer tools, and client SDKs.
allowed-tools: [read_file, write_file, edit_file, create_file, search_code, fetch, http_get, http_post, execute_command]
version: "1.0.0"
---

# Manage API Catalog

Use this skill to create and maintain the `/.well-known/api-catalog` Linkset file per RFC 9727. The API Catalog provides a machine-readable index of all public API endpoints, their OpenAPI specifications, and documentation URLs — enabling agent orchestrators and developer tooling to auto-discover a service's API surface without prior knowledge.

## Core Rules

- Format strictly according to RFC 9727 — the catalog is a Linkset document, not a generic JSON file.
- Map endpoints for OpenAPI specifications using `service-meta` relation type, and documentation using `service-doc`.
- The catalog MUST be placed at `/.well-known/api-catalog` (no `.json` extension per RFC 9727 spec).
- Serve with `Content-Type: application/linkset+json` or `application/linkset` as required by the request `Accept` header.
- Keep catalog entries stable — do not remove or rename existing `anchor` values once published; deprecate using the `status` field if the spec supports it.
- Treat the catalog as a public, signed contract: do not include internal-only API groups or unreleased endpoints without an explicit deprecation flag
- Validate every entry against the current RFC 9727 spec before deploy; reject schema-drifted Linksets (OWASP ASI04)
- Every `service-meta` and `service-doc` URL must be on the operator's own domain; reject third-party URLs at code review
- Set `ETag` and `Last-Modified` headers on the served catalog so external scanners and clients can detect silent changes (OWASP ASI01)

## When to Use

- Publishing a new API service's endpoint catalog for agent discovery
- Adding a new API version or endpoint to an existing catalog
- Verifying that agent clients and developer tooling can correctly parse the Linkset format
- Making a service compliant with agentic discovery standards (RFC 9727 is referenced by WorkOS and `isitagentready.com`)
- Updating or deprecating catalog entries after API changes

## Suggested Process

1. **Collect API specs and docs**: Gather all OpenAPI spec file URLs (e.g., `https://api.example.com/openapi.yaml`) and human-readable documentation URLs (e.g., `https://docs.example.com/api/orders`) for each logical API group.

2. **Build the Linkset document**: Structure each API group as a Linkset object with `anchor` (the canonical base URL for the API) and the relevant `service-meta` and `service-doc` links:
   ```json
   {
     "linkset": [
       {
         "anchor": "https://api.example.com/v1",
         "service-meta": [{ "href": "https://api.example.com/openapi.yaml", "type": "application/yaml" }],
         "service-doc": [{ "href": "https://docs.example.com/api/v1", "type": "text/html" }]
       }
     ]
   }
   ```

3. **Place at well-known path**: Deploy the catalog to `/.well-known/api-catalog`. For Cloudflare Pages, add as `public/.well-known/api-catalog` (no extension, ensure routing doesn't add one). For Workers, serve from `GET /.well-known/api-catalog`.

4. **Configure response headers**: Set `Content-Type: application/linkset+json` on the response. Add `Access-Control-Allow-Origin: *` or scoped CORS headers for cross-origin agent fetches.

5. **Validate format**: Run `curl https://yourdomain.com/.well-known/api-catalog -H "Accept: application/linkset+json"` and confirm:
   - Response status `200 OK`
   - `Content-Type: application/linkset+json`
   - Valid JSON Linkset structure

6. **Wire up discovery**: Add a `Link` header via `configure-agent-headers` pointing to the catalog (`rel="https://www.iana.org/assignments/link-relations/api-catalog"`) so agent scanners find it passively.

7. **Verify in scanner**: Check that `isitagentready.com` (or equivalent) confirms the API catalog is readable.

## Output Format

- `/.well-known/api-catalog` — Linkset JSON document (no file extension)
- Response headers: `Content-Type: application/linkset+json`, `Access-Control-Allow-Origin`

## Checklist

- [ ] Catalog file uses Linkset format per RFC 9727 (not plain JSON or OpenAPI).
- [ ] All API groups have `anchor` values that match their canonical base URLs.
- [ ] OpenAPI spec URL (`service-meta`) is active, reachable, and returns valid spec.
- [ ] Documentation URL (`service-doc`) is reachable and human-readable.
- [ ] File exists at `/.well-known/api-catalog` (no `.json` extension).
- [ ] Linkset returns `Content-Type: application/linkset+json` response header.
- [ ] CORS headers allow cross-origin agent fetches.
- [ ] Link header pointing to catalog is configured via `configure-agent-headers`.
- [ ] Scanner (e.g., `isitagentready.com`) confirms catalog is readable.

## Related Skills

- **configure-agent-headers**: Expose the API catalog via HTTP Link headers for passive agent discovery.
- **configure-agent-skills**: Set up the Agent Skills index manifest for capability-level (not endpoint-level) discovery.
- **configure-mcp**: Set up the MCP server card — often deployed alongside the API catalog for dual-mode discovery.
- **configure-oauth-metadata**: Wire up the authorization server metadata that protects catalog entries.
- **manage-auth-md**: Reference the catalog from the agentic registration document.

## Output Contracts

When the catalog is consumed by an infra agent, registry publisher, or CI
pipeline, emit:

- **`contracts/schemas/api-contract-spec.json`** describing the catalog shape, the entry list, and the deprecation status of each anchor. The consuming agent can then validate before publishing.
- **`contracts/schemas/edge-deployment-spec.json`** listing the well-known path, the served content type (`application/linkset+json`), and the CORS headers.
- For human-readable reports, a markdown table of the catalog entries and any version or deprecation changes.

Skip emission for routine single-entry additions that do not cross a role boundary.

## Failure Modes

- **Wrong content type**: the catalog is served with `application/json` instead of `application/linkset+json`. Mitigation: enforce the content type at the edge; verify with `curl -I`.
- **Anchor rename**: an existing `anchor` is renamed, breaking external clients. Mitigation: anchors are immutable once published; deprecate via `status: deprecated` and keep the anchor stable.
- **Stale OpenAPI spec**: the `service-meta` URL points to a spec that no longer matches the runtime API. Mitigation: validate the spec on every deploy; surface drift in CI.
- **CORS blocking scanner**: a cross-origin scanner cannot fetch the catalog. Mitigation: set `Access-Control-Allow-Origin` per the deployment's CORS policy; verify with a preflight.
- **Third-party URL**: a `service-meta` or `service-doc` URL points to a non-operator domain. Mitigation: enforce an allowlist at code review; reject third-party URLs.
- **Cache stale**: an intermediary serves an older version of the catalog. Mitigation: set `ETag` and `Last-Modified`; clients should revalidate before each session.

## Security Guardrails (OWASP ASI)

- **ASI01 Goal Hijack**: a malicious or compromised catalog entry could redirect agents to attacker-controlled endpoints. Validate every `href` against the operator's own domain allowlist.
- **ASI03 Identity & Privilege Abuse**: every entry that points to an authenticated endpoint must declare its auth requirement; do not infer auth from the URL.
- **ASI04 Supply Chain**: the catalog must be schema-validated against RFC 9727 before every deploy; reject schema-drifted Linksets.
- **ASI07 Inter-Agent Communication**: the catalog is consumed by external agents and scanners; treat it as a public contract and review all changes before publish.
- **ASI09 Human-Agent Trust Exploitation**: do not present a catalog as "RFC 9727 compliant" without a successful schema validation run; surface the validator output in the deploy record.

### 2026: RFC 9727 and Catalog Versioning

- **RFC 9727 API Catalog implementation:** Publish `/.well-known/api-catalog` returning a `linkset+json` document with `anchor`, `href`, and `type: application/openapi+json` link relations for each API. This enables automated API discovery by agent orchestrators and developer tooling.
- **API catalog versioning:** Each catalog entry should include a `version` field and a `deprecated` boolean flag. Automated clients (agents, SDKs) use the catalog to select the highest non-deprecated version without human intervention.

## 2027: Three-Tier Agentic Discovery

The 2027 discovery stack consolidates three well-known layers — publish all three when the service exposes each surface, and keep them consistent (an entry appearing in two layers must reference the same artifact):

| Tier | Well-known path | Standard | Covers |
|------|-----------------|----------|--------|
| 1 — A2A | `/.well-known/agent-card.json` (IANA permanent) | A2A v1.0+ (AAIF) | Agent identity, skills, auth schemes, signatures (JCS RFC 8785 + JWS RFC 7515) |
| 2 — Plain APIs | `/.well-known/api-catalog` | RFC 9727 Linkset | OpenAPI specs, docs, status — what this skill has always managed |
| 3 — AI Catalog | `/.well-known/ai-catalog.json` | Linux Foundation Agent-Card/ai-catalog (adoption votes pending in MCP + A2A steering committees) | Typed umbrella container indexing MCP Server Cards (`application/mcp-server-card+json`), A2A Agent Cards (`application/a2a-agent-card+json`), plugins, datasets, model cards, nested catalogs |

- AI Catalog entries are **media-type discriminated** and nestable; the catalog grows by adding typed entries, not new ad-hoc formats.
- Include the optional **Trust Manifest** extension when artifacts need verifiable provenance: publisher identity (DID or SPIFFE SVID), attestations, and source provenance per entry.
- Treat the AI Catalog as **emerging**: adoption votes are pending — publish it as an additive layer, and never make Tier 2 or Tier 3 the sole discovery path for a production API.
- Keep `agent.json`-era references out: the A2A card URI was renamed in v0.3.0 (2025-07-30); stale references to `/.well-known/agent.json` must be treated as a discovery failure.
