---
name: test-heal
description: |-
  Repairs failing tests whose failure is the test's own fault — and only those. Consumes a failure triage (test_issue | environment_issue | flaky | application_issue), fixes test code, fixtures, selectors, and waits, never application code, and never re-runs the suite itself: it applies fixes, sanity-checks that they parse, commits once, and hands a machine-readable Loop Decision back to the orchestrator, which owns re-running gate-runner. application_issue failures are returned untouched as pipeline fix-up work.
  Not for: application-code fixes (returned untouched as pipeline fix-up work), triaging failures (the triage is its input), or re-running suites (the orchestrator owns gate-runner).
version: 0.1.0
license: Apache-2.0
discoverable: false
authors:
  - agentic-os
---

# test-heal

Called by `sdlc-engine` Phase 10 (autonomous mode) when `gate-runner` fails on
test-side causes. Heal and re-run are deliberately separate responsibilities:
this skill edits and commits, `gate-runner` re-runs — a healer that re-runs its
own work can mask its own failures.

> **Methodology owner.** How flake causes are isolated and classified is defined by the `flaky-debugging`
> blueprint in `agentic-qe`
> (`skills/qe-blueprints/references/catalog/execute/flaky-debugging.md`). This skill
> executes; the blueprint is the authority on method. If the two ever disagree,
> the blueprint wins and this file is what gets corrected — one source of truth,
> so two agents cannot follow two different sets of practices.

For a managed run, use the runtime dispatch, budget, transition, and evidence
operations from `../../references/runtime-authority.md`. A repair report or
JSONL append cannot reset attempts or advance the run; use `legacy.export` for
compatibility ledgers.

## Inputs

- `run_dir` — the active run directory
- `gate_plan` — the runner/commands `gate-runner` detected (never re-detect here)
- `failures` — the failing tests with output excerpts from `qa-report.md`
- `branch` — the active feature branch (all edits stay on it)

## Step 1 — Triage every failure

Classify each failure by OWNERSHIP. When the `test-failure-triage` agent
already ran, map its cause classes onto this taxonomy instead of re-triaging:
TIMING / SELECTOR / DATA / ASSERTION-LOGIC / SHARED-STATE → `test_issue`
(or `flaky` for single-occurrence timing), ENV → `environment_issue`,
PROPAGATION or a genuine regression → `application_issue`.

| Class | Signals | Allowed action |
|---|---|---|
| `test_issue` | selector not found on unchanged UI, assertion against stale copy/fixture, order-dependent state, hard-coded wait too short | **Fix the test** (targeted edits at the cited file:line) |
| `environment_issue` | missing env var, service not running, port conflict, missing browser binary | **No code edit** — report the environment remediation |
| `flaky` | passes in isolation / fails in batch, timing-dependent, single occurrence | **Stabilize the test** (deterministic waits, isolation), never `.skip` |
| `application_issue` | test is right, behavior is wrong: real regression, 5xx from own code | **Never touch** — return it to the pipeline as a fix-up implementation task |

When a failure cannot be confidently classified, treat it as
`application_issue` — mis-healing a real regression is the worst outcome.

## Step 2 — Apply fixes (test-side classes only)

- Edit only test code, fixtures, and test utilities. Application source is
  out of scope no matter what the diff would be.
- Prefer robust selectors (role/test-id) over brittle ones; replace fixed
  sleeps with condition waits; isolate shared state.
- Forbidden regardless of pressure: `.skip`/`.only`/commenting a test out,
  loosening an assertion until it can't fail, adding retries around a real
  regression, sleeps as a fix.

## Step 3 — Sanity-check and commit

- Parse-only verification using the `gate_plan` runner (compile/collect the
  edited test files — e.g. the runner's list/dry-run mode). Do **not** run
  the suite; that is the orchestrator's re-run.
- One commit on the current branch: `test: heal <n> failing test(s) — <short reason>`.

## Step 4 — Report with a Loop Decision

Write `<run_dir>/test-heal-report.md`:

```markdown
# Test Heal Report

## Meta
run_id, branch, commit, healed_count, returned_count

## Healed
- <test id> — <class> — <file:line> — <one-line fix>

## Returned to pipeline (application_issue)
- <test id> — <why the application is at fault>

## Environment remediation
- <env issue and the command/setting that fixes it, if any>

## Loop Decision
outcome: needs_rerun | converged | capped
```

- `needs_rerun` — fixes were committed; the orchestrator re-invokes
  `gate-runner` (counted against loop `gate-runner.retry`, cap 2, per
  `references/gate-catalog.md`).
- `converged` — nothing left that this skill may fix (all remaining failures
  are `application_issue`/environment); the orchestrator routes them onward.
- `capped` — the orchestrator told this skill the loop budget is exhausted;
  report only, no edits.

## Constraints

- Never modify application source, CI config, or gate commands.
- Never re-run the test suite; parse-only checks are the ceiling.
- Never hide a failure (`.skip`, deleted test, gutted assertion).
- All file IO via Read/Write/Edit tools; edits stay on the active branch.
- Validate `test-heal-report.md` sections before returning (the pipeline
  treats a missing `## Loop Decision` as `converged` and escalates).
