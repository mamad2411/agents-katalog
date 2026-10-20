---
name: golang-asvs-gates
description: >
  Map OWASP ASVS controls to CI/CD release gates for Go services: authN/Z,
  validation, crypto, logging evidence, and waiver process. Use for owned
  SSDLC programs under authorization.
---

# Golang ASVS Gates

## Research grounding

Runbook for turning **OWASP ASVS** (Application Security Verification Standard)
requirements into **enforceable release gates** for Go applications—not a full
ASVS copy. Skill id: `golang-asvs-gates`.

## Scope And Authorization

- **In scope:** apps and pipelines you own; agreed ASVS level (L1/L2/L3).
- **Out of scope:** claiming compliance without evidence; testing out of scope apps.
- Prefer progressive enforcement (report → gate).
- Pair with `secure-sdlc-checklist`, `code-quality-standards`, domain security skills.

## When To Use

- Defining merge/release blockers for Go services mapped to ASVS chapters.
- Preparing audit evidence packs for appsec reviews.
- Closing gaps: missing security headers tests, auth tests, dependency scan gates.
- Focus tokens: **golang, asvs, gates**.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Full SSDLC program design | `secure-sdlc-checklist` |
| Only dependency vulns | `govulncheck` / container scan skills |
| Manual pentest execution | recon + class-specific skills |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus — sample gate mapping

| ASVS theme | Go gate example |
| --- | --- |
| V2 Auth | Tests for session/JWT validation; no default secrets in config |
| V3 Session | Cookie flags tests; logout invalidates |
| V4 Access | AuthZ matrix tests; deny by default |
| V5 Validation | Fuzz/handler tests; no SQL concat (`sqlclosecheck`/lint) |
| V6 Crypto | `govulncheck`; ban weak TLS via config test |
| V7 Error | No stack traces in client JSON (httptest) |
| V8 Data | PII log redaction tests |
| V9 Communicate | TLS min version assert |
| V10 Malicious | CI supply-chain: pin modules, cosign optional |
| V14 Config | `go test` fails if `debug=true` in prod config schema |

## Workflow

### 1. Confirm scope and success criteria

1. Target ASVS level, apps, authorization, audit date.
2. Success: gate set in CI; evidence stored per release; waivers tracked.
3. Choose must-pass vs warn controls.

### 2. Inventory

1. Existing CI jobs for Go (test, lint, scan).
2. ASVS requirements applicable (tailor—do not cargo-cult all L3).
3. Gaps vs current tests.

### 3. Baseline

1. Run candidate gates in warn mode for 2 sprints; measure fail rates.
2. Snapshot failing controls.

### 4. Implement gates

```yaml
# CI sketch
jobs:
  asvs-gates:
    steps:
      - run: go test ./... -count=1
      - run: go test ./... -race -count=1
      - run: staticcheck ./...
      - run: govulncheck ./...
      - run: go test ./internal/authz/... -count=1  # V4 evidence
      - run: go test ./internal/httpsec/... -count=1 # headers, errors
      # optional: gosec, semgrep, container scan
```

```go
// Example gate test: production config rejects insecure defaults
func TestProdConfigSafe(t *testing.T) {
	cfg := MustLoad("config.prod.yaml")
	if cfg.Debug {
		t.Fatal("debug must be false in prod")
	}
	if cfg.HTTP.CookieSecure != true {
		t.Fatal("secure cookies required")
	}
}
```

1. Map each CI step → ASVS IDs in a matrix doc.
2. Store junit/logs as release artifacts.
3. Waiver: control ID, reason, expiry, approver, compensating control.

### 5. Verify with evidence

```bash
go test ./... -count=1
go test ./... -race -count=1
govulncheck ./...
staticcheck ./...
```

1. Intentionally break a control on a branch → gate red.
2. Waiver path tested; expired waiver fails build.
3. Auditor can pull matrix + last green run artifacts.

### 6. Observe and harden

1. Track flaky gates separately from true security fails.
2. Raise level gradually (L1→L2) when fail rate stable.
3. Re-map when ASVS version updates.

### 7. Hand off

1. Publish ASVS↔CI matrix with owners.
2. Train devs on fixing common gate fails.
3. Link SSDLC and class-specific remediations.

## Waiver rules

| Allowed | Not allowed |
| --- | --- |
| Short expiry ≤90d | Infinite critical auth waiver |
| Compensating control | “Fix later” without owner |
| Risk accepted by security | Dev self-approve only |

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Evidence | Automated tests + artifacts | Spreadsheet claims only |
| Gates | Fail closed on auth tests | Optional security job |
| Scope | Tailored ASVS set | 200 controls nobody owns |
| Topic fidelity | ASVS gates for Go CI | Generic go test only |

## Output Checklist

- [ ] ASVS level and app scope set
- [ ] Control↔CI matrix published
- [ ] Gates running in CI (warn then enforce)
- [ ] Waiver process with expiry
- [ ] Evidence artifacts retained
- [ ] Intentional fail test proves gate works
- [ ] `code-quality-standards` applied

## Rules

- Evidence over claims; authorized apps only.
- Prefer automated gates with human risk acceptance.
- Focus on `golang-asvs-gates`.
- Do not fake compliance by skipping tests.
