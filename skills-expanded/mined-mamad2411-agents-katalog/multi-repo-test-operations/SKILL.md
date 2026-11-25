---
name: multi-repo-test-operations
description: Execute and validate test suites across a multi-repo workspace — per-repo interpreter discovery, stable baseline suites, and cross-pulse validation of flagged at-risk work
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [testing, pytest, multi-repo, cron, qa, pulse, validation]
    triggers: [run tests, test suite, pytest, multi-repo, sweep validation, at-risk work, py_compile]
    related_skills: [qa-pulse, recurring-status-checks, codebase-inspection]
---

# Multi-Repo Test Operations

Run and validate test suites when work spans several repositories with different toolchains. Complements `qa-pulse` (the pulse lifecycle) by covering the execution mechanics that vary per repo. Use whenever a QA/pulse cycle must run suites in more than one repo, or must verify that previously-flagged work was committed and still passes.

## Core Principle

**Never assume the same Python invocation works across repos.** Each repo has its own interpreter setup. A blind `./venv/Scripts/python.exe` on a repo without a venv fails with exit 127 (`No such file or directory`) and wastes a cycle.

## Step 1: Discover the Interpreter

Before any suite run:

```bash
ls -d .venv venv 2>/dev/null            # which venvs exist in this repo?
./venv/Scripts/python.exe -m pytest --version 2>&1 | head -1   # venv has pytest?
python -m pytest --version 2>&1 | head -1                      # system fallback
```

Pick the first interpreter that reports a pytest version.

## Workspace Conventions (the operator's repos, Windows)

| Repo | Interpreter | Notes |
|------|-------------|-------|
| `hermes-agent` | `venv/Scripts/python.exe` | Py3.11, pytest 9.1.1 |
| `_project` | system `python` | 3.11.9, NO venv |

Verify conventions with Step 1 — they can change (venv migrations happen; see PULSE.md history).

## Step 2: Use the Stable Baseline Where One Exists

`hermes-agent` combined regression (approval + scripts + hermes_state), ~399 tests / ~27-31s:

```bash
venv/Scripts/python.exe -m pytest tests/tools/test_approval.py tests/scripts/ tests/hermes_state/ -q -p no:cacheprovider
```

Suite **composition** is more stable than test **counts** (399↔384 across cycles as tests land). Report the count as-is; don't treat drift as regression.

## Step 3: Validate Resolved At-Risk Work

When a prior cycle flagged uncommitted changes as at-risk (e.g. "commit or stash before next rebase"):

1. Check git log/status — did it get committed?
2. **Committed** → validate: `python -m py_compile <file>` + run the affected suite (or the full repo suite if small)
3. **Still uncommitted** → re-flag with the consecutive-cycle count (escalation language applies)
4. Mark resolved/at-risk in the report and pulse log

This is the ideal "one meaningful thing" for an otherwise-quiet cycle: it closes the loop on prior flags and proves the committed fix holds.

## Pitfalls

- **Don't reuse `venv/Scripts/python.exe` across repos.** Verify per repo (`ls -d .venv venv` first, then a pytest version probe).
- **Don't run the full test collection** — use targeted suites or the stable baseline (full collection is 40s+ just to collect on `hermes-agent`).
- **Don't treat test-count drift as regression** — composition matters; counts vary as tests are added/removed.
- **Don't leave flagged at-risk work unverified** — next cycle, check whether it was committed; validate with py_compile + suite if so.
- **Don't append to PULSE.md/digests with `write_file` after a partial read** — use `cat >>` heredoc for PULSE.md and the `append-digest.py` script for the daily digest (see `qa-pulse` / `recurring-status-checks` for the full append-safety rules).

## Related Skills

- `qa-pulse` — the pulse lifecycle this execution layer feeds (quiet-hours gate, regression tracking, PULSE.md/digest appends, Discord report format)
- `recurring-status-checks` — stakeholder status reconstruction when live polling is unavailable
- `codebase-inspection` — LOC/language analysis with pygount
- `discord-report-format` — delivery formatting conventions
