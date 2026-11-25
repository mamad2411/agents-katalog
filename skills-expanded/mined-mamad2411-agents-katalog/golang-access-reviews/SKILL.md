---
name: golang-access-reviews
description: >
  Run access-review campaigns for Go services and platforms: inventory
  roles/bindings, collector jobs, reviewer workflows, evidence packs, and
  remediation. Use for owned systems under authorization.
---

# Golang Access Reviews

## Research grounding

Runbook for **periodic access reviews** where Go services, operators, or
collectors participate: enumerating entitlements, driving reviewer decisions,
and closing the loop with revoke APIs and audit evidence. Skill id:
`golang-access-reviews`.

## Scope And Authorization

- **In scope:** owned IdP/apps, labs, or authorized compliance engagements.
- **Out of scope:** harvesting third-party accounts or social-engineering reviewers.
- Prefer read-only collectors first; write/revoke only with change control.
- Redact PII, HR data, and secret material from export packs.
- Pair automation code with `code-quality-standards`.

## When To Use

- SOX/ISO/SOC2-style user access reviews for apps backed by Go services.
- Building or operating a Go job that exports IAM bindings, K8s RBAC, or app roles.
- Closing reviews: revoke stale service accounts, bot tokens, and human roles.
- Focus tokens: **golang, access, reviews**.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Implementing runtime RBAC enforcement | `golang-access-control` |
| AuthZ system design | `golang-authz-design` |
| AD tiering model | `golang-ad-tiering` |
| Continuous authZ policy tests only | `golang-access-control` matrix tests |
| Secrets rotation program | `secrets-management-hygiene` |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Area | Guidance |
| --- | --- |
| Scope of review | Humans, service accounts, bot users, CI OIDC roles, break-glass |
| Sources | IdP groups, app DB roles, K8s RoleBindings, cloud IAM, API keys |
| Go collectors | Batch jobs with context timeouts, pagination, deterministic exports |
| Cadence | Quarterly human; monthly privileged; continuous for break-glass |
| Evidence | Signed CSV/JSON of decisions, reviewer ID, timestamp, ticket |
| Remediation | Revoke via API + verify next login/token fails; dual control for admins |
| Pitfalls | Orphan SA keys, shared logins, “temporary” groups without expiry |

## Workflow

### 1. Confirm scope and success criteria

1. Record campaign owner, systems in scope, regulation/control ID, authorization.
2. Success: 100% of in-scope identities decided; revokes executed or risk-accepted
   with expiry; evidence stored in retention system.
3. Define SLA: reviewer response window and escalation path.

### 2. Inventory entitlements (Go-friendly collectors)

1. Enumerate identity sources and permission stores per service.
2. Prefer machine-readable export endpoints or DB read replicas.
3. Go job patterns: `context.WithTimeout`, page tokens, idempotent object keys.

```go
type Entitlement struct {
	Principal   string `json:"principal"`
	PrincipalType string `json:"principal_type"` // user|sa|group
	System      string `json:"system"`
	Role        string `json:"role"`
	Resource    string `json:"resource"`
	LastUsed    *time.Time `json:"last_used,omitempty"`
	SourceRef   string `json:"source_ref"`
}

func Collect(ctx context.Context, src Source) ([]Entitlement, error) {
	var out []Entitlement
	var page string
	for {
		batch, next, err := src.Page(ctx, page)
		if err != nil {
			return nil, err
		}
		out = append(out, batch...)
		if next == "" {
			return out, nil
		}
		page = next
	}
}
```

4. Join HR/manager graph carefully; minimize PII in working sets.

### 3. Baseline campaign pack

1. Freeze inventory snapshot (hash + timestamp).
2. Tag privileged vs standard; auto-propose “remove” for dormant >N days if policy allows.
3. Generate reviewer work items (manager certifies team; system owner certifies bots).

### 4. Run review and remediate

1. Reviewers decide: keep / remove / reduce; require comment on keep for privileged.
2. Go remediation workers: call IdP/app revoke APIs with dry-run flag first.
3. For Go apps: disable role row, revoke refresh tokens, bump session version.
4. Dual control for global-admin and production break-glass.
5. Record decision evidence with immutable storage (WORM/bucket retention).

### 5. Verify with evidence

```bash
go test ./internal/accessreview/... -count=1
go test ./... -race -count=1
govulncheck ./...

# Dry-run revoke against owned staging
# go run ./cmd/accessreview -mode=dry-run -campaign=2026-Q1
# go run ./cmd/accessreview -mode=apply  -campaign=2026-Q1
```

1. Sample 10 keeps and 10 removes: re-export inventory matches decisions.
2. Removed principal cannot call privileged API (403/401).
3. Evidence pack hash stored; redacted sample attached to ticket.

### 6. Observe and harden

1. Metrics: open items, overdue reviews, revoke failures, dormant privileged count.
2. Alert on revoke API errors and on new privileged grants outside review window.
3. Feed recurring grants into Joiner-Mover-Leaver automation gaps.

### 7. Hand off

1. Close campaign report: coverage %, open exceptions with expiry.
2. Update runbook and calendar for next cycle.
3. Apply `code-quality-standards` to collectors/remediators.

## Campaign roles

| Role | Responsibility |
| --- | --- |
| Campaign owner | Scope, SLA, exception acceptance |
| System owner | Bot/SA and app role accuracy |
| Manager reviewer | Human need-to-have certification |
| Security/compliance | Sample testing and evidence retention |
| Automation (Go jobs) | Collect, notify, revoke, re-verify |

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Inventory | Automated paginated export | Manual spreadsheet only |
| Privileged | Monthly + dual control | Annual rubber stamp |
| Bots/SAs | Included with owners | “Service account” ignored |
| Revoke | API + verify | Delete row without session kill |
| Evidence | Hashed snapshot + decisions | Screenshot of Slack “LGTM” |
| Topic fidelity | Go collectors + revoke workers | Generic go test only |

## Output Checklist

- [ ] Campaign scope, owner, authorization recorded
- [ ] Entitlement sources inventoried and snapshotted
- [ ] Reviewer assignments and SLA set
- [ ] Decisions complete or exceptions with expiry
- [ ] Revokes applied and re-verified
- [ ] Evidence pack retained (redacted as needed)
- [ ] Metrics/alerts for overdue and revoke failures
- [ ] Next campaign scheduled
- [ ] `code-quality-standards` applied to automation code

## Rules

- Authorized use only; minimize PII; evidence over guesses.
- Prefer dry-run before mass revoke.
- Do not skip service accounts and CI identities.
- Focus on `golang-access-reviews`; route runtime enforcement to
  `golang-access-control`.
- Never paste live credentials or full HR dumps into chat/notes.
