---
name: enterprise-verify
description: Use when enterprise work is about to be declared complete and the claim needs fresh evidence, postcondition tracing, and an explicit proof-scope verdict
---

# Enterprise Verify

Final evidence gate for enterprise work.

## Mandatory Closure Gates

Verification fails closed unless all three gates are satisfied in the report.

### Contract Clause Coverage

Every explicit contract, TDD, plan, and postcondition clause must have a coverage
row with clause id/text, exact source evidence, executable assertion or test
evidence, runtime/browser/live proof or structured not-applicable reason,
current head SHA, and verdict. A PC-level PASS, suite-level PASS, or prose
summary is not enough. A receipt is usable only when it names the command/log,
current head, clause or surface it proves, and exercised runtime path. Missing
source, assertion, or runtime proof for a non-N/A clause makes the verification
verdict `UNPROVED`.

### Proof Subject Integrity And Freshness

The report must inventory final HEAD, target/base branch or SHA, PR head when
relevant, review artifact head, forge artifact head, verify artifact head, gate
summary head, receipt heads, browser proof heads, and runtime provenance/deploy
source. Every item must refer to the same final diff and target. Any mismatch,
unknown head, stale pre-pivot artifact, or runtime proof from a different
deploy/source fails verification.

### Runtime Route And Surface Inventory

For async, worker, UI, API, and integration work, verification must list every
claimed route, event, queue transition, terminal branch, readiness endpoint,
health endpoint, runtime volume/dependency check, and data-semantic path. Each
surface is marked `PROVED`, `NOT PROVED`, or structured `N/A` with command or
artifact evidence. A full workflow or full-system claim based on a subset fails
verification, and the proof-scope verdict must be no broader than the proved
rows. For browser-worker-style lanes, inventory must include accept response
metadata (`runId`, BullMQ queue id, worker identity, and `readinessSnapshot`),
backwards-compatible health routes including `/api/health`, terminal worker
branches, disk/data volume readiness, and claimed scrape/data semantics.

## Required Background

- `verification-before-completion`

## Required Workflow

1. Run the agent-bound verify gate in [agent-stage-gates.md](../enterprise/references/agent-stage-gates.md) before accepting stage entry.
2. Run the full relevant verification commands now, not from memory.
3. Build the contract clause coverage matrix before accepting any PC-level
   result as proof.
4. Build the proof subject integrity/freshness inventory and fail on head/base/
   runtime drift.
5. Build the runtime route/surface inventory for async, worker, UI, API, and
   integration claims.
6. Confirm the recorded `build_packet` exists, passes the mechanical packet gate and architecture contract gate, and covers every changed source, test, artifact, intent-continuity row, touched-file SRP classification, DB/query ownership packet, module boundary, folder placement, public seam, dependency direction, forbidden import, and architecture test path.
7. Classify the final diff as `required`, `enabling`, or `drift`.
8. Verify the Intent Continuity Ledger: original user words, business outcome,
   operator acceptance, non-goals, and proof command must all match the final
   diff and reported verdict.
9. Map every changed runtime file to code-level execution proof.
10. Verify the Touched File SRP Assessment for every changed file: `fix-now`
   refactors are implemented and proven, `follow-up` rows are explicit non-goals
   with blast-radius evidence, and `note-only` rows have source evidence.
11. Trace every cross-layer behavior source-to-consumer, including edge cases from plan/contract.
12. Require live DB proof and local full-schema Postgres proof for schema/query/data claims, unless the contract recorded structured not-applicable proof with applicability predicate/source evidence/non-DB scope or narrowed claim; require headless browser proof for UI/PDF/file/upload/rendered workflows.
13. Verify DB/query ownership for reads as well as writes: every SELECT/report/
   verifier/live-proof/migration/write path uses the approved owner seam, current
   DB/schema target, tenant/owner/supplier predicates, affected-row/readback
   expectation, bounded proof, cleanup/rollback, and redaction control.
