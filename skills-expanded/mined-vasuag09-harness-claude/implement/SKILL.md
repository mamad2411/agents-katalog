---
name: implement
description: Execute a plan via test-driven development — write tests first, then minimal code, phase by phase. Use after /plan (and /architect if needed) to write the actual feature. Delegates to the harness-claude:tdd-guide agent.
---

# /implement — build it, test-first

Goal: turn the plan into working, tested, clean code — one phase at a time.

## Do this
1. **Branch first (non-trivial work).** Apply branch-at-first-write (`rules/git.md`): not a
   git repo → skip silently; already on a non-default branch → stay there; on the default
   branch (main/master/develop, or what `git symbolic-ref refs/remotes/origin/HEAD` resolves
   to) → create `claude/feat-<slug>` (slug from `.claude/STATE.md`) **before** the first
   file edit. Never commit or push — that stays gated behind the user's explicit ask.
2. Take the plan's tasks in order — read `.claude/planning/<slug>/PLAN.md` if present (slug
   in `.claude/STATE.md`) so a fresh-context executor works from the file, not the
   conversation. For each task/phase:
   - **Delegate to `harness-claude:tdd-guide`** (or run TDD inline): write a failing test against an
     acceptance criterion (RED) → minimum code to pass (GREEN) → refactor.
   - Keep files modular and lean (<800 lines), immutable patterns, inputs validated.
   - Let the format/typecheck hooks run; fix what they flag immediately.
3. **Parallel-fan-out checkpoint — evaluate before editing, don't skip.** Before you start
   editing a phase serially, count the files it will *write*. If it spans **3+ independent files
   with disjoint write-sets and no dependency between them** (the plan may already flag this
   phase as a `/harness-claude:orchestrate` candidate), you **must** surface the fan-out option: name the file
   split and propose `/harness-claude:orchestrate`, then let the user choose before proceeding.
   Surfacing the offer is **mandatory whenever the trigger fires** — that is the only path by
   which parallel mode ever gets used; what stays **opt-in is *acting* on it** — never silently
   start a multi-agent run (it spawns workers and costs more tokens). If the trigger doesn't fire,
   note that in one line and edit serially.
4. After each phase, confirm its exit check (test green, build clean) before moving on.
5. If the build breaks and the fix is non-obvious, hand off to `/harness-claude:build-fix`.
6. Stay inside the plan. If reality diverges from it, stop, update the plan, then resume
   — don't silently improvise scope.

## Token discipline
Delegate search/exploration and isolated edits to cheaper models; keep the orchestrator
focused on integration. Compact at phase boundaries, not mid-phase.

## Common rationalizations (don't accept these from yourself)

| Excuse | Reality |
|--------|---------|
| "I'll write the tests after the code works" | Tests written after mirror the implementation, not the criterion. RED first, or it isn't TDD. |
| "This phase is too small to test" | Small phases grow. The test is the phase's exit check — without it, "done" is an opinion. |
| "The plan is close enough; I'll adjust as I go" | Silent divergence is how scope creeps. Stop, patch the plan, resume. |
| "Branching is overhead for this" | A branch is one command and fully reversible; un-picking mixed work on the default branch is neither. |
| "Fan-out doesn't apply here" (without counting) | Count the write-set first. Skipping the count is how the offer never fires. |

## Red flags — stop and re-check
- Code exists for which no test was ever RED.
- You're editing a file the plan never named.
- A hook flagged something and you deferred it "until the end".
- You're three phases in with no green checkpoint between them.

## State
On completion, patch `.claude/STATE.md`: `phase: implement`, `status: done`,
`next_skill: /review`.

## Exit criterion
All phases complete, tests written-first and green, build/types/lint clean. Then
proceed to the Verify phase (`/harness-claude:review`).
