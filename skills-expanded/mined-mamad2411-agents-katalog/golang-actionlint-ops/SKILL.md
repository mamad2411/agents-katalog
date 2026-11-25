---
name: golang-actionlint-ops
description: >
  Operate actionlint for GitHub Actions in Go repositories: install, CI gate,
  config, shellcheck integration, and safe workflow patterns. Use for owned repos.
---

# Golang Actionlint Ops

## Research grounding

Runbook for running **[actionlint](https://github.com/rhysd/actionlint)** on
repos that build Go (and any monorepo workflows): catch workflow syntax errors,
expression mistakes, and risky patterns before merge. Skill id:
`golang-actionlint-ops`.

## Scope And Authorization

- **In scope:** repositories and orgs you own or are authorized to change.
- **Out of scope:** modifying third-party org workflows without permission.
- Prefer PR-time checks; production deploy workflows need change control.
- Redact secrets from workflow logs and issue attachments.
- Pair workflow/code changes with `code-quality-standards`.

## When To Use

- Adding or tightening CI for `.github/workflows/*` in a Go project.
- Debugging flaky or invalid GHA YAML, `runs-on`, or `if:` expressions.
- Enforcing shell best practices in `run:` steps via shellcheck integration.
- Focus tokens: **golang, actionlint, ops**.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Go unit/lint quality only | `golang-best-practices` / `code-quality-standards` |
| Supply-chain attestations | `golang-attestations` |
| Secrets in CI hygiene | `secrets-management-hygiene` |
| Full SSDLC program | `secure-sdlc-checklist` |
| Generic ops without GHA | matching ops skill in catalog |
| Bandit (Python SAST) | `golang-bandit-ops` is misnamed neighbor — use Python bandit skill |

## Domain Focus

| Area | Guidance |
| --- | --- |
| Binary | `actionlint` via go install, aqua, asdf, or pinned GitHub release |
| Inputs | `.github/workflows/*.yml` and `action.yml` |
| Config | `actionlint.yaml` / `.github/actionlint.yaml` for ignore rules |
| Shell | shellcheck on `run:` blocks when installed |
| Go CI patterns | modules cache, `setup-go` version pin, `-race` job optional |
| Risks | `pull_request_target` + checkout untrusted code; script injection from titles |
| Ops | Fail CI on findings; allowlist only with owner + expiry comment |

## Workflow

### 1. Confirm scope and success criteria

1. Record repo, default branch, workflow owners, authorization.
2. Success: actionlint clean on main; CI required check; documented ignores.
3. List workflows that deploy or use secrets (higher scrutiny).

### 2. Inventory

1. List all workflow files and reusable workflows.
2. Note runners (GitHub-hosted vs self-hosted) and secret names (not values).
3. Existing ignores / continue-on-error that hide failures.

### 3. Baseline

1. Run actionlint once; save full output as baseline.
2. Categorize: syntax errors (must fix) vs style/ignorable.
3. Pin tool version for reproducibility.

### 4. Install and configure

```bash
# Pin version in ops docs; example pattern
go install github.com/rhysd/actionlint/cmd/actionlint@v1.7.7
actionlint -version

# Lint all workflows from repo root
actionlint

# Explicit paths
actionlint .github/workflows/*.yml

# JSON for CI parsing
actionlint -format '{{json .}}'
```

Example CI job (illustrative):

```yaml
# .github/workflows/actionlint.yml
name: actionlint
on:
  pull_request:
    paths: ['.github/workflows/**', '.github/actions/**']
  push:
    branches: [main]
    paths: ['.github/workflows/**']
jobs:
  actionlint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-go@v5
        with:
          go-version: '1.22'
      - name: Install actionlint
        run: go install github.com/rhysd/actionlint/cmd/actionlint@v1.7.7
      - name: Run actionlint
        run: actionlint
```

Config sketch:

```yaml
# actionlint.yaml
self-hosted-runner:
  labels:
    - go-builder
config-variables:
  - MY_ORG_VAR
```

### 5. Fix Go-repo workflow footguns

1. **Script injection:** never interpolate untrusted `github.event.issue.title`
   etc. directly into `run:`; use env:

```yaml
- env:
    TITLE: ${{ github.event.issue.title }}
  run: echo "$TITLE"   # still validate; prefer no shell if possible
```

2. **Go setup:** pin `go-version` or `go-version-file: go.mod`; cache modules.
3. **Permissions:** default `contents: read`; elevate per-job least privilege.
4. **pull_request_target:** avoid building untrusted PR code with secrets.
5. **action pins:** prefer SHA pins for third-party actions on release workflows.

### 6. Verify with evidence

```bash
actionlint
go test ./... -count=1   # ensure app still builds if workflows call make test
govulncheck ./...
```

1. Open a PR that breaks a workflow expression → check must fail.
2. Confirm shellcheck findings (if installed) are triaged.
3. Document remaining ignores with owner + expiry in `actionlint.yaml` comments.

### 7. Hand off

1. Make actionlint a required status check on protected branches.
2. Add owner to CODEOWNERS for `.github/workflows/`.
3. Schedule quarterly review of `pull_request_target` and self-hosted labels.

## Ops checklist table

| Control | Good | Bad |
| --- | --- | --- |
| Version pin | Tagged actionlint in CI | `go install ...@latest` only |
| Trigger | Path-filtered + main | Never runs on workflow edits |
| Permissions | Least privilege GITHUB_TOKEN | `write-all` default |
| Untrusted input | env + quoting | `${{ github.event.* }}` in run script |
| Self-hosted | Labeled + isolated | Shared dirty runners for PRs |

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Topic fidelity | actionlint ops on GHA for Go repos | Only generic go test |
| Ignores | Rare, commented, owned | Mass global ignore |
| Deploy workflows | SHA-pinned actions | Floating `@main` actions |
| Secrets | OIDC / environment protection | Long-lived PATs in plain secrets |

## Output Checklist

- [ ] Repo scope and workflow owners recorded
- [ ] actionlint installed/pinned and baseline captured
- [ ] CI job runs actionlint on workflow changes
- [ ] High-risk patterns (`pull_request_target`, script injection) reviewed
- [ ] Permissions least-privilege checked
- [ ] Ignores documented with owner/expiry
- [ ] Required check enabled where appropriate
- [ ] `code-quality-standards` applied to any scripts shipped

## Rules

- Authorized repos only; evidence over guesses.
- Prefer failing closed on workflow lint errors.
- Do not disable security-relevant workflow checks without ticket + expiry.
- Focus on `golang-actionlint-ops` (actionlint + Go CI workflows).
- Never commit live secrets to workflows or notes.
