---
name: golang-brakeman-ops
description: >
  Operate Brakeman (Ruby on Rails SAST) in polyglot monorepos that also ship Go:
  CI wiring, baseline/ignore management, severity gates, ticket routing, and how
  Go services consume shared Rails findings. Authorized repos only—not Ruby exploit.
---

# Golang Brakeman Ops

## Research grounding

Operational runbook for **Brakeman** in environments where **Go** and **Rails**
coexist (monorepo, multi-service product). Covers CI ops, baselines, and
cross-language security gates—not writing Rails exploits. Skill id: `golang-brakeman-ops`.

## Scope And Authorization

- **In scope:** owned Rails apps + Go gateways you may scan and fix.
- **Out of scope:** scanning third-party apps without authorization, suppressing findings to ship knowingly vulnerable code without risk acceptance.
- Prefer PR-time scans; production deploys blocked only by agreed severities.
- Redact secrets found in reports; treat Brakeman output as sensitive.
- Pair Go-side fixes with `code-quality-standards`; Rails fixes with team Ruby standards.

## When To Use

- Monorepo has `**/Gemfile` Rails apps **and** Go modules; you need Brakeman green in CI.
- Establishing ignore file governance, confidence thresholds, and SARIF upload.
- Go edge service depends on Rails API—security gate must cover both sides.
- Migrating from ad-hoc Brakeman runs to owned pipeline with SLAs.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Go-native SAST (CodeQL/govulncheck) | `golang-codeql-ops`, govulncheck workflows |
| Generic secure code review | `golang-code-review-security` |
| SSDLC program design | `secure-sdlc-checklist` |
| Implementation quality | `code-quality-standards` |
| Pure Ruby style (no security ops) | team Ruby skill / RuboCop guides |

## Domain Focus

| Area | Guidance |
| --- | --- |
| Tool | `brakeman` CLI / Docker image; pin version in CI |
| Inputs | Rails root, `--format json/sarif`, `--confidence-level`, `config/brakeman.ignore` |
| Gates | Fail PR on High/Medium new findings; baseline known issues with ticket IDs |
| Go interaction | Shared CI workflow matrix; artifact consumed by security dashboard Go job |
| Pitfalls | Global ignore without expiry, unpinned Brakeman, scanning wrong app root, silencing SQL injection noise incorrectly |

### Severity handling

| Confidence / severity | PR gate | SLA to fix |
| --- | --- | --- |
| High + High confidence | Block merge | 7d |
| Medium | Block or warn (policy) | 30d |
| Weak / experimental | Report only | Backlog |
| Ignored with ticket | Allowed | Review at ticket expiry |

## Workflow

### 1. Confirm scope and success criteria

1. List Rails app paths, CI system, owners for each app, Go services that call them.
2. Success: Brakeman in CI on every Rails-touching PR; no unowned ignores; dashboard shows open counts.
3. Agree version pin and upgrade cadence.

### 2. Inventory

1. Existing Brakeman config, ignore files, Jenkins/GitHub Actions jobs.
2. Whether Go-only PRs wrongly skip or wrongly run Brakeman.
3. Path filters: `rails-app/**` vs whole monorepo.

### 3. Baseline

1. Run full scan; export JSON; open ticket per accepted risk in ignore file.
2. Record current High count and oldest finding age.
3. Hash ignore file; require CODEOWNERS on changes.

### 4. Wire CI (polyglot)

```yaml
# Example GitHub Actions matrix fragment
jobs:
  brakeman:
    if: contains(github.event.pull_request.labels.*.name, 'rails') ||
        contains(github.event.pull_request.changed_files, 'apps/rails/')
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Brakeman
        run: |
          docker run --rm -v "$PWD/apps/rails:/app" presidentbeef/brakeman:v6 \
            -q -f sarif -o /app/brakeman.sarif --no-exit-on-warn \
            --confidence-level 2
      - name: Upload SARIF
        uses: github/codeql-action/upload-sarif@v3
        with:
          sarif_file: apps/rails/brakeman.sarif
  go-test:
    runs-on: ubuntu-latest
    steps:
      - run: go test ./...
```

Ignore entry policy (JSON comments via Brakeman ignore notes):

```text
# Every ignore MUST include: ticket URL, owner, expiry YYYY-MM-DD, residual risk
brakeman -I  # interactive only in dev; never hand-edit production ignores blindly
```

### 5. Verify with evidence

```text
# Local (authorized app path only)
cd apps/rails
bundle exec brakeman -q -w2 -f json -o /tmp/brakeman.json
# or pinned docker image as in CI

# Diff new findings vs baseline
jq '.warnings | length' /tmp/brakeman.json

# Ensure Go pipeline still green
go test ./...
govulncheck ./...
```

1. Introduce a deliberate test finding in a branch; confirm CI fails then reverts.
2. Confirm ignore without ticket rejected by custom CI script if you enforce policy.

### 6. Observe and harden

1. Metrics: findings open by severity, mean age, ignore count, Brakeman version lag.
2. Alert when ignore file grows > N without net warning reduction.
3. Quarterly re-scan with higher confidence; retire stale ignores.

### 7. Hand off

1. Runbook for “new High in main”; link Rails and Go on-call.
2. Dashboard job (often Go) ingests SARIF from all languages.
3. Apply `code-quality-standards` to any custom gate scripts.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Version | Pinned Brakeman image | `latest` floating |
| Ignore | Ticket + expiry + owner | `# false positive` forever |
| Scope | Rails app root only | Scan monorepo node_modules noise |
| Gate | New High blocks PR | Warnings only, never read |
| Polyglot | Path filters + matrix | Brakeman on pure-Go PRs every time |

## Output Checklist

- [ ] Rails roots and owners listed; authorization OK
- [ ] Brakeman version pinned in CI
- [ ] SARIF/JSON artifacts uploaded
- [ ] Ignore policy enforced (ticket/expiry)
- [ ] Gate severity agreed and tested
- [ ] Go CI coexistence verified (path filters)
- [ ] Metrics for open findings and ignores
- [ ] Exceptions documented
- [ ] `code-quality-standards` on gate scripts
- [ ] Next Brakeman upgrade date set

## Rules

- Authorized repositories only.
- Do not mass-ignore High confidence SQLi/XSS without risk acceptance.
- Keep focus on Brakeman **ops** in Go-adjacent monorepos; deep Rails fix patterns stay with Rails owners.
- Never commit production secrets found during scans—rotate and purge.
- Evidence: CI logs + SARIF, not “we ran it once locally.”
