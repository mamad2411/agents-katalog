---
name: enterprise-review
description: Use when enterprise implementation is complete enough for a structured review that separates spec compliance from code quality and classifies drift explicitly
---

# Enterprise Review

Review the work in two stages. Never mix them.

## Required Background

- `code-reviewer`
- `requesting-code-review`

## Stage Order

Use [review-separation.md](references/review-separation.md).

1. Stage 1: spec compliance
2. Stage 2: code quality

If Stage 1 fails, Stage 2 does not start.

Before review starts, run the agent-bound review gate in [agent-stage-gates.md](../enterprise/references/agent-stage-gates.md).

For non-trivial, schema-sensitive, tenant-sensitive, money/order/inventory/invoice, or UI workflow changes, review should be multi-agent when available: split spec/contract, schema/data, code execution, E2E/workflow, security/tenant, and headless UI lenses. If delegation is unavailable, run the same lenses sequentially and label the limitation.

## Current-Head Adversarial Gate

Review must pull apart the current final diff, not summarize build intent.

- State the exact head SHA and tree/diff being reviewed.
- Inspect current implementation code and consumers before accepting migration, docs, evidence, or mock claims.
- Include a `breakdown attempt` section that actively probes races, null/falsy values, wrong branch/base, wrong route method, stale evidence, duplicate helper/writer, ownership leaks, unsafe environment matching, and affected-row omissions.
- Compare implementation behavior against the locked contract, current PR thread history when present, and repo trap matrix.
- Build or refresh the review feedback trap bank from two sources before verdict: `Current PR Trap Rows` from the current PR/final diff/thread history, and `Recent PR / Last-150 Trap Rows` from recent merged PR/review/check evidence when available. Name both sources in the review output; if either source applies but is not inspected, block `PASS` and recycle the review. The verdict must explicitly name any `missing` or `unclosed` trap rows, or state that each row is proved or source-evidenced not applicable. For Helpdesk-like repos, replay last-150-dev classes explicitly: stale UI/read-model rehydration, config/env/outage semantics, proof-lane selector misses, stale proof-subject/preflight failures, weak assertions, DB/query ownership gaps, integration side-effect/idempotency faults, redaction/diagnostic leaks, and SRP/domain-boundary drift. Do not collapse the redaction/diagnostic class into generic "sanitized errors"; name redaction or diagnostic leakage explicitly when integration, logging, proof, or error surfaces are touched.
- Block `PASS` when any hard-stopper review lane is skipped, unverifiable, stale after a pivot, or based on migration/diff/mock evidence instead of current code.

## Required Checks

- every contract item has a matching implementation target
- every contract item has a real test
- the recorded `build_packet` exists, passes the mechanical packet gate, and names every changed source/test/artifact path
- the recorded `build_packet` passes the architecture contract gate: exact module boundary, folder placement, public seam, owner layer, allowed dependency direction, forbidden imports, and architecture tests
- the Intent Continuity Ledger still maps original user words, business outcome,
  operator acceptance, non-goals, and proof commands to the implemented diff
- the Architecture Ratchet Matrix is honored: changed boundaries keep their public seam, owner layer, dependency direction, forbidden imports, architecture proof, and future regression trap
- every changed file has a source-backed Touched File SRP Assessment; `fix-now`
  rows are implemented and proven, and mixed-responsibility touched files are not
  left as vague follow-up cleanup
- every DB/query path, including SELECT/report/verifier/live-proof reads, has a
  DB/Query Ownership Packet and uses the approved owner seam, current DB/schema
  target, scope predicates, bounded proof, and readback/affected-row expectation
- changed files are classified as `required`, `enabling`, or `drift`
- every build change is inside the packet's allowed paths; any unlisted path is a review failure unless the contract was recycled before the edit
- build receipts show the packet's expected RED/GREEN loops; missing, wrong-reason, or post-hoc RED/GREEN evidence fails spec compliance
- proof scope in the contract still matches the implementation reality
- contract traceability statuses are updated from `pending` to their real state before handoff
- schema/query claims have current-code reads plus real DB proof, not migrations/diffs/mocks
- schema/query/data-sensitive claims have local full-schema Postgres proof or a contract-backed blocker/narrowed claim; production proof targets, secret output, and repo dumps are review failures
- read-only query changes are schema/query claims for ownership purposes; review
  fails SELECT/report/proof queries that bypass the owning seam or omit tenant,
  owner, current-DB, bounded-work, or readback semantics
