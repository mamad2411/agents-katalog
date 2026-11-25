---
name: enterprise-build
description: Use when a locked enterprise contract and mechanical build packet exist and implementation must proceed through strict TDD, contract traceability, receipt-only progress, and staged review handoffs. Always use this for enterprise build-stage work; stop if the complete build body is unavailable.
---

# Enterprise Build

Contract-driven implementation for portable enterprise work.

This complete body is the build skill. If an invocation lacks these full
instructions or appears stale, stop before editing and load the complete body
from `/Users/ben/.agent-platform/skills/enterprise-build/SKILL.md`.
Do not proceed from incomplete build instructions.

During build the proof verdict is always `not-yet-claiming`, and any enterprise completion, PR-ready, merge-ready, or safe-to-merge claim remains fail-closed until later review, forge, verify, and ship gates pass on the current final diff.

Build is mechanical execution from a locked job card. It must not discover
requirements, choose architecture, widen ownership, invent proof, or decide new
paths. If the packet is incomplete, build stops and recycles to plan/contract.

## Required Background

- `test-driven-development`
- `subagent-driven-development` when the plan has safe isolated tasks

## Entry Gate

Before reading the build packet body or any downstream artifacts, run:

```bash
enterprise-precheck --skill enterprise-build
```

If it exits non-zero, stop and report stderr verbatim. Do not hand-craft packet
files, receipt logs, postcondition registries, or evidence markers to bypass it.

Before editing source files, confirm:

- the current agent session recorded the plan
- the current agent session recorded the contract
- the current agent session recorded the `build_packet`
- the recorded contract status is `LOCKED`
- the `build_packet` passes the mechanical packet check in the stage gate
- the loaded skill body is this complete enterprise-build body
- every path about to be touched passes `enterprise-containment --repo-root "$PWD" --agent-id <agent-id> --path <file>`
- every behavior about to be implemented maps to a locked `Intent Continuity
  Ledger` row with original user words, business outcome, operator acceptance,
  non-goals, and proof command
- when the lane is issue-backed, every behavior about to be implemented maps to a
  locked `Issue Claim Verification` row and contract item; issue body text or a
  suggested patch is not build authority
- every path about to be touched has a source-backed `Touched File SRP Assessment`
  in the packet, including required `fix-now` actions for mixed-responsibility files
- every query/read/write/report/migration/proof path build will touch or rely on
  has a `DB/Query Ownership Packet`, including reads and bounded proof/readback

If any of those are missing, stop and go back upstream.

## Required Workflow

1. Read the locked contract, the mechanical build packet, the implementation plan, and the current repo profile.
2. Run the agent-bound build gate in [agent-stage-gates.md](../enterprise/references/agent-stage-gates.md) before editing source files.
3. Run the pre-edit authority scan before adding new code.
4. Execute only the packet's `Postcondition Execution Order`.
5. Before touching each runtime, test, artifact, or migration path, run `enterprise-containment --repo-root "$PWD" --agent-id <agent-id> --path <file>` and stop if the path is not covered by the locked packet.
6. Before implementing each behavior, execute its `Intent Continuity Ledger` row:
   preserve the original user words, business outcome, operator acceptance, and
   non-goals, and stop if the implementation would satisfy only a generic task
   while losing the operator-facing intent.
7. For issue-backed work, execute only `Issue Claim Verification` rows that the
   contract converted into postconditions, invariants, or explicit non-goals.
   Stop if an issue claim is still unverified or contradicted without a contract
   correction.
8. Before touching each file, execute its `Touched File SRP Assessment`: preserve the owner layer and public seam, perform contracted `fix-now` extraction/refactor work, and stop if the file is mixed-responsibility but the packet lacks a `fix-now`, blocked, or narrowed classification.
9. Before adding, changing, or relying on any DB query, execute its `DB/Query Ownership Packet`: use the approved reader/writer seam, preserve tenant/owner/current-DB predicates, prove affected-row/readback behavior, keep proof bounded, and run cleanup/rollback steps when required.
10. For each postcondition, run the packet's `Expected RED`, make the smallest allowed edit, then run the packet's `Expected GREEN`.
11. Record progress and command receipts in the build status model from [build-status-tracking.md](references/build-status-tracking.md). RED/GREEN receipts must use the harness receipt fields (`receipt_id`, `command_status`, `proof_type`, `test_file`, `test_name`, `output_sha256`, `head_sha`, `head_sha_after`, `base_sha` when PR-scoped, and artifact/log paths).
12. Validate postcondition state transitions with `python3 scripts/validate_postcondition_transitions.py --status-file <path> --receipt-log <path>` before handoff. `verified` is not a build-produced state.
13. Record build-stage handoff data before review with exact artifact keys:

```bash
enterprise-agent-session record-stage --repo-root "$PWD" --agent-id <agent-id> --stage build --artifact build_packet=<path> --artifact postconditions=<path> --artifact command_receipts=<path>
```

