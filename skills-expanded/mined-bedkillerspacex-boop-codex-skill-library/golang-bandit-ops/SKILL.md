---
name: golang-bandit-ops
description: >
  Operate Bandit (Python SAST) in repos that also contain Go or polyglot
  monorepos: install, CI gates, baselines, and routing pure Go SAST elsewhere.
  Use for owned codebases under authorization.
---

# Golang Bandit Ops

## Research grounding

Runbook for **Bandit** (Python security linter) operations in environments
labeled under the `golang-*` skill family—typically **polyglot monorepos** where
Go services coexist with Python tooling/scripts. Skill id: `golang-bandit-ops`.

## Scope And Authorization

- **In scope:** repositories you own; CI you control.
- **Out of scope:** scanning third-party codebases without permission.
- Treat findings as starting points; verify true positives.
- Pair with `code-quality-standards`; pure Go static analysis → `staticcheck`/`gosec`/semgrep Go rules.

## When To Use

- Monorepo has Python (scripts, ML, serverless) beside Go services.
- Adding Bandit to CI without drowning in noise.
- Establishing baselines and per-path excludes.
- Focus tokens: **golang, bandit, ops** (Bandit ops in Go-centric estates).

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Go-only SAST | `staticcheck`, `govulncheck`, gosec, `golang-asvs-gates` |
| Full SSDLC | `secure-sdlc-checklist` |
| Python style | `python-style-and-typing` |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Area | Guidance |
| --- | --- |
| Tool | `bandit` CLI / `bandit -r` |
| Targets | `**/*.py` only—not Go |
| Config | `.bandit` / `bandit.yaml` skips and excludes |
| Severity | Gate on high/medium; track low |
| Baseline | `bandit -f json` baseline file for debt |
| Pitfalls | Running Bandit on Go files (noop/noise); ignoring `#nosec` abuse |

## Workflow

### 1. Confirm scope and success criteria

1. Repo paths with Python, CI system, authorization.
2. Success: Bandit CI job on Python changes; high severity fails; Go jobs separate.
3. Owner for suppressions.

### 2. Inventory

```bash
# Find Python in a Go monorepo
rg --files -g '*.py'
```

1. Virtualenv/poetry tools present.
2. Existing security scanners.

### 3. Baseline

```bash
pip install bandit==1.7.10
bandit -r python/ -f json -o bandit-baseline.json || true
```

1. Triage baseline; fix or accept with expiry.

### 4. Operate in CI

```yaml
# Illustrative GitHub Actions job
jobs:
  bandit:
    if: contains paths python/**
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: '3.12' }
      - run: pip install bandit==1.7.10
      - run: bandit -r python/ -ll -ii
  go-sec:
    steps:
      - run: go test ./...
      - run: govulncheck ./...
      - run: staticcheck ./...
```

1. Exclude generated code, venv, tests only when justified.
2. `# nosec` requires comment with ticket/reason.
3. Do not use Bandit as substitute for Go analysis.

### 5. Verify with evidence

```bash
bandit -r python/ -ll
go test ./... -count=1
govulncheck ./...
```

1. Introduce known Python issue in branch → Bandit fails.
2. Go-only PR does not needlessly run Bandit if path filtered (optional optimization).

### 6. Observe and harden

1. Track open high findings age.
2. Upgrade Bandit pinned version quarterly.
3. Cross-train: Python findings owners vs Go owners.

### 7. Hand off

1. Document config location and severity policy.
2. Link Go gates in same SSDLC doc.
3. Apply `code-quality-standards` to both languages.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Scope | Python paths only | Expect Bandit to secure Go |
| Noise | Baseline + path excludes | Fail on all low forever unowned |
| Suppress | Ticketed nosec | Blanket skip |
| Topic fidelity | Bandit ops in Go monorepos | Generic go test only |

## Output Checklist

- [ ] Python paths inventoried
- [ ] Bandit pinned and configured
- [ ] CI gate with severity policy
- [ ] Baseline triage done
- [ ] Separate Go SAST present
- [ ] Suppression policy documented
- [ ] `code-quality-standards` applied

## Rules

- Bandit ≠ Go security scanner.
- Focus on `golang-bandit-ops` as polyglot ops.
- Authorized repos only.
- Justify every skip.
