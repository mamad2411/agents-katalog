---
name: benchmark-framework-runner
description: Run one host benchmark pass for a selected framework argument across FerrisGrid and competitor CLI surfaces.
---

# Benchmark Framework Runner

Use this skill when the user wants Codex to execute or prepare benchmark runs for one framework at a time.

## Required Argument

`framework` must be one of:

- `ferrisgrid`
- `playwright`
- `agent-browser`
- `browser-use`
- `selenium`

## Optional Arguments

- `scenario`: one scenario ID from `docs/tests/test-cases.md`
- `trial`: trial number, usually `1`
- `mode`: `browser` or `desktop`
- `result_dir`: output directory under `docs/tests/results/host-v1/`

## Workflow

1. Read `docs/tests/host-runbook.md` and `docs/tests/test-cases.md`.
2. Select the framework-specific execution surface for the chosen `framework`.
3. Use the exact task prompt and success criteria for the chosen scenario.
4. Keep the execution host-only.
5. Do not inspect fixture source, DOM state, or browser automation internals during timed execution unless the scenario explicitly allows it.
6. Record `started_at`, `ended_at`, `wall_time_ms`, `tokens_input`, `tokens_output`, and `tokens_total` in the result file.
7. If the token ledger is unavailable, backfill token cost from the Codex JSONL log by intersecting the run window with the log timestamps. Mark tokens as `pending` only when the log is missing.

## Framework Rules

- `ferrisgrid`: use `ferrisgrid observe` and `ferrisgrid act` only.
- `playwright`: use the Playwright CLI or a local script invoked from the CLI.
- `agent-browser`: use the installed CLI surface only.
- `browser-use`: use the installed CLI surface only.
- `selenium`: use a local script invoked from the CLI.

## Output

Write one Markdown result file per framework/scenario/trial under `docs/tests/results/host-v1/`.
