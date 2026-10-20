---
name: quality-eval-core
description: "Shared reference for the quality-eval cluster: the four quality gates (write → commit → CI → ship), the evidence ladder that says what proves a pass at each, pass@k vs a single green run, and the AI write-and-review blind spot. USE WHEN deciding what counts as done, choosing which gate catches a failure class, or wiring a measurement loop — the conventions every quality-eval spoke shares."
cluster: quality-eval
version: 1.0.0
---

# Quality-Eval Core

Shared model for the `quality-eval` cluster. The TDD, E2E, verification, benchmark,
linting, and audit spokes all depend on these conventions — keep them consistent here so
no spoke contradicts another about what "done" means.

## 1. The four gates (the cluster's defining model)

Quality is enforced at **four stages**, cheapest-and-earliest first. Each gate catches a
different failure class; a failure that escapes one is meant to be caught by the next.

```
Edit ──write-time──> Commit ──commit-time──> CI ──build-time──> Release ──ship-time──> Prod
   plankton-          verification-loop        e2e / windows-      production-audit
   code-quality       tdd-workflow             desktop-e2e
                      ai-regression-testing    browser-qa · benchmark
```

| Gate | Stage | Catches | Spokes |
|---|---|---|---|
| Write | every file edit | style / lint / type drift | `plankton-code-quality` |
| Commit | before a PR | "not actually finished", missing tests, regressions | `verification-loop`, `tdd-workflow`, `ai-regression-testing`, `error-handling` |
| CI | build / pipeline | broken behavior, slow paths, broken UI | `e2e-testing`, `windows-desktop-e2e`, `browser-qa`, `benchmark` |
| Ship | pre-launch | "what breaks in prod?" | `production-audit` |

**Rule:** push each check to the **earliest** gate that can catch it. A write-time linter
should not be doing a production audit's job, and a production audit should not be the
first place a type error is noticed.

## 2. The evidence ladder

A claim is only as strong as the artifact behind it. Climb the ladder; never report a rung
you didn't run.

1. **Asserted** — "it works." (no value)
2. **Ran** — a command exited 0; paste the output.
3. **Tested** — a named test covers the behavior and is green.
4. **Measured** — a number against a baseline (coverage %, p95 latency, pass rate).
5. **Reproduced** — green **k times** (`pass@k`), or across agents/runs.

Everything below "Ran" is a guess. `verification-loop` and `eval-harness` exist to force a
claim up this ladder before a PR.

## 3. pass@k — one green run is not a pass

Anything non-deterministic (agent output, flaky E2E, perf, LLM calls) must be judged by
**how often** it passes, not whether it *can*:

- `pass@1` — succeeded once. Says almost nothing for a stochastic task.
- `pass@k` — succeeded in ≥1 of k runs (capability ceiling).
- **pass rate** — fraction of k runs that pass (reliability floor — the number that matters for shipping).

`eval-harness` defines criteria + computes this for Claude Code tasks; `agent-eval` uses it
to rank agents; `e2e-testing`/`browser-qa` use it to separate a real failure from a flake.

## 4. The AI write-and-review blind spot

When the **same model** writes code and reviews it, its blind spots are correlated — it
approves the bugs it was prone to make. Defenses, in order:

- An **independent** check the model can't reason its way around: a deterministic test (`tdd-workflow`, `ai-regression-testing`), a real browser (`browser-qa`), a real OS UIA tree (`windows-desktop-e2e`).
- A gate the model **cannot satisfy by editing its own config** — treat changes to lint/test/CI config in the same iteration as suppressing a violation as a red flag (`plankton-code-quality`).
- A **second judge** for subjective output (a different model/agent — `agent-eval`).

## 5. Tooling matrix

| Concern | Default tool | Spoke |
|---|---|---|
| Web E2E | Playwright (Page Object Model) | `e2e-testing` |
| Desktop E2E | pywinauto + Windows UIA | `windows-desktop-e2e` |
| Visual / interaction QA | headless browser automation | `browser-qa` |
| Write-time lint/format | Plankton (biome / ruff / gofmt …) via PostToolUse hooks | `plankton-code-quality` |
| Perf baseline | JSON baselines in `.benchmarks/`, git-tracked | `benchmark` |
| Eval / pass@k | EDD harness | `eval-harness` |
| Agent comparison | reproducible-task CLI | `agent-eval` |
| Errors | typed errors / retries / circuit breakers (TS · Python · Go) | `error-handling` |

## 6. Shared guardrails

- **Evidence over assertion** — paste the command output; "Ran/Tested/Measured", never "Asserted".
- **pass@k for anything stochastic** — report the pass *rate*, not a lucky single green run.
- **Earliest gate wins** — catch each failure class at the cheapest stage that can.
- **Independent judgment** — don't let the thing under test grade itself; break the write-and-review loop.
- **No config laundering** — a gate satisfied by loosening its own config is not satisfied; flag it.
- **State coverage honestly** — a passing suite over thin tests is a weaker claim than its green color implies; name the gap.
