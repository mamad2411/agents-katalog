---
name: audit-customization-types
description: Use when auditing customization types and cross-type interactions across agents, instructions, prompts, and skills with deterministic, grid-first governance outcomes.
---

# Audit Customization Types

## Specialization

Evaluate governance at the type layer across customization domains (`agents`, `instructions`, `prompts`, `skills`) and produce audit outcomes that identify type-level and cross-type conflicts, interaction failures, and remediation priorities.

This skill is singular in objective: type governance audit and cross-type interaction audit.

## Review Mode

- Default mode is report-only.
- Do not modify customization artifacts during review unless the user explicitly asks for remediation edits.

## Normative Language

- MUST: Mandatory requirement. Failure means the audited type posture fails.
- SHOULD: Advisory requirement. Failure does not auto-fail, but requires recommendation and tracking.

## Standards

Use these standards exactly:

| ID | Standard | Type | Pass Criteria | Failure Action |
|---|---|---|---|---|
| TYP-M1 | Type coverage completeness | MUST | Audit covers all in-scope types requested (`agents`, `instructions`, `prompts`, `skills`) with explicit included/excluded scope rows. | Mark failed; re-run with complete type scope declaration. |
| TYP-M2 | Interaction matrix completeness | MUST | Every evaluated pair has an explicit result row in the type matrix (same-type and cross-type where in scope). | Mark failed; add missing pair rows and status. |
| TYP-M3 | Evidence traceability | MUST | Each failed or advisory interaction finding links to concrete item-level evidence (file paths and check IDs). | Mark failed; add evidence links before finalizing. |
| TYP-M4 | Deterministic disposition contract | MUST | Final disposition is derived from defined rule set (MUST failures and open blocking conflicts) and reported consistently. | Mark failed; restate disposition using deterministic rule set. |
| TYP-M5 | Severity mapping consistency | MUST | Interaction failures are assigned severity using one explicit severity mapping table and applied consistently across all failure rows. | Mark failed; add or correct severity mapping and reclassify failures consistently. |
| TYP-S1 | Same-type non-conflict and non-failure | SHOULD NOT conflict | Artifacts within the same type do not conflict or cause another artifact in that type to fail execution. | Record advisory; recommend type-local resolution plan and owner. |
| TYP-S2 | Cross-type non-conflict and non-failure | SHOULD NOT conflict | Artifacts across different types do not conflict or cause another type to fail execution. | Record advisory; recommend cross-type resolution plan and owner. |
| TYP-S3 | Boundary clarity | SHOULD | Type responsibilities and boundaries are explicit and do not duplicate another type's primary responsibility. | Record advisory; recommend boundary clarification and mapping updates. |
| TYP-S4 | Catalog and taxonomy parity | SHOULD | Lifecycle catalogs and taxonomy references reflect current type responsibilities and active audit skills. | Record advisory; recommend catalog/taxonomy updates. |
| TYP-S5 | Brevity | SHOULD | Type-audit wording is economical and avoids repetitive narrative outside required evidence grids. | Record advisory; recommend concise reductions while preserving evidence quality. |
| TYP-S6 | Growth governance alignment | SHOULD | Type-level outcomes follow growth discipline: reuse-before-create, anti-duplication, delta-first remediation, and explicit auditability. | Record advisory; recommend minimal, self-contained consolidation and scope-tight remediations. |

## Trigger Conditions

Invoke this skill when any condition below is true:

- A type-level governance audit is requested.
- Cross-type conflicts or execution failures are suspected.
- Multiple item-level audits need reconciliation at the type layer.
- A governance release/cadence check requires type and cross-type status.

## Inputs

Required inputs:

- Target scope: `all` or one/more of `agents`, `instructions`, `prompts`, `skills`, `cross-type`.
- Audit date in ISO format (`YYYY-MM-DD`).
- Evidence roots for item-level findings (`.docs/changes/**` and relevant customization roots).

Optional inputs:

