---
name: dev-flow-loop
description: Use when the user asks for Loop Engineering, goal-preserving automation, repeated or multi-round dev-flow control, loop DAGs, task discovery inboxes, automation guardrails, loop review, or an outer loop that drives phase-level dev-flow work.
---

# Dev Flow Loop

Loop Engineering owns the goal, baseline, cross-phase Loop Phase DAG, envelope, and continue/repair/stop decisions. Dev-flow owns each phase plan, isolated implementation, independent task review, and acceptance. All user-facing replies and persisted Markdown artifacts are written in Chinese.

## Start Contract

- The required content baseline is always `requirements.md`, `design.md`, `test-plan.md`, and `test-cases.xlsx`.
- `design.md` combines high-level and detailed design in one document; do not recreate separate high-level-design.md or detailed-design.md files.
- A delivery-loop request or `/dev-flow-loop` implementation request authorizes drafting or updating `requirements.md`, `design.md`, `test-plan.md`, `test-cases.xlsx`, the Loop Phase DAG, envelope, and `loop-state.md` before the Loop Start Gate. This drafting authorization does not authorize phase execution or external side effects.
- `design.md` always includes a project-specific system architecture diagram and a flowchart or sequence diagram for every retained typical workflow. Add other diagrams only when short prose is insufficient.
- Treat A/B, 01, and single-row template entries as repeatable examples, never quantity limits. Inventory actual items from requirements, code, existing interface/protocol documents, and runtime evidence; add one ordered section or row per confirmed item, remove unused examples, and record unknowns instead of inventing or omitting content.
- Use one combined loop-start checker over all four baseline artifacts, the Loop Phase DAG, and envelope.
- The Loop Phase DAG may expose multiple dependency-ready phases. Parallelism applies only to those Phase nodes, never to tasks inside one OpenSpec phase.
- Present one Loop Start Gate and persist one loop_start_ready signal. The Gate asks once whether to enable parallel Phase execution and, when enabled, defaults to one worktree per Phase with a finite max_parallel_phases, one Loop integration branch, serial post-acceptance Phase integration, a final-delivery mode, and cleanup policy. Approval authorizes only the reviewed choices inside the baseline and envelope.

## Steps

1. Recover goal, existing Loop Markdown, phase evidence, budget, and actual repository state.
2. Draft the four required content artifacts from the bundled Chinese templates, plus the Loop Phase DAG and finite envelope. Keep OpenSpec/opsx originals outside the Loop directory.
3. Run one combined loop-start checker with a 0-100 score and the shared max_checker_evaluations budget from dev-flow-master/references/state-and-gates.md.
4. Present the single Loop Start Gate with scope, score, P0/P1 findings, Phase waves, parallel choice, max_parallel_phases, worktree and integration policy, budget, stop conditions, and side effects. Persist loop_start_ready.
5. Resolve the Ready Phase Set from all dependency-ready DAG nodes and matching phase-artifacts.md or opsx-index.md entries. If parallel execution was approved, dispatch a non-overlapping subset up to max_parallel_phases into dedicated Phase worktrees; otherwise dispatch one Phase. Each Phase creates one OpenSpec delta and executes its OpenSpec tasks with one writer at a time after its combined planning checker.
6. After each dispatched Phase reaches acceptance, cherry-pick accepted Phase commits one Phase at a time into the Loop integration branch in stable Phase-ID order. Run affected checks after each integration and one cross-Phase integration check after the wave. Dependent phases become ready only after prerequisites are accepted, integrated, and verified.
7. Let phase_eval consume the reused acceptance plus integration evidence and choose continue, repair, or stop. Do not duplicate unchanged review.

## Boundary

Default read-only for explicit triage and workflow-review requests. Delivery or implementation requests may draft the pre-gate Loop artifacts named above. The Loop Start Gate may approve Phase worktrees, local Phase branches/commits, serial integration into the named Loop integration branch, and post-integration cleanup for this Loop. Push, PR, target-branch merge, scheduler, paid, destructive, or external effects remain unapproved unless the same Gate explicitly names them. Stop when scope, budget, repair, concurrency, integration, or side-effect boundaries are exceeded.

## References

- references/control-plane.md: start bundle, checker, gate, signals, evidence order, phase dispatch, and eval.
- assets/baseline-templates/requirements.md: requirements baseline.
- assets/baseline-templates/design.md: combined high-level and detailed design.
- assets/baseline-templates/test-plan.md: test strategy and representative coverage.
- assets/baseline-templates/test-cases.xlsx: complete execution-level test cases.
- ../dev-flow-master/references/state-and-gates.md: shared bounded-convergence and task-review policy.
