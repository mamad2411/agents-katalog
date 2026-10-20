---
name: follow-tool-mutants-rs-optimize mutation
description: Make cargo-mutants faster — skip lists, shard/parallel jobs, CI integration
argument-hint: "[scope]"
related:
  - follow-tool-mutants-rs
  - follow-tool-nextest
  - run-test
  - setup-cicd
---

## Goal

Cut cargo-mutants run time — filter low-value mutants, parallel jobs, sharding across machines, incremental CI — while keeping the full signal

## Scope

- Optimizing an already-set-up cargo-mutants (setup → `workflows/setup-mutants`)
- Covers: `#[mutants::skip]`, `exclude_globs`/`exclude_re`, `--jobs`, `--shard`, CI strategy
- Doesn't cover: writing tests for missed mutants (do `/update-tests`)

## Execute

### 1. Baseline

> Goal: capture the old numbers and find mutants that aren't worth it

1. Run `cargo mutants` timed — record duration and mutant count
2. Look through `mutants.out/` — find functions/files with many but low-value mutants (logging, getters, trivial)
3. Identify the slow tests — mutants × test-time is the main cost

### 2. Prune Low-Value Mutants

> Goal: cut the mutant count with skip lists

1. Use `#[mutants::skip]` on uninteresting functions/impls (requires the `mutants` crate as a dependency)
2. Set `exclude_globs` in `.cargo/mutants.toml` for generated/testdata/infra files
3. Use `exclude_re` (config) or `--exclude-re "pattern"` to filter specific mutation patterns
4. Use `examine_globs` to focus only on critical modules — e.g. domain logic, not UI glue
5. Every exclusion must be justified — write a comment or documentation

### 3. Parallelize

> Goal: use the CPU fully and split work across machines

1. Set `--jobs`/`-j` for parallel builds+tests on one machine — start conservative (`-j2`/`-j3`) since cargo build is resource-hungry
2. Set `test_tool = "nextest"` if not already — fail-fast cuts time per mutant
3. Use `--in-place` if tree copying is slow (big workspace) — but beware side effects on the working tree
4. Multiple machines → `--shard k/n` (k from 0 to n-1) — CI runs each shard as a separate job, then merges results
5. Every shard must run with the same args and denominator `n` — otherwise the split is wrong

### 4. CI Integration

> Goal: place cargo-mutants in the pipeline cost-effectively

1. PR checks → run changed code only (`-f`/`--in-diff` with the diff from base) or a small shard
2. Full run → main branch or scheduled (nightly) — mutation testing is too slow to block every PR
3. Use `--baseline=skip` in CI when a pre-check already proved the tests pass — skip the unmutated re-test
4. Upload `mutants.out/` as an artifact — results stay reviewable afterwards
5. Install via `taiki-e/install-action` in GitHub Actions instead of `cargo install` — faster

### 5. Measure And Report

> Goal: re-measure and summarize the trade-offs

1. Re-run after each change — compare duration and caught/missed against the baseline
2. Do `/report-before-after` with before/after numbers
3. If exclusions cause should-have-been-caught mutants to be missed → loosen the filter and report

## Rules

- Baseline always first — never tune without the old numbers
- `#[mutants::skip]`/`exclude_*` must have a reason — don't skip just to make the score look good
- Set `--jobs` conservative — cargo build consumes high CPU/memory, the machine may thrash
- All shards need identical args and `n` — only then is the aggregate result correct
- Scoped PR runs never replace full runs — always keep a scheduled full run

## Expected Outcome

- Mutation runs measurably faster, both local and CI
- Mutant scope focuses on critical code — low-value mutants skipped with reasons
- CI runs scoped on PRs and full on schedule
