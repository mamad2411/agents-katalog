---
name: benchmark
description: Measure whether a harness component (a skill, agent, or rule) actually earns its keep — run the same task k times with and without it, in isolated git worktrees, and report pass@k (works once) and pass^k (works consistently). Opt-in; not wired into the default pipeline. Use to decide keep-vs-cut on evidence, or to fill the R5 benchmark for a /extract proposal.
---

# /benchmark — does this component earn its keep?

Goal: replace opinion with evidence. Run a task **k times with** a named component enabled and
**k times without** it, each trial in its own throwaway `git worktree`, then compare reliability.
Report **pass@k** (passed in ≥1 trial — "can it work") and **pass^k** (passed in all k trials —
"does it work reliably"), and a verdict.

> **Opt-in.** No default-pipeline skill or hook invokes `/benchmark`. It forks git worktrees and
> (when you supply a real task) spawns work k×2 times — always an explicit, deliberate run.
> Git boundary: it only `git worktree add/remove` (an isolated sandbox); it never commits,
> pushes, or branches the working tree.

## When to run
- You want to decide whether a skill / agent / rule is worth keeping (keep-vs-cut on data).
- A `/extract` proposal sits at R5 MANUAL and you want a real empirical signal — benchmark it
  with `--component <draft-name>` so the result lands where R5 looks.

## The harness contract
`scripts/eval/benchmark.js` is generic: it knows nothing about your component. It toggles the
component **only** through env vars the task command honors, for each trial:

| env | meaning |
|-----|---------|
| `HARNESS_COMPONENT` | the component name (label) |
| `HARNESS_COMPONENT_ENABLED` | `1` (with) · `0` (without) |
| `HARNESS_TRIAL` | 0-based trial index |

A trial **passes iff its score command exits 0**. Default score = the task's own exit code;
recommended = `node scripts/eval/checkpoint.js <spec>` so a trial is scored against a spec's
acceptance criteria (reusing the v0.4 gate).

## Do this
1. **Define the task.** Decide what "doing the task" means and write a command that performs it
   in the current worktree, reading `HARNESS_COMPONENT_ENABLED` to enable/disable the component
   under test (e.g. include the skill's guidance only when `=1`). For a model-driven task, the
   command drives a subagent; for a deterministic check, any shell script works.
2. **Define scoring.** Either let the task's exit code be the signal, or pass `--score` (e.g.
   `checkpoint.js` against the task's spec) so PASS/FAIL is judged against acceptance criteria.
3. **Run the benchmark:**
   ```
   node scripts/eval/benchmark.js --component <name> --task '<cmd>' [--score '<cmd>'] [--k 5]
   ```
   Exit **0** = pass verdict (component earns its keep) · **1** = fail verdict (no reliability
   gain) · **2** = usage/setup error (no `--task`, not a git repo, no HEAD commit).
4. **Read the result.** The run prints both cohorts' pass@k / pass^k / success-rate and the
   verdict, and writes `.claude/eval/benchmarks/<slug>.json` (`<slug>` = the component name).
   The verdict is: **earns its keep iff** `with.successRate > without.successRate` **or**
   (`with.passCaret && !without.passCaret`).
5. **Act on it.** Recommend keep or cut with the numbers. For an `/extract` proposal, the
   artifact now feeds R5: re-run `node scripts/eval/extract-rubric.js <draft>` and R5 reports
   PASS/FAIL from the benchmark instead of MANUAL. Promotion into `skills/` is still a human
   call (R4 + your approval) — a passing benchmark never auto-promotes.

## Security & trust
- `--task` / `--score` are author-authored shell, same trust boundary as the test scripts and
  the `eval` fences in checkpoint.js. Don't pass untrusted commands.
- The result artifact records metrics only (counts, rates, the commands you supplied) — no trial
  output or secrets are captured.
- Worktrees are always removed after the run, including on task/score failure.

## Notes
- Self-contained: pure Node + `git` + shell, no companions (mgrep/graph/context7), no network.
- Keep k small for model-driven tasks (each trial is a real run); larger k for cheap
  deterministic tasks buys tighter pass^k confidence.

## Exit criterion
A benchmark result (`.claude/eval/benchmarks/<slug>.json`) exists with both cohorts' pass@k /
pass^k and a verdict, and you've made an evidence-based keep-vs-cut recommendation (or fed the
artifact back into a `/extract` proposal's R5).
