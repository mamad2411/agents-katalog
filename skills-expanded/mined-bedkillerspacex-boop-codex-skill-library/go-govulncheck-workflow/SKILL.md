---
name: go-govulncheck-workflow
description: >
  Run and gate golang.org/x/vuln/cmd/govulncheck in local and CI workflows: install,
  module/symbol analysis modes, interpreting findings, upgrade paths, and suppress
  discipline. Use for owned Go modules — not as a guarantee of exploit absence.
---

# govulncheck Workflow

## Scope And Authorization

- **In scope:** Go modules you maintain; CI for those repos.
- **Out of scope:** Scanning private modules without access rights; ignoring findings
  in production internet-facing services without risk acceptance.
- govulncheck reports **known** vulnerabilities in the Go vuln DB affecting your code paths
  (symbol mode) or modules (weaker).
- Pair with `go-module-hygiene` and `code-quality-standards`.

## When To Use

- Pre-release security gate for Go services.
- Investigating Dependabot/renovate Go CVE alerts with call-graph relevance.
- Periodic scheduled scans on main.
- Verifying a version bump actually removes a vuln symbol reachability.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Module version hygiene | `go-module-hygiene` |
| Sum DB verification | `go-sumdb-verify` |
| Container image CVEs | `gcr-vulnerability-scanning` |
| Race conditions | `go-race-detector-workflow` |
| Implementation quality | `code-quality-standards` |

## Concepts

| Mode | Meaning |
| --- | --- |
| Source/symbol analysis | Default: reports vulns if vulnerable functions are reachable |
| Binary analysis | `govulncheck ./path/to/binary` |
| Module-only | Lists module vulns without reachability (noisier) |
| Go vuln DB | https://vuln.go.dev entries |
| False confidence | Unreachable today may become reachable after code change |

## Workflow

### 1. Install

```bash
go install golang.org/x/vuln/cmd/govulncheck@latest
govulncheck -version
```

Pin tool version in CI for reproducibility when required.

### 2. Local scan

```bash
cd /path/to/module
go mod tidy
govulncheck ./...
```

Exit non-zero on findings (default for actionable vulns).

### 3. Interpret output

| Field | Use |
| --- | --- |
| Vulnerability ID | `GO-YYYY-…` / aliases CVE |
| Module / package | Where to upgrade |
| Found call stacks | Prove reachability |
| Fixed in | Target version |

If stacks show only test code, still fix before shipping tests that embed vuln if policy requires; usually prioritize production graphs.

### 4. Remediate

```bash
go get example.com/module@vX.Y.Z
go mod tidy
go test ./...
govulncheck ./...
```

If no fixed version: isolate usage, feature-flag off, or vendor patch; document risk.

### 5. CI gate

```yaml
# GitHub Actions sketch
- uses: actions/setup-go@v5
  with:
    go-version-file: go.mod
- name: govulncheck
  run: |
    go install golang.org/x/vuln/cmd/govulncheck@v1.1.3
    govulncheck ./...
```

Run on PRs and main; optional scheduled nightly with latest DB.

### 6. Binary scan (release)

```bash
go build -o dist/app ./cmd/app
govulncheck dist/app
```

Useful for confirming release artifacts.

### 7. Exceptions

- Rare: accepted risk with ticket, expiry, compensating controls.
- Do not blanket-ignore entire IDs in CI without review.
- Prefer upgrading over permanent suppress.

### 8. Metrics

- Open vuln count on main
- Time-to-remediate CRITICAL
- Flake rate from DB updates (rebuild pin carefully)

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Gate | Fail PR on reachable HIGH+ | Scan once a year manually |
| Fix | Upgrade module + retest | `replace` to random fork forever |
| Scope | `./...` module | Only scan one package ignoring cmd |
| Trust | Combine with module hygiene | Assume govulncheck ⇒ secure app |
| Output | Track GO IDs in tickets | Delete CI job because noisy |

## Output Checklist

- [ ] govulncheck installed/pinned
- [ ] `govulncheck ./...` clean or findings triaged
- [ ] Upgrades tested
- [ ] CI gate enabled
- [ ] Binary scan for releases optional/required per policy
- [ ] Exceptions ticketed with expiry
- [ ] Related module hygiene applied
- [ ] `code-quality-standards` applied

## Rules

- Owned modules only.
- Prefer official fixed versions.
- Reachability helps prioritize; still read impact.
- Keep Go toolchain current — stdlib vulns matter.
- Not a substitute for secure coding or container scanning.
