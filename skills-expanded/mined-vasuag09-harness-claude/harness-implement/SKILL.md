---
name: harness-implement
description: Orchestrate the entire IMPLEMENT phase — test-driven implementation of the approved plan, resolving build/type errors as they arise. Use after /harness-plan. Sequences /implement and /build-fix, delegates to subagents, and halts if reality diverges from the plan.
---

# /harness-implement — run the Implement phase

Thin orchestrator over the Implement skills. Requires an approved plan from
`/harness-claude:harness-plan` (or `/harness-claude:plan`). Refuse to start without one for non-trivial work.

## Sequence

1. For each plan phase, in order:
   - **`/harness-claude:implement`** — **delegate to the `harness-claude:tdd-guide` agent**: failing test (RED) →
     minimum code (GREEN) → refactor, against the phase's acceptance criteria.
   - **Parallel-fan-out checkpoint (mandatory when it triggers):** before editing a phase
     serially, if it spans 3+ independent files with disjoint write-sets and no dependency, you
     **must** surface `/harness-claude:orchestrate` — name the file split and let the user choose.
     The offer is not optional (that's the only way parallel mode fires); *acting* on it stays
     opt-in — never auto-start a multi-agent run.
   - Let the format/typecheck/quality hooks run; act on what they surface.
   - If the build/types break and the fix isn't obvious → **`/harness-claude:build-fix`** (delegate to
     the `harness-claude:build-error-resolver` agent), minimal diffs only.
   - Confirm the phase's **exit check** (tests green, build clean) before the next phase.

2. **Plan-divergence gate:** if reality contradicts the plan (a phase is wrong, missing,
   or bigger than scoped), **HALT** — report the divergence, update the plan with the
   user, then resume. Never silently improvise scope.

## Rules
- Delegate search/exploration and isolated edits to cheaper models; keep the orchestrator
  focused on integration.
- Files stay modular and lean (<800 lines), immutable patterns, validated inputs.
- Compact at phase boundaries, not mid-phase.
- Do **not** commit or push — branch creation follows `rules/git.md`
  (branch-at-first-write in `/harness-claude:implement`).

## Output
Phase-by-phase summary (what was built, tests added, build status). Then hand off to
`/harness-claude:harness-verify`.
