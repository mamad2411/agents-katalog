---
name: statement-auditor
description: Run a Codex LP statement audit workflow that isolates statement ingestion, ties the batch to the NAV pack, and stages a sign-off workbook for human approval.
---

# Statement Auditor Task Pack

Use this task pack when the user needs a pre-distribution LP statement audit and sign-off packet.

Before running:

- read [`references/workers.md`](./references/workers.md)
- read [`../finance-modeling-office-pro/references/source-inventory.md`](../finance-modeling-office-pro/references/source-inventory.md) for provenance
- use the reusable skill content under `codex/skills/fund-admin/`
- use [`docs/runtime/spreadsheets.md`](../finance-modeling-office-pro/references/runtime-spreadsheets.md) for workbook output discipline

## Inputs

Minimum inputs:

- statement batch identifier
- statement files
- fund NAV pack or trusted NAV source

Optional inputs:

- prior exception log
- distribution deadline
- sign-off template

## Output Contract

Primary artifacts:

- `./out/signoff-<batch>.xlsx`
- `./out/signoff-<batch>.md`

Supporting scratch files are allowed under:

- `./out/tmp/statement-auditor/`

## Connector Gate

Preferred connector:

- `nav`

If the connector is unavailable, continue only if the trusted NAV pack is already local and complete. State the fallback source explicitly.

## Task-Pack Flow

1. Scope the batch and trusted NAV source.
2. Extract statement facts from untrusted files.
3. Recompute and tie out the capital accounts.
4. Write the sign-off workbook.
5. Verify and stop for human approval.

## Phase 1: Scope The Batch

- Confirm the batch, fund, and investor scope.
- Confirm whether this is a full distribution run or a targeted re-audit.
- Label the generated statements as untrusted upstream outputs.

## Phase 2: Extract Statement Facts

Target artifact:

- `./out/tmp/statement-auditor/statement-facts.md`

Capture:

- beginning and ending balances
- contributions and distributions
- fee and expense lines
- any malformed or missing fields

If delegation is available and explicitly authorized, this phase maps to `stmt-statement-reader`.

## Phase 3: Recompute And Tie Out

Use:

- `nav-tieout`

Target artifact:

- `./out/tmp/statement-auditor/tieout-result.md`

Rules:

- recompute from trusted NAV components
- flag both numeric mismatches and missing-support issues
- distinguish hard failures from soft review flags

If delegation is available and explicitly authorized, this phase maps to `stmt-reconciler`.

## Phase 4: Write The Sign-Off Workbook

Write:

- `./out/signoff-<batch>.xlsx`

The workbook should contain:

- batch summary
- investor-level tie-out results
- hold or release recommendation per statement
- follow-up items

If delegation is available and explicitly authorized, this phase maps to `stmt-flagger`.

## Phase 5: Verify And Stop

Run:

- `python scripts/verify_xlsx.py ./out/signoff-<batch>.xlsx`

Write the review memo to:

- `./out/signoff-<batch>.md`

The review memo must state:

- output paths
- connector availability
- tie-out completion status
- hold or release counts
- residual risk before investor-relations sign-off

Do not treat the output as an automatic release authorization.
