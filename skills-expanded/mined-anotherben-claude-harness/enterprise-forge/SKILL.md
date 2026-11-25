---
name: enterprise-forge
description: Use when reviewed enterprise work still needs adversarial probing, mechanical checks, and recycle-loop bug closure before final verification
---

# Enterprise Forge
## Global Precheck

Before reading further, writing artifacts, delegating, or changing files, run:

```bash
enterprise-precheck --skill enterprise-forge
```

If it exits non-zero, stop and report stderr verbatim. Do not hand-craft packet files or evidence markers to bypass it.


The forge exists to break optimistic assumptions before production does.

## Mandatory Closure Gates

Forge fails closed unless all three gates are satisfied and recorded in the
forge report.

### Contract Clause Coverage

Every explicit contract, TDD, plan, and postcondition clause must have its own
coverage row. Each row must include the clause id/text, exact source evidence,
executable assertion or test evidence, runtime/browser/live proof or structured
not-applicable reason, current head SHA, and verdict. A PC-level PASS,
suite-level PASS, vague receipt, or prose summary is not enough. A receipt is
usable only when it names the command/log, current head, clause or surface it
proves, and exercised runtime path. Missing source, assertion, or runtime proof
for a non-N/A clause is a forge failure and must recycle through contract/TDD.

### Proof Subject Integrity And Freshness

Forge must inventory final HEAD, target/base branch or SHA, PR head when
relevant, review artifact head, forge artifact head, verify artifact head if it
exists, gate summary head, receipt heads, browser proof heads, and runtime
provenance/deploy source. These must point at the same final diff and target.
Any mismatch, unknown head, stale pre-pivot artifact, or runtime proof from a
different deploy/source is a failed forge.

### Runtime Route And Surface Inventory

For async, worker, UI, API, and integration work, forge must list every claimed
route, event, queue transition, terminal branch, readiness endpoint, health
endpoint, runtime volume/dependency check, and data-semantic path. Each surface
is marked `PROVED`, `NOT PROVED`, or structured `N/A` with command/artifact
evidence. A full workflow or full-system claim based on a subset is a forge
failure, and any proof-scope verdict must be no broader than the proved rows.
For browser-worker-style lanes, inventory must include accept response metadata
(`runId`, BullMQ queue id, worker identity, and `readinessSnapshot`),
backwards-compatible health routes including `/api/health`, terminal worker
branches, disk/data volume readiness, and claimed scrape/data semantics.

## Entry Rule

Run this after `enterprise-review`, not instead of it.

Before forge starts, run the agent-bound forge gate in [agent-stage-gates.md](../enterprise/references/agent-stage-gates.md).

Forge is the "pull the code apart" gate. No enterprise PR readiness, merge, or ship-ready claim may bypass it after build/review.

For non-trivial, schema-sensitive, tenant-sensitive, money/order/inventory/invoice, or UI workflow changes, forge should be multi-agent when available: split schema/data, code execution, E2E/workflow, security/tenant, and headless UI attack lenses. If delegation is unavailable, run the same attack lenses sequentially.

When forge lenses are delegated, use Codex headless by default and follow
[codex-headless-workers.md](../enterprise/references/codex-headless-workers.md).
Each worker must receive only the compact forge packet for its lens and must
return the required proof artifact. Do not count cmux panes, OpenCode, Kimi, or
other runtimes as forge proof unless parity has been proven for MCP access,
skills, repo policy, and structured output in the current repo.

Forge must record a structured `enterprise_attack_lens_packet` in the forge report.
Missing lenses or lenses without agent/session/worker/receipt proof are a failed
forge, even if the prose sounds adversarial.

## Recurring Trap Lenses

Apply these lenses on every non-`QUICK` forge pass and record either proof or a blocking bug:

- Affected-row lens: UPDATE/DELETE/repair/projection flows must check the row actually changed before clearing state or reporting success.
- SQL ownership lens: tenant, owner, current database/schema, aliases, latest-vs-earliest semantics, and parameter typing must be proven against current query code.
- DB/query ownership lens: every SELECT, report, verifier, live-proof, repair,
  projection, sync, migration, and write path must prove the approved owner seam,
  current DB/schema target, scope predicates, affected-row or readback behavior,
  bounded proof command, and cleanup/rollback. Read-only queries are in scope.
