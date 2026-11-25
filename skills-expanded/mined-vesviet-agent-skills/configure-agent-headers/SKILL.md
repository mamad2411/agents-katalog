---
name: configure-agent-headers
description: Exposes well-known agentic endpoints via RFC 8288 HTTP Link headers and optional DNS-AID SVCB records, making a web service natively discoverable by AI agents without requiring dedicated well-known endpoint scans. Use when declaring agent-readiness (MCP server, API catalog, OAuth metadata, agent skills) on a Cloudflare Pages or Workers site without changing application routing.
allowed-tools: [read_file, write_file, edit_file, create_file, search_code]
version: "1.0.0"
---

# Configure Agent Headers

Use this skill to expose well-known agentic endpoints natively via HTTP response headers (RFC 8288 Link headers) and DNS Service Bindings (DNS-AID). This is the lowest-friction way to declare agent-readiness — no routing changes, no new pages, just headers and optional DNS records.

## Core Rules

- Serve `Link: </.well-known/...>; rel="..."` headers on all primary responses (especially `GET /`).
- Link header format MUST conform to RFC 8288 — use `rel` types that match the agentic discovery spec.
- DNS-AID SVCB records are optional but recommended for domain operators who want DNS-level discoverability.
- Headers must be set at the edge or CDN level — do not rely solely on origin application code which may not apply to all routes.
- Do not expose internal-only endpoints via Link headers. Only publicly accessible discovery endpoints.
- Verify that every URL in a Link header is on a domain the operator controls; third-party URLs in Link headers can enable agent phishing (OWASP ASI01)
- Do not place credentials, tokens, or PII in Link header values; Link headers are publicly cacheable
- `Link: </.well-known/mcp-server-card>; rel="mcp-server-card"` or `/.well-known/mcp/server-card.json` (plus `rel="agent-card"` for `/.well-known/agent-card.json` and `/.well-known/ai-catalog.json`).
- **Markdown Content Negotiation & Content Signals**: Support `Accept: text/markdown` by returning `Content-Type: text/markdown; charset=utf-8`, `Vary: Accept`, and `x-markdown-tokens` alongside `robots.txt` Content Signals (`ai-train`, `search`, `ai-input`) to cut agent token overhead.
- **Web Bot Auth (RFC 9421)**: When operating signed crawlers or verifier bots, advertise `/.well-known/http-message-signatures-directory` and validate `Signature` / `Signature-Input` / `Signature-Agent` headers.
- Treat the Link header itself as a discovery contract: schema-drift between the declared `rel` and the served payload must be rejected by the scanner (OWASP ASI04)

## When to Use

- Making a Cloudflare Pages / Workers site agent-ready without changing application code
- Declaring MCP server presence, API catalog, agent skills manifest, or oauth metadata via headers
- Setting up DNS-AID for domain-level agent discoverability (enterprise or DNS-operator contexts)
- Verifying that an existing site already exposes correct Link headers for agentic scanners

## Suggested Process

1. **Identify target endpoints**: List all well-known paths to expose — typically a subset of: `/.well-known/mcp/server-card.json`, `/.well-known/api-catalog`, `/.well-known/agent-skills/index.json`, `/.well-known/oauth-protected-resource`, `/.well-known/oauth-authorization-server`.

2. **Choose header injection method**: For Cloudflare Pages, use the `_headers` file in `public/`. For Workers/Workers for Platforms, set headers in the worker response. For other CDNs, use their header injection config.

3. **Format Link headers**: Each well-known path needs its own `Link` header line with the correct `rel` type:
   ```
   /.well-known/mcp/server-card.json: rel="mcp-server-card"
   /.well-known/api-catalog: rel="https://www.iana.org/assignments/link-relations/api-catalog"
   /.well-known/oauth-authorization-server: rel="https://www.iana.org/assignments/link-relations/oauth-authorization-server"
   ```
   Refer to each spec for the canonical `rel` string.

4. **Deploy and verify**: Run `curl -I https://yourdomain.com/` and confirm the Link headers appear. Use `isitagentready.com` or a similar scanner to confirm agent-readable discovery.

