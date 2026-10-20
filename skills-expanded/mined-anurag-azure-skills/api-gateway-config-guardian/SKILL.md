---
name: "api-gateway-config-guardian"
description: "Cloud-agnostic API gateway configuration validation and remediation (Azure APIM, AWS API Gateway, GCP API Gateway/Apigee, OCI API Gateway) expressed as IaC (Terraform, Bicep, CloudFormation, ARM, OpenAPI). Detects implementation gaps and missing functionality — auth/token propagation, cookie rewrite after refresh, CORS, routing, rate limiting, observability — and fixes them in place."
version: 1
created: "2026-06-24T03:34:24+05:30"
updated: "2026-06-26"
---
## When to Use
Use whenever the artifact under review is an **API gateway configuration** — independent of cloud or IaC language. Resolve the provider and format from the input/TSA, never hard-code:

- Provider → `tsa.technology.api.gateway` ∈ { AzureApiGateway/APIM, AWS API Gateway (REST/HTTP), GCP API Gateway/Apigee, OCI API Gateway, Kong, NGINX, … }
- IaC format → Terraform (`*.tf`, `templatefile`), Bicep, ARM, CloudFormation/SAM, Pulumi, or a raw policy/contract document (APIM `<policies>` XML, OpenAPI `x-amazon-apigateway-*`, Apigee proxy XML).

Activate this skill for the validate-and-fix task: given a gateway config file (plus optional requirements/spec), confirm it implements the intended behaviour, find gaps, and emit a corrected file in the **same format**.

## Procedure
1. **Identify** provider + IaC format + the resources declared (gateways, APIs/products, routes/operations, policies, backends, auth, CORS, throttling).
2. **Extract intended behaviour** from the supplied requirements/spec and (when RAG is enabled) from `get_rag_context`. Treat the requirement spec as the source of truth for *what* the gateway must do.
3. **Trace each request-lifecycle stage** the gateway controls: inbound transform → authN/authZ → routing/backend selection → backend request transform → backend response transform → outbound transform → error handling. A gap at any stage is a finding.
4. **Run the Validation Rules** (below) for the resolved provider. Map every rule to PASS / PARTIAL / FAIL with file:line evidence.
5. **Remediate** every FAIL/PARTIAL: edit the config in place, preserving structure, naming, variables, and the IaC idiom (do not rewrite Terraform as Bicep). Keep changes minimal and annotated.
6. **Re-validate** the edited file against the same rules; iterate until all gates PASS or the loop budget is exhausted. Report residual items.
7. **Emit** the full corrected file plus a changelog of what changed and why.

## Patterns
- **Token continuity end-to-end.** Whatever credential the backend authenticates on (Authorization header, cookie, mTLS, API key) MUST carry the *current* value on the forwarded request. After a token refresh/exchange, rewrite **every** representation of that token the backend reads — header AND cookie — before forwarding, not just one.
- **Refresh/exchange side-channels are atomic.** If the gateway refreshes a token mid-request, the new token must (a) replace the forwarded credential for the in-flight call and (b) be persisted to the client (Set-Cookie / response) so subsequent calls carry it.
- **Cookie scoping behind fronting layers (CDN/WAF/Front Door/CloudFront).** Derive `Domain`/`Path`/`SameSite`/`Secure` from configuration, not from `Origin`/`Host` request headers (which reflect the internal hop, not the public domain). Cross-origin + credentials ⇒ `SameSite=None; Secure`; same-origin ⇒ `Lax`.
- **CORS and credentials are consistent.** `allow-credentials=true` forbids `*` origins; allowed methods/headers cover actual usage; preflight is handled before auth.
- **Fail closed on auth, fail open on enrichment.** Missing/invalid credential ⇒ reject (401/403). A best-effort enrichment side-call (refresh, claims lookup) failing ⇒ continue and let the validator reject, never 500.
- **Idempotent, declarative IaC.** No literal secrets; values via variables/secret refs; named values/parameters; deterministic ordering.

