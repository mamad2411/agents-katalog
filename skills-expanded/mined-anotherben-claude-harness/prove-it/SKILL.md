---
name: prove-it
description: "Post-fix runtime proof gate. Use after Codex implements or reviews a bug fix, feature fix, PR, workflow change, or claimed repair; before saying fixed/done, committing, opening a PR, merging, or shipping. Requires mandatory blast-radius, review-feedback trap replay, actual runtime evidence at the boundary where the bug manifests, browser proof for UI/workflow changes, and clear verdicts when proof is missing."
---

# Prove It

Use this skill to prove a claimed fix works in the actual system. The goal is not confidence. The goal is evidence.

## Prime Directive

Do not say "fixed" unless the broken behavior has been exercised at the real boundary where the user, system, worker, integration, or downstream consumer depends on it.

Code inspection is not proof. Type checks are not proof. Unit tests are supporting evidence, not the proof, unless there is no higher runtime surface for the behavior.

Only `PROVED` is a passing result. `PARTIALLY PROVED`, `UNPROVED`, and `DO NOT CLAIM FIXED`
are failed proof gates. They may be useful diagnostic labels, but they must block "fixed",
"done", ready-PR, merge-ready, ship-ready, or safe-to-merge claims unless the user explicitly
overrides the proof failure in that same turn.

If the verdict is not `PROVED`, say "implemented", "attempted", or "failed proof"; do not say
"fixed".

## Required Gates

Run these gates before the final verdict:

1. Run `blast-radius` every time. It is mandatory for every claimed fix.
2. Replay review-feedback traps for the touched domain/PR. Ingest valid Cursor/Copilot/human review
   findings and prior blast-radius/prove-it artifacts, then prove each applicable invariant locally.
3. Run `business-review` when the change touches UI, workflow, user-facing API behavior, operations, support, finance/reconciliation, reporting, business state, or a path a human depends on.
4. Run `zoom-out` when the affected area is unfamiliar, crosses modules, has unclear callers, or the domain workflow is not obvious.

Verdict caps and hard failures:

- Partial proof is a fail. `PARTIALLY PROVED` is a blocking verdict, never a warning or acceptable closeout state.
- Any HIGH or CRITICAL `blast-radius` finding: `DO NOT CLAIM FIXED`.
- Missing required `business-review`: proof failure.
- Required browser proof missing for UI/workflow changes: `UNPROVED`.
- Only code inspection, type checks, or unit tests: `UNPROVED`.
- Happy path without a realistic counterexample: proof failure.
- Any unmapped claim, unverified side effect, mock-only proof for a real integration boundary, stale
  evidence, wrong-head evidence, or important untested edge case: proof failure.
- Any proof command that exits successfully while the asserted runtime resource is absent, any generic
  proof lane that can shadow the domain-specific lane, or any committed proof artifact with machine-local
  command prefixes, stale PR-state checklist items, contradictory status, or wrong-head/base evidence: proof failure.
- Any valid review finding that applies to the touched invariant class but was not converted into a
  local regression, runtime proof, or documented `NOT APPLICABLE` evidence before PR/merge: proof failure.
- Any review-derived trap that still relies on "CI will catch it" or "review will catch it" caps the
  result at `PARTIALLY PROVED` and blocks fixed/ready/merge claims.
- Any valid PR conversation found after local proof that could reasonably have been caught by local
  testing is a proof-system miss. Before merge/ready claims, patch the code, add the focused local
  regression or runtime canary that would have caught it, and update the responsible skill/runbook
  with the new trap class or command recipe. If the skill/runbook update is blocked, state the blocker
  and keep the PR out of `PROVED` until Ben explicitly accepts the exception.
- Any runtime-to-proof drift, unproven external retry/fallback fault matrix, missing tenant/supplier/owner scope
  invariant, unproven public seam consumer, weak redaction/log-shape proof, custom UI control without keyboard/focus
  evidence, schema-coupled DB mock, source-string-only proof, or unbounded hot-path/live-proof query: proof failure when relevant.

## Workflow

### 1. Inventory the Claims

Write the exact claims the agent wants to make. Split compound claims.

Examples:

- "The invoice creation crash is fixed."
- "Receive flow pricing now uses the asynchronously loaded supplier price."
- "Existing pending order behavior is unchanged."
- "The admin user can complete the workflow from the UI."

Each claim must map to evidence in the proof ledger. Unmapped claims are a failed proof gate.

### 2. Select the Highest Proof Surface

