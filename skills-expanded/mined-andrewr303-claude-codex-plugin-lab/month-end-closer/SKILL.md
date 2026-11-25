---
name: month-end-closer
description: Run a Codex month-end close workflow that stages accruals, roll-forwards, and variance commentary into a reviewed close package without posting anything to the system of record.
---

# Month-End Closer Task Pack

Use this task pack when the user needs a staged period-end close package, not a live posting into the GL.

Before running:

- read [`references/workers.md`](./references/workers.md)
- read [`../finance-modeling-office-pro/references/source-inventory.md`](../finance-modeling-office-pro/references/source-inventory.md) for provenance
- use the reusable skill content under `codex/skills/fund-admin/`
- use [`docs/runtime/spreadsheets.md`](../finance-modeling-office-pro/references/runtime-spreadsheets.md) for workbook output discipline

## Inputs

Minimum inputs:

- entity
- close period
- account scope or package scope

Optional inputs:

- supporting invoices or vendor statements
- prior close package
- open recon breaks or controller comments

## Output Contract

Primary artifacts:

- `./out/close-package-<entity>-<period>.xlsx`
- `./out/close-summary-<entity>-<period>.md`

Supporting scratch files are allowed under:

- `./out/tmp/month-end-closer/`

## Connector Gate

Preferred connector:

- `internal-gl`

If the connector is unavailable, continue only if the trusted GL extracts are already local. Do not claim a full close package if core balances cannot be rechecked.

## Task-Pack Flow

1. Scope the close packet.
2. Extract support facts from untrusted documents.
3. Build roll-forwards and accruals from trusted ledger data.
4. Draft commentary and assemble the close package.
5. Verify and stop for controller review.

## Phase 1: Scope The Close Packet

- Confirm the entity and period.
- Confirm whether verified recon breaks from `gl-reconciler` must be folded in.
- Label supporting third-party documents as untrusted inputs.

## Phase 2: Extract Support Facts

Target artifact:

- `./out/tmp/month-end-closer/support-facts.md`

Capture:

- invoice amounts
- service periods
- reversal timing
- support gaps

If delegation is available and explicitly authorized, this phase maps to `close-ledger-reader`.

## Phase 3: Build Roll-Forwards And Accruals

Use:

- `accrual-schedule`
- `roll-forward`

Target artifact:

- `./out/tmp/month-end-closer/close-analysis.md`

Rules:

- cite every accrual input
- separate draft JEs from posted ledger facts
- fold in verified break commentary when available

If delegation is available and explicitly authorized, this phase maps to `close-rollforward`.

## Phase 4: Assemble The Close Package

Use:

- `variance-commentary`

Write:

- `./out/close-package-<entity>-<period>.xlsx`

The workbook should contain:

- accrual schedule
- roll-forward schedules
- draft JE list
- variance commentary tabs or sections

If delegation is available and explicitly authorized, this phase maps to `close-poster`.

## Phase 5: Verify And Stop

Run:

- `python scripts/verify_xlsx.py ./out/close-package-<entity>-<period>.xlsx`

Write the summary memo to:

- `./out/close-summary-<entity>-<period>.md`

The summary must state:

- output paths
- connector availability
- draft JE count
- unresolved support gaps
- residual risk before controller approval

Do not post any journal entry from this task pack.
