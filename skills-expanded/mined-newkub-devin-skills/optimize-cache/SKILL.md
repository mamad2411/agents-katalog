---
name: follow-tool-moonrepo-optimize cache
description: Tune moonrepo cache and affected targets to make build/test faster
argument-hint: "[scope]"
related:
  - follow-monorepo
  - run-build
---

## Goal

Raise the cache hit rate and cut `moon run` time — local/remote cache tuning and affected-target filtering, measured before and after

## Scope

Use when a moonrepo monorepo is slow or cache misses often — it doesn't cover setup/tasks definition (see `workflows/setup-moonrepo/SKILL.md` and `workflows/config-pipeline/SKILL.md`)

## Execute

### 1. Baseline

> Goal: capture the old numbers before optimizing

1. Run `moon run :build` cold and time it
2. Re-run warm — record which tasks cache hit/miss from the output
3. Use `moon query` to see the project/task graph and find bottlenecks — do `/deep-optimize` if deeper analysis is needed

### 2. Fix Cache Misses

> Goal: cut cache misses from imprecise config

1. Check each task's `inputs` — if too broad or including frequently changing files (generated files, timestamps) → limit to the source globs that actually affect the output
2. Check `outputs` completeness — missing outputs = artifacts lost on cache restore
3. Check env vars entering the hash — move frequently changing ones out of hashed inputs/env
4. One at a time — fix one key then re-measure; never change several keys at once

### 3. Remote Cache

> Goal: set up remote cache for team/CI

1. moonrepo supports remote caching — configure per official docs for the backend used (don't invent config keys)
2. Store credentials/tokens via `/follow-secret-manager`, never commit
3. In CI pass the required env vars — verify with cache hits across CI runs

### 4. Affected Targets

> Goal: run only what changed

1. Use `moon run :<task> --affected` to run only projects changed vs the base
2. Use `--base`/`--head` flags to set the comparison range in CI (check `moon run --help` for current flags)
3. Use `moon query affected` or related queries to inspect before a real run
4. Use project/task selectors (`moon run <project>:<task>`) for scoped runs

### 5. Compare And Report

> Goal: measure after fixes vs the baseline

1. Re-run cold + warm runs — compare time and hit rate with step 1
2. No improvement or regression → revert that point and report
3. Passing → `/report-before-after` with real numbers

## Rules

### 1. Evidence-Based

- Baseline always first — never optimize without the old numbers
- Fix one point at a time, high impact → low

### 2. Cache Correctness

- Preserve behavior — optimize ≠ change build output
- Don't trim `inputs` that really affect the output just to raise the hit rate (stale cache = bug)

### 3. Safety

- Remote cache credentials only via the secrets manager
- If unsure about an option/flag → check `moon <cmd> --help` or official docs

- Use /deep-optimize if needed

## Expected Outcome

- Cache hit rate improved, measurable before/after
- Affected-target runs used in CI to cut unnecessary work
- Remote cache works across local and CI (when configured)
