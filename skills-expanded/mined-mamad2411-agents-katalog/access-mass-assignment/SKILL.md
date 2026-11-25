---
name: access-mass-assignment
description: Mass assignment and over-posting validation — detect writable fields not intended for the caller's role through body, query, nested, and array injection.
disable-model-invocation: true
risk: safe-active
allowed-modes: [auto, bug-bounty, red-team, ctf, blue-team, offensive, grey-hat, forensic, reverse-engineering, mobile-pentest]
authorization-required: yes
evidence-outputs: [command-log, redacted-evidence, finding-draft]
---

# Mass assignment — over-posting validation

Use this skill to validate that API endpoints reject unexpected writable properties from request bodies, query parameters, nested objects, and arrays. Focus on field-level authorization: what the client sends vs what the server accepts and persists.

## Required inputs

- Written scope naming the target API, authorized test accounts, allowed endpoint families, and explicit permission for field-injection testing on test-owned records only.
- User-owned or project-approved test accounts. Each test account must own at least one mutable record (profile, order, team, etc.).
- Valid authorization cache. Separate permission for MFA, password reset, session, OAuth, JWT, or tenant-isolation validation.
- Known rate limits, lockout thresholds, testing window, and detection contact.

## Required gates

1. `pentest_agent_load_config` → `pentest_agent_validate_policy`.
2. `pentest_agent_parse_scope` → `pentest_agent_validate_target`.
3. `pentest_agent_check_authorization` before active probing.
4. `pentest_agent_build_command` for dry-run argv preview.
5. `pentest_agent_execute_tool` for execution.
6. `pentest_agent_append_evidence` → `pentest_agent_record_finding` → report.

## Workflow

### Phase 1 — field surface discovery

Map writable fields by comparing request shapes against response shapes:
1. Send a GET for the test-owned resource; note every field in the response body.
2. Send a PUT/PATCH with only allowed fields; inspect the response for additional server-computed or hidden fields.
3. Check registration, invite, and create endpoints — responses often leak internal field names (`is_admin`, `role`, `plan`, `balance`, `verified`, `subscription_tier`).
4. Review client-side code, OpenAPI schemas, and GraphQL introspection for field definitions not exposed in normal API docs.

Build a field inventory with these buckets:
- **Client-writable fields**: documented as user-settable.
- **Server-managed fields**: documented as read-only, computed, or admin-only.
- **Unknown fields**: not in docs but appear in responses.

### Phase 2 — flat injection

For each writable endpoint (registration, profile update, order create, team invite, etc.):
1. Send the normal request payload plus one extra server-managed field (`is_admin: true`, `role: "admin"`, `plan: "enterprise"`, `balance: 10000`, `credits: 9999`, `verified: true`).
2. Re-read the resource to check whether the injected field was persisted.
3. Test boolean, string, integer, and null variants of each field.
4. Test edge values: `0`, `-1`, `""`, `[]`, `{}`, `null`.

Flag any server-managed field that is:
- accepted and persisted silently;
- accepted and reflected in response but not persisted;
- rejected with a clear validation error (lowest risk).

### Phase 3 — nested and array injection

Target frameworks that use deep binding (Spring, Laravel, Rails, Django with nested serializers):
1. **Nested object injection**: `{"user": {"role": "admin", "is_admin": true}, "profile": {"bio": "test"}}`.
2. **Array wrapping**: wrap scalar fields in arrays `{"role": ["admin"]}`.
3. **JSON in string fields**: `{"metadata": "{\"is_admin\": true}"}` — if metadata is later deserialized.
4. **Form-encoded over-posting**: send `bio=test&is_admin=true&role=admin` to a JSON endpoint.

### Phase 4 — query parameter and header injection

Test parameter-binding that picks up fields from query strings or headers:
1. Append `?is_admin=true&role=admin` to a POST/PUT request.
2. Inject custom headers: `X-Role: admin`, `X-Plan: enterprise`.
3. Test whether `X-HTTP-Method-Override` combined with field injection reaches different handlers.

### Phase 5 — state-change verification

When a field injection succeeds (field persisted):
1. Verify persistence by re-reading the resource.
2. Check whether the change enabled a privilege escalation: can the test account now access admin endpoints, export data, or modify other records?
3. Revert the field to its original value if the endpoint allows.
4. If the field cannot be reverted, notify the scope contact immediately.

## Decision points

- **Stop at field rejection**: if all server-managed fields are rejected with 400/422 and clear validation errors, record negative result.
- **Escalate on persistence**: any server-managed field accepted and persisted → finding, even if privilege escalation is not yet proven.
- **Escalate on privilege gain**: persisted field leads to elevated function access → critical finding.

## Prohibited behavior

- Injecting fields into records owned by other users.
- Modifying billing, payment, subscription, or financial fields on production accounts.
- Creating admin accounts, escalating real user privileges, or disabling security controls.
- Bulk field-injection across many endpoints without per-endpoint approval.
- Storing raw response bodies containing other users' data or internal field values.

## Stop conditions

- Any server-managed field persisted on a test-owned record → record finding, stop injecting further fields on that endpoint.
- Rate limiting, WAF blocks, account lockout.
- Field injection triggers email/SMS notifications to real users.
- Response contains other users' data or internal configuration.

## Evidence — field-injection matrix

For each tested endpoint, record:

```text
Endpoint: <method> <path>
Field: <field name> | type: <server-managed | unknown>
Injected value: <value> | format: <JSON | form | query | header>
Requestor role: <role>
Accepted in response: <yes | no>
Persisted on re-read: <yes | no | not checked>
Privilege impact: <none | field modified | role escalation>
Confidence: <confirmed | likely | needs-review>
```

Aggregate into a field×endpoint matrix. Include:
- endpoints tested and their normal writable field set;
- injected fields and their persistence status;
- any confirmed privilege impact with reproduction steps;
- negative results where fields were correctly rejected.

Never store raw request/response bodies containing tokens, passwords, cookies, or other users' data.

## Report handoff

When a finding is confirmed:
1. `pentest_agent_record_finding` with affected endpoint, injected field, persistence proof, privilege impact, CVSS estimate (7.5–9.0 for privilege escalation via field injection), and remediation guidance.
2. Reference the field-injection matrix.
3. Recommend: explicit field allowlists per endpoint+role, schema validation rejecting unknown fields, nested-object depth limits, and field-injection tests in CI.