## Anti-Patterns
- Updating the `Authorization` header after refresh but leaving the stale token in the forwarded `Cookie` (or vice-versa) — the backend reads the one you didn't update. *(This is the canonical "refresh works but call still 401s" defect.)*
- Deriving cookie `Domain` from `Origin`/`Host` behind a CDN/Front Door → mis-scoped cookie the browser drops.
- `Max-Age`/TTL on the rotated credential far shorter than its real lifetime, defeating the refresh-grace design.
- Parsing multi-valued response headers (e.g. multiple `Set-Cookie`) with naive `StartsWith`/split, silently extracting nothing.
- Hard-coding provider/region/stack assumptions instead of resolving from the config/TSA.
- Secrets, subscription keys, or client secrets inlined in the IaC.

## Tool Selection
- `read_file` / `write_file` / `command_line` — read the config, write the corrected file, run formatters/validators (`terraform validate`, `terraform fmt`, `bicep build`, `cfn-lint`, `az apim … --validate`, `openapi` linters) when available.
- `get_rag_context` (Slingshot-ASK) — retrieve the authoritative requirement spec, prior incidents, and provider policy references for *this* account/project before deciding a gap is real.
- `get_account_project_access_details` (Slingshot-ASK) — resolve `account_name`/`project_name`/`resource_name` for RAG scoping.
- `todo` — track each FAIL finding to closure across validate→fix→re-validate iterations.

## Validation Rules
Cloud-agnostic gates (map provider primitives onto each):
- **AUTH-1** Every protected route enforces authN; unauthenticated requests fail closed (401/403).
- **AUTH-2** Credential the backend reads is identified; after any refresh/exchange the forwarded **header and cookie** both carry the new value before backend forward. *(FAIL = the refresh-token cookie defect.)*
- **AUTH-3** Token validation (issuer/audience/signature/expiry) matches the issuer that mints the token.
- **COOKIE-1** Cookie attributes (`Domain`/`Path`/`Secure`/`HttpOnly`/`SameSite`/`Max-Age`) are config-driven and correct behind the fronting layer.
- **CORS-1** CORS is internally consistent with credentials mode and precedes auth for preflight.
- **ROUTE-1** Every intended operation maps to a backend; no dangling/duplicate routes; backend URLs are variables/refs.
- **RESIL-1** Timeouts, retries, rate-limit/quota, and circuit-breaking present where required.
- **ERR-1** Structured, non-leaking error responses; enrichment side-calls fail open.
- **OBS-1** Logging/tracing/metrics correlation IDs emitted per observability spec.
- **IAC-1** No literal secrets; idempotent; provider-version pinned; formats/validates clean.
FAIL the configuration if any required gate FAILs; PARTIAL where present-but-incomplete.

## Deployability Gate (delegate to iac-deployability-verificationv2)
A fixed config is worthless if it cannot deploy. Before emitting, run the deployability gate:
**API authenticity** (no invented functions/methods/attributes/resource args), **self-containment** (declare
every variable/param/secret you reference; emit a companion vars file), **topology correctness**, and
**native-tool verification** — never report PASS on well-formedness alone. See `iac-deployability-verificationv2`.

### API-authenticity examples (per provider — the embedded-expression runtime has its OWN narrow surface)
- **Azure APIM policy C#**: request/response `Headers` is `IReadOnlyDictionary<string,string[]>` — read via the
  indexer, `TryGetValue`, or `GetValueOrDefault`. There is **no `GetValues()`** (that's `System.Net.Http`). Client
  IP behind Front Door comes from `X-Forwarded-For`, not `context.Request.IpAddress`.
- **AWS API Gateway (VTL / mapping templates)**: only `$context`, `$input`, `$util` members that are documented;
  client IP behind CloudFront is `$context.identity.sourceIp` resolved from forwarded headers.
- **GCP Apigee**: Message Templates / flow variables (`request.header.*`, `client.ip`) — `client.ip` is the LB
  hop unless `X-Forwarded-For` is used.
- **CloudFormation/Terraform**: only documented resource types and arguments; pin provider versions.
Rule: if you cannot confirm an identifier exists in the target runtime's documented surface, do NOT use it.

## RAG Sources
When `use_rag` is enabled, call `get_rag_context` (scoped by `get_account_project_access_details`) for: the requirement/spec the gateway must satisfy, prior production incidents (e.g. auth/token regressions), provider-specific policy references, and confirmation of any uncertain provider API/attribute. Prefer retrieved spec/incident evidence over assumptions; cite what was retrieved in the findings.