14. Run the repo gate matrix locally before final signoff: PR body/delivery gate, no-new-mock guard, DB ownership gate, live-proof registry, and required CI mirrors.
15. Confirm review/forge evidence covers the current final diff, not a pre-pivot version.
16. Confirm branch/reason-set coverage for every new mode flag, reason string, status/code, SQL branch, or structured result path: positive, negative, sibling-reason, idempotent repeat, and placeholder-ordering proof where applicable.
17. Confirm cast/index safety for SQL/parser casts from JSON, text, external payloads, or numeric-looking IDs: empty, malformed, and out-of-range values are guarded before casting, and indexed predicates remain indexable or have query-plan proof.
18. Confirm proof-lane integrity: live-proof registry and command selectors choose the domain-specific lane for mixed generic/domain diffs and fail non-zero when asserted runtime resources are absent.
18.5. Confirm last-150-dev trap closure when recent repo evidence applies: every applicable trap-bank row from plan/contract/review/forge has current-head source evidence, receipt-backed command proof, and a verdict. Verification fails if stale UI/read-model, config/env/outage, proof-lane, proof-subject, weak-assertion, DB/query ownership, integration fault, redaction, or SRP/domain rows are missing, only broadly asserted, or no broader than stale pre-pivot proof.
19. Confirm live DB proof commands are bounded to the proof claim or include a concrete performance budget and query-plan/runtime evidence.
20. Confirm verification and PR-readiness artifacts are portable and current-head/current-base: no committed machine-local `/Users/...` command prefixes, `PATH=...`, `NODE_PATH=...`, stale pending/remaining sections, stale PR-creation checklist items, contradictory gate status, or wrong-head/base proof.
21. Confirm runtime-to-proof parity, integration fault matrices, boundary/scope invariants, architecture ratchets, local full-schema proof, observability/redaction contracts, public seam/UI/accessibility contracts, and test-integrity contracts are present or structured not-applicable with applicability predicate, source evidence, current head, and non-runtime/non-DB scope.
22. Write the report using [verification-report-template.md](references/verification-report-template.md).
23. Record the verification report in the current agent session.
24. State the proof-scope verdict explicitly. The only passing verdict is `PROVED`; `PARTIALLY PROVED`, `UNPROVED`, stale proof, mock-only proof, wrong-head proof, missing intent continuity, missing touched-file SRP proof, missing DB/query ownership proof, missing contract clause coverage, proof subject drift, missing runtime surface inventory, missing lifecycle/field matrix proof, missing branch/reason-set proof, unsafe cast/index proof, false-green proof-lane proof, unbounded live-proof query evidence, missing runtime/proof parity, missing integration fault proof, missing boundary/scope invariants, missing architecture ratchet proof, missing local full-schema proof for schema/query work, missing observability/redaction proof, missing public seam/UI/accessibility proof, weak test-integrity proof, or non-portable/stale artifact proof is a failed verification.
25. Only after fresh verification passes should work move to `enterprise-harness` or the `pr-readiness`/`merge` gate for final ship control.

For non-trivial, schema-sensitive, tenant-sensitive, money/order/inventory/invoice, or UI workflow changes, verification should be multi-agent when available: split evidence freshness, schema/live DB proof, E2E/workflow trace, and headless browser/UI proof. If delegation is unavailable, run the same checks sequentially and label the limitation.

## Evidence Artifact Schema Gate

Verification artifacts fail closed unless their proof is fresh, typed, and tied to the actual merge target.

