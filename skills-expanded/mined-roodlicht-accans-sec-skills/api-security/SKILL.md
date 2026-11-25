---
name: api-security
description: API security review against OWASP API Top 10 2023. Covers auth (OAuth2/JWT/API-keys), object-level authorization (BOLA/IDOR), schema validation, rate-limiting, CORS, SSRF, and GraphQL-specific concerns (introspection, query depth, batching).
---

# API Security

## When to use

This skill is the API-specific lens: REST and GraphQL endpoints, their auth, their contract, their abuse surface. It complements `security-review` when the code is an API layer, and it is invoked by framework skills (`django-security`, `spring-security`, `rails-security`, `nextjs-security`) for the API-specific rules.

Triggers on:

- A question like "review this API for security issues", "is the auth on this endpoint OK", "do we cover OWASP API Top 10", "do we have enough rate-limiting", "how do we handle CORS".
- New or changed OpenAPI/Swagger/GraphQL schemas.
- Code exposed as an external API: REST controllers, GraphQL resolvers, gRPC handlers, webhook endpoints, service-mesh routes.
- A PR touching auth middleware, rate-limiting, schema validation, or CORS config.
- A handoff from `security-review` or a framework skill that points to API-specific depth.

### When NOT (handoff)

- Framework-specific API config (Django REST Framework, Spring MVC, Rails API-only, Next.js route handlers) → the relevant framework skill first. They know their own defaults and foot-guns better.
- Pure code-pattern question without API context ("is this query safe") → `secure-coding`.
- Active API pentesting with exploitation → `web-exploit-triage` and `payload-crafter`.
- Dependency vulns in API libraries → `cve-triage`.
- API-gateway config in the cloud (WAF rules, AWS API Gateway resource policies) → `iac-security`.
- Runtime WAF tuning on existing production is out of scope; that is ops work.

## Approach

Seven phases organized around OWASP API Security Top 10 2023 (API1–API10). Each phase covers one or more API categories.

### 1. Inventory: endpoints and contract (API9)

What is not documented cannot be audited. Always start with the inventory.

- **Endpoint list.** From code (route decorators, router definitions), from a schema (OpenAPI, GraphQL SDL), or via a spider. Complete means: public endpoints, admin endpoints, internal or debug endpoints, webhook receivers, old versions still live.
- **API9 Improper Inventory Management.** Old v1 endpoints still running, staging endpoints on the same host, debug endpoints in production. Document what is alive, what is deprecated, and what must be turned off immediately.
- **Contract check.** Is there a machine-readable contract (OpenAPI 3.x, GraphQL schema)? If not: get one before going further. Without a contract, schema validation (phase 3) is not enforceable.

### 2. Authentication (API2)

- **Mechanism.** OAuth 2.0 / OIDC, API keys, JWT, session cookies, mTLS. Each has its own failure modes.
- **OAuth 2.0.** PKCE required for public clients (mobile, SPA). No more Implicit flow (deprecated in OAuth 2.1). Strict redirect-URI matching, no wildcards. Use the state parameter against CSRF on the callback.
- **JWT.** `alg: none` rejected. Prevent algorithm confusion (do not accept an RS256 key as an HS256 secret). Expiry (`exp`) and not-before (`nbf`) checked. `kid` in the header must hit a whitelist, not be used for unvalidated key lookup.
- **API keys.** Scoped per client, not one master key for everything. Rotatable. Not in the URL query (ends up in logs); use `Authorization: Bearer` or a custom header. Rate-limit per key (see phase 4).
- **Session cookies.** HttpOnly, Secure, SameSite=Lax/Strict. Server-side session invalidation on logout. Rotate on privilege change.
- **mTLS** for service-to-service in a zero-trust setup. Certificate validation always on, no fallback to plain TLS.

Multi-factor for admin and privileged flows. Recovery flows (password reset, e-mail change, MFA reset) are separate auth paths with their own weaknesses; review them separately.

### 3. Authorization (API1, API3, API5)

The three authorization categories from the OWASP API Top 10 together. This is where most production bugs live.