- Prior type-audit report path for delta comparison.
- Conflict focus matrix (specific pairs only).
- Source catalog file path (default: `./references/source-catalog.md`).
- Maximum age threshold in days for source freshness (default: 30).

## Source Governance Rules

- Keep the source catalog in Markdown grid format.
- Every source row MUST include: Source, What It Provides, Why It Is Valuable, In Use (Yes or No), Last Evaluated (YYYY-MM-DD), Current Status (Current, Needs Review, Deprecated).
- Mark a source as Needs Review when Last Evaluated exceeds the freshness threshold.
- Mark a source as Deprecated when it is no longer maintained or no longer relevant to type-level governance audit.
- Do not remove historical sources without adding a short deprecation note in the Notes column.
- Re-evaluate sources before publishing standards recommendations that depend on current platform behavior.

## Required Outputs

- A type-level governance audit report using [audit-customization-types-report-template.md](./references/audit-customization-types-report-template.md).
- Review result summaries MUST be returned in Markdown grid format (tables), not prose lists.
- Output report MUST include same-type and cross-type interaction grids with explicit pair outcomes.
- Output report MUST include a severity mapping grid used to classify interaction failures.
- Report outputs MUST be stored under `.docs/changes/governance/type-audits/`.
- Recommended report path: `.docs/changes/governance/type-audits/audit-customization-types.md`.
- Source-governance summary when source validation is requested.
- Updated [source-catalog.md](./references/source-catalog.md) when source tracking changes are made.

#### Violation Code Legend

| Code Prefix | Standard | Type | Skill Source |
|---|---|---|---|
| TYP-M* | Mandatory type-governance check | MUST | audit-customization-types |
| TYP-S* | Advisory type-governance check | SHOULD | audit-customization-types |

## Workflow

1. Resolve requested type scope and build the interaction matrix (same-type and cross-type pairs).
2. Collect current item-level evidence from audited artifact sets and recent review outputs.
3. Re-evaluate tracked sources in [source-catalog.md](./references/source-catalog.md) for freshness before source-sensitive guidance.
4. Run `test-type-interaction-matrix.ps1` (from `.github/scripts/powershell/`) to validate interaction-pair coverage and failure-propagation totals when a prior or in-progress report exists.
5. Evaluate TYP-M* standards first with evidence.
6. Evaluate TYP-S* standards with evidence.
7. Validate growth-governance alignment before final disposition: duplication control, reuse-before-create, delta-first remediation, and explicit review outputs.
8. For each interaction pair, record disposition (`Pass`, `Advisory`, `Fail`, `Blocked`) and linked evidence.
9. Assign failure severities using one explicit severity mapping table and apply it consistently.
10. Produce deterministic final disposition from MUST failures and open blocking conflicts.
11. Produce ranked recommendations with owners and priority.
12. If a conflict is detected, include resolution options and required follow-up checks.
13. Confirm deterministic coverage: each requested outcome is mapped to a report artifact or explicit decision.

## Output Format Rules

- MUST return outcomes in Markdown grid format.
- MUST include these grids in order:
  1. Type Scope Grid
  2. Standards Outcome Grid
  3. Same-Type Interaction Grid
  4. Cross-Type Interaction Grid
  5. Severity Mapping Grid
  6. Failure Detail Grid
  7. Ranked Recommendations Grid
  8. Disposition Grid
- MUST include at least one X of Y metrics grid.
- SHOULD keep narrative concise and place it after the grids.

## Storage Rules

- Store type-audit reports under `.docs/changes/governance/type-audits/`.
- Use descriptive file names: `audit-customization-types.md` (versioned names allowed for reruns, for example `audit-customization-types-v2.md`).

## Done Criteria

An audit is complete only when:

- All MUST and SHOULD checks were executed with evidence.
- Required grids were produced in the required order.
- Same-type and cross-type interaction matrices were fully populated for in-scope pairs.
- Severity mapping was defined and applied consistently across failure rows.
- Final disposition is deterministic and traceable to standards outcomes.
- Source-catalog freshness was checked when source-sensitive recommendations are present.
