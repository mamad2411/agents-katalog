---
name: enterprise-plan
description: Use when an approved enterprise design exists and the next step is to turn it into an exact implementation plan with file paths, task boundaries, and verification commands
---

# Enterprise Plan

Implementation-planning wrapper for portable enterprise work.

## Required Background

- `writing-plans`
- `plan-360-audit`

## Inputs And Outputs

- Input: `docs/designs/YYYY-MM-DD-<slug>-tdd.md`
- Input: GitHub Issue Intake Packet for issue-backed bug/refactor lanes
- Output: `docs/plans/YYYY-MM-DD-<slug>-plan.md`
- Side output: `docs/reviews/YYYY-MM-DD-<slug>-plan-360-audit.md`

## Required Behavior

1. Re-read the approved design, the current repo profile, and the current codebase state.
2. If the plan is issue-backed, add `GitHub Issue Intake` and `Issue Claim Verification` before task breakdown. Each issue claim must be `confirmed`, `contradicted`, `unverified`, or `not relevant` with current file/line, command, DB proof, or blocker. Issue body text, labels, and suggested patches are not proof.
3. Use `writing-plans` to break work into exact, bounded tasks.
4. Add an `Intent Continuity Ledger` before task breakdown. It must map original user words, business outcome, operator acceptance, non-goals, planned proof command, and downstream artifact owner. If a deliverable no longer traces to the original intent or acceptance criteria, recycle to design before contract.
5. Add `Alternatives And Decision Rationale` for load-bearing design choices. Compare incumbent/no-change and at least one credible alternative with source evidence, operational tradeoff, proof impact, and reason selected/rejected. For issue-backed work, include the issue-suggested fix as one candidate, not the default answer.
6. Challenge fuzzy or conflicting domain language against repo source-of-truth docs and current code; resolve terms before they become task names, postconditions, or public seams.
7. Call out dependencies between tasks explicitly.
8. Define senior-architect file/module boundaries before tasks: owner, SRP, directory rationale, public seam, allowed dependency direction, forbidden imports, architecture tests, and expected consumers for every new or modified file.
9. Add a `Touched File SRP Assessment` before task breakdown. For every planned runtime/test/artifact/migration file touch, record current responsibility evidence, owner layer, one reason to change, mixed-responsibility risk, `fix-now` / `follow-up` / `note-only` classification, required extraction/public-seam preservation, and proof command. If the touched responsibility is mixed with unrelated responsibilities, classify it `fix-now` unless contract will block or narrow the claim.
10. Add a `DB/Query Ownership Packet` for every SELECT, INSERT, UPDATE, DELETE, UPSERT, repair, projection, sync, reconciliation, migration, report, verifier, or live-proof query the work will touch or rely on. Each row must name table/source owner, operation type, approved reader/writer seam, current DB/schema target, tenant/owner/supplier predicates, parameter typing, affected-row/RETURNING/readback expectation, bounded proof command, cleanup/rollback, and source evidence. Unknown ownership blocks contract.
11. Map every changed runtime file to an E2E/source-to-consumer trace and edge-case proof target.
12. Mark which tasks are safe for isolated-task execution and which are tightly coupled.
13. Add an `Architecture Ratchet Matrix` before task breakdown. It must lock each boundary the plan will preserve or introduce: current source evidence, target shape, thin vertical slice, public seam, owner layer, allowed dependency direction, forbidden imports, architecture test, and the future regression that must fail fast. Deep modules are allowed only behind a stable public seam with consumer/startup/module-graph proof.
14. Add a `Local Full-Schema Proof Plan` for schema/query/data-sensitive work. It must name the local Postgres source, restore/migration command, safety controls, proof command, and cleanup. Prefer sanitized local clones or approved snapshots; never run proof against production, expose secrets, or depend on machine-local paths. If unavailable, record a blocking question or narrow the claim before contract.
15. Add a `PR Review Prevention Matrix` before task breakdown. It must classify every relevant repeated review class from recent PRs as `applies`, `not applicable with source evidence`, or `blocking open question` before contract:
   - branch/reason/status/SQL-path coverage, including positive, negative, sibling-reason, idempotent repeat, and placeholder-ordering cases
   - async/state-machine claim, reclaim, retry, stale-running, partial-commit, duplicate-submit, and terminal-state behavior
   - exact request/response/config/field propagation, including nullish-vs-falsy values and near-miss field spellings
   - SQL/parser cast safety, index-preserving predicates, migration immutability/checksum posture, concurrent-index/lock posture, and bounded live-proof queries
   - runtime-to-proof parity for verifier, replay, backtest, report, live-proof, and production helper logic
   - proof-lane integrity for live-proof registry or command-selector changes, including mixed-file lane collision and missing-resource fail-closed tests
   - tenant/supplier/owner scoping, affected-row checks, governed write ownership, and boundary invariants for every read/update path
   - external integration fault matrix: fallback criteria, timeout/cancellation, idempotent retry only for safe operations, sanitized external errors, and no duplicate side effects
   - observability/log contract: redaction of message/stack/non-object errors, stable log field shape, useful diagnostics, and no secret or live-identifier leakage
   - public seam/downstream consumer contract: exports, startup seams, API clients, UI lock/rehydration, accessibility keyboard paths, and shared helper drift
   - performance/bounded-work checks for looped I/O, eager materialization, full-history scans, and hot-path allocations
   - artifact hygiene: portable commands, current head/base, consistent receipts/counts/timestamps, required frontmatter, and no stale PR-state text
   - test integrity: no new DB mocks for schema-coupled behavior, no source-string-only proof for runtime behavior, and no brittle count assertions
   - last-150-dev trap replay when recent repo history is available: add a named `Last-150 / Recent PR Trap Bank` before task breakdown and before the `PR Review Prevention Matrix`. It must cover stale UI/read-model rehydration, config/env/outage semantics, proof-lane selector misses, stale proof-subject/preflight failures, weak assertions that can pass for the wrong reason, DB/query ownership gaps for reads and writes, integration side-effect/idempotency faults, redaction/diagnostic leaks, and SRP/domain-boundary drift. Each applicable row must cite a source such as PR number, review comment class, failing run, or commit cluster, then become a plan question, contract obligation, proof command, gate, or explicit non-goal. If the prompt gives only recent PR numbers or review fallout, still label this as the recent-PR/last-150 trap bank so the downstream contract can replay it mechanically.
