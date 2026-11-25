---
name: pyproject-strict-ruff-with-per-file-ignores
description: Strict ruff config (E, F, I, S = pycodestyle errors, pyflakes, isort, security) plus targeted per-file-ignores for assert-in-tests, vendored upstream code, and infra helpers that legitimately use subprocess.
category: build
version: 1.0.0
version_origin: extracted
tags: [ruff, lint, config, security]
confidence: medium
source_type: extracted-from-git
source_url: https://github.com/Tracer-Cloud/opensre.git
source_ref: main
source_commit: fb5ba0a1b4ef511d16c56a80f1f126b1f581d724
source_project: opensre
source_path: pyproject.toml
imported_at: 2026-04-18T00:00:00Z
---

# Strict Ruff Config with Per-File Ignores

## When to use
You want ruff's full default + security ruleset (`E`, `F`, `I`, `S`) on for the whole repo, but real-world code has legitimate exceptions: `assert` is idiomatic in pytest (`S101`), vendored test fixtures shouldn't be reformatted, and infra helpers genuinely need `subprocess`.

## How it works
- Top-level `[tool.ruff.lint]` enables a small but high-signal rule set:
  - `E` — pycodestyle errors
  - `F` — pyflakes (unused imports, undefined names)
  - `I` — isort (import order)
  - `S` — flake8-bandit (security)
- `per-file-ignores` is a glob → list-of-rules map. Use globs that mirror your test naming convention so new test files pick up the ignores automatically.
- Vendored upstream code (e.g. `tests/e2e/upstream_*/pipeline_code/**`) gets the entire `S` family suppressed because it's not yours to fix.

## Example
```toml
[tool.ruff.lint]
select = ["E", "F", "I", "S"]

[tool.ruff.lint.per-file-ignores]
# assert is idiomatic in pytest
"*_test.py"                       = ["S101"]
"tests/**/*_test.py"              = ["S101"]
"tests/**/test_*.py"              = ["S101"]
# vendored third-party pipeline code — not ours to fix
"tests/e2e/upstream_lambda/pipeline_code/**"      = ["S"]
"tests/e2e/upstream_apache_flink_ecs/pipeline_code/**" = ["S"]
"tests/e2e/upstream_prefect_ecs_fargate/pipeline_code/**" = ["S"]
# subprocess / url-open / temp-file usage in infra helpers is intentional
"tests/shared/**"                 = ["S108", "S310", "S603", "S607"]
"tests/**/infrastructure_sdk/**"  = ["S108", "S603", "S607"]
"tests/**/trigger_lambda/**"      = ["S108", "S603", "S607"]
```

## Gotchas
- Suppress per-rule, not per-category, when possible (`S101` not `S`) so you keep coverage on the rules you care about.
- Use multiple globs covering both naming conventions (`*_test.py` AND `test_*.py`) — pytest accepts both, ruff doesn't fold them.
- Avoid suppressing rules globally; one `noqa` at the call site is better than a project-wide ignore.
- `select = ["E","F","I","S"]` is a great starter; add `B` (flake8-bugbear) and `UP` (pyupgrade) when the team is ready.
