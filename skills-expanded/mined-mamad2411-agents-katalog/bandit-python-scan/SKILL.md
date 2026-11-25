---
name: bandit-python-scan
description: >
  Bandit SAST for owned Python codebases: install/run CLI, severity baselines,
  pyproject/YAML config, skipping tests properly, CI gates, and triage of BXXX
  rules (subprocess, pickle, assert, hard-coded passwords). Use when adding or
  tuning Bandit — not as a substitute for full security review or for attacking
  third-party apps.
---

# Bandit Python Scan

## Scope And Authorization

- **In scope:** Python repositories you own or are authorized to scan/modify.
- **Out of scope:** Scanning third-party private code without permission; using findings to exploit production without authorization.
- Bandit is heuristic SAST — false positives need tickets, not blind `# nosec` spam.
- Pair with `python-style-and-typing` and `code-quality-standards`; broader SAST programs may add more tools.

## When To Use

- Adding Bandit to local dev or CI for Django/Flask/FastAPI/CLI apps.
- Triaging `subprocess`, `pickle`, `yaml.load`, `eval`, hard-coded secret findings.
- Creating baselines when adopting Bandit on a large legacy tree.
- Tuning excludes for virtualenvs and migrations.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Full code quality / tests | `code-quality-standards` |
| Secrets in git inventory | `secrets-management-hygiene` |
| Injection class testing | `injection-checking` / class-specific skills |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Item | Guidance |
| --- | --- |
| Tool | `bandit` + `bandit[toml]` optional |
| Config | `.bandit`, `bandit.yaml`, or `pyproject.toml` `[tool.bandit]` |
| Severity | LOW/MEDIUM/HIGH; confidence similarly |
| nosec | Inline skip with rule id + justification ticket |
| Tooling | CLI, pre-commit, GitHub Action/Azure Pipeline, SARIF export |

## Workflow

### 1. Confirm scope and success criteria

1. Repo paths, Python version, CI system, authorization to enforce gates.
2. Success: CI runs Bandit; new HIGH issues fail build; baseline tracked for legacy.
3. Owners for triage queue.

### 2. Inventory project layout

```bash
python -m pip show bandit || python -m pip install bandit
find . -name '*.py' | head
ls pyproject.toml setup.cfg .bandit 2>/dev/null
```

1. Identify app vs tests vs scripts/vendor.
2. Note existing linters (ruff, pylint) for overlap.
3. List critical packages (auth, crypto, subprocess wrappers).

### 3. Baseline scan

```bash
bandit -r src/ -f txt -ll
bandit -r src/ -f json -o bandit-report.json
bandit -r . -x ./tests,./venv,.//.tox -f screen
```

1. Count by test id (`B602`, `B301`, …).
2. Separate true issues vs test fixtures needing skips.
3. Save baseline JSON for regression comparison if needed.

### 4. Configure and fix

**`pyproject.toml` sketch:**

```toml
[tool.bandit]
exclude_dirs = ["tests", "venv", ".tox", "migrations"]
skips = []  # prefer fixing over global skips
```

**Common fixes:**

| Rule | Issue | Direction |
| --- | --- | --- |
| B602/B603 | shell=True / untrusted args | `shell=False`, arg list, allowlist |
| B301/B302 | pickle | safer serializers; sign data |
| B506 | yaml unsafe load | `safe_load` |
| B105-B107 | hard-coded passwords | env/secret manager |
| B101 | assert used | real checks outside tests |
| B201 | flask debug | disable in prod |

```bash
# Pre-commit snippet idea
# - repo: local
#   hook: bandit -r src
```

1. Fix true positives with code changes.
2. `# nosec B602` only with comment + ticket; never bare `# nosec` without id when avoidable.
3. CI: fail on HIGH severity (`-lll` / severity level flags per version).

### 5. Verify with evidence

```bash
bandit -r src/ -ll -ii
# Introduce deliberate bad snippet in branch → CI fails
# Remove → CI passes
```

1. Confirm excludes don’t hide `src`.
2. SARIF upload works if using code scanning UI.
3. Document residual accepted findings with expiry.

### 6. Observe and harden

1. Track finding counts over time in CI metrics.
2. Periodic full scan including previously excluded paths.
3. Combine with dependency scanners (pip-audit) — Bandit won’t catch CVEs in deps.

### 7. Hand off

1. Developer doc: run Bandit locally before PR.
2. Triage SLA for new HIGH.
3. Config owned in repo; changes reviewed.

## CI Gate Example

```bash
bandit -r src/ -f json -o bandit.json -ll
# fail if any HIGH severity in report (jq)
```

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Adoption | Fix or baseline with owners | `-lll` off forever |
| Skips | Per-line rule id + reason | `# nosec` on whole file |
| Scope | App code scanned | Only tests scanned |
| Secrets | Remove hard-coded | Ignore B105 as noise always |
| CI | Blocks new HIGH | Advisory log nobody reads |

## Output Checklist

- [ ] Bandit installed and runnable
- [ ] Baseline report captured
- [ ] Config excludes sensible paths only
- [ ] True positives fixed or ticketed
- [ ] CI gate enforced for severity policy
- [ ] nosec policy documented
- [ ] Residual risk list with owners
- [ ] Dev docs updated
- [ ] `code-quality-standards` applied

## Rules

- Authorized repos only.
- Prefer fixes over suppressions.
- Bandit is necessary but not sufficient security review.
- Never commit secrets found — rotate them.
- Keep configs reviewed like code.