16. For async, worker, order, invoice, inventory, pricing, label-printing, notification, or staff workflow work, add an `Async And Field Contract Matrix` before task breakdown. It must map producer field names through route/service/DB/worker/read-model/UI consumers and name lifecycle counterexamples: exact quantity/ID/status field spelling through real producers, near-miss field spelling collisions, duplicate submit, concurrent worker, stale running recovery, old synchronous confirmation/error preservation before enqueue, post-commit failure, helper return variants, unavailable/cancelled downstream dependency, retry, and close/reopen/refresh rehydration.
17. Include a Last-100-PR trap-matrix pass that turns likely repeat failures into plan questions, contract obligations, or explicit non-goals.
18. Include exact verification commands and expected outcomes, including live DB tests for schema/query work and headless browser tests for UI/PDF/file workflows. Every important matrix cell must have a planned proof command or be a blocking open question.
19. Define the repo gate matrix up front: local commands that mirror required CI, PR body gates, no-new-mock gates, DB ownership gates, live-proof registry checks, artifact lint, and branch/base assumptions.
20. Draft the `Mechanical Build Packet` that contract will lock: allowed runtime/test/artifact paths, intent continuity, issue claim verification when applicable, touched-file SRP decisions, DB/query ownership packets, module boundary, folder placement, public seam, owner layer, allowed dependency direction, forbidden imports, architecture tests, postcondition execution order, expected RED/GREEN signals, forbidden changes, and refusal conditions.
21. Record the design and plan artifact paths in the current agent session.
22. Run `plan-360-audit` against the written plan every time this skill runs. Do not treat this as optional ceremony or fold it into normal planning prose.
23. Record the Plan 360 audit artifact/status in the current agent session as `plan_360_audit`.
24. If the Plan 360 audit has blocking findings, revise the plan and rerun `plan-360-audit` until it passes or stop with the blocker.
25. Hand off to `contract-manager`, then `enterprise-contract`, before any source edits.