- **API1 Broken Object Level Authorization (BOLA / IDOR).** Endpoint `/api/documents/{id}` checks authentication but not whether the actor is allowed to see `{id}`. Fix: ownership check on every lookup path. Not at the route level, at the resource level. Query like `SELECT * FROM documents WHERE id = :id AND (owner = :user OR :user IN shared_with)`.
- **API3 Broken Object Property Level Authorization.** The classic mass-assignment: client sends `{"id": 1, "role": "admin"}` and the API accepts `role` blindly. Fix: input schema that whitelists only accepted fields. Output schema that does not return sensitive fields (e.g. `password_hash`, `internal_notes`). Framework primitives: DRF Serializers, Spring `@JsonIgnore`, Rails `strong_parameters`, Pydantic `model_dump(include=...)`.
- **API5 Broken Function Level Authorization.** Admin endpoints reachable for non-admins, usually because the authZ check happens per route instead of being centrally enforced. Fix: a central policy-enforcement point (middleware or decorator), deny-by-default for routes without an explicit role claim. Test: try every admin endpoint as a regular user.

Authorization tests belong in the integration suite, not only in the code review.

### 4. Resource limits and business-flow abuse (API4, API6)

- **API4 Unrestricted Resource Consumption.** Rate-limiting per IP and per authenticated identity (API key/user). Different limits per endpoint class: auth endpoints stricter (e.g. 5/minute) than read endpoints (60/minute) than write endpoints (20/minute). Pagination required on list endpoints with a max page size. Body-size limits (e.g. 1 MB unless file upload). Query complexity for GraphQL (see phase 6).
- **API6 Unrestricted Access to Sensitive Business Flows.** Ticket-resale bots, credit farming, coupon stacking, bulk signup for fraud. Fix: CAPTCHA or proof-of-work on high-value flows, device fingerprinting for detection, velocity checks (N transactions per minute per account), and anomaly detection in monitoring. This overlaps with fraud engineering, not pure security, but the API is the attack surface.

Rate-limit responses: HTTP 429 with `Retry-After` header, not 503 or timeout. Logs must record rate-limit hits with identity, endpoint, and window.

### 5. SSRF and configuration (API7, API8)

- **API7 Server Side Request Forgery.** Endpoints that make an outbound HTTP call based on user input (webhook dispatch, URL preview, image proxy, PDF rendering, OAuth redirect). Fix: allowlist of permitted hosts. Block private IP ranges (10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16, 127.0.0.0/8, 169.254.169.254 for cloud metadata) including DNS resolution (prevent rebinding). Timeouts and redirect limits. Use libraries with SSRF checks (e.g. `SafeRequests` in Python, `safe-request` in Node).
- **API8 Security Misconfiguration.** CORS config without wildcards (`Access-Control-Allow-Origin: *` is acceptable only on explicitly public, non-auth endpoints). Security headers: HSTS, CSP, X-Content-Type-Options: nosniff, X-Frame-Options, Referrer-Policy. Default error pages that do not leak stack traces or framework info. Verbose API errors back to the client only in non-prod.

CORS-specific: `Access-Control-Allow-Credentials: true` with `Origin: *` is impossible and some browsers block it, but the misconfiguration attempt itself signals that the auth model has not been thought through.

### 6. GraphQL-specific (where applicable)

REST checks above largely apply to GraphQL too, plus:

- **Introspection.** Turn off in production (`introspection: false` in Apollo, `GraphQLSchema` without `__schema` resolver). Reduces the recon surface. Alternative for devs: commit the schema as a file and serve it locally.
- **Query-depth limit.** Limit nesting depth to prevent exponential queries. Libraries: `graphql-depth-limit` (Node), `graphql-core` query-complexity (Python).
- **Query-complexity scoring.** Cost per field (e.g. list fields 10 points, scalar 1 point), total budget per request. Stops a single batched query from becoming a DB nightmare.
- **Batching limit.** Cap alias-based batching (N queries in one request); otherwise it undermines per-request rate limits.
- **Persisted queries.** In high-stakes setups, only accept server-known queries (hash-based). Client sends a hash, server knows the query. Shields against arbitrary queries from a compromised client.
- **Authorization in resolvers.** Do the actor check per resolver. GraphQL fields can each have their own authZ rules, and a blanket check at the root produces IDOR in nested queries.

