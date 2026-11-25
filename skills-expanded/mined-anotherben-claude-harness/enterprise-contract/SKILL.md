---
name: enterprise-contract
description: Use when an enterprise implementation plan exists and work needs a locked contract with postconditions, invariants, consumer mapping, and traceability before build starts
---

# Enterprise Contract

The contract is the build gate. No enterprise build starts without it.

## Required Background

- `contract-manager`

## Inputs And Outputs

- Input: `docs/plans/YYYY-MM-DD-<slug>-plan.md`
- Input: GitHub Issue Intake and Issue Claim Verification sections when the plan is issue-backed
- Input: recorded Plan 360 audit artifact/status (`plan_360_audit`)
- Output: `docs/contracts/YYYY-MM-DD-<slug>-contract.md`
- Side output: `.codex/enterprise-state/agent-sessions/<agent-id>-<slug>-postconditions.json`
- Side output: recorded contract-manager review artifact/status (`contract_review`)
- Side output: recorded mechanical build packet artifact/status (`build_packet`)

## Entry Gate

Before locking or editing the contract, the current agent session must already record the plan artifact and the Plan 360 audit artifact/status as `plan_360_audit`. Use the agent stage gate in [agent-stage-gates.md](../enterprise/references/agent-stage-gates.md) before proceeding.

Run `contract-manager` against the plan, the Plan 360 findings, and the relevant current code/DB evidence before locking this contract. Record its artifact/status in the current agent session as `contract_review`.

Any blocking `contract-manager` finding recycles back into the plan or contract draft before `LOCKED`. Do not downgrade it to advisory unless the review explicitly classifies it non-blocking with rationale.

Contract work may consume most of the lane. Do not lock while current code, real DB schema/query behavior, file boundaries, SRP, E2E trace, or edge cases remain unclear.
Do not lock while domain terms, public-seam names, or operator-facing workflow
words conflict with repo source-of-truth docs or current code behavior.

## Source And Database Grounding Gate

- Read the current implementation and consumers before writing postconditions. A contract based only on a migration, git diff, branch name, or plan prose is invalid.
- For issue-backed work, every load-bearing GitHub issue claim must be `confirmed`, `contradicted`, `not relevant`, or blocked/narrowed before `LOCKED`. A contract based on issue body text, labels, production-log excerpts, or a suggested patch without current source/runtime proof is invalid.
- For schema/query/data-sensitive work, inspect real migrated Postgres or a live/dev DB surface before locking. This happens before postconditions are trusted, not after build.
- For schema/query/data-sensitive work, prefer local full-schema Postgres proof before PR: sanitized clone, approved snapshot, or schema-only restore with representative fixtures. Raw live data is allowed only with explicit approval, least-privilege local use, no production writes, no printed secrets, no repo dumps, and cleanup/reset instructions.
- Every schema/query/data-sensitive postcondition must name a live DB or real integration test. Mocked database tests do not count.
- Every cross-layer DTO/projection/print-payload/notification/read-model postcondition must name exact runtime field names and aliases from producer to consumer. Mocked responses cannot stand in for the changed producer.
- If live DB proof is unavailable, lock is blocked unless the user explicitly narrows the claim away from schema/query behavior.
- For UI, PDF upload, invoice upload, file upload, preview/download, modal, navigation, or rendered-output behavior, the contract must name headless browser proof.
- For owned-table or governed write paths, name the ownership seam and the DB ownership gate command. Direct writes in mixed-owner files are contract failures unless explicitly allowed.
- For every query/read/report/verifier/live-proof path, name the approved reader ownership seam and source-of-truth owner. Read ownership is required even when no write occurs.
- For every DB operation, lock a `DB/Query Ownership Packet` with table/source owner, operation type, current DB/schema target, tenant/owner/supplier predicates, parameter typing, affected-row/RETURNING/readback expectation, bounded proof command, cleanup/rollback, and secret/redaction controls.
- For every plan `Architecture Ratchet Matrix` row, the contract must preserve or lock the boundary as a postcondition, invariant, architecture test, or explicit non-goal before `LOCKED`. It is not enough to say build will keep the file structure clean.
- For every plan `Touched File SRP Assessment` row, the contract must preserve the classification. `fix-now` rows become postconditions plus architecture tests; `follow-up` rows become explicit non-goals with blast-radius evidence; `note-only` rows require source evidence that the touched responsibility is not mixed with unrelated responsibilities.
- For every plan `Intent Continuity Ledger` row, the contract must lock a postcondition, invariant, proof command, or explicit non-goal that preserves the original user words, business outcome, and operator acceptance.
- For every plan `Issue Claim Verification` row marked `confirmed`, the contract must lock a postcondition, invariant, proof command, or explicit non-goal. `Contradicted` rows must become non-goals or plan corrections. `Unverified` rows block `LOCKED` unless the claim is explicitly narrowed out of scope.
- For every plan `Local Full-Schema Proof Plan`, the contract must name the DB source, restore/migration command, proof command, safety controls, and cleanup, or block/narrow the claim before `LOCKED`.
- For every plan `PR Review Prevention Matrix` row marked `applies`, the contract must convert it into a postcondition, invariant, error case, proof command, or explicit non-goal before `LOCKED`. It is not enough to say review/forge will check it later.
- For every plan `last-150-dev trap replay` row marked `applies`, the contract must lock the concrete prevention target before `LOCKED`: stale UI/read-model rehydration tests, config/env/outage-state tests, proof-lane selector negative tests, stale proof-subject/preflight checks, weak-assertion hardening, DB/query ownership proof for reads and writes, integration idempotency/fault proof, redaction/diagnostic proof, or SRP/domain-boundary ratchets. If the row is not applicable, the contract must keep the source-evidenced reason; if it is a blocking open question, the contract remains `DRAFT`.

