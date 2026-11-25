---
name: shift
description: Spec versioning + reverse-drift detection. Use when a spec changes after lock, or /shift. Not for COSMETIC-only edits or pre-lock spec work.
---

# Shift

Specs change. Implementations drift. You detect both with precision. You classify what changed in the
spec (semantic diff) and detect when the implementation has moved away from it (reverse drift). You do
not fix — you surface. Domain-neutral: a "spec" is any durable contract (a task card, an interface, a
model's assumption ledger, a curriculum's learning objectives).

## What this does / does not do

Does: receive two versions of a spec artifact, classify the change, detect reverse drift against the
implementation, identify affected downstream consumers, decide whether a loop-back is required, and
write a receipt + compatibility report. Does **not**: fix drift, edit the spec or implementation, or
coordinate the migration (that is a human + executor's job when loop-back fires).

## When NOT to use

- The change is COSMETIC only (docs, a rename with no behavior change, whitespace) — there is nothing
  to classify or cascade.
- No prior version of the spec exists to diff against — there is no delta to classify.

## Reference Routing

| Situation | Reference |
|---|---|
| Receipt write delegation | `engine/shared/references/script-delegation-contract.md` |

## Inputs

| Field | Required | Description |
|---|---|---|
| `spec_before` | yes | previous spec version (from archive or VCS) |
| `spec_after` | yes | current spec version |
| `implementation_path` | for drift check | the implementation to check against the spec |
| `consumer_list` | no | module/artifact IDs that depend on this spec |

## How to do it

### Step 1 — Classify the change (semantic diff)

| Class | Definition |
|---|---|
| `BREAKING` | removes or incompatibly changes existing behavior — callers must change |
| `DEPRECATION` | marks behavior for future removal with a declared sunset |
| `ADDITIVE` | new capability alongside existing behavior — no consumer change required |
| `COSMETIC` | docs, rename with no behavior change, whitespace |

A single change may produce multiple classes (e.g. DEPRECATION + ADDITIVE when one path is deprecated
and a replacement added). Record all that apply. When in doubt between ADDITIVE and BREAKING: if any
existing consumer must change to accommodate the change, it is BREAKING.

### Step 2 — Detect reverse drift

Compare the implementation against `spec_after`. Reverse drift = the implementation was edited without a
spec update, OR the spec was updated without the implementation following (the most common pattern).
Record `reverse_drift_detected` and `reverse_drift_details`.

### Step 3 — Downstream consumer impact

For each consumer in `consumer_list`, determine whether the change touches an interface it calls, a
schema it validates against, or a behavior it depends on. Record `downstream_consumers_affected` and
`affected_consumer_ids`.

### Step 4 — Loop-back decision

If `BREAKING` AND any downstream consumer is affected: set `loop_back_required: true` — the originating
pipeline must surface to the user before proceeding (breaking changes need migration coordination). Do
not suppress this signal.

### Step 5 — Write the report + receipt

Write the compatibility report and semantic diff to `<workspace>/shift/`; then the receipt.

> Note: the v6 helper scripts (semantic-differ, reverse-drift-detector, compatibility-checker) are not
> yet ported to v7 (tracked in source-coverage.md). Until they are, perform the classification and drift
> reasoning directly and record it; the contract above is unchanged.

## Output Contract

**shift receipt** (`<workspace>/receipts/shift-receipt-<timestamp>.json`): base + `change_class`
(array — all that apply), `reverse_drift_detected`, `reverse_drift_details`,
`downstream_consumers_affected`, `affected_consumer_ids`, `compatibility_report_path`,
`semantic_diff_path`, `loop_back_required`. persistence: Spec-Anchored.

## Proactive Triggers

- **A change touches an existing caller's required behavior**: it is BREAKING, not ADDITIVE — classify
  conservatively; test against all known callers.
- **The spec was updated but the implementation was not**: reverse drift — the most common pattern;
  always run the drift check on the post-change implementation.
- **`loop_back_required: true`**: do not suppress — a human must coordinate consumer migration before
  the change ships.
- **A single change deprecates one path and adds another**: record BOTH classes; do not collapse to one.
- **No prior spec version exists**: there is no delta — do not fabricate a classification.

## Completion Criteria

**Done when:** a shift receipt is written with the change class(es), the reverse-drift result, the
consumer impact, and the loop-back decision; the compatibility report exists.

**Not done if:** a BREAKING change with affected consumers was written without `loop_back_required:
true`; the drift check was skipped; shift edited the spec or implementation.

**Next step:** if `loop_back_required`, the originating pipeline surfaces to the user; otherwise the
change proceeds. Downstream specs touched by a BREAKING change are marked NEEDS_REVERIFICATION.

## Related Skills

- **archive**: Triggers shift post-archive on a BREAKING/ADDITIVE spec change. NOT a classifier itself.
- **specify**: Owns the change-class declaration on the task card; shift verifies the realized delta against it.
- **executor**: Fixes drift shift surfaces. NOT shift's job — it surfaces, executor fixes.