### 7. Downstream API consumption (API10)

If your API itself consumes other APIs (third-party, internal services), you are also the attacker's target surface via transitive trust.

- **Treat upstream input as user input.** A JSON response from a third-party API is not a trusted source. Validate the schema on receipt.
- **TLS validation on** for outbound calls, no `verify=False`.
- **Timeout and retry strategy.** Unbounded retries on 5xx = DoS amplification. Circuit breakers on persistent failures.
- **Secret hygiene on outbound auth.** API keys for external providers in the vault, no hardcoded credentials. See `secrets-scanner`.

## Output

Report structure (compatible with the `security-review` report format):

```
API security review — <service/scope>
Contract: <OpenAPI 3.x file | GraphQL SDL | none (blocker)>
Endpoints in scope: N | Tested: M

OWASP API Top 10 2023 pass:
  API1 BOLA:                 <clean | findings: ...>
  API2 Broken Authentication:<clean | findings: ...>
  API3 BOPLA / mass assign:  <...>
  API4 Resource consumption: <...>
  API5 Function-level authZ: <...>
  API6 Business-flow abuse:  <...>
  API7 SSRF:                 <...>
  API8 Misconfiguration:     <...>
  API9 Inventory:            <...>
  API10 Downstream APIs:     <...>

GraphQL-specific (if applicable):
  Introspection in prod:     <off | on - finding>
  Depth limit:               <n | none - finding>
  Complexity scoring:        <on | none - finding>
  Batching limit:            <n | unlimited - finding>

Findings (severity-sorted, blockers first, follow security-review format)

Verification-loop:
  Verdict: ...
  Security verdict: ...
```

Findings themselves as in `security-review`: location, CWE/API category, severity, reproduction, fix direction. Reproduction preferably as a curl example against a test endpoint, not against production.

## References

- OWASP API Security Top 10 2023 — [https://owasp.org/API-Security/editions/2023/en/0x11-t10/](https://owasp.org/API-Security/editions/2023/en/0x11-t10/). Canonical categorization.
- OWASP API Security Project — [https://owasp.org/www-project-api-security/](https://owasp.org/www-project-api-security/). Broader context plus cheat sheets per category.
- OpenAPI Specification 3.1 — [https://spec.openapis.org/oas/v3.1.0](https://spec.openapis.org/oas/v3.1.0). Schema basis for validation.
- OAuth 2.0 RFC 6749 — [https://datatracker.ietf.org/doc/html/rfc6749](https://datatracker.ietf.org/doc/html/rfc6749). Original spec.
- OAuth 2.0 Security Best Current Practice — [https://datatracker.ietf.org/doc/html/draft-ietf-oauth-security-topics](https://datatracker.ietf.org/doc/html/draft-ietf-oauth-security-topics). Current guidance (PKCE, forbidden flows).
- OAuth 2.1 draft — [https://datatracker.ietf.org/doc/html/draft-ietf-oauth-v2-1](https://datatracker.ietf.org/doc/html/draft-ietf-oauth-v2-1). Consolidation of OAuth 2.0 plus BCP.
- JWT BCP RFC 8725 — [https://datatracker.ietf.org/doc/html/rfc8725](https://datatracker.ietf.org/doc/html/rfc8725). JWT-specific security gotchas.
- CORS / Fetch Standard — [https://fetch.spec.whatwg.org/#cors-protocol](https://fetch.spec.whatwg.org/#cors-protocol). Primary CORS source.
- GraphQL Specification — [https://spec.graphql.org/](https://spec.graphql.org/).
- OWASP GraphQL Cheat Sheet — [https://cheatsheetseries.owasp.org/cheatsheets/GraphQL_Cheat_Sheet.html](https://cheatsheetseries.owasp.org/cheatsheets/GraphQL_Cheat_Sheet.html). Introspection, depth, batching.
- NIST SP 800-204 — [https://csrc.nist.gov/pubs/sp/800/204/final](https://csrc.nist.gov/pubs/sp/800/204/final). Microservices security.

## Categories

- appsec
