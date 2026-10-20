---
name: enum-cors-csp
description: CORS and CSP enumeration to map cross-origin trust boundaries and content-security gaps. Passive-first header audit across all in-scope endpoints, followed by safe active probing to classify per-endpoint CORS policy, CSP directives, and trust-chain weaknesses without exploitation.
disable-model-invocation: true
risk: safe-active
allowed-modes: [auto, bug-bounty, red-team, ctf, blue-team, offensive, grey-hat, forensic, reverse-engineering, mobile-pentest]
authorization-required: yes
evidence-outputs: [command-log, redacted-evidence, finding-draft, cors-policy-map, csp-directive-audit]
---

# Enum CORS and CSP

Use this skill to enumerate and classify Cross-Origin Resource Sharing (CORS) policies and Content Security Policy (CSP) directives across an in-scope target. CORS defines which external origins can read responses; CSP defines which resources the browser is allowed to load. Together they form the client-side trust boundary. This skill maps that boundary per endpoint, identifying gaps, overly permissive configurations, and misconfigurations that enable cross-origin attacks or content injection.

## Required inputs

- Validated target with list of in-scope endpoints, subdomains, and API paths.
- Scope file defining allowed testing methods and rate limits.
- Authorization cache valid for all in-scope hosts.
- Session token (if available) to test authenticated endpoint behavior. CORS on auth-required endpoints is higher impact than on public endpoints.
- List of known third-party origins the application integrates with for CSP comparison.

## Required gates

1. Use `pentest_agent_load_config` and `pentest_agent_validate_policy` before planning.
2. Use `pentest_agent_parse_scope` and `pentest_agent_validate_target` for every endpoint before active probing.
3. Use `pentest_agent_check_authorization` before any request that includes credentials or targets an authenticated endpoint.
4. Use `pentest_agent_build_command` for dry-run preview when using catalog tools for header capture and multi-origin probing.
5. Use `pentest_agent_execute_tool` for all active probing with rate-limit and output policy enforcement.
6. Use `pentest_agent_append_evidence` for policy maps, header audit results, and identified gaps.

## Workflow

### Phase 1 — Baseline header collection

Capture the full security header posture before testing individual policies.

- For each in-scope endpoint, send a baseline GET or OPTIONS request and record all response headers related to cross-origin and content security.
- Collect: `Access-Control-Allow-Origin`, `Access-Control-Allow-Credentials`, `Access-Control-Allow-Methods`, `Access-Control-Allow-Headers`, `Access-Control-Expose-Headers`, `Access-Control-Max-Age`, `Timing-Allow-Origin`, `Cross-Origin-Resource-Policy`, `Cross-Origin-Opener-Policy`, `Cross-Origin-Embedder-Policy`.
- Collect CSP directives: `Content-Security-Policy`, `Content-Security-Policy-Report-Only`, `X-Content-Security-Policy` (legacy).
- Collect related headers: `X-Frame-Options`, `X-Content-Type-Options`, `Referrer-Policy`, `Permissions-Policy`.
- Record which endpoints return which headers. An endpoint with no CORS headers behaves differently from one with permissive CORS headers.

### Phase 2 — CORS policy classification per endpoint

For each endpoint, determine the effective CORS policy by testing specific origin values.

