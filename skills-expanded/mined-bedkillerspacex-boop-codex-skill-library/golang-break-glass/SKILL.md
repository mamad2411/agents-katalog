---
name: golang-break-glass
description: >
  Implement and operate break-glass emergency access for Go services: time-boxed
  privilege elevation, dual control, full audit, auto-expiry, and post-use review.
  Owned/lab/authorized production only—not stealth backdoors.
---

# Golang Break Glass

## Research grounding

Runbook for **break-glass** (emergency privileged access) patterns around **Go**
control planes, admin APIs, and platform tooling. Emphasizes auditability and
auto-revocation. Skill id: `golang-break-glass`.

## Scope And Authorization

- **In scope:** owned systems where emergency access is formally approved.
- **Out of scope:** hidden backdoors, shared root passwords without audit, bypassing customer isolation without authorization.
- Test break-glass in stage with full logging before production drills.
- Redact session tokens from tickets; keep audit events immutable.
- Pair with `code-quality-standards` and identity provider policies.

## When To Use

- Designing **emergency admin** paths for Go admin APIs or operators CLIs.
- Replacing standing global admin with just-in-time elevation.
- Drills: “production outage, need temporary superuser for 30 minutes.”
- Board KRI: count of break-glass uses (`golang-board-reporting`).

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Database-specific break-glass | `golang-break-glass-db` |
| Normal RBAC / OAuth design | `api-auth-and-jwt-abuse` (auth design) / IdP skills |
| Secrets rotation program | `secrets-management-hygiene` |
| Change freeze process | `golang-change-freeze` |
| Code quality | `code-quality-standards` |

## Domain Focus

| Area | Guidance |
| --- | --- |
| Trigger | Page + ticket + reason code; optional second approver |
| Token | Short-lived JWT/session (≤ 30–60m), audience-bound, step-up MFA |
| Enforcement | Go middleware checks `bg` claim + expiry + ticket ID |
| Audit | Who, why, what actions, start/end; SIEM immutable store |
| Pitfalls | Eternal “emergency” role, no MFA, logs without actor, break-glass that skips all audit |

### State machine

```text
request → approve (optional) → issue token → elevate → auto-expire → post-review
                ↘ deny
```

## Workflow

### 1. Confirm policy and success criteria

1. Who may request/approve; max duration; which actions allowed under BG.
2. Success: elevation works in drill; every use has ticket + SIEM events; auto-expiry proven.
3. Legal/compliance constraints (SOX, SOC2 change management).

### 2. Inventory current privilege

1. Standing admin roles, shared accounts, god-mode feature flags.
2. Gaps: no expiry, no MFA step-up, admin API unauthenticated in internal network only (still risky).

### 3. Baseline

1. Count users with permanent admin; sample last 90d admin actions without tickets.
2. Record current outage access path (Slack DM root password? replace it).

### 4. Implement Go break-glass

```go
type BreakGlassClaims struct {
    jwt.RegisteredClaims
    TicketID string   `json:"ticket"`
    Reason   string   `json:"reason"`
    Scopes   []string `json:"scopes"`
}

func RequireBreakGlass(scopes ...string) func(http.Handler) http.Handler {
    return func(next http.Handler) http.Handler {
        return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
            c, err := claimsFrom(r)
            if err != nil || c.ExpiresAt.Before(time.Now()) {
                http.Error(w, "break-glass required", http.StatusForbidden)
                return
            }
            if !scopesAllowed(c.Scopes, scopes) {
                http.Error(w, "insufficient break-glass scope", http.StatusForbidden)
                return
            }
            audit.Log(r.Context(), "break_glass_action", c.Subject, c.TicketID, r.Method, r.URL.Path)
            next.ServeHTTP(w, r)
        })
    }
}
```

1. Issuer service: MFA + dual control → sign short-lived token; store grant record.
2. Deny listing permanent `role=admin` on sensitive routes; require BG claim instead.
3. Metrics: `break_glass_grants_total`, `break_glass_actions_total`, `break_glass_active`.

### 5. Verify with evidence

```text
go test ./internal/breakglass/... -race
go test ./internal/breakglass/... -run TestExpiry

# Stage drill
# 1) request grant → 2) call admin API → 3) wait expiry → 4) confirm 403
curl -sS -H "Authorization: Bearer $BG_TOKEN" https://admin.stage/v1/dangerous
# after expiry
curl -sS -o /dev/null -w '%{http_code}\n' -H "Authorization: Bearer $BG_TOKEN" \
  https://admin.stage/v1/dangerous
```

1. Confirm SIEM has grant + each action + expiry event.
2. Confirm unapproved token mint fails.

### 6. Observe and harden

1. Alert on any grant in prod; daily digest of BG uses.
2. Post-use review within 2 business days; revoke residual access.
3. Chaos: clock skew tests with `golang-clock-skew` awareness for JWT `exp`.

### 7. Hand off

1. Runbook + pager: how to request BG during SEV-1.
2. Link `golang-break-glass-db`, board reporting KRIs.
3. Apply `code-quality-standards`.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Duration | ≤ 60m default | Days-long elevation |
| Authn | MFA + ticket | Shared password in vault screenshot |
| Audit | Immutable SIEM | App log only, 7d retention |
| Scope | Least privilege scopes | Full superuser for any outage |
| Standing access | Removed after BG ships | Keep god-mode “just in case” |

## Output Checklist

- [ ] Policy: requesters, approvers, max TTL, scopes
- [ ] Go issuer + middleware with expiry enforcement
- [ ] Stage drill with proof of auto-expiry
- [ ] SIEM events for grant and actions
- [ ] Prod alert on grant
- [ ] Post-use review process
- [ ] Standing admin reduced or eliminated
- [ ] Exceptions documented
- [ ] `code-quality-standards` applied
- [ ] Residual risk noted

## Rules

- Break-glass is emergency **and** fully audited—not a stealth backdoor.
- Authorized environments only.
- Prefer short TTL and scoped elevation over permanent roles.
- Focus on app/control-plane BG; DB-specific → `golang-break-glass-db`.
- Never share long-lived root credentials in chat.