- Intent-continuity lens: original user words, business outcome, operator
  acceptance, and non-goals must still map to implemented behavior and proof.
  Generic task completion without operator acceptance proof is a forge bug.
- Runtime shape lens: mocks, fixtures, service returns, route catalogs, evidence artifacts, and helper inputs must match current source/live proof.
- Route/source lens: scenario packs and docs must match mounted route paths, HTTP methods, auth boundaries, and consumers.
- UI falsy lens: zero, empty string, false, duplicate keys, labels, overflow, and rendered browser state must survive the real UI path.
- Proof-quality lens: dry-run-only, partial-proof, mock-only, missing-field, wrong-base, stale-head, string-boolean, source-string-only, or non-current evidence is a forge bug.
- Duplication lens: new helpers/writers must not duplicate existing authority without a named seam and contract authorization.
- Architecture-contract lens: the build packet must name exact module boundary, folder placement, public seam, owner layer, allowed dependency direction, forbidden imports, and public-seam architecture tests; vague architecture language is a forge bug.
- Architecture-ratchet lens: changed boundaries must prove the future regression trap, not just current load success. Deep modules without a public seam consumer test are forge bugs.
- Touched-file SRP lens: every touched file must prove its current responsibility,
  owner layer, one reason to change, and contracted `fix-now`/`follow-up`/
  `note-only` classification. A mixed-responsibility file touched without the
  contracted `fix-now` extraction or a blocking/narrowed claim is a forge bug.
- Local-full-schema lens: schema/query/data-sensitive work must prove the real runtime query path against local restored Postgres or carry a contract-backed blocker/narrowed claim. Proof against production, secret output, or repo dumps is a forge bug.
- Async lifecycle lens: queue/worker/scheduler/background side effects must prove atomic claim, duplicate scheduler/worker behavior, stale running recovery, retry policy, post-commit bookkeeping failure, and idempotent committed side effects.
- Field-contract lens: UI/API/DB/worker/read-model/print/notification projections must prove exact runtime field names, aliases, null/falsy handling, and consumer expectations from real source or live proof. Non-zero quantity fields, zero/falsy quantity fields, and near-miss field spellings with the same words in different order or case must be traced from the actual producer, not a mocked response.
- Sync-to-async preservation lens: async enqueue routes must prove old synchronous validation, recoverable confirmation, and error outcomes still happen before acceptance.
- Commit-boundary lens: irreversible stock/money/invoice/pricing/sync side effects must be separated from later bookkeeping/projection failures so committed work is not reported as uncommitted failure.
- Return-variant lens: printing, notification, and integration helpers must gate dedupe/lock/retry side effects on explicit success, not truthiness.
- Branch/reason-set lens: every new flag, reason string, status/code, SQL `CASE`, or structured result branch must prove positive, negative, sibling-reason, idempotent repeat, and placeholder-ordering behavior. One literal happy path is not enough.
- Cast/index lens: JSON/text/external-ID casts must be guarded for empty, malformed, and out-of-range values before casting; indexed predicates must remain indexable or carry query-plan proof.
- Proof-lane lens: live-proof registries, command selectors, CI mirrors, and route/file matchers must prove domain-specific lane selection for mixed diffs and fail non-zero when asserted runtime resources are absent.
- Artifact-portability lens: verification and PR-readiness artifacts must be current-head, current-base, portable, and internally consistent; machine-local command prefixes, stale pending sections, stale PR-creation checklist items, and contradictory gate status are forge bugs.
- Bounded-proof lens: live DB or integration proof commands must be scoped to the proof claim; unbounded historical scans on growing tables are forge bugs unless the performance budget and query plan are explicit.
- Runtime-proof parity lens: verifier, replay, backtest, report, readiness, and live-proof logic must share production helpers or prove equivalent predicates, inputs, and truth conditions.
- Integration fault lens: external fallback, timeout/cancellation, retry, and error handling must be attacked by fault type and side-effect idempotency; non-idempotent retry and raw external error leakage are forge bugs.
- Boundary invariant lens: tenant, supplier, owner, identifier-family, affected-row, omitted-field/upsert, and rollout-default changes must prove preserved contracts on missing, stale, wrong-family, null, false, zero, and already-existing paths.
- Observability/redaction lens: logs, errors, serializers, and diagnostics must survive adversarial message/stack/non-object/header/cookie/token/live-identifier cases without losing useful operator context.
- Public seam/UI/accessibility lens: exports, startup seams, API client keys, UI lock rehydration, nested route matching, and custom listbox/combobox keyboard/focus behavior must be proven through real consumers.
- Test-integrity lens: schema-coupled DB mocks, source-string-only assertions, leaked test env, non-isolated module imports, and brittle count assertions are forge bugs when used as runtime proof.
- Deletion-test lens: new or moved modules must earn their seam. If deleting the
  module removes only pass-through code and does not push real complexity back
  into callers, classify it as shallow architecture.
