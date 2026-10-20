---
name: golang-authz-design
description: >
  Design authorization architectures for Go systems: RBAC vs ABAC vs ReBAC,
  policy engines, PDP/PEP split, tenancy, and evolution. Use before large authz
  implementations on owned systems.
---

# Golang AuthZ Design

## Research grounding

Runbook for **authorization architecture decisions** for Go services—where
policy lives, how it is evaluated, and how it scales across microservices.
Skill id: `golang-authz-design`. Implementation details → `golang-access-control`.

## Scope And Authorization

- **In scope:** systems you own; design reviews and ADRs.
- **Out of scope:** bypassing others’ authz for unauthorized access.
- Prefer incremental migration designs with dual-run.
- Pair with `golang-access-control`, `golang-access-reviews`, `code-quality-standards`.

## When To Use

- Choosing RBAC vs ABAC vs relationship-based models for a Go platform.
- Introducing OPA/Cedar/Casbin/Zanzibar-style systems.
- Multi-tenant isolation design for Go SaaS.
- Focus tokens: **golang, authz, design**.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Coding middleware/matrix tests | `golang-access-control` |
| Gateway authentication | `golang-api-gateway-auth` |
| Human access campaigns | `golang-access-reviews` |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Model | Best for | Watch-outs |
| --- | --- | --- |
| RBAC | Coarse enterprise apps | Role explosion |
| ABAC | Attribute-rich (clearance, geo) | Policy complexity |
| ReBAC | Sharing graphs (docs, folders) | Consistency of graph |
| Hybrid | Common: RBAC + tenant ABAC | Clear precedence |

| Component | Role |
| --- | --- |
| PEP | Go middleware/handler enforces decision |
| PDP | Policy engine decides allow/deny |
| PIP | Loads attributes (user, resource) |
| PAP | Policy admin API |

## Workflow

### 1. Confirm scope and success criteria

1. Apps, tenancy model, compliance, authorization.
2. Success: ADR approved; pilot service enforces new design; migration plan.
3. Non-goals explicit (e.g., not fine-grained file ACL in v1).

### 2. Inventory

1. Current checks (hardcoded roles, gateway scopes).
2. Resource types and sharing requirements.
3. Latency budget for authz (p99).

### 3. Baseline

1. Pain: bugs, IDOR history, slow feature delivery.
2. Measure current authz latency.

### 4. Design

1. Draw trust boundaries; never trust client attributes without PIP validation.
2. Choose model; document precedence (deny overrides).
3. Central PDP vs library PDP in each Go binary—trade consistency vs latency.
4. Policy-as-code repo, review, versioning, tests.
5. Tenancy: every resource has `tenant_id`; cross-tenant requires explicit break-glass.
6. Offline/fail mode: fail closed for mutations; optional read cache with TTL documented.
7. ADR template sections: context, decision, consequences, migration.

```go
// PEP shape — design target for Go services
type PDP interface {
	Decide(ctx context.Context, in DecisionInput) (Decision, error)
}
```

### 5. Verify with evidence

1. Threat scenarios from `golang-attack-trees` against design.
2. Pilot: matrix tests + load test PDP p99.
3. Failure injection: PDP down → fail closed proven.

```bash
go test ./internal/authz/... -count=1
go test ./... -race -count=1
```

### 6. Observe and harden

1. Decision metrics and deny reasons (cardinality-safe).
2. Policy change audit (`golang-audit-logging`).
3. Quarterly design review as product features add relations.

### 7. Hand off

1. Publish ADR + sequence diagrams.
2. Implementation skill handoff to `golang-access-control`.
3. Training for feature teams on “new resource checklist”.

## Decision table

| Requirement | Lean toward |
| --- | --- |
| Simple 5 roles | RBAC in-process |
| Document sharing | ReBAC/Zanzibar-like |
| Rego expertise + central | OPA as PDP |
| Ultra-low latency | Embedded policy, careful cache |

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Decision | Written ADR | Tribal knowledge |
| Tenancy | Mandatory resource attr | Optional filter in UI |
| Fail mode | Closed on PDP error | Open allow |
| Topic fidelity | Authz architecture | Generic go test only |

## Output Checklist

- [ ] Goals/non-goals and tenancy model set
- [ ] Model and PDP/PEP split chosen
- [ ] ADR published
- [ ] Pilot metrics and fail-closed evidence
- [ ] Policy lifecycle (review/version/test)
- [ ] Migration plan for legacy checks
- [ ] `code-quality-standards` for pilot code

## Rules

- Deny by default; least privilege.
- Focus on `golang-authz-design`.
- Authorized design work only.
- Do not skip object-level checks in design.