14. Do not add scope, files, helpers, writers, commands, or proof that are not in the contract/build packet.
15. Run or stage the repo gate commands named by the contract/build packet as soon as their prerequisites exist, not only after PR creation.
16. For async, worker, order, invoice, inventory, pricing, label-printing, notification, or staff workflow postconditions, run the field/lifecycle counterexample commands as soon as each seam exists. Do not defer exact field-spelling proof, duplicate-submit, concurrent-worker, stale-running, old synchronous confirmation/error preservation, post-commit failure, helper return variant, unavailable dependency, retry, or rehydration proof to final verify.
17. For every newly introduced mode flag, reason string, structured code, SQL branch, or recovery branch, add targeted RED/GREEN proof for positive, negative, sibling-reason, and idempotent repeat behavior before continuing.
18. For every SQL/parser cast from JSON, text, or external IDs, prove malformed, empty, and out-of-range values are guarded before the cast, and prove indexed predicates remain indexable or are explicitly accepted by the contract.
19. For every live-proof registry, verification command, CI mirror, or proof-lane selector touched during build, add negative proof that the command fails when its asserted runtime resource is absent and that mixed generic/domain diffs select the domain-specific lane.
20. For every verifier/replay/backtest/report/live-proof path, prove parity with production helpers or equivalent predicates and truth conditions.
21. For every external integration, prove the contracted fault matrix: fallback eligibility, timeout/cancellation, idempotent retry boundaries, sanitized errors, and no duplicate side effects.
22. For every tenant/supplier/owner/identifier/upsert/default-change path, prove boundary invariants, affected-row behavior, omitted/nullish/falsy value handling, and rollout/default preservation.
23. For every logging, error, diagnostic, public seam, API client, custom UI control, navigation, or artifact change, run the contracted redaction, consumer, accessibility, artifact-hygiene, and test-integrity commands.
24. For every changed boundary, deep module, extraction, or helper layer, run the contracted architecture ratchet command and prove the public seam, owner layer, dependency direction, forbidden imports, and future regression trap.
25. For every schema/query/data-sensitive path, run the contracted local full-schema Postgres proof or stop on the recorded blocker/narrowed claim before PR-ready evidence is written.
26. Build artifacts and command receipts must be portable: do not commit workstation-local command prefixes, home-directory paths, `PATH=...`, `NODE_PATH=...`, stale pending checklists, or PR-creation leftovers as proof.
27. Hand off to `enterprise-review` after each meaningful task boundary or after the whole build, depending on the path size.

## Last-150 PR Trap Replay Execution

When the build packet contains PR Review Prevention Matrix, Known Review Trap Matrix, or last-150-dev trap replay rows, build must execute them as implementation work, not leave them for reviewers. For each applicable row:

- create or update the RED/GREEN proof named by the contract
- prefer a deterministic ratchet, focused regression test, live-proof selector test, local full-schema proof, or headless workflow proof over prose evidence
- include negative cases for missing resources, stale proof subjects, wrong route/method, wrong head/base, unlinked/degraded integration state, zero/null/false values, and weak assertions that can pass for the wrong reason
- preserve SRP/refactor-as-you-touch and domain ownership while adding the trap; do not patch only the consumer if the invariant belongs in a domain owner, repository, policy module, or public seam
- record receipt-backed evidence for the trap before marking the related postcondition green
- in the build verdict/output, explicitly state that applicable trap rows are build implementation work, not reviewer-only notes, prose evidence, or deferred cleanup

If the packet names a recent trap class but not its RED/GREEN command, stop and recycle to contract. Build cannot invent the missing prevention path.

## Mechanical Build Packet Rules

The packet is the build authority. It must include `Allowed Runtime Paths`,
`Allowed Test Paths`, `Allowed Artifact Paths`, `Module Boundary`,
`Folder Placement`, `Public Seam`, `Owner Layer`, `Allowed Dependency Direction`,
`Touched File SRP Assessment`, `DB/Query Ownership Packet`, `Forbidden Imports`,
`Architecture Tests`, `Postcondition Execution Order`, `Expected RED`,
`Expected GREEN`, `Required Commands`, `Forbidden Changes`, and `Refusal Conditions`.

Build may only:

- edit paths listed in `Allowed Runtime Paths`, `Allowed Test Paths`, or `Allowed Artifact Paths`
- implement the next postcondition in the listed order
- implement only behavior that traces to the packet's `Intent Continuity Ledger`
  or an explicit contract non-goal
- implement issue-backed behavior only when the issue claim is confirmed and
  converted into a contract item; issue prose alone is not authority
- execute the packet's touched-file SRP/refactor action before adding new behavior
  to mixed-responsibility files
- use only the approved reader/writer/query owner seams named by the DB/Query
  Ownership Packet
- use helpers, writers, routes, schemas, flags, and commands named by the packet
- preserve the packet's owner layer, public seam, dependency direction, forbidden imports, and architecture-test contract
- record receipts for commands it actually ran
- record `green` only from actually run PASS receipts, never from commands that are merely staged, queued, planned, headless-ready, delegated, or expected to pass in CI