- Contract-clause coverage lens: every contract/TDD/plan/PC clause must map to
  exact source evidence, executable assertion/test evidence, and runtime proof
  or structured N/A. PC-level or suite-level PASS without clause rows is a forge
  bug.
- Proof-subject freshness lens: final HEAD, base/target, PR head, review/forge/
  verify artifacts, gate summaries, command receipts, browser proofs, and runtime
  provenance must identify the same subject. SHA drift or pre-pivot proof is a
  forge bug.
- Runtime-surface inventory lens: every claimed route, event, readiness/health
  surface, terminal branch, runtime volume/dependency, and data-semantic path
  must be marked proved/not-proved. A narrow `/ready` or UI smoke cannot support
  a full async/worker/workflow claim.
- Last-150 PR replay lens: when recent merged PR, review-comment, or check-failure evidence is available, replay the concrete trap classes that recently escaped earlier stages. For Helpdesk-like repos this includes stale UI/read-model rehydration, config/env/outage semantics, proof-lane selector misses and missing-resource false greens, stale proof-subject/preflight failures, weak assertions, DB/query ownership gaps for reads and writes, integration idempotency/fault side effects, redaction/diagnostic leaks, and SRP/domain-boundary drift. Each relevant row must be proved, rejected with source evidence, or recycled as a contract/TDD bug.

## PR Timing Attack

Forge must attack review timing, not just code:

- If the lane is high-risk, verify the PR is draft or that the open-PR exception is explicitly justified and backed by review/forge/verify/harness evidence.
- If Copilot/advisory review is slow or non-blocking, verify there is an `advisory-harvest` path so useful findings are not lost after merge.
- If Copilot has already reviewed an older head, treat that review as stale for changed files unless the repo is configured to review each push or a re-review was requested.
- If a Copilot/advisory comment credibly points at security, data loss, tenant, schema/query, money/order/invoice/inventory, or user-visible breakage, escalate it from advisory to blocking recycle.

## Required Workflow

1. Run the checks in [mechanical-checks.md](references/mechanical-checks.md).
2. Build the contract clause coverage matrix before reading PC-level results as
   proof.
3. Build the proof subject integrity/freshness inventory and fail on head/base/
   runtime drift.
4. Build the runtime route/surface inventory for async, worker, UI, API, and
   integration claims.
5. Probe contract promises from a new angle.
6. Apply the lenses in [adversarial-lenses.md](references/adversarial-lenses.md).
7. Map every changed runtime file to code-level execution proof.
8. Trace every cross-layer behavior source-to-consumer, including edge cases from plan/contract.
9. For async, worker, order, invoice, inventory, pricing, label-printing, notification, or staff workflow changes, attack every lifecycle and field-contract matrix cell before final verification.
10. Require live DB proof for schema/query/data claims and headless browser proof for UI/PDF/file/upload/rendered workflows.
11. Attack the repo gate matrix: PR body/delivery gate, no-new-mock guard, DB ownership gate, live-proof registry, and required CI mirrors.
12. Attack source-read coverage and live query/schema readback proof. Migration-only, mock-only, or diff-only schema proof is a forge failure.
13. Attack intent continuity: every implemented behavior and proof artifact must
    trace back to original user words, business outcome, operator acceptance, and
    explicit non-goals.
