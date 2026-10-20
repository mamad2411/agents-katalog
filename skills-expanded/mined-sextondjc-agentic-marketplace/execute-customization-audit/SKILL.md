---
name: execute-customization-audit
description: Use when producing the executive governance report as a single, aggregated output derived from existing governance audit artifacts.
---

# Execute Customization Audit

## Specialization

Produce one executive-level governance audit report by aggregating existing governance audit artifacts.

This skill is aggregation-only. It must not perform standalone item/type governance audits as primary evidence.

## Trigger Conditions

Invoke this skill when any of the following is true:

- An executive governance disposition is requested.
- Type and item audits exist and need one reconciled executive disposition.
- Leadership needs a single report with roll-up status and failure reasoning.

## Required Inputs

- Audit date (`YYYY-MM-DD`).
- Target scope (`full-workspace` by default).
- Required source artifacts:
  - `.docs/changes/governance/audits/governance-audit.md`
  - `.docs/changes/skill/reviews/governance-audit-types-skills.md`
  - `.docs/changes/customization/reviews/governance-audit-types-customizations.md`
  - `.docs/changes/customization/reviews/governance-audit-types-optimization.md`
- Report template guidance: [README.md](./references/README.md)

## Executive Standards

| ID | Standard | Type | Pass Criteria | Failure Action |
|---|---|---|---|---|
| EXE-M1 | Single report output | MUST | Exactly one executive report is produced for the run. | Mark failed and stop publication until consolidated into one report. |
| EXE-M2 | Failure matrix position and detail | MUST | Failure matrix appears near top and includes explicit reason why each source audit failed. | Mark failed and move matrix to required order with reason detail rows. |
| EXE-M3 | Any fail rolls up to executive fail | MUST | A single `Fail` outcome from any source level forces executive `FAILED`. | Mark failed if executive disposition is not `FAILED`. |
| EXE-M4 | Required section order | MUST | Report starts with Executive Briefing, then Aggregate Outcome Grid, Failure Matrix, Per-Type Results, Ranked Recommendations. | Mark failed and reorder sections before publication. |
| EXE-M5 | Human-readable evidence links | MUST | Evidence is markdown hyperlinks to human-readable markdown artifacts; script files and raw JSON are not used as primary evidence links. | Mark failed and replace evidence with human-readable markdown links. |

## Required Outputs

- Single report at `.docs/changes/governance/audits/execute-customization-audit.md`.
- Required report sections in this order:
  1. Executive Briefing
  2. Aggregate Outcome Grid
  3. Failure Matrix
  4. Per-Type Results
  5. Ranked Recommendations
- Optional sections (after required sections):
  - Delta vs Prior Grid
  - Evidence Index
  - Open Decisions Grid
- Final disposition (`PASSED`, `FAILED`, `PROVISIONAL-FAILED`).

## Workflow

1. Verify all required source artifacts exist for the target date.
2. If any required source artifact is missing, produce `PROVISIONAL-FAILED` with missing-source rows.
3. Aggregate source outcomes into one executive outcome grid.
4. Build failure matrix near the top with explicit failure reasoning per failing source.
5. Build per-type roll-up rows with outcomes, MUST fail counts, SHOULD advisory counts, and evidence links.
6. Set final disposition using strict roll-up rule: any single source `Fail` -> executive `FAILED`.
7. Ensure evidence links are markdown links to human-readable markdown artifacts.
8. Render report using the template guidance in [README.md](./references/README.md).
9. Save the single report to the required output path.

## Done Criteria

- Exactly one executive report was produced.
- Report section order matches EXE-M4.
- Failure matrix appears near top and includes failure reasons.
- Final disposition respects EXE-M3 roll-up rule.
- Evidence links are human-readable markdown links only.

