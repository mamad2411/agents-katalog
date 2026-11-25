---
name: valuation-reviewer
description: Run a Codex portfolio valuation review workflow that ingests GP materials, cross-checks them against trusted portfolio data, and stages an LP-ready review pack for sign-off.
---

# Valuation Reviewer Task Pack

Use this task pack when the user needs a quarter-end or package-level valuation review, not a deal-underwriting model build.

Before running:

- read [`references/workers.md`](./references/workers.md)
- read [`../finance-modeling-office-pro/references/source-inventory.md`](../finance-modeling-office-pro/references/source-inventory.md) for provenance
- use the reusable skill content under `codex/skills/private-equity/`
- use [`docs/runtime/spreadsheets.md`](../finance-modeling-office-pro/references/runtime-spreadsheets.md) for workbook output discipline

## Inputs

Minimum inputs:

- fund name
- GP valuation package files
- reporting period

Optional inputs:

- prior quarter pack
- portfolio-company list
- return-threshold or reviewer commentary template

## Output Contract

Primary artifacts:

- `./out/lp-pack-<fund>.xlsx`
- `./out/valuation-review-<fund>.md`

Supporting scratch files are allowed under:

- `./out/tmp/valuation-reviewer/`

## Connector Gate

Preferred connector:

- `portfolio`

If the connector is unavailable, continue only if the trusted portfolio data required for the tie-out is already local. State the limitation clearly.

## Task-Pack Flow

1. Scope the package and review target.
2. Extract structured facts from untrusted GP materials.
3. Re-run the valuation review against trusted portfolio data.
4. Assemble the LP review pack.
5. Verify and stop for IR and finance review.

## Phase 1: Scope The Review

- Confirm the fund and reporting period.
- Confirm whether the package is a full-quarter pack or a targeted portco update.
- Label GP-provided materials as untrusted inputs.

## Phase 2: Extract Structured Package Facts

Target artifact:

- `./out/tmp/valuation-reviewer/package-facts.md`

Capture:

- reported marks
- valuation methodology notes
- portfolio-company KPIs
- unresolved package gaps

If delegation is available and explicitly authorized, this phase maps to `valuation-package-reader`.

## Phase 3: Re-Run The Review

Use:

- `portfolio-monitoring`
- `returns-analysis` when scenario stress checks are required

Target artifact:

- `./out/tmp/valuation-reviewer/review-result.md`

Rules:

- distinguish GP-reported marks from reviewer-adjusted views
- tie every challenge flag to trusted supporting data
- state whether the portfolio connector or local portfolio files were used

If delegation is available and explicitly authorized, this phase maps to `valuation-runner`.

## Phase 4: Assemble The LP Review Pack

Write:

- `./out/lp-pack-<fund>.xlsx`

The workbook should contain:

- fund summary
- portfolio-company review table
- mark or methodology flags
- follow-up questions and release notes

If delegation is available and explicitly authorized, this phase maps to `valuation-publisher`.

## Phase 5: Verify And Stop

Run:

- `python scripts/verify_xlsx.py ./out/lp-pack-<fund>.xlsx`

Write the review memo to:

- `./out/valuation-review-<fund>.md`

The review memo must state:

- output paths
- connector availability
- challenged marks or packages
- what verification ran
- residual risk before LP distribution

Do not position the pack as final external reporting without human sign-off.
