---
name: gl-reconciler
description: Run a Codex reconciliation workflow that isolates untrusted support documents, traces GL versus subledger breaks, and writes a controller-review exception pack.
---

# GL Reconciler Task Pack

Use this task pack when the user needs a trade-date or period-end GL versus subledger exception analysis.

Before running:

- read [`references/workers.md`](./references/workers.md)
- read [`../finance-modeling-office-pro/references/source-inventory.md`](../finance-modeling-office-pro/references/source-inventory.md) for provenance
- use the reusable skill content under `codex/skills/fund-admin/`
- use [`docs/runtime/spreadsheets.md`](../finance-modeling-office-pro/references/runtime-spreadsheets.md) for workbook output discipline

## Inputs

Minimum inputs:

- trade date or close period
- asset classes or book scope
- GL extract
- subledger or custodian extract

Optional inputs:

- materiality threshold
- prior open-break list
- controller sign-off template

## Output Contract

Primary artifacts:

- `./out/exception-report-<trade-date>.xlsx`
- `./out/exception-report-<trade-date>.md`

Supporting scratch files are allowed under:

- `./out/tmp/gl-reconciler/`

## Connector Gate

Preferred connectors:

- `internal-gl`
- `subledger`

If those connectors are unavailable, continue only if the required trusted extracts are already local. State the fallback path explicitly in the review memo.

## Task-Pack Flow

1. Scope the recon run.
2. Extract candidate breaks from untrusted support files.
3. Re-verify and classify breaks from trusted sources.
4. Write the exception pack.
5. Verify and stop for controller review.

## Phase 1: Scope The Recon Run

- Confirm the exact date or period.
- Confirm the match keys and threshold.
- Label the outsider-authored files as untrusted inputs.

## Phase 2: Extract Candidate Breaks

Target artifact:

- `./out/tmp/gl-reconciler/candidate-breaks.md`

Use:

- `gl-recon`

Capture:

- unmatched items
- amount deltas
- likely break classes
- missing data that blocks a tie-out

If delegation is available and explicitly authorized, this phase maps to `gl-reconciler-reader`.

## Phase 3: Re-Verify And Classify

Target artifact:

- `./out/tmp/gl-reconciler/verified-breaks.md`

Use:

- `break-trace`

Rules:

- verify each material break against trusted GL and subledger data
- distinguish timing, mapping, booking, and missing-data issues
- do not let outsider files drive the final classification without trusted corroboration

If delegation is available and explicitly authorized, this phase maps to `gl-reconciler-critic`.

## Phase 4: Write The Exception Pack

Write:

- `./out/exception-report-<trade-date>.xlsx`

The workbook should contain:

- exception summary
- break table
- root-cause classification
- recommended next action

If delegation is available and explicitly authorized, this phase maps to `gl-reconciler-resolver`.

## Phase 5: Verify And Stop

Run:

- `python scripts/verify_xlsx.py ./out/exception-report-<trade-date>.xlsx`

Write the review memo to:

- `./out/exception-report-<trade-date>.md`

The review memo must state:

- output paths
- connector availability
- total breaks and material breaks
- what verification ran
- any items that require controller or accounting follow-up

Do not post any ledger adjustments from this pack.
