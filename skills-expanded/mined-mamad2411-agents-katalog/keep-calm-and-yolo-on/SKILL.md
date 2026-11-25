---
name: keep-calm-and-yolo-on
description: >-
  Orchestrate lightweight, reviewed development of a complex repository feature through
  requirements, architecture, an executable plan, serial implementation, P0/P1 review, authorized
  local task commits, and final verification. Always use when explicitly invoked. Auto-trigger only
  for feature design or implementation involving a material migration, compatibility-sensitive
  public interface, authentication, privacy, trust boundary, paid or irreversible effect, complex
  concurrency, distributed or offline synchronization, or at least two of: dependent subsystems,
  architectural tradeoffs, three or more coherent commits, or cross-layer or cross-platform tests.
  Do not auto-trigger for diagnosis, status, review-only work, routine operations, localized fixes,
  mechanical refactors, or simple UI, configuration, documentation, or dependency changes.
---

# Keep calm and YOLO on

## Scope and authority

Deliver the accepted complex feature through requirements, architecture, a plan, serial
implementation, independent P0/P1 review, local task commits, and final verification.
For feasibility-only requests, inspect and report without entering architecture design or
execution gates. Design, review, and plan-only requests stop at their requested deliverable;
none authorizes implementation or commits.

Use three routine user approval gates: requirements, architecture, and executable plan.
Combine architecture and plan only when no material architecture choice remains or the
user requests fewer checkpoints. Resolve facts from the repository before asking; ask one
material decision at a time using the host's available interaction mechanism. Decide and
record low-risk reversible choices; honor delegated choices without asking again.

Execution requires authorization for both implementation and local task commits.
Resolve missing commit authority before approving an execution plan; if declined, do not
enter the commit loop. After plan approval, do not ask again for each task.
This workflow does not authorize push, base-branch merge, PR changes, deployment,
publication, history rewriting, or branch/worktree deletion.

## Preflight and planning

Read applicable instructions, relevant skills, manifests, and tests. Inspect nearby code,
Git status, branches, worktrees, and relevant history. Pin the feature baseline and required
checks/commit conventions. Preserve unrelated changes; never stage, stash, reset, clean,
overwrite, or move them. Explain why this skill applies. Before promising execution,
confirm implementation and independent-review subagents and safe local commits are available;
otherwise report the capability or authority blocker.

1. Requirements: confirm objective, observable acceptance and evidence, scope/non-goals,
   constraints, compatibility/migrations, and assumptions. Resolve all material questions
   before approval. Obtain the user's confirmation before architecture design, including
   design-only requests. No production edits yet.
2. Architecture: design from existing code. Include material alternatives, boundaries and
   interfaces, data/control flow, and relevant persistence, concurrency, error/recovery,
   compatibility, and verification. Exclude unrelated hardening and generic production
   readiness work. Confirm and freeze the design.
3. Plan: create one Markdown plan in a dedicated temporary directory; report its absolute
   path. For cross-session resumption, use a verified ignored repository-local directory.
   Record accepted requirements/architecture, implementation and commit authority,
   dependency-ordered cohesive tasks, each task's goal, modules, core changes, checks,
   commit boundary, status/hash, and final checks plus aggregate review scope.
   Combine tasks when intermediate commits would be invalid. No estimates, staffing,
   generic risk registers, or release ceremony unless requested. Obtain approval before
   implementation; update statuses, hashes, and evidence as work proceeds.

## Serial task loop

Use a dedicated feature branch; prefer an isolated worktree when safely useful, especially
with unrelated dirty work, concurrent user edits, or invasive changes. Only one task may
mutate the source at a time; noninterfering read-only investigation may run in parallel.
The primary agent integrates and commits. Subagents must not stage, commit, stash,
switch branches, merge, clean, or change Git refs.

For each dependency-ready task:

1. Mark in progress and pin its baseline, goal, boundaries, dependencies and acceptance.
   Spawn an implementation subagent with the task contract, plan, repository path,
   applicable instructions and checks; require implementation/testing without commits.
2. Inspect the full scoped diff, reject unrelated churn, and run focused plus required
   checks. Use a failing regression test first for non-trivial automatable behavior when
   practical; otherwise establish reproducible acceptance before implementation.
3. Self-review, then use a different read-only reviewer. Provide raw baseline/current
   identities, accepted contract, full scoped diff, surrounding code and check evidence,
   not the implementer's conclusions or an intended verdict.
4. Require GO/NO-GO and substantiate every P0/P1. Verify reviewed scope and evidence,
   and unchanged source, index, refs and expected diff. A stale, malformed, incomplete,
   unverifiable, failed-tool, or state-mutating review is invalid, not GO and not a round.
   On reviewer mutation, preserve changes and stop for inspection; never auto-delete them.
5. For a valid NO-GO, reproduce blockers, send confirmed ones to a repair subagent
   (normally the implementer), and make the smallest complete fix. Reject unsupported
   assertions. Re-run checks and review the entire current task diff. Reuse the reviewer
   for continuity unless scope changed materially, a finding is disputed, or state is
   unreliable, in which case use a fresh reviewer.
6. Only the primary agent may commit, after valid GO, all required checks pass, no known
   P0/P1 remains, and staging contains task-owned changes only. Use repository conventions,
   record completed status/hash/evidence, and continue.

Review only changed behavior plus necessary context for correctness, acceptance, data
integrity, compatibility, relevant concurrency, recovery and test adequacy.
P0 is rare catastrophic security/privacy compromise, data loss/corruption, or outage.
P1 is unmet acceptance, major/blocking regression or deterministic crash, unsafe migration,
broken required compatibility, serious reliability failure, or missing critical coverage.
P2 is a bounded edge case, noncritical coverage or maintainability issue; fix only when cheap
and in scope, otherwise retain it as follow-up. P3 is optional style/naming/polish.
Do not block on pre-existing issues, intentional behavior, speculation, style, or unrelated
security/dependency/compliance/performance programs. Each P0/P1 needs a stable ID, location
(or justified cross-cutting scope), evidence/failure path, impact, minimum fix and validation.
GO requires no P0/P1 or other blocking evidence and all required checks passing; it does
not promise absence of undiscovered defects.

After the third valid full review still finds substantiated P0/P1, stop without committing
that task. Preserve current work and earlier commits; report blockers, checks and plan status
and ask the user how to proceed. Never dilute severity or checkpoint-commit to force convergence.

## Final gate and changed scope

After all tasks are committed, run final repository/integration/end-to-end checks. Spawn
a brand-new, read-only reviewer with no inherited conversation context for aggregate review
from feature baseline to current HEAD; never reuse a task reviewer. Supply accepted
contracts, plan, raw diff and actual evidence. Aggregate P0/P1 requires a new remediation
task through the same loop, then another newly spawned clean-context aggregate reviewer.

Pause on material changes to accepted requirements, architecture, compatibility, migration,
risk, authority or result. Explain evidence and the smallest change, return only to the
affected approval gate, update the plan, and resume without reopening settled choices.

If local integration is later requested, use $review-and-merge-branch when available.
Report outcomes, task commits, checks/evidence, resolved blockers and retained P2s,
working-tree state and remote status. Do not claim completion with required failed,
blocked or skipped checks without accepted alternative evidence. Distinguish build,
test, signing, install, runtime/UI acceptance, deployment, publication, merge and push.
