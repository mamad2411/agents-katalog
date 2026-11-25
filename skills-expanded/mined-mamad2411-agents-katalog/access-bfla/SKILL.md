---
name: access-bfla
description: Broken Function Level Authorization — validate that role boundaries prevent unauthorized function access across API versions, HTTP methods, path variants, and content types.
disable-model-invocation: true
risk: safe-active
allowed-modes: [auto, bug-bounty, red-team, ctf, blue-team, offensive, grey-hat, forensic, reverse-engineering, mobile-pentest]
authorization-required: yes
evidence-outputs: [command-log, redacted-evidence, finding-draft]
---

# BFLA — function-level authorization validation

Use this skill to verify that lower-privilege roles cannot invoke admin, management, internal, or cross-tenant functions on an authorized, in-scope target. Focus on API surface reachability: what endpoints exist, which roles can reach them, and whether function-level enforcement breaks under version drift, method override, path manipulation, or content-type switching.

## Required inputs

- Written scope naming the target API, tenant, identity provider, authorized test roles (at least two distinct privilege levels), allowed endpoint families, and explicit permission for function-access testing.
- User-owned or project-approved test accounts only. Never use borrowed, harvested, shared, or customer accounts.
- Valid authorization cache for the target. If the engagement also probes MFA, password reset, session, OAuth, JWT, or tenant-isolation, those must have separate explicit scope permission.
- Known rate limits, lockout thresholds, testing window, detection contact, and rollback path.
- List of in-scope API base paths, known admin/management/internal endpoints (from docs, client code, or passive recon), and role definitions.

## Required gates

1. `pentest_agent_load_config` → `pentest_agent_validate_policy` before any planning.
2. `pentest_agent_parse_scope` → `pentest_agent_validate_target` for each target host/API.
3. `pentest_agent_check_authorization` before any active probe.
4. `pentest_agent_build_command` for dry-run argv preview when catalog tools (ffuf, curl) are used.
5. `pentest_agent_execute_tool` for all execution — never raw shell.
6. `pentest_agent_append_evidence` → `pentest_agent_record_finding` → report handoff.

## Workflow

### Phase 1 — role matrix and endpoint inventory

Build a role×endpoint matrix before any probing. For each role, list:
- exact permission set (read own, read team, write own, admin, billing, export, etc.);
- expected denial for functions outside that set;
- known endpoint families (REST, GraphQL, gRPC, WebSocket, webhooks, internal job endpoints).

Derive endpoint inventory from docs, OpenAPI/GraphQL schemas, client-side route maps, proxy history, and passive recon. Flag any endpoint where:
- different API versions expose different function gates;
- path segments suggest admin, internal, management, operations, or system names;
- headers (X-Internal, X-Admin, X-Role) or query flags bypass normal routing.

### Phase 2 — low-risk function reachability

Validate one role×endpoint pair at a time. Use the least-privilege role first. For each pair:
1. Dry-run the expected request through `pentest_agent_build_command`.
2. Send the request with `pentest_agent_execute_tool`.
3. Compare actual status code, body shape, and headers against expected denial.
4. Record result, role, endpoint, HTTP method, status code, response summary, and timestamp.

Check these function-access dimensions:
- **Direct access**: call admin endpoint with user token.
- **Method override**: `X-HTTP-Method-Override`, `X-Method-Override`, `_method` query param.
- **API version drift**: probe `/api/v0/`, `/api/v1/`, `/api/v2/`, `/api/internal/`, `/api/beta/` with user token.
- **Path normalization**: `/../`, double encoding, trailing slash variants.
- **Content-type switching**: send same function intent as XML, form-encoded, or multipart when the API normally expects JSON.
- **Header injection**: `X-Forwarded-For: 127.0.0.1`, `X-Internal: true`, `X-Admin: 1`, `X-Role: admin`.

### Phase 3 — state-changing function guard

If scope explicitly allows low-risk state-change validation (write to test-owned records only):
1. Attempt DELETE, PATCH, or PUT on a test-owned resource using a lower-privilege role.
2. Verify the operation was denied or the resource was not modified.
3. Never write to records owned by other accounts.
4. Stop immediately if a state change succeeds unexpectedly — record the finding and do not escalate.

### Phase 4 — microservice and gateway edges

When scope includes internal service mesh or gateway paths:
- Check whether Service-A tokens are accepted by Service-B endpoints.
- Probe for trust-by-header patterns (`X-User-Id`, `X-Auth-User`, `X-Original-User` injected by reverse proxies).
- Test async/webhook endpoints: jobs, callbacks, and event handlers that may re-process requests without re-authorization.

## Decision points

- **Downgrade to report-only**: when function discovery requires brute-forcing large wordlists, probing unlisted internal hosts, or triggering alerts.
- **Escalate finding**: when a lower-privilege role successfully invokes a function that modifies data owned by another user, tenant, or the system.
- **Stop**: when evidence shows a real admin function was executed — sufficient for a finding; do not enumerate further admin capabilities.

## Prohibited behavior

- Brute-forcing admin paths without rate limits and scope approval.
- Modifying production data, user records, billing, or configuration.
- Accessing, exporting, or dumping function output that contains other users' data.
- Using real customer credentials, session tokens, or harvested JWTs.
- Persisting elevated access, creating backdoor accounts, or modifying role assignments.
- Raw storage of tokens, cookies, passwords, authorization codes, refresh tokens, recovery links, or PII.

## Stop conditions

- Any unexpected HTTP 2xx/3xx on an admin-class endpoint from a user role → record finding, stop probing that endpoint family.
- Rate limiting, WAF blocks, account lockout, or MFA challenge storm.
- Tenant-boundary crossing: user in Org-A can invoke Org-B admin functions.
- Third-party identity-provider scope gap (e.g., IdP token accepted as internal admin).
- Evidence requires raw secrets; redact and stop for maintainer review.

## Evidence — role-matrix format

For each tested function, record in `pentest_agent_append_evidence`:

```text
Role: <role name>
Endpoint: <method> <path>
Expected: <403 | 404 | redirect to login | ...>
Observed: <status code> | body shape: <summary>
Impact: <none | information disclosure | state change | cross-tenant>
Confidence: <confirmed | likely | needs-review>
```

Aggregate into a role×function matrix for the finding. Include:
- tested roles and their intended privilege boundaries;
- endpoints that correctly denied access (negative results);
- endpoints that incorrectly allowed access (positive findings);
- affected API versions and method-override vectors.

Never store raw tokens, cookies, passwords, authorization codes, refresh tokens, recovery links, customer data, or unredacted sensitive response bodies.

## Report handoff

When a finding is confirmed:
1. `pentest_agent_record_finding` with affected endpoint, role, observed behavior, impact rationale, CVSS estimate, and remediation guidance.
2. Reference the role-matrix evidence.
3. Recommend: per-endpoint authorization middleware, negative testing in CI, API version audit, method-override disablement, and internal-endpoint network isolation.