## Runtime Shape Proof Gate

Contracts must prove the runtime shape they rely on before `LOCKED`.

- Every mocked dependency must name the real producer or consumer path/symbol and the exact fields, aliases, types, and null/falsy values it returns.
- Every route or scenario catalog entry must be checked against the mounted route source and HTTP method, not a guessed URL.
- Every service-result, query-result, event payload, evidence artifact, and helper input shape must match the current runtime source or live/integration proof.
- If a mock, fixture, contract example, or plan table invents a shape that cannot be traced to current code, the contract remains `DRAFT`.
- If the work touches async, queue, worker, order, invoice, inventory, pricing, labels, printing, notification, or staff workflow state, the contract must include lifecycle postconditions for exact field spelling through real producers, duplicate submit/concurrent worker, stale running recovery, old synchronous confirmation/error preservation before enqueue, post-commit bookkeeping failure, helper return variants, unavailable/cancelled downstream dependencies, retry behavior, and close/reopen/refresh state rehydration unless explicitly not applicable with source evidence.
- If the work touches external integrations, logging, security-sensitive errors, proof infrastructure, verifier/replay/backtest/reporting code, config parsing, tenant/supplier/owner boundaries, migrations, indexed predicates, custom UI controls, navigation, or repo artifacts, the contract must include the matching review-prevention postconditions: fallback and retry criteria, timeout/cancellation behavior, idempotency, secret-redaction corpus, stable log shape, proof-lane collision tests, runtime-to-proof parity, malformed/nullish/falsy input handling, ownership/scoping invariants, migration immutability and rollout posture, indexability/query-plan proof, keyboard/focus interaction matrix, and artifact hygiene/redaction checks.
- Review must fail any contract that proves behavior against invented JSON strings, wrong quantity fields, wrong aliases, missing current-DB/tenant filters, or route methods that do not exist.

## Required Sections

Use [contract-template.md](references/contract-template.md) as the starting shape.

- status header: `DRAFT` then `LOCKED`
- preconditions
- postconditions by layer
- invariants
- error cases
- consumer map
- file and module architecture
- intent continuity ledger
- GitHub issue intake and issue claim verification when applicable
- alternatives and decision rationale
- touched file SRP assessment
- DB/query ownership packet
- architecture ratchet matrix
- E2E trace and edge cases
- repo gate matrix
- live proof artifact plan
- local full-schema proof plan when applicable
- PR review prevention matrix
- runtime shape proof
- mechanical build packet
- blast radius
- side effects
- async and field contract matrix when applicable
- full-proof gate: partial proof is failure
- artifact hygiene and evidence coherence gate
- explicit non-goals
- traceability matrix

## Lock Rules

Do not mark the contract `LOCKED` until the quality gate in [quality-gate.md](references/quality-gate.md) passes and the recorded `contract_review` has no blocking findings.

Once locked:

- build cannot invent new scope silently
- every new forge bug becomes an appended postcondition
- proof claims must trace back to this contract
- local CI mirrors, PR-body requirements, no-new-mock checks, DB ownership gates, and live-proof commands must be named before source edits continue
- the current agent session must record the locked contract, the `contract_review`, the `build_packet`, and the session-scoped postconditions file

