---
name: model-builder
description: Coordinate a new-from-scratch financial model build in Codex using the imported financial-services skills. Use when the user wants a DCF, LBO, three-statement, or comps model built from a ticker plus assumptions, and the workflow should be run with explicit sequencing, artifact contracts, and review gates.
---

# Model Builder Coordinator

Use this coordinator when the task is to build a fresh financial model from scratch, not to update an existing coverage model.

Before running:

- read [`references/workers.md`](./references/workers.md)
- read [`../finance-modeling-office-pro/references/source-inventory.md`](../finance-modeling-office-pro/references/source-inventory.md) for provenance if you need to compare the original managed-agent decomposition
- use the canonical source skills under `plugins/vertical-plugins/financial-analysis/skills/`

## Inputs

Minimum inputs:

- target company or ticker
- model type: `dcf`, `lbo`, `3-statement`, or `comps`
- assumption set, or an explicit instruction to derive a first-pass assumption set

Optional inputs:

- user-provided template workbook
- projection period
- scenario set
- required output filename

## Output Contract

Primary artifacts:

- `./out/model.xlsx`
- `./out/model-review.md`

Supporting scratch files are allowed under:

- `./out/tmp/model-builder/`

## Coordinator Flow

1. Scope the ask.
2. Build a normalized input packet.
3. Build the workbook.
4. Audit the workbook.
5. Stop and surface for review.

## Phase 1: Scope The Ask

- Confirm the exact model type.
- Confirm whether a template file must be used.
- Confirm whether the user expects only the workbook or also a written review summary.
- If key assumptions are missing, create an explicit assumption checklist before building.

## Phase 2: Build A Normalized Input Packet

Target artifact:

- `./out/tmp/model-builder/input-packet.md`

The input packet should contain:

- target identifier
- chosen model type
- historical data summary
- consensus or market data summary if available
- explicit assumptions
- unresolved gaps labeled clearly

If delegation is available and explicitly authorized, this phase maps to the `model-data-puller` worker.

## Phase 3: Build The Workbook

Use the matching skill:

- `dcf-model`
- `lbo-model`
- `3-statement-model`
- `comps-analysis`

Use `xlsx-author` conventions for file production.

Rules:

- all calculations stay as formulas
- all outputs write to `./out/model.xlsx`
- all hardcoded inputs are sourced or marked `[ASSUMPTION]`
- all major sections are built in a reviewable order, not as one opaque final dump

If delegation is available and explicitly authorized, this phase maps to the `model-builder-builder` worker and owns the write scope:

- `./out/model.xlsx`
- `./out/tmp/model-builder/*`

## Phase 4: Audit The Workbook

Run both:

- logical/model audit using `audit-xls`
- repo-local verification using `python scripts/verify_xlsx.py ./out/model.xlsx`

Write findings to:

- `./out/model-review.md`

The review file must state:

- workbook path
- model type
- what was verified
- whether any formula errors were detected
- any residual risk, including static-only verification limits

If delegation is available and explicitly authorized, this phase maps to the `model-auditor` worker.

## Phase 5: Review Gate

Stop after the workbook and review note are complete.

Surface:

- output file path
- audit result
- unresolved assumptions
- any areas that need analyst review before downstream use

Do not proceed into downstream pitch or note generation inside this coordinator.
