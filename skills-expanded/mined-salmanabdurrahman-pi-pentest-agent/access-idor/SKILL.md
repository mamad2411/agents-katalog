---
name: access-idor
description: Insecure Direct Object Reference — validate object-level authorization across REST, GraphQL, gRPC, and WebSocket transports with role-pair evidence.
disable-model-invocation: true
risk: safe-active
allowed-modes: [auto, bug-bounty, red-team, ctf, blue-team, offensive, grey-hat, forensic, reverse-engineering, mobile-pentest]
authorization-required: yes
evidence-outputs: [command-log, redacted-evidence, finding-draft]
---

# IDOR — object-level authorization validation

Use this skill to validate that object ownership and access-control checks prevent cross-account, cross-tenant, and cross-role object access on an authorized, in-scope target. Focus on identifier surfaces, transport differences, and the boundary between "denied correctly" and "leaked object."

## Required inputs

- Written scope naming the target API, tenant, identity provider, authorized test accounts (minimum two distinct accounts with separate owned objects), allowed object families, and explicit permission for cross-account read validation.
- User-owned or project-approved test accounts only. Each test account must own at least one object (profile, order, message, file, etc.) created specifically for this engagement.
- Valid authorization cache for the target. Separate explicit permission required for MFA, password reset, session, OAuth, JWT, or tenant-isolation validation.
- Known rate limits, lockout thresholds, testing window, and detection contact.

## Required gates

1. `pentest_agent_load_config` → `pentest_agent_validate_policy`.
2. `pentest_agent_parse_scope` → `pentest_agent_validate_target`.
3. `pentest_agent_check_authorization` before any active probe.
4. `pentest_agent_build_command` for dry-run argv preview.
5. `pentest_agent_execute_tool` for execution — never raw shell.
6. `pentest_agent_append_evidence` → `pentest_agent_record_finding` → report.

## Workflow

### Phase 1 — identifier surface inventory

Map every location where an object identifier appears in the in-scope API:
- URL path segments (`/users/123`, `/orders/abc-def`);
- query parameters (`?id=42`, `?resource=...`);
- JSON body fields (`{"user_id": 5}`, `{"target": "..."}`);
- GraphQL arguments (`user(id: "7")`);
- gRPC message fields;
- WebSocket message payloads;
- headers (`X-Resource-Id`);
- cookie values.

For each location, record the identifier format: sequential integer, UUID v1/v4, ULID, slug, composite key, base64-encoded value, or opaque token. Predictable or enumerable formats (sequential integers, timestamp-based UUIDv1) carry higher risk.

High-value object families to prioritize: user profiles, orders/transactions, messages/inbox, files/attachments, billing records, audit logs, admin tools, background job results, multi-tenant resources.

### Phase 2 — paired-account validation

Use two test accounts (Account-A and Account-B) with distinct owned objects.

For each identifier surface:
1. Account-A owns object with ID X.
2. Account-B owns object with ID Y.
3. Account-A requests object Y (cross-account read).
4. Account-B requests object X (reciprocal cross-account read).
5. Account-A attempts PATCH/DELETE on object Y (cross-account write).
6. Account-B attempts PATCH/DELETE on object X (reciprocal cross-account write).

For each attempt, record: requesting role, target object owner, endpoint, HTTP method, expected denial (403/404), observed status, and whether body content leaked.

### Phase 3 — blind detection and transport differences

When the API returns consistent denial codes (always 403 or always 404), use differential signals:
- **Timing**: request existing vs non-existing IDs; if response time differs for existing objects, object existence leaks.
- **Response size**: compare Content-Length for known-own vs guessed-other objects.
- **ETag/Last-Modified**: presence of cache validators may confirm object existence.
- **Transport consistency**: test the same object access across REST, GraphQL, and gRPC if the API exposes multiple transports — authorization may differ per transport.

### Phase 4 — bypass techniques

Test these only when the target explicitly allows access-control bypass validation:
- **Parameter pollution**: `?id=123&id=456`.
- **Content-type switching**: request JSON resource as form-encoded.
- **Method tunneling**: `POST /api/resource/123` with `X-HTTP-Method-Override: GET`.
- **Array wrapping**: `{"ids": [123, 456]}` where a single ID is expected.
- **Cache confusion**: vary `Accept`, `Authorization`, or custom headers to test CDN key misalignment.
- **Injected headers**: `X-User-Id: <victim_id>`, `X-Original-User: admin`.

### Phase 5 — microservice and async edges

When scope includes internal service paths:
- Test whether Service-A tokens are accepted by Service-B for object access.
- Probe webhook/event payloads for embedded object references that lack re-authorization.
- Test background job endpoints: job IDs, export IDs, report IDs.

## Decision points

- **Stop at denial consistency**: if every cross-account attempt returns 403 and no differential signals leak, record negative result and move on.
- **Escalate on confirmed access**: when Account-A reads or modifies Account-B object → immediate finding.
- **Downgrade when noisy**: if validation requires bulk ID enumeration (>50 requests), switch to report-only or ask maintainer.

## Prohibited behavior

- Bulk ID enumeration against production data without scope approval.
- Accessing or dumping real customer objects, PII, PHI, or financial records.
- Modifying objects owned by other accounts unless scope explicitly authorizes the exact modification for proof.
- Using harvested IDs from passive recon without authorization for the object's owner.
- Storing raw response bodies containing other users' data.

## Stop conditions

- Successful cross-account read or write → record finding, do not expand enumeration.
- Rate limiting, WAF blocks, account lockout.
- Object response contains PII, credentials, tokens, or sensitive business data → redact and stop.
- Tenant boundary crossing: Org-A account accesses Org-B objects.

## Evidence — role-pair matrix

For each tested object family, record:

```text
Object type: <profile | order | message | file | ...>
Identifier: <ID> | format: <integer | uuid | slug | ...>
Requestor: <Account-A (owner) | Account-B (non-owner)>
Endpoint: <method> <path>
Expected: <403 | 404>
Observed: <status> | body size: <N> | timing: <ms>
Differential: <none | size | timing | etag>
Impact: <none | object-exists leak | content leak | state change>
Confidence: <confirmed | likely | needs-review>
```

Aggregate into a role×object-family matrix for the finding. Include:
- each tested object family and its identifier format;
- cross-account read results (positive and negative);
- cross-account write results when tested;
- transport consistency check results;
- differential signal observations.

Never store raw response bodies containing other users' data, tokens, cookies, or PII.

## Report handoff

When a finding is confirmed:
1. `pentest_agent_record_finding` with affected object family, identifier surface, observed access, CVSS estimate (typically 7.5–9.1 for PII/PHI exposure, 5.0–6.5 for existence leak), and remediation guidance.
2. Reference the role-pair matrix evidence.
3. Recommend: per-object ownership checks in data layer, authorization tests in CI per endpoint, UUIDv4+ for identifiers, and transport-consistent authorization middleware.