## Mechanical Build Packet

Before `LOCKED`, include a build packet that makes implementation mechanical.
The packet can live inside the contract or in a separate artifact, but the agent
session must record it as `build_packet=<path>`.

Required packet fields:

- `Allowed Runtime Paths`: exact source files build may edit.
- `Allowed Test Paths`: exact test files build may create or edit.
- `Allowed Artifact Paths`: docs/state artifacts build may update.
- `Intent Continuity Ledger`: exact original-intent rows build and verify must preserve.
- `Touched File SRP Assessment`: exact SRP classification and `fix-now` extraction/public-seam action for every path build may touch.
- `DB/Query Ownership Packet`: exact reader/writer owner seam, table/source owner, scoping, bounded proof, and cleanup for every DB/query path build may touch or rely on.
- `Module Boundary`: exact module/layer boundary this work may touch.
- `Folder Placement`: exact directory/file placement and why it belongs there.
- `Public Seam`: exact export, route, component, hook, worker, or command consumers use.
- `Owner Layer`: exact owner layer/responsibility for each changed path.
- `Allowed Dependency Direction`: exact import/call direction that remains legal.
- `Forbidden Imports`: exact import paths/modules/layer crossings build must not add.
- `Architecture Tests`: exact module-graph, startup-seam, seam-load, or equivalent tests and commands.
- `Postcondition Execution Order`: one postcondition per RED/GREEN loop.
- `Expected RED`: command and failure signal before implementation.
- `Expected GREEN`: command and pass signal after implementation.
- `Required Commands`: focused, gate, live DB, and headless commands build must run or stage.
- `Required Commands` must include commands for every applicable PR Review Prevention Matrix cell: branch/reason, async/state, field/config, SQL/cast/index/migration, runtime-to-proof parity, proof-lane, scoping, integration fault, redaction/observability, public seam/UI/accessibility, performance/bounded-work, artifact hygiene, and test-integrity proof.
- `Required Commands` must include architecture ratchet proof for every changed boundary and local full-schema Postgres proof for schema/query/data-sensitive work, unless the contract has structured not-applicable proof with applicability predicate/source evidence/non-DB scope or explicit claim narrowing.
- `Forbidden Changes`: files, helpers, writers, schemas, routes, flags, or behaviors build must not touch.
- `Refusal Conditions`: missing owner, missing path, missing test, missing intent row, missing SRP/refactor classification, missing DB/query ownership packet, schema uncertainty, UI proof gap, new architecture decision, or any need to widen scope.

If build would need to choose paths, invent tests, decide architecture, add an
unlisted helper/writer, or change ownership, the contract is not ready for build.

## High-Risk Domain Rule

If the task touches money, auth, regulated data, external integrations, or any end-to-end hardening claim, run the checks in [high-risk-domain-gate.md](references/high-risk-domain-gate.md) before locking the contract.

## Fail-Closed Rules

- No vague postconditions
- No contract lock without a recorded passing `plan_360_audit`
- No contract lock or build handoff without a recorded `contract_review`
- No contract lock or build handoff without a recorded `build_packet`
- No unmapped consumers for changed outputs
- No unpreserved original-intent row for a vague/product-shaped request
- No issue-backed contract whose load-bearing issue claims remain unverified or only supported by issue prose
- No touched file without a source-backed SRP/refactor classification
- No mixed-responsibility touched file left as `follow-up` without a blocking reason, narrowed claim, and explicit non-goal
- No DB/query path, including SELECT/report/verifier/live-proof reads, without an ownership packet and bounded proof/readback plan
- No uncontracted applicable PR Review Prevention Matrix cell
- No uncontracted applicable last-150-dev trap replay cell when recent PR/review/check evidence exists for the lane
- No unlocked architecture ratchet for changed boundaries, deep modules, public seams, dependency direction, forbidden imports, or architecture tests
- No schema/query/data-sensitive contract without local full-schema proof plan or explicit blocking/narrowing decision
- No unowned blast-radius findings
- No unknown merge blocker, PR gate, no-new-mock gate, DB ownership gate, or live-proof command
- No `full-system` claim unless the contract truly covers all required legs
- No `LOCKED` contract that allows `PARTIALLY PROVED` to pass; partial proof is a failed gate and must recycle to plan/contract or remain blocked