`QUICK` is not a shortcut around build semantics. Canonical build accepts a
`QUICK` lane only when the current agent session records
`path_classification=QUICK`, a locked quick contract, and a mechanical
`build_packet`. Helpdesk's repo overlay may choose QUICK from its runtime card,
but once it invokes canonical `enterprise-build`, this skill still requires
contracted containment, actual RED/GREEN receipts, transition validation, and a
build-stage handoff. QUICK only skips the full non-QUICK plan/audit/contract
chain; it never permits freehand edits, missing packet fields, prose-only proof,
or GREEN from staged commands.

Build must stop and recycle to contract when:

- a needed file, test, helper, writer, schema, route, owner, command, DB proof, or headless proof is not named
- a behavior lacks an Intent Continuity Ledger row, or the build would satisfy a
  generic implementation task while losing original operator acceptance or non-goals
- an issue-backed behavior lacks a confirmed Issue Claim Verification row and
  contract item
- a touched file lacks an SRP assessment, or a mixed-responsibility touched file
  lacks a contracted `fix-now`, blocker, or narrowed claim
- a DB/query path lacks an ownership packet, including read-only SELECT/report/
  verifier/live-proof queries
- `enterprise-containment --path <file>` fails for any path that build would touch
- the RED signal does not fail for the packet's stated reason
- the GREEN command cannot prove the stated postcondition
- the GREEN command was not actually run and receipt-backed on the current head
- the available proof would be `PARTIALLY PROVED`, mock-only, stale, wrong-head, or missing an important lifecycle/field matrix cell
- branch/reason-set, cast/range, runtime-proof parity, proof-lane, integration fault, boundary invariant, architecture ratchet, local full-schema, observability/redaction, public seam/UI/accessibility, artifact-portability, test-integrity, or bounded live-proof coverage is needed but not named by the packet
- an implementation choice requires architecture, ownership, scope, route, schema, or public API judgment
- a code pivot would invalidate review/forge evidence already recorded
- a current recent-PR trap class applies but has no contracted ratchet, proof command, or explicit non-goal

Build output is receipts, not claims: changed paths, postcondition id, command,
mode, exit status, `receipt_id`, `command_status`, `proof_type`, `test_file`,
`test_name`, `output_sha256`, current/base/head-after fields, artifact/log path,
and any blocker or recycle reason.
Build cannot call work ready, safe, complete, mergeable, verified, or done.

## Pre-Edit Authority Scan

Before source edits, search for existing owners and record reuse versus new-code rationale in the build artifact.

- Search existing helpers before adding money, date/month, quantity/count, status, route/catalog, evidence, tenant, or environment logic.
- Search existing writers before adding any DB write, repair, projection, sync, reconciliation, or state-transition path.
- Search existing readers/repositories before adding any SELECT, report, verifier, live-proof, projection, or dashboard query. Reads must use the owned source-of-truth seam unless the locked DB/Query Ownership Packet authorizes a new reader.
- If a second helper or writer is still needed, name the old owner, new owner, transaction boundary, rollback behavior, and consumer split.
- Do not add an independent writer beside an existing convergence/gatekeeper path unless the locked contract explicitly authorizes that authority change.
- Review treats an undocumented duplicate helper/writer as a build defect, not a cleanup preference.

For schema/query/data-sensitive work, the first relevant RED test must be live DB or real integration proof against migrated Postgres. Mocked DB tests may supplement behavior coverage but do not satisfy schema/query proof.

For UI, PDF upload, file upload, preview/download, modal, navigation, or rendered-output work, build must leave a headless browser command ready for review/verify.

For repos with no-new-mock or DB ownership gates, build must keep the diff compliant while coding. Do not introduce new inline DB mocks for schema/query proof, and do not route writes through mixed-owner direct-write files unless the locked contract explicitly owns that seam.

If the locked contract already exists and the prompt asks for the next step, classify the transition as `STAGE_ONLY` build entry rather than re-triaging the whole program.

If the prompt explicitly states that the committed repo profile and repo-local overlay are already current, do not reopen discover work by default.

## Rules

- One `RED` -> one `GREEN`
- Source-string tests, fixture-only tests, and hard-coded mocked responses cannot be the primary proof for runtime behavior, worker behavior, DB writes, print payloads, notifications, or UI lock state
- Build in tracer bullets: one observable behavior, one failing test, one minimal
  implementation. Do not write all tests first and then all code.
- The test must fail for the right reason before code is added
- Contract amendments only happen through the forge recycle loop
- If a planned task is independent, isolated-task execution is preferred over one large mixed diff
- For bounded work, keep build-status notes terse and leave enough runway for review and verification in the same session
- CI-driven code pivots invalidate previous review/forge coverage for the affected files. Re-run review/forge on the current diff after the pivot.
- Avoid brittle assertions on volatile implementation constants. Idempotence, ranking, tuning, heuristic, or generated-score tests should prove invariant behavior, state transitions, and no-ratchet stability unless the exact number is a locked business rule.
