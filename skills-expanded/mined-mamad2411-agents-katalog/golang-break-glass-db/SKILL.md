---
name: golang-break-glass-db
description: >
  Emergency database access for Go platforms: just-in-time DB credentials, bastion
  session recording, time-boxed roles, dual control, and audited queries. Use for
  owned/lab databases under authorization—not covert data access.
---

# Golang Break Glass DB

## Research grounding

Runbook for **database break-glass** used by **Go** services and operators:
JIT credentials, proxy bastions, role elevation, and post-incident review.
Skill id: `golang-break-glass-db`.

## Scope And Authorization

- **In scope:** owned databases (Postgres/MySQL/etc.) and operator tooling you control.
- **Out of scope:** unauthorized data exfiltration, disabling audit to “move faster,” customer DB access without ticket.
- Prefer read-only BG by default; write/DDL requires higher approval.
- Redact connection strings and row samples from tickets.
- Pair with `golang-break-glass` for app admin paths and `secrets-management-hygiene`.

## When To Use

- SEV-1 needs human SQL access when automation is down.
- Replacing shared `app_admin` passwords with JIT roles.
- Go migrate/operator jobs need emergency superuser with auto-revoke.
- Compliance requires every prod DB session recorded.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| App/API break-glass (non-DB) | `golang-break-glass` |
| Normal app DB pooling / migrations | `database-migration-safety` |
| CMK/KMS key rotation | `golang-cmk-rotation` |
| Secrets program | `secrets-management-hygiene` |
| Code quality | `code-quality-standards` |

## Domain Focus

| Area | Guidance |
| --- | --- |
| Identity | SSO → vault DB dynamic secrets or cloud IAM DB auth |
| Path | SSO → approve → short-lived creds → bastion/proxy → DB |
| Recording | Proxy session logs / pgaudit / cloud audit; retain per policy |
| Go side | Migrator uses separate CI role; humans never embed prod DSN in apps |
| Pitfalls | Shared superuser, SSL off, no row-level audit, BG role left active |

### Access tiers

| Tier | Privs | Approvers | Max TTL |
| --- | --- | --- | --- |
| BG-RO | SELECT limited schemas | 1 on-call | 60m |
| BG-RW | DML on listed tables | 2 (on-call + data owner) | 30m |
| BG-DDL | Schema changes | 2 + change ticket | 30m |
| BG-SUPER | Full (rare) | Incident commander | 15m |

## Workflow

### 1. Policy and success criteria

1. Define tiers, approvers, allowed schemas, data classes forbidden from export.
2. Success: drill issues RO creds, connects via bastion, expires, audit complete.
3. Align with change freeze (`golang-change-freeze`) exceptions.

### 2. Inventory

1. Current DSNs in Go configs, shared passwords, jump hosts, existing vault roles.
2. Which Go services use which DB users (least privilege map).
3. Audit plugins enabled? (`pgaudit`, MySQL audit, Cloud SQL flags).

### 3. Baseline

1. Count standing human superusers; last password rotation.
2. Sample connections without ticket IDs in last 90 days.

### 4. Implement JIT path

```text
# Vault dynamic DB creds (illustrative)
vault read database/creds/bg-ro-prod
# Returns username/password with lease TTL

# Cloud SQL IAM (example)
gcloud sql generate-login-token
```

Go operator wrapper (pattern):

```go
// Issue temporary grant record, never log password.
type DBGrant struct {
    Ticket   string
    Tier     string
    Expires  time.Time
    Requester string
}

func (s *Service) MintRO(ctx context.Context, g DBGrant) (user, pass string, err error) {
    if err := s.policy.Authorize(ctx, g); err != nil {
        return "", "", err
    }
    creds, err := s.vault.DBCreds(ctx, "bg-ro-prod")
    if err != nil {
        return "", "", err
    }
    s.audit.Grant(ctx, g, creds.LeaseID) // no secret material
    return creds.Username, creds.Password, nil
}
```

1. Force TLS to DB; reject non-bastion source IPs via DB `pg_hba` / firewall.
2. App runtime roles stay non-superuser; BG never shipped inside app containers.

### 5. Verify with evidence

```text
go test ./internal/dbbreakglass/... -race

# Stage drill
# mint RO → psql via proxy → SELECT 1 → wait lease expire → reconnect fails

# Confirm audit
# SIEM query: event=db_break_glass_grant OR db_session_start
```

1. Prove RW requires second approver in stage policy engine.
2. Confirm secrets not present in Go app logs (`rg password` on log sample).

### 6. Observe and harden

1. Alert every prod BG-RW/DDL grant; weekly RO summary.
2. Revoke vault leases on incident close; rotate if credential leakage suspected.
3. Quarterly remove unused standing grants.

### 7. Hand off

1. SEV-1 runbook section “DB break-glass.”
2. Link app BG skill and migration safety.
3. Apply `code-quality-standards` to minting service.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Creds | Dynamic TTL lease | Shared `root` password in 1Password forever |
| Path | Bastion + TLS + audit | Laptop public IP allowlisted to 5432 |
| Default | RO first | Everyone gets SUPERUSER |
| App config | No human DSN in pods | Prod password in K8s secret used by humans |
| Review | Post-use ticket close | Grant and forget |

## Output Checklist

- [ ] Tiers, approvers, TTLs documented
- [ ] JIT credential source (Vault/IAM) configured
- [ ] Network path restricted to bastion/proxy
- [ ] Session/query audit verified
- [ ] Stage expiry drill passed
- [ ] Alerts on RW/DDL grants
- [ ] App roles least-privilege verified
- [ ] Exceptions with expiry
- [ ] `code-quality-standards` applied
- [ ] Residual risk noted

## Rules

- Authorized DB access only; every session ticketed.
- Prefer RO; escalate privileges only as needed.
- Never disable audit during emergencies without executive approval + ticket.
- Focus on DB BG; app admin BG → `golang-break-glass`.
- Never paste live DSNs or result sets with PII into chat.
