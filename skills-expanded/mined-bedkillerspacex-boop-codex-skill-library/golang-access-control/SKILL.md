---
name: golang-access-control
description: >
  Implement and review access-control matrices in Go services: RBAC/ABAC,
  middleware enforcement, policy tests, and least-privilege handlers.
  Use for owned APIs and internal tools under authorization.
---

# Golang Access Control

## Research grounding

Runbook for **access control in Go**: defining who can do what to which
resource, enforcing decisions at the handler/interceptor boundary, and proving
denies with tests. Skill id: `golang-access-control`.

## Scope And Authorization

- **In scope:** systems you own, labs/CTFs, or engagements with written authorization.
- **Out of scope:** unauthorized privilege escalation against third parties.
- Prefer non-production policy changes; use change windows for production
  authz rule flips.
- Redact roles, tokens, personal data, and customer identifiers from notes.
- Pair code/config with `code-quality-standards`.

## When To Use

- Designing or refactoring RBAC/ABAC for a Go HTTP/gRPC service.
- Fixing broken object-level authorization (IDOR-class) in Go handlers.
- Adding central `Authorize(ctx, action, resource)` instead of ad-hoc if-checks.
- Focus tokens: **golang, access, control**.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| AuthN / JWT validation only | `api-auth-and-jwt-abuse` or `golang-api-gateway-auth` |
| Periodic human access campaigns | `golang-access-reviews` |
| AuthZ architecture patterns only | `golang-authz-design` |
| IDOR recon methodology | `idor-broken-object-authorization` |
| Abuse rate limits | `golang-abuse-prevention` |
| Implementation quality baseline | `code-quality-standards` |
| Org SSDLC | `secure-sdlc-checklist` |

## Domain Focus (Go authz)

| Area | Guidance |
| --- | --- |
| Models | RBAC (roles→permissions), ABAC (attrs: tenant, owner, clearance), ReBAC |
| Placement | After authN, before business logic; same for gRPC unary/stream interceptors |
| Context | Put principal in `context.Context` via typed key; never trust client role claims alone |
| Object ACL | Check resource ownership/tenant on every ID path (`/users/{id}`) |
| Admin | Separate role + break-glass with audit log; no silent superuser in prod flags |
| Policy as data | Casbin/OPA/Cedar or table-driven maps; version policies |
| Testing | Table tests for allow/deny matrix; fuzz IDs across tenants |
| Pitfalls | Middleware only on “main” router; missing OPTIONS; fail-open on policy error |

## Workflow

### 1. Confirm scope and success criteria

1. Record service owner, environment, authZ model target (RBAC vs ABAC), auth.
2. Success: documented matrix; unauthorized cross-tenant access denied; tests cover matrix cells.
3. Break-glass role procedure documented with logging.

### 2. Inventory

1. List roles, groups, service accounts, and API keys that call the service.
2. List resources and actions (CRUD + domain verbs: `approve`, `export`, `impersonate`).
3. Find enforcement points: gateway, service middleware, per-handler checks, DB RLS.
4. Flag “trust client headers” and dual-write legacy permission paths.

### 3. Baseline

1. Export current allow paths (integration tests, manual matrix, or policy dump).
2. Capture sample deny failures and any known IDOR tickets.
3. Version policy files / Casbin model / OPA bundles before edit.

### 4. Apply Go access control

1. Define a single decision API:

```go
type Principal struct {
	UserID   string
	TenantID string
	Roles    []string
}

type Action string
type Resource struct {
	Type string
	ID   string
	// attrs: OwnerID, TenantID, Classification, ...
}

func Authorize(ctx context.Context, p Principal, act Action, res Resource) error {
	// fail closed: unknown → deny
	if !policyAllows(p, act, res) {
		return ErrForbidden
	}
	return nil
}
```

2. Middleware/interceptor: authenticate → load principal (server-side) →
   authorize for route default action → handler may re-check object-level.
3. Object-level: after load-by-ID, call `Authorize` with resource attrs; do not
   filter only in UI.
4. Prefer deny by default; empty role set → no permissions.
5. Map denies to HTTP 403 (or 404 if anti-enumeration policy) / gRPC `PermissionDenied`.
6. Audit log: principal, action, resource, decision, reason code (no secrets).

### 5. Verify with evidence

```bash
go test ./internal/authz/... -count=1
go test ./... -race -count=1
go vet ./...
staticcheck ./...
govulncheck ./...
```

Table-test skeleton:

```go
func TestAuthorizeMatrix(t *testing.T) {
	cases := []struct {
		name    string
		p       Principal
		act     Action
		res     Resource
		wantErr bool
	}{
		{"owner read", Principal{UserID: "u1", TenantID: "t1", Roles: []string{"user"}},
			"read", Resource{Type: "doc", ID: "d1" /* OwnerID u1 */}, false},
		{"cross-tenant", Principal{UserID: "u2", TenantID: "t2", Roles: []string{"user"}},
			"read", Resource{Type: "doc", ID: "d1" /* tenant t1 */}, true},
	}
	// ...
}
```

1. Cross-tenant IDOR: user A token + user B object ID → denied.
2. Role removal: revoke role → next request denied without redeploy if policy dynamic.
3. Policy engine down → fail closed (or documented break-glass).

### 6. Observe and harden

1. Metrics: `authz_deny_total{action,reason}`, `authz_error_total` (engine failures).
2. Alert on spike of denies (attack or broken deploy) and on engine errors.
3. Review admin and impersonation paths quarterly.
4. Ensure new routes register default required permission in a central map.

### 7. Hand off

1. Publish matrix (roles × actions × resources) to the service README/runbook.
2. Link access-review process for human entitlements (`golang-access-reviews`).
3. Apply `code-quality-standards`; schedule policy review date.

## Enforcement placement

| Layer | Role |
| --- | --- |
| API gateway | Coarse authN + crude scopes; not sole object ACL |
| Go middleware | Route-level permission; attach principal |
| Handler | Object load + ABAC attributes |
| Data store | Optional RLS / tenant column predicates as defense-in-depth |

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Decision | Central Authorize + matrix tests | Scattered `if role == "admin"` |
| Object ACL | Check tenant/owner after load | Trust `?user_id=` from client |
| Fail mode | Deny on policy error | Allow when Casbin/OPA times out |
| Claims | Server loads roles from IdP/DB | Trust JWT `roles` without issuer rules |
| Admin | Audited break-glass | Hidden `DEBUG_ADMIN=1` in prod |
| Topic fidelity | Go authz matrix work | Generic Control Tower cloud checklist only |

## Output Checklist

- [ ] Scope, owner, model (RBAC/ABAC), authorization recorded
- [ ] Roles, actions, resources inventoried
- [ ] Enforcement points mapped; dual paths eliminated or listed
- [ ] Go Authorize API + middleware/interceptor in place
- [ ] Object-level checks on all ID routes
- [ ] Matrix tests include cross-tenant deny cases
- [ ] Fail-closed on policy errors documented
- [ ] Audit logging for sensitive decisions
- [ ] Metrics/alerts for deny and engine failure
- [ ] `code-quality-standards` applied; residual risk noted

## Rules

- Authorized use only; evidence over guesses.
- Prefer fail-closed authZ and reversible policy changes.
- Never ship “temporary” unrestricted admin without expiry and audit.
- Focus on `golang-access-control`; route JWT, gateway, and review campaigns
  to neighbor skills.
- Never paste live tokens or full customer role dumps into notes.