Choose the highest real boundary available. Load `references/proof-surfaces.md` when selecting evidence for UI, API, DB, async, integration, CLI, or generated-artifact proof.

Common choices:

- UI/workflow: run the app and prove it in a browser.
- API: hit the real running route, with realistic auth/tenant context when applicable.
- DB/data: query the live dev database before and after the action.
- Worker/async: enqueue or trigger the job, observe processing, and verify the side effect.
- Integration: use a safe sandbox/live-safe external path; if unavailable, say what could not be proved.
- Generated artifact: open, render, parse, or consume it with the real downstream tool.

Use lower-level tests only as supporting evidence when a higher surface exists.

### 2A. Declare Mock Boundaries

Before running proof, list every mocked, stubbed, fixture-only, or generated response boundary.
For each one, name the real producer/consumer path and either:

- prove the same fields at a real boundary, or
- mark the claim failed.

Do not prove an API projection, worker side effect, DB write, print payload, notification, or UI state
by mocking the endpoint that contains the changed behavior unless another proof exercises that real
endpoint or downstream artifact.

### 2B. Replay Review-Derived Traps

Before golden-path proof, build a local trap replay list from valid current/prior Cursor, Copilot,
human-review, blast-radius, and prove-it findings for the touched domain. Classify each row as
`APPLIES` or `NOT APPLICABLE`.

Common trap classes:

- identity shape: UUID vs integer, local ID vs external ID, alias/name/case/whitespace fallback
- timestamp/source authority: action time vs projection time vs generated artifact time
- serializer/storage equivalence: `undefined` vs omitted vs JSON null, snake_case vs camelCase
- audit/log shape: omitted optional audit fields, literal `undefined` in idempotency/audit keys,
  serialized quoted headers such as `"x-api-key":"secret"`, and redaction parity between object and text errors
- parser shape: partial numeric parses (`1.2.3`), punctuation-only matches (`.`), `NaN`/infinite values,
  and loose regexes that accept malformed external amounts or identifiers
- dedupe/lock/notification state: declined, unavailable, cancelled, skipped/no-op, success, error
- UI rehydration: close, refresh, reopen, stale transient state, backend lock still active
- post-commit bookkeeping: committed side effect with failed projection/status/notification update
- proof integrity: wrong-head, stale artifact, generic lane shadowing a domain-specific lane

For every `APPLIES` row, add or run a focused local regression, real-boundary proof, or live canary
before claiming `PROVED`. If the review finding is a false positive, record the source read or runtime
evidence that disproves it and still cover the nearest cheap invariant when practical.

If a valid Cursor/Copilot/human PR conversation appears after the local proof package was marked
complete, stop and add a `Local Proof Miss` row:

- what local proof should have caught it
- the focused regression/canary added now
- the skill, repo skill, or runbook updated so the miss is not repeated
- any blocker to updating that skill/runbook

Do not merge, promote, or call the PR ready while this row is missing or unresolved.

### 3. Prove the Golden Path

Exercise the behavior that was broken from the user's or system's natural entry point through completion.

Capture concrete evidence:

- URL, screenshot, browser trace, or visible UI state.
- Request command and response status/body.
- DB query and result showing the expected state.
- Worker log, job record, queue state, or downstream side effect.
- File opened, rendered, parsed, or consumed successfully.

Summaries are fine, but include enough exact evidence that another agent could tell what was actually run.

### 4. Try to Disprove It

Run at least one realistic counterexample: the edge case most likely to show the fix is fake.

Pick from the shape of the bug:

- Null, empty, missing, malformed, duplicate, stale, or historical data.
- Second tenant, wrong permission, cancelled/soft-deleted row, or old record shape.
- Bulk variant, alternate entry point, worker path, retry, or concurrent attempt.
- Case/whitespace/alias mismatch for identity fixes.
- New mode flag, reason string, status/code branch, SQL branch, sibling reason, malformed or out-of-range
  external ID, de-indexing cast, proof-lane matcher collision, or missing-resource proof-command case.
- External timeout/retry/fallback fault, non-idempotent retry, wrong identifier family, omitted-field upsert, default
  rollout change, verifier/runtime parity case, secret corpus shape, keyboard-only UI path, and mocked/source-string proof case.

If no meaningful counterexample exists, state why. Do not skip this silently.

### 5. Confirm Side Effects

If the change writes, syncs, schedules, sends, calculates, imports, exports, or mutates state, verify the destination.

Examples:

- Data written: inspect the row or downstream read model.
- Sync triggered: inspect sync status/log and destination state.
- Notification sent: inspect the safe delivery channel or queued message.
- Price/totals changed: inspect the persisted calculated value and the UI/API that reads it.

