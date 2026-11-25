---
name: follow-tool-github-actions-optimize ci
description: Tune GitHub Actions CI — caching, matrix, concurrency, artifact reuse for speed
argument-hint: "[scope]"
related:
  - follow-tool-github-actions
  - run-verify
---

## Goal

Reduce GitHub Actions workflow time and cost — dependency caching, matrix strategy, concurrency groups, artifact reuse — measuring before and after

## Scope

Use when existing workflows are slow or run redundantly — it does not cover creating new workflows (see `workflows/setup-workflows/SKILL.md`)

## Execute

### 1. Baseline

> Goal: measure current CI time before optimizing

1. Review workflow run history in GitHub — record the duration of the slowest jobs
2. Identify the most time-consuming steps: dependency install, build, test — run /deep-optimize if deeper analysis is needed
3. Check the cache hit rate of existing `actions/cache` or setup-action caching

### 2. Dependency Caching

> Goal: cache dependencies so install is faster

1. Use the setup actions' `cache` option when supported (e.g. `actions/setup-node` offers `cache: npm|pnpm|yarn|bun`) — check official docs for the action you use
2. If manual caching is needed: use `actions/cache` with a key built from the lockfile hash and the correct cache dir path
3. Use `restore-keys` as a fallback when the lockfile changes
4. Don't cache the whole `node_modules` folder if the package manager has its own store cache that fits better

### 3. Matrix Strategy

> Goal: parallelize sensibly with a matrix

1. Use `strategy.matrix` for multiple OS/versions only when needed — an oversized matrix = high cost
2. Use `fail-fast: false` when every combination's result should be visible; `true` when failing fast matters
3. Use `include`/`exclude` to drop unnecessary combinations

### 4. Concurrency And Artifact Reuse

> Goal: cut redundant runs and repeated work across jobs

1. Set `concurrency: ${{ github.workflow }}-${{ github.ref }}` with `cancel-in-progress: true` for CI — cancel stale runs on a new push
2. Use `actions/upload-artifact` + `actions/download-artifact` to share build outputs across jobs instead of rebuilding (e.g. build once → test/deploy jobs consume the artifact)
3. Use `needs` to order jobs — build before test/deploy
4. Use `paths`/`paths-ignore` filters in triggers to skip runs when only docs etc. change

### 5. Compare And Report

> Goal: measure after the change against the baseline

1. Trigger new runs — compare duration and cache hit rate with step 1
2. If nothing improved or CI broke → revert that point and report
3. Passing → `/report-before-after` with real numbers

## Rules

### 1. Evidence-Based

- Always baseline from real run history first — never optimize without numbers
- Fix one point at a time, high impact → low

### 2. Correctness

- Preserve behavior — never reduce test coverage or skip checks for speed
- Cache keys must include the lockfile hash — stale cache = broken builds
- Artifact reuse requires deterministic outputs — rebuild otherwise

### 3. Cost

- Large matrices with fail-fast disabled = high minutes — balance coverage vs cost
- `cancel-in-progress: true` for PR workflows; be careful on release workflows (may cancel a release mid-run — use for CI only)

- Use /deep-optimize if needed

## Expected Outcome

- CI duration measurably lower from before/after run history
- High dependency cache hit rate
- Concurrency groups prevent redundant runs
- Artifact reuse across jobs cuts rebuilds
