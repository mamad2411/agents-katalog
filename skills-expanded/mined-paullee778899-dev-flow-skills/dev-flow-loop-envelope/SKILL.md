---
name: dev-flow-loop-envelope
description: Use when defining budget, allowed side effects, cadence, stop conditions, locks, safety limits, auto-continue, baseline scope, or approval boundaries for repeated or scheduled Loop Engineering.
---

# Dev Flow Loop Envelope

Define the finite envelope for repeated, scheduled, background, persistent, or auto-continuing Loop activity. This skill prepares controls; `dev-flow-scheduler` owns automation mutation. All user-facing replies and persisted Markdown artifacts are written in Chinese.

## Steps

1. **Recover coordinates.** Read the Loop goal, baseline, Loop Phase DAG, current envelope, trigger, actual side effects, and approvals from Markdown.
   **Complete when:** scope, owner, trigger, existing limits, and conflicts are explicit.

2. **Set finite limits.** Define cadence, iteration/repair/checker/retry limits, max_parallel_phases, wall time or cost ceiling, run-overlap lock, and checkpoints using `references/budget-and-safety.md`.
   **Complete when:** every repeated branch has a finite budget, measurable stop, and escalation action.

3. **Set side-effect boundaries.** Separate allowed effects, approval-required effects, and forbidden effects. For Phase parallelism, define the one-time Gate choice, worktree default, Loop integration branch, serial Phase integration, fallback, final delivery, and cleanup. `within_confirmed_baseline` applies only to the approved baseline and those named effects.
   **Complete when:** every possible write, Git, scheduler, external, paid, or destructive action has one outcome and owner.

4. **Prepare combined review input.** Compare envelope values with the approved requirements.md, design.md, test-plan.md, test-cases.xlsx, the Loop Phase DAG, and actual budget, then return it to the one combined loop-start checker.
   **Complete when:** limits, DAG, baseline, and side effects agree as one start bundle.

5. **Return draft or blocker.** The Loop owner persists `loop_start_ready` only after combined review and the Loop Start Gate; this skill emits no separate readiness signal.
   **Complete when:** the envelope draft is reviewable, or a blocker names the missing limit and next owner.

## Context Pointers

- `references/budget-and-safety.md`: limits, defaults, auto-continue, approvals, blockers, and escalation.
- `../dev-flow-loop/references/control-plane.md`: baseline, Loop Phase DAG, content checker, and phase-eval lifecycle.

A draft is not approval. Only the user-approved Markdown envelope authorizes continuation.