14. Attack DB/query ownership for reads as well as writes: owned source seams,
    current DB/schema target, tenant/owner predicates, affected-row/readback,
    bounded proof, cleanup, and no bypassing the owning repository/service.
15. Attack Cortex/source-grounding proof: stale indexes, ignored paths, exact-text gaps, default source-type omissions, dynamic exports, generated code, and any claim that uses Cortex as truth without direct source reads.
16. Attack architecture depth: deletion-test failures, shallow pass-through modules, private-helper test
    exports, leaked retry/cache/query ordering, and one-adapter seams that do
    not earn their abstraction.
17. Attack SRP/folder layout mechanically: verify changed files match the packet's owner layer and public seam, dependency direction is obeyed, forbidden imports are absent, architecture tests exercise the consumer seam instead of private helpers, and touched-file `fix-now` refactors happened.
18. Apply the recurring trap lenses above and record proof or bugs for each relevant lens.
18.5. Apply the Last-150 PR replay lens before final forge verdict when the lane is PR-producing or touches a surface represented in recent review failures.
19. Attack PR timing and Copilot/advisory state: draft policy for high-risk lanes, stale Copilot reviews after code pivots, and advisory-harvest follow-up for non-blocking comments.
20. Treat any CI-driven implementation pivot as a fresh forge target for the affected files; previous `FORGED` output does not cover code it never saw.
21. Treat missing intent continuity, DB/query ownership, touched-file SRP, contract clause coverage, proof subject integrity, runtime surface inventory, branch/reason-set, cast/index, runtime-proof parity, proof-lane, integration fault, boundary invariant, architecture-ratchet, local-full-schema, observability/redaction, public seam/UI/accessibility, artifact-portability, test-integrity, or bounded-proof evidence as forge failures, not advisory polish.
22. If proof would be `PARTIALLY PROVED`, treat that as a forge failure and recycle the missing proof cell through contract/TDD before PR readiness.
23. If a bug is found, append a new contract item and recycle it through TDD.
24. Re-run until no bugs remain or a circuit breaker fires.

## Safeguards

- maximum 5 recycle iterations
- bug count must decrease each round
- stop if the same class of failure repeats 3 times

## Output

Write a forge report under `docs/reviews/` with:

- mechanical check results
- contract clause coverage matrix with source, assertion, runtime proof, N/A
  predicates, head SHA, and verdict for every clause
- proof subject integrity/freshness inventory for final HEAD, base/target, PR
  head, review/forge/verify artifacts, gate summaries, receipts, browser proof,
  and runtime provenance
- runtime route/surface inventory for every claimed route, event, terminal
  branch, readiness/health endpoint, runtime volume/dependency, and data
  semantic path
- proof-scope boundary showing the widest proved scope and any subset-overclaim
  blockers
- changed-file, source-read, Cortex-grounding, and query/readback proof failures
- intent-continuity failures against original user words, business outcome,
  operator acceptance, non-goals, and proof commands
- DB/query ownership failures for reads, writes, reports, migrations, and proof
  queries
- touched-file SRP/refactor failures and missing `fix-now` execution
- architecture-depth failures: shallow modules, weak seams, leaked internals, or
  tests coupled to private implementation
- new bugs and appended contract items
- PR timing, draft/high-risk, and Copilot/advisory-harvest findings
- structured `enterprise_attack_lens_packet` with every required lens
- recycle history
- final verdict: `FORGED`, `REJECTED`, or `CIRCUIT BREAK`

Record the forge report in the current agent session before moving to verification.

Before PR readiness or merge, the forge record must still match the current code state. If implementation changes after forge, rerun forge before verify/harness/merge.
