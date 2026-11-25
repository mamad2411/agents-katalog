---
name: dev-flow-acceptance
description: Use when dev-flow execution is settled and the main agent must run final acceptance, collect evidence, write the delivery report, produce a phase result, or decide readiness.
---

# dev-flow-acceptance

Own final readiness and the delivery report. It verifies integrated behavior; it does not implement fixes, repeat unchanged task reviews, or bypass earlier gates. All user-facing replies and persisted Markdown artifacts are written in Chinese.

## Evidence Policy

Markdown artifacts are the workflow record. Apply the shared bounded-convergence quality policy from `../dev-flow-master/references/state-and-gates.md`. Task reviewer scores and findings remain authoritative for task content; acceptance adds fresh integration and system evidence only where task-local evidence cannot prove the whole workflow.

## Steps

1. **Reconcile inputs.** Follow `references/readiness-and-report.md`; read actual state, the canonical OpenSpec tasks, progress, and reviewer evidence.
   **Complete when:** every task, requirement, test, gate, Git state, and deferral is accounted for.

2. **Run fresh integration checks.** Execute only the final, regression, and system-level checks needed to prove the integrated workflow; verify `/opsx:verify <change>` when applicable.
   **Complete when:** every required integration command has a fresh result or an explicit approved deferral.

3. **Reuse independent judgments.** Aggregate the per-task independent reviewer scores/findings and the integration evidence. Do not start another checker over the same unchanged evidence. Start a focused checker only when new cross-task behavior or unresolved integration risk lacks independent judgment.
   **Complete when:** content quality meets the 95 target or 90 floor with no P0/P1 blocker, or a concrete `not-ready` route exists.

4. **Persist readiness.** Write the delivery report and `review_evidence_ready`/`acceptance_ready`. For Loop phases, mark the Phase accepted and return the same result to the Loop; acceptance does not mark it integrated. Loop adds serial integration evidence before `phase_eval` settles the Phase.
   **Complete when:** report, evidence summary, Phase acceptance state, and actual worktree state agree.

5. **Return control.** Report `ready-to-report`, `ready-for-review`, or `not-ready`. Independent CR remains separately user-triggered.
   **Complete when:** the final state names evidence, residual risk, Git status, next owner/action, and every blocked criterion.

## Context Pointers

- `references/readiness-and-report.md`: inputs, focused integration checks, report, evidence reuse, failure recovery, and signal.
- `../dev-flow-master/references/state-and-gates.md`: Markdown state, quality thresholds, findings, and readiness.

Artifact existence, an agent report, or a passing subset of tests is never acceptance completion.