5. **Configure DNS-AID (optional)**: Add `SVCB` records to the domain's DNS pointing to the agentic service metadata endpoint. Document the record values for the domain operator.

6. **Audit scope**: Check that no internal-only endpoints are leaked via Link headers. Review the list of exposed `rel` types against the domain's actual capabilities.

### 2026: Link Header Security and DNS-AID SVCB Adoption

- Link header security: when exposing `Link: <url>; rel="mcp-server"`, ensure the target URL is under your own domain; third-party URLs in Link headers can enable agent phishing attacks.
- DNS-AID SVCB adoption status: DNS-AID is still an IETF draft (not RFC) as of mid-2026; implement Link headers as primary discovery mechanism; DNS-AID only as supplementary signal for DNS-aware clients.

## Output Format

- `public/_headers` or worker response headers file with Link header entries
- DNS-AID SVCB record configuration (documentation for DNS operator, if needed)

## Checklist

- [ ] Well-known endpoints are identified and all publicly accessible.
- [ ] Link headers conform to RFC 8288 syntax — correct angle-bracket format and `rel` types.
- [ ] Headers appear on `GET /` response (verified via `curl -I`).
- [ ] DNS-AID SVCB records are documented if domain-level discovery is needed.
- [ ] No internal-only endpoints are exposed via Link headers.
- [ ] Link headers verified in target deployment environment (staging then production).
- [ ] `isitagentready.com` or equivalent scanner confirms headers are readable.
- [ ] Headers are set at edge, not just origin (so all routes receive them).

## Related Skills

- **configure-oauth-metadata**: Wire up the `oauth-authorization-server` and `oauth-protected-resource` endpoints that Link headers will point to.
- **configure-mcp**: Set up the MCP server card endpoint declared in Link headers.
- **manage-api-catalog**: Wire up the RFC 9727 API catalog endpoint declared in Link headers.
- **configure-agent-skills**: Set up the agent skills index manifest declared in Link headers.

## Output Contracts

When the Link header set is recorded as a deployable artifact (CI output,
edge-config change, or handoff to an infra agent), emit:

- **`contracts/schemas/edge-deployment-spec.json`** listing each Link header entry, the route it attaches to, and the `rel` type. The deployment agent can then validate the spec against the live headers.
- For a single-route change, a markdown table is sufficient; the JSON spec is required when more than one route is updated or when an infra agent consumes the output.

Skip emission for ad-hoc local edits.

## Failure Modes

- **Wrong rel type**: the `rel` value does not match the IANA-registered relation. Mitigation: copy `rel` strings from the spec; never paraphrase.
- **Third-party URL in Link header**: an attacker-controlled URL is exposed via a `rel` type. Mitigation: only include URLs on the operator's own domain; reject third-party URLs at code review.
- **Header not on all routes**: the Link header is set on the origin but the CDN strips it. Mitigation: configure the header at the edge layer (`public/_headers`, Workers response, CDN config) and verify with `curl -I` per route.
- **Internal endpoint leaked**: an internal-only `.well-known/...` path is exposed publicly. Mitigation: maintain an allowlist of publicly accessible discovery paths; review the Link header set against it on every change.
- **Cache poisoning**: a Link header is cached by an intermediary with stale content. Mitigation: set appropriate `Cache-Control` headers and validate after deploy.

## Security Guardrails (OWASP ASI)

- **ASI01 Goal Hijack**: a malicious Link header could redirect an agent to a phishing surface. Only emit URLs on the operator's own domain.
- **ASI04 Supply Chain**: the `rel` types and the target payloads must be schema-validated against the published spec; schema-drift must fail the deploy.
- **ASI05 RCE Guard**: never construct Link header values from dynamic template strings that include user-supplied content; use a static allowlist of paths and rel types.
- **ASI07 Inter-Agent Communication**: the Link header is consumed by external agents; treat it as a public, signed contract and audit it on every change.
- **ASI09 Human-Agent Trust Exploitation**: do not present a Link header set as "agent-ready" when scanner validation has not been run; verify with `isitagentready.com` before claiming compliance.