- every changed runtime file has code-level execution proof
- every cross-layer behavior has source-to-consumer E2E trace and edge-case coverage
- async/worker/order/invoice/inventory/pricing/label-printing/notification/staff workflow changes have explicit proof for exact field spelling through real producers, near-miss field spelling collisions, duplicate submit, concurrent worker/scheduler, stale running recovery, old synchronous confirmation/error preservation before enqueue, post-commit bookkeeping failure, helper return variant success semantics, unavailable/cancelled downstream dependencies, retry behavior, and close/reopen/refresh rehydration where applicable
- runtime shape proof is still true: mocks, fixtures, route catalogs, helper inputs, query aliases, and service return examples match current source/live proof
- UI/PDF/file/upload/rendered workflows have headless browser proof
- repo gate matrix commands are present and credible: PR body/delivery gate, no-new-mock guard, DB ownership gate, live-proof registry, and required CI mirrors
- proof-lane integrity is proven: live-proof registry and command selectors choose domain-specific lanes for mixed generic/domain diffs, and proof commands fail non-zero when expected tables, columns, routes, workers, browser states, or artifacts are absent
- SQL/parser casts from JSON, text, external payloads, or numeric-looking IDs guard empty, malformed, and out-of-range values before casting; changed predicates on indexed columns preserve indexability or carry explicit query-plan proof
- every new mode flag, reason string, status/code branch, SQL `CASE` branch, or structured error path has positive, negative, sibling-reason, idempotent repeat, and placeholder-ordering proof where applicable
- live DB proof queries are bounded for focused proof lanes; unbounded historical scans on hot or growing tables are review findings unless the contract records a concrete performance budget and runtime evidence
- evidence and verification artifacts are portable and current: no committed machine-local `/Users/...` command prefixes, `PATH=...`, `NODE_PATH=...`, stale `Pending`/`Remaining` sections, stale `Create PR` tasks inside an open PR, contradictory gate status, or wrong-head/base proof
- runtime-to-proof parity is proven for verifier, replay, backtest, report, readiness, and live-proof code; proxy metrics or retyped predicates that can drift from production helpers are review failures
- external integration fault matrices are proven for fallback criteria, timeout/cancellation, idempotent retry boundaries, sanitized errors, and duplicate side effects
- tenant/supplier/owner/identifier/omitted-field/affected-row invariants are locked and tested for every changed read, update, upsert, and governed write path
- security/observability/logging changes prove adversarial redaction corpus coverage, stable log shape, useful diagnostics, and no live operational identifier leakage
- public seam and UI consumer proof covers exports, startup seams, API client/server key matching, UI lock/rehydration, nested-route specificity, custom-control keyboard/focus behavior, and downstream consumers
- test integrity is proven: no new schema-coupled DB mocks, no source-string-only runtime proof, env mutations restored, module-load tests isolated, and no brittle count-only assertions as primary proof
- the review is against the current final diff. If CI or a gate forced a code pivot, earlier review output for affected files is stale and must be rerun.
- build did not invent requirements, paths, tests, helpers, writers, ownership, architecture, or proof commands outside the packet
- no claim is only `PARTIALLY PROVED`; partial proof, mock-only proof, stale proof, wrong-head proof, or untested important matrix cells fail spec compliance
- every applicable current trap-bank row is either implemented and receipt-proved, explicitly not applicable with source evidence, or recycled to contract/build. A row being "probably covered" by broad tests is not enough when recent reviewers found the same class after green checks.
- SRP/folder-layout claims are proven by public-seam architecture tests or explicitly recycled; private-helper-only proof is a review failure
- SRP/refactor-as-you-touch is a review gate, not taste. If a touched file is
  doing multiple jobs and the changed responsibility is one of them, review fails
  unless the contracted `fix-now` refactor happened or the contract narrowed the
  claim with a recorded blocker.
- apply the deletion test to new or moved modules: if deleting it only removes a
  pass-through and does not force complexity back into callers, treat it as a
  shallow seam or unnecessary abstraction
- reject source-string, fixture-only, or hard-coded-response tests as primary proof for runtime behavior that has a real source, DB, worker, browser, or integration boundary

## Reviewer Independence

If an independent reviewer is available for medium or large work, use one. If not, perform the review yourself but label the limitation explicitly. Do not pretend self-review is the same as independent review.

If the prompt explicitly states that the committed repo profile and repo-local overlay are already current, review should proceed without reopening discover work unless the diff reveals profile drift.

When the review artifact is written, record it in the current agent session before moving to forge or verify.

## Completion Handoff

- Writing the review artifact is not the finish line.
- If the current prompt asks for completion, verification, PR readiness, merge, or an end-to-end cycle, review must hand off directly to `enterprise-forge` in the same lane.
- Do not hand off from review directly to verify, harness, PR creation, or merge unless the user explicitly asked for review-only output and no completion/merge claim is being made.
- Do not stop after review waiting for another prompt unless the user explicitly asked for review-only output.
