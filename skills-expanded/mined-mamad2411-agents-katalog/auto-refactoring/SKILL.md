---
name: auto-refactoring
description: >-
  Runs an autonomous refactoring loop that picks files, applies behavior-preserving
  changes, runs the test suite, measures a quality metric (lint warnings, test coverage,
  type errors, complexity), and keeps improvements or reverts failures. Loops indefinitely.
  Triggers on "auto-refactor", "refactor loop", "clean up my codebase", "improve code
  quality", "reduce complexity", or requests to iteratively improve code health metrics.
license: MIT
metadata:
  author: tylergibbs
  version: "1.0.0"
  argument-hint: "[config-file]"
---

# Auto-Refactoring

Autonomous refactoring loop: pick a file, refactor it, run tests + measure a metric,
keep improvements, discard failures.

**Contract: every change either improves the codebase or gets thrown away.**

## Discovery Flow

If `refactor.json` exists, skip to [Setup Phase](#setup-phase).

1. **Explore with 2 parallel subagents:**

   **Agent 1 — Structure & Stack**: Directory tree, language/framework, build system,
   project purpose.

   **Agent 2 — Quality Tools**: Test suites, linters, type checkers, coverage tools.
   What's configured and how to run it.

2. **Present findings and ask one question:**

   > Here's what I found:
   > - [project summary]
   > - [quality tools/metrics]
   >
   > **What do you want to optimize?**
   > 1. Lint warnings ([N] current)
   > 2. Test coverage ([X]%)
   > 3. Type errors ([N])
   > 4. Cyclomatic complexity
   > 5. Custom metric

   Infer config from exploration — see [CONFIG.md](CONFIG.md) for fields and metric catalog.

3. **Write `refactor.json`**, show for confirmation, then proceed.

## Setup Phase

1. Parse `refactor.json`
2. Create branch `autorefactor/<tag>` (append `-2`, `-3` if exists)
3. Verify tests pass and record baseline metric
4. Add `results.tsv` and `run.log` to `.gitignore`
5. Initialize `results.tsv` with header row
6. **This is the last interaction.** From here, fully autonomous.

## The Loop

**LOOP FOREVER. NEVER stop. NEVER ask permission to continue.**

```
1. PICK: Scan target_files, prefer worst per-file metric, cooldown files
   that failed last 3 attempts. Review results.tsv for trends.

2. ANALYZE: Read file, identify issues, pick a strategy from STRATEGIES.md,
   form a concrete hypothesis.

3. EDIT: One conservative, behavior-preserving change. No behavior changes.

4. TEST: Run test_command > run.log 2>&1. Fail → revert, log, move on.

5. MEASURE: Run metric_command. Improved or equal → keep. Regressed → revert.
   Exception: equal metric + simpler code → keep.

6. COMMIT (if kept): Descriptive message with strategy, metric delta, hypothesis.
   Do NOT commit results.tsv or run.log.

7. LOG: Append to results.tsv (iteration, timestamp, file, strategy,
   hypothesis, metric_before, metric_after, status, reason).

8. Every 10 iterations, print progress summary. GOTO 1.
```

## Critical Rules

- **Protect context window** — see [CONTEXT.md](CONTEXT.md). Always redirect output.
- **results.tsv is your memory** — survives git resets, full history.
- **One change per iteration** — isolate variables.
- **Never change behavior** — structure only.
- **Respect the revert** — don't fix a failing refactoring with more changes.
- **When stuck** — see [STRATEGIES.md](STRATEGIES.md).

## Output

- **Git history** on `autorefactor/<tag>` — each improvement is a commit
- **results.tsv** — full experiment log
- **run.log** — most recent test output