- Required fields for each evidence item: command, mode, execution status, result, timestamp, current head SHA, target base branch or SHA, PR head when relevant, working directory, and artifact path or log reference.
- Browser/runtime proof must also record browser proof head or deployed/runtime source, route/surface exercised, and runtime provenance.
- Reject dry-run-only evidence unless the contract explicitly allows dry-run proof for that claim.
- Reject wrong-base, stale-head, proof-subject drift, missing-field, inconsistent boolean/string or string-boolean, no-command, no-output, or pre-pivot artifacts.
- Reject vague receipts that say only `PC PASS`, suite PASS, screenshot PASS, or browser PASS without command/log path, current head, clause/surface id, and exercised route or runtime path.
- For PR readiness, evidence must name the PR target branch and prove review/forge/verify covered the same final diff.
- The verification report must list the artifact schema checks that passed and the exact reason for any skipped field.
- The verification report must list the mechanical build packet check: allowed-path coverage, RED/GREEN receipts, forbidden-change scan, and refusal-condition status.
- The verification report must list the architecture contract check: public-seam/SRP proof, module boundary, folder placement, owner layer, dependency direction, forbidden import scan, and architecture-test command evidence.
- The verification report must list the intent-continuity check, touched-file SRP
  check, and DB/query ownership check, each with source evidence, current head,
  command evidence, and verdict.

## Completion Reliability

- The verification document is the exit artifact. Write it before polishing optional prose or summaries.
- If time or context is tight, write a minimal but valid verification report first, then enrich it only if time remains.
- Update contract traceability statuses from `pending` to `passed` or `failed` based on the fresh evidence you just ran.
- If review already finished and fresh commands already ran in this session, move straight into the report and verdict. Do not reopen upstream design or discovery work.
- For bounded work, prefer a short, concrete report over a long narrative.

## Rules

- No `should work`
- No `probably fine`
- No completion claim without fresh output
- No `full-system` verdict unless the evidence actually covers the full system
- No PC-level, suite-level, or gate-level PASS as a substitute for clause-level
  source, assertion, and runtime proof.
- Do not invoke `enterprise-harness` as a substitute for fresh verification evidence
- No mocked DB proof for schema/query/data claims
- No GUI/manual browser proof as required evidence; UI verification must remain headless
- No stale review/forge proof after a CI or gate-driven code pivot
- No final claim when final HEAD, base/target, PR head, artifacts, gate summaries,
  receipts, browser proof, or runtime provenance disagree.
- No final claim for async/worker/UI/API work without a proved/not-proved runtime
  route/surface inventory.
- No proof-scope verdict broader than the proved rows in that inventory.
- No final claim while repo gate matrix commands are unrun, missing, or only assumed
- No final claim while applicable recent PR trap-bank rows are unproved, stale, or only handled by prose
- No final claim on `PARTIALLY PROVED`; partial proof is failure, not a reduced-confidence pass
- No PR-ready or merge-ready claim unless `enterprise-review`, `enterprise-forge`, and `enterprise-verify` were recorded for the current final diff.
- No final claim when any changed path, helper/writer, public seam, folder placement, dependency direction, architecture test, test command, or proof was invented during build instead of named by the mechanical build packet.
- No final claim when original user intent, operator acceptance, or non-goals are
  no longer traceable to proof rows.
- No final claim when a touched mixed-responsibility file skipped its contracted
  `fix-now` refactor or lacks a narrowed/blocked non-goal.
- No final claim when a DB/query path, including read-only SELECT/report/
  verifier/live-proof queries, lacks owner seam, scoping, readback/affected-row,
  bounded proof, cleanup, or current DB/schema evidence.
- No final claim when proof commands can exit `0` for missing asserted resources, when a generic proof lane can shadow a domain lane, or when live-proof queries are unbounded on growing data without an explicit performance budget.
- No final claim when verification artifacts contain workstation-local command prefixes, stale PR-state checklists, contradictory gate status, or wrong-head/base evidence.
- No final claim for async, worker, order, invoice, inventory, pricing, label-printing, notification, or staff workflow work unless exact real-producer field spelling, near-miss field spelling collisions, duplicate submit/concurrent worker, stale running recovery, old synchronous confirmation/error preservation before enqueue, post-commit bookkeeping failure, helper return variant success semantics, unavailable/cancelled downstream dependency, retry behavior, close/reopen/refresh rehydration, accept response metadata, backwards-compatible health routes, terminal worker branches, disk/data volume readiness, claimed scrape/data semantics, and exact field-contract proof are either PROVED or structured not-applicable with applicability predicate, source evidence, current head, and non-runtime/non-DB scope.