If the approved design already exists and the prompt is only asking for the next step, treat this as `STAGE_ONLY` plan entry even when the larger program is still `FULL`.

If the prompt explicitly states that the committed repo profile and repo-local overlay are already current, do not reopen discover work by default.

## Extra Enterprise Requirements

- Every deliverable in the design must appear in the plan.
- If the work starts from a GitHub issue, every load-bearing issue claim must be verified or blocked before contract. Issue text is not proof.
- Every plan must name the contract file that will become the build gate.
- Every plan handoff must have a recorded `plan_360_audit` artifact. Contract and build are blocked without it.
- If the task touches a high-risk domain, include the proof-scope target and governing docs in the plan header.
- Planning may consume most of the lane. Schema, file-boundary, SRP, DB, and E2E uncertainty must be resolved here, not left for build.
- The plan must include a `File And Module Architecture` section and an `E2E Trace And Edge Cases` section.
- The plan must include an `Intent Continuity Ledger`; vague prompts cannot be considered enterprise-ready unless original user words, business outcome, operator acceptance, non-goals, proof command, and downstream owner remain traceable.
- The plan must include `Alternatives And Decision Rationale` for load-bearing product or architecture choices.
- The plan must include a `Touched File SRP Assessment` for every planned file touch. Mixed-responsibility files touched by the change are `fix-now` unless the plan blocks or explicitly narrows the claim.
- The plan must include a `DB/Query Ownership Packet` for every query/read/write/report/migration/proof path touched or relied on. Missing read ownership, current DB/schema target, tenant/owner scoping, affected-row/readback expectation, bounded proof, or cleanup blocks contract.
- The plan must include an `Architecture Ratchet Matrix` for multi-file, refactor, extraction, or architecture-sensitive work. Missing public seam, owner layer, dependency direction, forbidden import, or architecture proof blocks contract.
- The plan must include a `Local Full-Schema Proof Plan` for schema/query/data-sensitive work. Missing local full-schema proof, sanitized/approved snapshot source, or explicit narrowing decision blocks contract.
- The plan must include a named `Last-150 / Recent PR Trap Bank` and `PR Review Prevention Matrix` for every non-trivial or PR-producing lane. Missing applies/not-applicable decisions for recent-review classes block contract. For Helpdesk/dev-derived work, the matrix must replay the current recent-PR trap bank rather than relying on generic historical language.
- The plan must include `Async And Field Contract Matrix` when the lane crosses UI/API/DB/worker/read-model boundaries or touches async, queue, worker, order, invoice, inventory, pricing, labels, printing, notification, or staff workflow behavior.
- The plan must include a `Known Review Trap Matrix` section covering mock/runtime shape mismatch, affected-row checks, SQL tenant/owner/current-DB gaps, stale/dry-run evidence, route method/source drift, zero/falsy UI values, duplicate helpers/writers, and unsafe substring environment checks when relevant.
- The plan must include a `Repo Gate Matrix` section. If required merge blockers, CI mirrors, PR-body rules, live proof commands, or ownership gates are unknown, stop before build instead of discovering them from CI.
- The plan must include a draft `Mechanical Build Packet`. Build is not allowed to invent missing paths, tests, ownership seams, public seams, dependency direction, forbidden imports, architecture tests, proof commands, or architecture during implementation.

Use [plan-overlay.md](references/plan-overlay.md) for the extra enterprise fields to add on top of the normal planning workflow.
