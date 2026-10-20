---
name: access-tenant-isolation
description: Multi-tenant isolation validation — verify that tenant boundaries prevent cross-tenant data access, function invocation, and side-channel leaks with strict stop-on-sight rules.
disable-model-invocation: true
risk: caution
allowed-modes: [auto, bug-bounty, red-team, ctf, blue-team, offensive, grey-hat, forensic, reverse-engineering, mobile-pentest]
authorization-required: yes
evidence-outputs: [command-log, redacted-evidence, finding-draft]
---

# Tenant isolation — cross-tenant boundary validation

Use this skill to validate that tenant, organization, workspace, or team boundaries prevent cross-tenant data access, function invocation, invitation abuse, export leakage, and side-channel exposure. This is the highest-sensitivity access-control skill: stop immediately on any confirmed cross-tenant data access and do not enumerate further.

## Required inputs

- Written scope explicitly naming the multi-tenant application, at least two authorized test tenants (created for this engagement), test accounts in each tenant, allowed boundary-test methods, and a named detection/escalation contact.
- User-owned or project-approved test tenants and test accounts only. Never use production customer tenants for boundary testing.
- Valid authorization cache for the target. Separate explicit permission required for any action that could expose another tenant's data.
- Known rate limits, lockout thresholds, testing window, and a clear "stop and report" contact path.

## Required gates

1. `pentest_agent_load_config` → `pentest_agent_validate_policy`.
2. `pentest_agent_parse_scope` → `pentest_agent_validate_target`.
3. `pentest_agent_check_authorization` before any active probe.
4. `pentest_agent_build_command` for dry-run argv preview.
5. `pentest_agent_execute_tool` for execution — never raw shell.
6. `pentest_agent_append_evidence` → `pentest_agent_record_finding` → report.

## Workflow

### Phase 1 — tenant architecture mapping

Before any probing, map the tenant model from docs, client code, and passive observation:
- How is tenant context established? (subdomain, path prefix, JWT claim, header, cookie, API key scope)
- What resources are tenant-scoped? (users, projects, files, billing, audit logs, integrations, webhooks, search indexes)
- Are there cross-tenant features? (invitations, shared channels, marketplace, partner portals)
- What background jobs span tenants? (exports, reports, billing runs, data pipelines)

### Phase 2 — direct cross-tenant access

Use two test tenants (Tenant-A, Tenant-B) with distinct test data.

For each tenant-scoped resource family:
1. Tenant-A user requests Tenant-A resources → expect success (baseline).
2. Tenant-A user requests Tenant-B resources using Tenant-B identifiers → expect 403/404.
3. Swap tenant context while keeping the same user session:
   - change tenant subdomain/path;
   - modify tenant-id claim in JWT (if allowed by scope);
   - swap tenant-scoped header or cookie.
4. Repeat with Tenant-B user requesting Tenant-A resources (reciprocal check).

Stop immediately on any cross-tenant data access. Record the finding; do not enumerate further objects or tenants.

### Phase 3 — cross-tenant side channels

Test for tenant existence and data leakage through indirect signals:
- **Search leakage**: Tenant-A user searches for a term that only exists in Tenant-B data. If results appear, cross-tenant search index exposure.
- **Export/Report leakage**: trigger an export or report in Tenant-A; check whether the output contains Tenant-B data or whether export IDs are predictable across tenants.
- **Notification/webhook leakage**: Tenant-A triggers an action that generates a notification; check whether Tenant-B can observe it through shared infrastructure.
- **Timing side channels**: request a known Tenant-B resource; compare response time to non-existent resource — faster response may confirm tenant existence.
- **Error message differentiation**: "tenant not found" vs "resource not found" vs "access denied" — message differences leak tenant topology.

### Phase 4 — cross-tenant function invocation

Test whether Tenant-A user can invoke functions in Tenant-B context:
- **Invitation abuse**: Tenant-A user sends an invitation to an email already associated with Tenant-B.
- **Tenant ID swapping in API calls**: `POST /api/tenant/{tenant-b-id}/users`.
- **Impersonation endpoints**: internal/admin endpoints that accept `?tenant_id=...` or `X-Tenant-Id: ...` headers.
- **Background job manipulation**: job IDs, export IDs, or batch operation IDs that may be cross-tenant.

### Phase 5 — cross-tenant persistence

Check whether cross-tenant artifacts survive:
- Tenant-A user uploads a file; check whether it becomes accessible via Tenant-B if a tenant-agnostic CDN URL is returned.
- Tenant-A user creates a webhook; check whether the webhook fires for Tenant-B events.
- Cached responses: Tenant-A request primes a shared cache; Tenant-B request receives the cached Tenant-A response (cache poisoning across tenants).

## Decision points

- **Stop-on-sight**: any confirmed cross-tenant data access → critical finding, stop all further probing, notify scope contact.
- **Escalate on side channel**: search leakage, timing confirmation, or error differentiation → high finding.
- **Downgrade on negative results**: all cross-tenant probes return 403/404 with no differential signals → record negative result.

## Prohibited behavior

- Accessing, enumerating, or dumping data from real customer tenants.
- Modifying data in any tenant not explicitly owned by the test account.
- Inviting, adding, or removing users from real tenants.
- Triggering notifications, emails, or webhooks to real tenant users.
- Exploiting a confirmed cross-tenant access to exfiltrate data beyond minimal proof.
- Storing raw response bodies that contain other tenants' data, PII, or secrets.

## Stop conditions

- First confirmed cross-tenant data access → critical finding, stop all probing, notify scope contact.
- First confirmed cross-tenant state change → critical finding, stop.
- Rate limiting, WAF blocks, tenant-level lockout.
- Response contains PII, credentials, tokens, or business data from another tenant.
- Any sign that probing is affecting production tenant availability.

## Evidence — tenant-pair matrix

For each tested boundary, record:

```text
Tenant-A: <tenant-a-id> | Tenant-B: <tenant-b-id>
Resource: <resource family> | endpoint: <method> <path>
Requestor: <Tenant-A user> targeting <Tenant-B resource>
Expected: <403 | 404>
Observed: <status> | body summary: <none | tenant-b data | error string>
Differential signal: <none | timing | search leak | error differentiation>
Impact: <none | tenant-exists leak | data leak | state change>
Confidence: <confirmed | likely | needs-review>
```

Aggregate into a tenant×resource matrix. Include:
- each tested resource family and tenant boundary;
- direct access results;
- side-channel observations;
- function-invocation results;
- any confirmed cross-tenant data access with minimal proof.

Never store raw response bodies containing other tenants' data, tokens, cookies, PII, or secrets.

## Report handoff

When a finding is confirmed:
1. `pentest_agent_record_finding` with affected resource families, cross-tenant access mechanism, minimal proof, CVSS estimate (9.0–10.0 for cross-tenant data access, 5.0–7.0 for side-channel leaks), and remediation guidance.
2. Reference the tenant-pair matrix.
3. Recommend: tenant-scoped authorization in data layer, tenant-context validation on every request, cross-tenant test suite in CI, search index isolation, and audit logging for cross-tenant access attempts.