- Send an `Origin: https://attacker.example.com` header. If the response includes `Access-Control-Allow-Origin: https://attacker.example.com`, the endpoint reflects arbitrary origins.
- Send an `Origin: null` header (simulating sandboxed iframes and file:// origins). If reflected, the endpoint trusts null origins.
- Send an `Origin: https://TARGET.evil.example.com` (prefix attack — tests regex anchoring). If the origin pattern is `*.target.com` and lacks the `^` anchor, this may match.
- Send an `Origin: https://evilTARGET.example.com` (suffix attack — tests missing `$` anchor). If reflected, the regex is unanchored.
- Send an `Origin: http://TARGET` (protocol downgrade). If the HTTPS endpoint reflects an HTTP origin, the scheme constraint is missing.
- For each test, record: origin sent, ACAO value returned, ACAC value returned, and whether the response includes the `Vary: Origin` header (proper caching behavior).

### Phase 3 — Credential-bearing CORS assessment

CORS with `Access-Control-Allow-Credentials: true` is the highest-impact configuration.

- Identify every endpoint that returns `ACAC: true` in any context. These endpoints can be read cross-origin when combined with a reflected origin.
- For each ACAC endpoint, send the Phase 2 origin probes with a valid session cookie to confirm that the ACAO reflection persists in authenticated responses.
- Check whether the same endpoint returns `ACAC: true` without authentication, with low-privilege authentication, and with high-privilege authentication. Privilege-tier variation in CORS policy is a configuration gap.
- Test pre-flight handling: send an `OPTIONS` request with `Origin`, `Access-Control-Request-Method`, and `Access-Control-Request-Headers` headers. Record which methods and headers the server allows cross-origin.
- Document every endpoint with reflected origin + ACAC:true as a high-priority CORS gap.

### Phase 4 — CSP directive audit

Audit the Content Security Policy for gaps that weaken protection.

- Parse the CSP header into its directive components: `default-src`, `script-src`, `style-src`, `img-src`, `connect-src`, `font-src`, `frame-src`, `frame-ancestors`, `form-action`, `base-uri`, `object-src`, `media-src`, `worker-src`, `manifest-src`, `upgrade-insecure-requests`, `block-all-mixed-content`, `report-uri`, `report-to`.
- Flag dangerous directive values: `'unsafe-inline'` in `script-src` (enables XSS), `'unsafe-eval'` in `script-src` (enables code injection), wildcard origins (`*`) in any directive, `data:` in `script-src`, `https:` without specific origins, missing `object-src` when `default-src` is permissive.
- Check whether CSP includes `frame-ancestors` or relies on legacy `X-Frame-Options`. `frame-ancestors` in CSP takes precedence but both should be set for defense in depth.
- Check whether `report-uri` or `report-to` is configured. CSP reporting indicates operational maturity; its absence with a strict policy may cause undetected violations.
- Check whether the CSP is delivered as `Content-Security-Policy` (enforcing) or `Content-Security-Policy-Report-Only` (monitoring). Report-only mode provides no protection.
- Test whether the CSP is consistent across endpoints. The main page and API endpoints often have different policies; the weaker policy governs the effective security boundary.

### Phase 5 — Trust-chain and integration gap analysis

Map the practical impact of CORS/CSP gaps against known integrations.

- Compare CORS-allowed origins against the integration map from Phase 1 of the enterprise-web skill (or build a fresh integration list). If the application embeds `https://trusted-partner.example.com` and that origin is in the CSP but the partner subdomain is unclaimed or vulnerable to takeover, the CSP trust is exploitable.
- Check `connect-src` and CORS together: CSP may allow `connect-src https://api.example.com` while CORS on that API endpoint reflects `*`. The combination enables cross-origin data exfiltration.
- Test subdomain trust chains. If CORS allows `*.example.com` and a subdomain is vulnerable to content injection (e.g., an abandoned S3 bucket, an unverified GitHub Pages site, or a user-controlled profile page), cross-origin attacks become possible.
- Document the trust-chain: which external origins are trusted by CORS and CSP, and whether those origins are verifiably controlled by the target organization.

## Decision points

- CSP enforcement: report-only CSP is a documentation finding, not an exploitable gap. Record it as a hardening recommendation.
- CORS on static assets: CORS gaps on static content (images, fonts) are lower severity than on API endpoints returning user data. Prioritize API endpoints.
- Credential-bearing CORS: endpoints with `ACAC: true` and reflected origin are always high severity. Stop CORS enumeration on that endpoint and escalate to vulnerability validation.
- Origin list depth: if you discover many subdomains, test a representative sample of origin bypass patterns rather than every subdomain. Flag the permissive pattern, not every instance.

## Prohibited behavior

No active exploitation of CORS gaps. Enumeration confirms policy; exploitation requires a separate authorized validation phase and a controlled attacker origin. No hosting of proof-of-concept pages on unauthorized infrastructure. No extraction of real user data during policy enumeration. No probing of out-of-scope origins. Do not run raw shell commands when a `pentest_agent_*` gate exists.

## Stop conditions

Stop on a specific endpoint when the policy is fully classified. Stop the full enumeration when all in-scope endpoints are mapped. Stop if CORS probing triggers a WAF block or rate limit. Stop if the authorization cache expires.

## Evidence

Append evidence via `pentest_agent_append_evidence`:
- Per-endpoint baseline header inventory.
- CORS policy matrix: endpoint, origin tested, ACAO result, ACAC result, Vary header, pre-flight methods.
- Credential-bearing CORS endpoint list with risk classification.
- CSP directive audit: per-endpoint CSP parsed into directive components with gap flags.
- Trust-chain map: CORS-allowed and CSP-allowed origins cross-referenced against integration inventory.

Never store session tokens, cookies, response bodies containing user data, or CSP report endpoint URLs containing internal hostnames. Redact all secrets.

## Report handoff

Record findings via `pentest_agent_record_finding` for: reflected origin with credentials (high), missing CORS headers on sensitive endpoints (medium), CSP with unsafe-inline and no nonce/hash (medium), CSP in report-only mode without enforcing policy (low), trust-chain gaps where a CSP-allowed or CORS-allowed origin is unverified (medium), and missing frame-ancestors on sensitive pages (medium). Render the final report with `pentest_agent_render_report`.
