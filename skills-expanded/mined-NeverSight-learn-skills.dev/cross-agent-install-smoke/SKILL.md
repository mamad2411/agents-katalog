---
name: cross-agent-install-smoke
description: >-
  Phase 1 dry-run JSON smoke and phase 2 temp-HOME install smoke for skills sync.
  Use when validating cross-harness install parity. NOT for live --apply installs.
user-invocable: true
argument-hint: "[phase]"
license: MIT
metadata:
  author: wyattowalsh
  version: "1.0.0"
---

# Cross-Agent Install Smoke

Validate additive skills sync without mutating live harness installs.

**Scope:** Install smoke only. Do not run live apply installs unless the maintainer explicitly requests it.

## Dispatch

| $ARGUMENTS | Action |
|------------|--------|
| Empty / `phase1` / `dry-run` | Run phase 1 dry-run JSON assertions |
| `phase2` / `local` / `smoke` | Run phase 2 temp-HOME smoke (requires `INSTALL_SMOKE=1`) |
| `all` | Run phase 1, then phase 2 when gated |
| `help` | Show phases, gates, and example commands |

## Phase 1 — Dry-Run JSON

Run the deterministic checker from the repo root:

```bash
uv run python skills/cross-agent-install-smoke/scripts/dry_run.py
```

Phase 1 executes the repo skills-sync dry-run command and asserts:

- top-level keys: `ok`, `mode`, `inventory_count`, `include_installed`, `agents`
- `mode` is `dry-run`
- each agent row includes `agent` plus list fields `missing`, `already_present`, `unresolved`, `skipped`

Pass criteria: script exits `0` and prints a JSON summary to stdout.

## Phase 2 — Temp-HOME Smoke

Phase 2 is opt-in and mutates only a temporary home directory.

```bash
INSTALL_SMOKE=1 uv run python skills/cross-agent-install-smoke/scripts/local_smoke.py
```

The script:

1. Refuses to run unless `INSTALL_SMOKE=1`
2. Creates an isolated `HOME` under a temp directory
3. Runs the repo validation command against the repo
4. Runs a single-harness skills-sync dry-run JSON probe
5. Cleans up the temp home

Never point phase 2 at a production home directory.

## Validation Contract

```bash
uv run python skills/cross-agent-install-smoke/scripts/check.py
INSTALL_SMOKE=1 uv run python skills/cross-agent-install-smoke/scripts/check.py
```

Completion criteria:

1. Phase 1 (`dry_run.py`) exits `0` in CI and local maintainer runs.
2. Phase 2 runs only when `INSTALL_SMOKE=1` is set.
3. `scripts/check.py` exits `0` for the selected phase gates.

## Critical Rules

1. Default to dry-run; never apply live installs from this skill.
2. Treat skills sync JSON as evidence, not authority over repo policy.
3. Run phase 1 before recommending any cross-harness install reconciliation.
4. Gate phase 2 behind `INSTALL_SMOKE=1` and a disposable temp `HOME`.
5. Report harness-specific inventory errors without masking top-level `ok: false`.
