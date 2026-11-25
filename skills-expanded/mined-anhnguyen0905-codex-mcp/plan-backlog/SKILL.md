---
name: plan-backlog
description: Backlog decomposition for the Planning phase — slicing rules, dependency ordering, and per-task acceptance criteria sized for single Codex runs.
---

# Backlog Breakdown

**Helpers**: required — task-waves.mjs, requirements-coverage.mjs (helper rule: missing → STOP and tell the user to reinstall the codex-flow plugin; non-zero exit → surface the error and STOP).

Decompose the approved plan into `.codex-flow/TASKS.md`. Each task is one Codex run and one review cycle.

## Task format

```markdown
## T1: <imperative title>
- Depends on: — | T<n>
- Files: <create/modify list>
- Requirements: <R-IDs covered>
- Steps: <concrete, file-level steps>
- Skills: <relevant skills from PLAN.md "Skills plan" (*Skills to use* + before-execution created skills), or — >
- Acceptance: <verifiable criteria for THIS task alone>; satisfies A<n>[, A<n>]
- Session: —
- Status: pending
```

`Session` and the transition log beneath `Status` are execution-time fields that the orchestrator
fills in Phase 4. The backlog always writes `- Session: —` and `- Status: pending`; do not add
transition lines while planning.

The `Files:` and `Depends on:` fields are also what `scripts/task-waves.mjs` reads to compute
parallel execution waves — keep them accurate and file-level, not vague.

## Sizing: size for one execution AND one review

A task is the unit Codex builds in one run and Claude verifies in one pass — size it for both:

- **One reviewable concern per task**: it should satisfy one clear acceptance check that a reviewer
  can confirm without holding several unrelated changes in their head. If review would have to juggle
  two unrelated concerns, that's two tasks.
- **Bounded blast radius**: prefer a diff a reviewer reads in a single sitting — roughly **≤ ~5 files
  / a few hundred changed lines**. Bigger diffs review shallowly and risk the 64 KB `diff` cap
  truncating what the reviewer sees. Too big → split.
- **~5–30 min of Codex work** as a secondary check: a task you can't describe in a few file-level
  steps is too big; a one-line tweak is usually too small to be its own review cycle — fold it in.
- **Mandatory slice overflow**: if `context-slice.mjs` reports
  `mandatory slice content exceeds tokenBudget`, split the oversized task in the backlog; never
  raise the slice budget.
- **Self-sufficient**: each task must be doable by a *fresh* Codex session from PLAN.md + the task
  text alone (a domain shift starts a new session with no prior memory). Put the context it needs in
  `Steps` and name the files to read — don't rely on "as we did in T2".

## Slicing rules

- **Contracts/foundations first**: the shared seams from PLAN.md (types, schemas, interfaces,
  migrations) become the earliest tasks, so every dependent task builds and reviews against a fixed
  contract instead of a moving one. Isolate risky tasks (migrations, public API changes) so a failed
  run has a small blast radius.
- **Independently verifiable**: each task's acceptance must be checkable when only that task is done
  (its tests pass, build stays green) — never "works after T5 lands".
- **Acceptance names the exact check**: state the command the reviewer runs — the test file/pattern,
  `npm run build`, or a concrete manual probe — not just prose. Phase 5 runs it verbatim.
- **Acceptance cites the plan's A-entries**: end each `Acceptance:` field with the citation form
  `; satisfies A<n>[, A<n>]` — every PLAN `A<n>` must be cited by at least one task, and the tokens
  after `satisfies` must be bare `A<n>` IDs (no suffixes). Citations are matched
  case-insensitively (`a3` resolves to `A3`), but each token must still be a bare `A<n>` ID.
- **Vertical over horizontal** where possible: a thin end-to-end slice (one endpoint + its test)
  reviews better than "all models, then all controllers".
- **File-disjoint where independent**: actively reshape task boundaries so independent tasks
  own disjoint `Files:` sets. If multiple tasks would edit a shared helper, move that helper edit
  into its own earlier task and make the other tasks depend on it. For multi-task backlogs, make
  `task-waves` width > 1 the norm, not the exception; serialize only work that truly must share a
  file.
- **Dependency-ordered**: a task may only depend on earlier tasks; no cycles.
- **Tests live inside the task** that adds the behavior — never a trailing "write tests" task.
- **Map skills once, here**: fill each task's `Skills:` field from PLAN.md's "Skills plan"
  (*Skills to use* + any before-execution created skills) so Phase 4 embeds a consistent,
  user-reviewable set per task instead of re-guessing each run (— if none apply).

## Sanity checks before showing the user

Re-run every check below after a plan change updates affected tasks or the improvement gate appends
tasks; do not schedule the changed backlog until all checks pass.

- Union of all task acceptance criteria covers every plan acceptance criterion (no orphan requirements).
- Run `node "${CLAUDE_PLUGIN_ROOT}/scripts/requirements-coverage.mjs" --requirements .codex-flow/REQUIREMENTS.md --tasks .codex-flow/TASKS.md --plan .codex-flow/PLAN.md`. Every effective R<n>.<m> must be cited
  by at least one task and no task may cite an unknown ID; fix the backlog before presenting it for
  approval. Every PLAN `A<n>` acceptance entry must be cited by at least one task's `Acceptance:`
  field; treat a non-zero exit (orphan `A<n>`, unknown citation) as fix the backlog before
  presenting it.
- No tasks that could run concurrently (in the same wave) touch the same file; dependency-ordered
  tasks may share files because they serialize (avoids Codex-vs-Codex merge conflicts).
- First task is small — it validates the plan's assumptions cheaply before the expensive middle.
- Mirror tasks with TaskCreate so the user sees live progress during execution.