For async, queue, worker, order, invoice, inventory, pricing, label-printing, or reconciliation
work, side-effect proof must include every relevant lifecycle leg, not just the happy path:

- accepted/queued state
- atomic claim or duplicate-submit behavior
- running/stuck-run recovery or explicit non-retry policy
- committed side effect
- post-commit bookkeeping failure behavior
- legacy synchronous validation/confirmation errors preserved before async acceptance
- helper return variants: success, unavailable, cancelled, skipped/no-op, and error
- retry/unavailable/cancelled downstream behavior
- UI/backend rehydration after close, refresh, or reopen
- branch/reason-set coverage for new modes, statuses, structured codes, and SQL branches
- cast/index safety for JSON/text/external IDs, including malformed and out-of-range values
- proof-lane integrity for command selectors and live-proof registries
- boundedness of live DB proof queries on growing tables
- artifact portability and current-head/current-base consistency
- runtime-to-proof parity for verifier, replay, backtest, report, and live-proof code
- integration fault matrix for fallback, timeout, cancellation, retry idempotency, sanitized errors, and duplicate side effects
- boundary/scope invariants for tenant, supplier, owner, identifier, affected rows, omitted fields, and governed writes
- observability/redaction proof for message, stack, non-object errors, headers, cookies, tokens, and live identifiers
- public seam and UI/accessibility proof for exports, startup seams, API clients, locks, navigation, and custom controls
- test-integrity proof: no schema-coupled DB mocks, no source-string-only proof, restored env, stable assertions

Any relevant leg left unproved is a failed proof gate.

### 6. Produce the Proof Ledger

End with this ledger. Save it as an artifact only when the active repo/workflow allows writing evidence files; otherwise include it inline in the final response.

```markdown
## Prove It Ledger

### Claim Inventory
- CLAIM-1: ...

### Gate Results
- Blast radius: PASS / NEEDS REVIEW / DO NOT CLAIM FIXED - [report or summary]
- Review trap replay: PASS / FAIL / not applicable - [artifact, proof, or applicability summary]
- Business review: PASS / REVISE / BLOCK / not applicable - [why]
- Zoom-out: completed / not applicable - [why]

### Review Trap Replay
| Source | Trap / invariant | Applies? | Local proof | Result |
|---|---|---|---|---|
| PR review / blast-radius / prove-it / Cursor / Copilot | ... | APPLIES / NOT APPLICABLE | Command, browser proof, DB query, source evidence | PASS / FAIL |

### Local Proof Misses
| Source | Missed invariant | Local proof added | Skill/runbook updated | Result |
|---|---|---|---|---|
| Cursor / Copilot / human PR thread | ... | Command, browser proof, DB query, or canary | Path or blocker | PASS / FAIL |

### Runtime Evidence
| Claim | Proof surface | Evidence | Result |
|---|---|---|---|
| CLAIM-1 | Browser/API/DB/worker/integration/etc. | Command, URL, screenshot, query, log, or observed state | PROVED/PARTIAL/FAILED |

### Counterexample Tried
- Case: ...
- Evidence: ...
- Result: PASSED / FAILED / BLOCKED

### Side Effects
- Destination checked: ...
- Evidence: ...
- Result: ...

### Trace Boundaries
- Could not prove: ...
- Why: ...
- Verdict impact: ...

### Verdict
PROVED / PARTIALLY PROVED / UNPROVED / DO NOT CLAIM FIXED

### Gate Result
PASS only when Verdict is PROVED. Otherwise FAIL.
```

## Verdict Rules

Choose exactly one verdict:

- `PROVED`: every claim has runtime evidence at the highest available surface, `blast-radius` has no blocking findings, review-derived traps were replayed or proven not applicable, required `business-review` passed, all side effects are confirmed, mock boundaries are covered by real proof, and realistic counterexamples were tried.
- `PARTIALLY PROVED`: failed proof gate. Some runtime evidence exists, but an important edge case, side effect, non-blocking gate, mock boundary, or claim mapping is incomplete.
- `UNPROVED`: code/tests changed, but the real runtime behavior was not proven at the required surface.
- `DO NOT CLAIM FIXED`: a blocking gate failed, a counterexample failed, required browser proof is missing, or the evidence shows the broken workflow still fails.

Be literal. A failed or missing proof is a useful result; it prevents a false completion claim.
Do not open a ready PR, mark a task done, or call a lane complete on anything except `PROVED`.
