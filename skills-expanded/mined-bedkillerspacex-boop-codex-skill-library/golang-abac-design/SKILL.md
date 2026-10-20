---
name: golang-abac-design
description: >
  Attribute-Based Access Control (ABAC) design in Go services: principal/resource/
  environment attributes, policy evaluation, PDP/PEP separation, deny-by-default,
  testing matrices, and audit logs. Use for owned authorization layers — not to
  bypass access control on third-party systems.
---

# Golang ABAC Design

## Scope And Authorization

- **In scope:** Authorization design/implementation in applications you own.
- **Out of scope:** Crafting policy bypasses for systems without permission.
- Default **deny**; explicit allow rules; log decisions for sensitive actions.
- Pair with `gin-middleware-auth` (authentication) and `code-quality-standards`.
- Legal/compliance mapping may need privacy/security architecture review.

## When To Use

- RBAC alone is too coarse (team, tenant, resource sensitivity, time, IP).
- Multi-tenant SaaS with resource attributes (owner, org_id, classification).
- Centralizing policy decisions outside handlers.
- Replacing ad-hoc `if user.Role ==` sprawl.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| JWT/session authentication | `gin-middleware-auth` / API auth skills |
| Feature experiments | `golang-ab-testing` |
| GCP IAM conditions | `gcp-iam-conditions` |
| OAuth flows | OAuth skills |
| Implementation quality | `code-quality-standards` |

## Concepts

| Term | Meaning |
| --- | --- |
| Principal | Who (user id, roles, groups, tenant, clearance) |
| Resource | What (type, id, owner, org, labels) |
| Action | Verb (`read`, `write`, `delete`, `approve`) |
| Environment | Context (time, IP, device, env name) |
| Policy | Rules mapping attributes → allow/deny |
| PEP | Policy Enforcement Point (middleware/handler check) |
| PDP | Policy Decision Point (engine evaluating policy) |
| Obligations | Extra requirements (MFA step-up, watermark) |

### ABAC vs RBAC vs ReBAC

| Model | Fit |
| --- | --- |
| RBAC | Stable org roles |
| ABAC | Attribute-rich decisions |
| ReBAC | Relationship graphs (owner, sharing) — can combine |

## Workflow

### 1. Model attributes

```go
type Principal struct {
    ID       string
    TenantID string
    Roles    []string
    Attrs    map[string]string // e.g. department, clearance
}

type Resource struct {
    Type     string
    ID       string
    TenantID string
    OwnerID  string
    Labels   map[string]string // e.g. classification=pii
}

type Env struct {
    Now       time.Time
    IP        string
    RequestID string
}
```

Document allowed keys; avoid unbounded free-form attr explosion.

### 2. Decision API

```go
type Decision struct {
    Allow   bool
    Reason  string // stable machine code: "tenant_mismatch"
    Policy  string // which rule matched
}

type PDP interface {
    Evaluate(ctx context.Context, p Principal, action string, r Resource, e Env) (Decision, error)
}
```

### 3. Deny-by-default engine sketch

```go
func (e *Engine) Evaluate(ctx context.Context, p Principal, action string, r Resource, env Env) (Decision, error) {
    if p.TenantID == "" || r.TenantID == "" || p.TenantID != r.TenantID {
        return Decision{Allow: false, Reason: "tenant_mismatch"}, nil
    }
    for _, rule := range e.rules {
        if rule.Matches(p, action, r, env) {
            if rule.Effect == EffectDeny {
                return Decision{Allow: false, Reason: rule.ID, Policy: rule.ID}, nil
            }
            return Decision{Allow: true, Reason: "allow", Policy: rule.ID}, nil
        }
    }
    return Decision{Allow: false, Reason: "no_match"}, nil
}
```

Order: explicit denies before allows; last-default deny.

### 4. PEP in handlers

```go
func (h *Handler) GetDoc(w http.ResponseWriter, r *http.Request) {
    p := principalFrom(r.Context())
    doc := h.load(r)
    d, err := h.pdp.Evaluate(r.Context(), p, "doc.read", doc.Resource(), envFrom(r))
    if err != nil {
        http.Error(w, "authz_error", http.StatusInternalServerError)
        return
    }
    if !d.Allow {
        http.Error(w, "forbidden", http.StatusForbidden)
        return
    }
    // return doc
}
```

Never trust client-supplied tenant_id without binding to authenticated principal.

### 5. Policy sources

| Source | Pros |
| --- | --- |
| Code rules | Simple, reviewed in PR |
| Declarative YAML/JSON | Non-dev updates with care |
| OPA/Rego | Expressive; ops complexity |
| Cedar / vendor | Managed policy language |

Start code-based; extract when rules churn high.

### 6. Testing matrix

```go
func TestAuthz(t *testing.T) {
    cases := []struct{
        name string
        p Principal
        action string
        r Resource
        want bool
    }{
        {"owner read", owner, "doc.read", doc, true},
        {"cross tenant", otherTenant, "doc.read", doc, false},
        {"viewer write", viewer, "doc.write", doc, false},
    }
    // evaluate each
}
```

Include: role combo, label classification, time-bound rules, missing attrs (fail closed).

### 7. Audit

Log: principal id, action, resource, decision, policy id, request id — **not** secret data.
Immutable audit stream for sensitive resources.

### 8. Performance

- Cache decisions carefully (invalidate on policy/attr change).
- Avoid remote PDP per micro-attribute without batching.
- Benchmark hot paths.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Default | Deny | Allow if no rule |
| Tenant | Server-side compare | Client header alone |
| Reasons | Stable codes | Random English only |
| Tests | Matrix of denies | Only happy allow |
| Drift | Central PDP | Copy-paste ifs diverge |

## Output Checklist

- [ ] Attribute model documented
- [ ] Actions catalogued
- [ ] PDP interface + deny default
- [ ] PEP on all sensitive handlers
- [ ] Tenant isolation enforced
- [ ] Test matrix covers deny paths
- [ ] Audit logging in place
- [ ] Policy change process defined
- [ ] `code-quality-standards` applied

## Rules

- Deny by default; fail closed on PDP errors for sensitive ops (or document exception).
- Authenticate first (`gin-middleware-auth`); authorize second.
- Never take authorization solely from client attributes.
- Stable reason codes for support/debug.
- Keep policies reviewable like code.
