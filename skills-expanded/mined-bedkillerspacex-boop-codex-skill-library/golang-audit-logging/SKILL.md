---
name: golang-audit-logging
description: >
  Implement security audit logging in Go services: event schema, required fields,
  sink reliability, redaction, and queryability. Use for owned systems under
  compliance or security requirements.
---

# Golang Audit Logging

## Research grounding

Runbook for **security-relevant audit logs** (who did what to which resource when)
from Go applications—distinct from debug application logs. Skill id:
`golang-audit-logging`.

## Scope And Authorization

- **In scope:** systems you own; lawful monitoring of authorized users.
- **Out of scope:** covert surveillance beyond policy; logging secrets in clear.
- Prefer append-only sinks; restrict who can read audit data.
- Pair with `golang-audit-trail`, `code-quality-standards`.

## When To Use

- Adding audit events for admin actions, authz denies, data export, config changes.
- Meeting SOC2/ISO “logging of security events” with Go services.
- Standardizing audit schema across microservices.
- Focus tokens: **golang, audit, logging**.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Immutable WORM storage design | `golang-audit-trail` |
| General metrics/tracing | `observability-metrics-tracing` |
| Access reviews | `golang-access-reviews` |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Field | Required |
| --- | --- |
| timestamp (UTC) | yes |
| actor (user/sa id) | yes |
| action | yes |
| resource type/id | yes |
| outcome (success/fail) | yes |
| source IP / request id | recommended |
| reason/code | for denies |
| Never | passwords, tokens, raw PII bodies |

**Events to always audit:** login success/fail, privilege change, secret access,
delete/export bulk, policy change, impersonation.

## Workflow

### 1. Confirm scope and success criteria

1. Compliance control IDs, retention, authorization.
2. Success: required events emitted; query finds sample; no secrets in samples.
3. Sink: SIEM, object log store, or dedicated audit service.

### 2. Inventory

1. Sensitive actions in Go handlers/jobs.
2. Existing logs that incorrectly double as audit.
3. Read ACL on log stores.

### 3. Baseline

1. List missing events (gap matrix).
2. Sample current log lines for leakage.

### 4. Implement

```go
type AuditEvent struct {
	Time       time.Time `json:"time"`
	ActorID    string    `json:"actor_id"`
	ActorType  string    `json:"actor_type"`
	Action     string    `json:"action"`
	Resource   string    `json:"resource"`
	ResourceID string    `json:"resource_id"`
	Outcome    string    `json:"outcome"`
	RequestID  string    `json:"request_id"`
	IP         string    `json:"ip,omitempty"`
	Reason     string    `json:"reason,omitempty"`
}

func (a *Auditor) Log(ctx context.Context, e AuditEvent) error {
	e.Time = time.Now().UTC()
	// write to dedicated sink; do not drop silently on failure for critical events
	return a.sink.Write(ctx, e)
}
```

1. Central helper; forbid ad-hoc string logs for audit.
2. Emit **after** authn knows actor; include deny paths.
3. Async buffer with retry; document loss policy (fail request vs best-effort).
4. Redact: structured allowlist of fields.
5. Clock: NTP; monotonic for ordering only where needed.

### 5. Verify with evidence

```bash
go test ./internal/audit/... -count=1
go test ./... -race -count=1
```

1. Integration test: perform admin action → event present with fields.
2. Secret canary not present in sink.
3. Query SIEM by actor/request_id works.

### 6. Observe and harden

1. Metrics: audit write failures; alert immediately.
2. Periodic coverage review vs action inventory.
3. Tamper-evidence upgrades → `golang-audit-trail`.

### 7. Hand off

1. Schema registry / version field on events.
2. Runbook for investigators.
3. Retention and legal hold notes.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Content | Actor/action/resource/outcome | “User did stuff” free text only |
| Secrets | Redacted | Authorization headers logged |
| Reliability | Alert on sink down | Best-effort forever silent drop |
| Topic fidelity | Audit logging in Go | Generic go test only |

## Output Checklist

- [ ] Event catalog agreed
- [ ] Schema and sink implemented
- [ ] Critical actions covered including denies
- [ ] Redaction verified
- [ ] Failure alerting on
- [ ] Retention documented
- [ ] `code-quality-standards` applied

## Rules

- No secrets in audit payloads.
- Prefer dedicated audit channel over stdout only.
- Focus on `golang-audit-logging`.
- Authorized monitoring only.
