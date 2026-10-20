---
name: golang-baseline
description: >
  Define and enforce a secure configuration baseline for Go services: TLS,
  headers, runtime flags, container defaults, and CI checks. Use for owned
  platforms under authorization.
---

# Golang Baseline

## Research grounding

Runbook for a **secure baseline** (minimum bar) every Go service must meet before
production—configuration, build, and runtime. Skill id: `golang-baseline`.

## Scope And Authorization

- **In scope:** services and platforms you own.
- **Out of scope:** enforcing baselines on third parties without agreement.
- Prefer automated checks; waivers with expiry.
- Pair with `golang-asvs-gates`, `golang-best-practices`, `code-quality-standards`.

## When To Use

- Creating org-wide “golden path” for new Go services.
- Auditing drift from security baseline.
- Encoding baseline as CI/policy-as-code.
- Focus tokens: **golang, baseline**.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Behavior anomaly baselining | `golang-baseline-behavior` |
| ASVS detailed gates | `golang-asvs-gates` |
| Style-only | `go-style-conventions` |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus — baseline controls (sample)

| Area | Minimum |
| --- | --- |
| Build | `-trimpath`, modules pinned, `govulncheck` clean or waived |
| HTTP | Timeouts; no `DefaultServeMux` pprof public; secure cookies if sessions |
| TLS | Min TLS1.2+; strong ciphers at edge |
| Process | Non-root container; read-only FS when possible |
| Config | No secrets in git; debug off in prod |
| Logs | Structured; no secret fields |
| Auth | Default deny on admin routes |
| Observability | `/healthz`/`/readyz` separate from admin |

## Workflow

### 1. Confirm scope and success criteria

1. Org unit, enforcement level, authorization.
2. Success: checklist published; ≥95% services compliant; CI blocks new violations.
3. Waiver board identified.

### 2. Inventory

1. Service templates (cookiecutter, Backstage).
2. Existing exceptions.
3. Measurement method (scorecard, OPA, CI).

### 3. Baseline document

1. Write versioned baseline (`baseline-go-v1`).
2. Map each control to automated test or scanner.
3. Severity: required vs recommended.

### 4. Encode and remediate

```go
func TestBaselineHTTPServer(t *testing.T) {
	// example: server must set ReadHeaderTimeout
	if srv.ReadHeaderTimeout == 0 {
		t.Fatal("ReadHeaderTimeout required")
	}
}
```

```bash
go test ./... -count=1
govulncheck ./...
staticcheck ./...
```

1. Update service template to pass by default.
2. Mass-remediate top violations.
3. Scorecards in catalog (`golang-backstage-plugins` / asset tags).

### 5. Verify with evidence

1. New service from template passes gates day-1.
2. Random sample audit of 10 services.
3. Waiver list has owners/expiry.

### 6. Observe and harden

1. Track compliance %; alert on regression.
2. Bump baseline version with changelog.
3. Feed incidents into new required controls.

### 7. Hand off

1. Publish baseline + how to comply.
2. Office hours for teams.
3. Link ASVS for deeper controls.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Spec | Versioned, testable | Wiki prose only |
| Enforce | CI + templates | Optional PDF |
| Waivers | Expiry | Forever exceptions |
| Topic fidelity | Secure Go baseline | Generic go test only |

## Output Checklist

- [ ] Baseline version published
- [ ] Controls mapped to automation
- [ ] Templates updated
- [ ] Compliance measurement live
- [ ] Waiver process working
- [ ] Sample audit evidence
- [ ] `code-quality-standards` applied

## Rules

- Minimum bar, not maximum ambition.
- Focus on `golang-baseline`.
- Authorized enforcement only.
- Prefer secure defaults in templates.
