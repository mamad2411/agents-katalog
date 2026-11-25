---
name: audit-instructions
description: Use when evaluating one or more workspace .instructions.md files for policy-domain integrity, applyTo scope correctness, and instruction-specific remediation guidance.
---

# Audit Instructions

## Specialization

Evaluate `.instructions.md` artifacts against instruction-governance standards and produce review outcomes (Pass, Pass With Advisories, Fail, Blocked) focused on policy-domain precision and rule scoping quality. Scope is singular: instruction quality review and follow-up governance.

This skill exists as a dedicated specialization for instruction-file audits so instruction review can use instruction-specific sources, storage, and outputs without sharing a mixed review workflow with agents or prompts.

## Review Mode

- Default mode is report-only.
- Do not modify instruction artifacts during review unless the user explicitly asks for remediation edits.

## Normative Language

- MUST: Mandatory requirement. Failure means the reviewed instruction fails.
- SHOULD: Advisory requirement. Failure does not auto-fail, but requires recommendation and tracking.

## Review Standards

Use these standards exactly:

| ID | Standard | Type | Pass Criteria | Failure Action |
|---|---|---|---|---|
| INR-M1 | Singular policy domain | MUST | File scope maps to one policy domain only. | Mark failed; recommend domain split or refocus. |
| INR-M2 | Valid frontmatter | MUST | `name`, `description`, and `applyTo` present when auto-application is required; YAML is valid and aligned with current VS Code custom instructions behavior. | Mark failed; provide exact frontmatter fix. |
| INR-M3 | `applyTo` is appropriately scoped | MUST | Pattern is not broader than the policy requires. Global `**` is used only for truly global rules. | Mark failed; recommend tighter pattern. |
| INR-M4 | No task workflow content | MUST | No multi-step decision trees or procedures. Policy mandates only. | Mark failed; recommend migrating workflow content to a skill or prompt. |
| INR-S1 | No conflict with other instruction files | SHOULD NOT conflict | No harmful overlap or contradictory rules with other active instruction files. | Record advisory finding and recommend escalation to type-governance audit for conflict resolution. |
| INR-S2 | Rationale present for non-obvious rules | SHOULD | Non-obvious mandates include a brief rationale comment. | Record advisory finding; recommend rationale addition. |
| INR-S3 | No conflict with agent or skill boundaries | SHOULD NOT conflict | Instruction behavior does not contradict active agent personas or skill boundaries. | Record advisory finding and recommend escalation to type-governance audit for boundary resolution. |
| INR-S4 | Brevity | SHOULD | Instruction wording is economical, avoids duplication, and does not include narrative padding beyond what policy clarity requires. | Record advisory finding; recommend concise reductions. |
| INR-S5 | Growth governance alignment | SHOULD | Instruction changes follow growth discipline: reuse-before-create, anti-duplication, delta-first edits, and explicit auditability. | Record advisory finding and recommend minimal, self-contained consolidation. |

## Trigger Conditions

Invoke this skill when any condition below is true:

- A new `.instructions.md` file is created.
- An existing `.instructions.md` file is modified.
- A periodic quality audit of workspace instruction files is requested.
- An instruction file fails discovery, invocation, or behavior expectations.
- A source-catalog freshness check is needed to verify current `.instructions.md` behavior and file-location rules.

## Inputs

Required inputs:

- Target instruction name or explicit list of target instruction files.
- Workspace instructions root path (default: `.github/instructions/`).
- Review date in ISO format (`YYYY-MM-DD`).

Optional inputs:

- Previous review artifact path if already known.
- Change request or incident context.
- Source catalog file path (default: `./references/source-catalog.md`).
- Maximum age threshold in days for source freshness (default: 30).

## Source Governance Rules

- **BLOCKING**: Read [source-catalog.md](./references/source-catalog.md) BEFORE producing any findings. Platform-specific assessments — including valid frontmatter fields, `applyTo` semantics, file-location rules, and auto-application behavior — MUST be grounded in the source catalog, not inferred from workspace scripts or local tooling whose contracts may be stale.
- Keep the source catalog in Markdown grid format.
- Every source row MUST include: Source, What It Provides, Why It Is Valuable, In Use (Yes or No), Last Evaluated (YYYY-MM-DD), Current Status (Current, Needs Review, Deprecated).
- Mark a source as Needs Review when Last Evaluated exceeds the freshness threshold.
- Mark a source as Deprecated when it is no longer maintained or no longer relevant to instruction review.
- Do not remove historical sources without adding a short deprecation note in the Notes column.
- Re-evaluate sources before finalizing frontmatter, location, and apply-pattern recommendations. If any source is Needs Review, resolve it before issuing source-sensitive recommendations.

## Required Outputs

- A per-instruction review report stored using template: [audit-instructions-report-template.md](./references/audit-instructions-report-template.md).
- A conflict report is not produced by this skill; conflict detection across instructions or with other customization types is a type-governance concern.
- Updated per-instruction history at: `.docs/changes/instruction/history/<instruction-name>-history.md`.
- Review result summaries MUST be returned in Markdown grid format (tables), not prose lists.
- Aggregate multi-instruction results MUST include at least one consolidated grid with per-instruction outcomes.
- Per-instruction review files MUST be stored under `.docs/changes/instruction/reviews/<instruction-name>/`.
- Reasoning package per reviewed instruction: assumptions, trade-offs, blockers, and one recommendation.
- Source-governance summary when source validation is requested.
- Updated [source-catalog.md](./references/source-catalog.md) when source tracking changes are made.

#### Violation Code Legend

| Code Prefix | Standard | Type | Skill Source |
|---|---|---|---|
| INR-M* | Mandatory instruction quality check | MUST | audit-instructions |
| INR-S* | Advisory instruction quality check | SHOULD | audit-instructions |

## Workflow

1. Resolve target instructions and collect current `.instructions.md` files.
2. Load the per-instruction history file from `.docs/changes/instruction/history/` before analysis.
3. Build a recommendation deny-list from history entries marked Rejected, Removed, or Illegitimate.
4. Re-evaluate tracked sources in [source-catalog.md](./references/source-catalog.md) for freshness and current `.instructions.md` behavior before source-sensitive checks.
5. Build coverage across all mandatory branches: policy-domain scope, frontmatter validity, `applyTo` precision, workflow leakage, instruction-file conflicts, boundary conflicts, brevity, source alignment, and history alignment.
6. Verify growth-governance alignment: duplication control, reuse-before-create, delta-first edits, and explicit review outputs.
7. Evaluate all INR-M* and INR-S* checks with evidence.
8. Evaluate source alignment against the current source-catalog state: file locations, frontmatter semantics, recursive discovery behavior, `applyTo` usage, and when instructions are auto-applied versus manually attached.
9. Produce Pass or Fail for MUST standards and advisory outcome for SHOULD standards.
10. For each failed or advisory check, record assumptions, trade-offs, blockers, and one recommendation.
11. Update the instruction history file with findings, decisions, and recommendation statuses.
12. Confirm deterministic coverage: each requested outcome is mapped to a report artifact or explicit decision.

## Output Format Rules

- MUST return review outcomes in Markdown grid format.
- MUST present aggregate results using a single consolidated grid with columns: Instruction, Outcome, MUST Failures, SHOULD Advisories, Report.
- SHOULD include a small aggregate metrics grid for totals (Pass, Pass With Advisories, Fail, Blocked).
- SHOULD keep narrative concise and place it after the grids.

## Storage Rules

- Store each instruction review under `.docs/changes/instruction/reviews/<instruction-name>/`.
- Use descriptive file names: `review.md`. Use versioned names (for example, `review-v2.md`) to disambiguate repeated runs.
- Keep aggregate cross-instruction summaries in `.docs/changes/instruction/reviews/`.

## History Management Rules

- Keep one history file per reviewed instruction at `.docs/changes/instruction/history/<instruction-name>-history.md`.
- Append new review entries; never rewrite prior decisions.
- Track each recommendation with status: Proposed, Accepted, Rejected, Removed, Implemented.
- Before publishing recommendations, remove any item that matches prior Rejected or Removed entries unless the user explicitly re-opens it.

## Done Criteria

A review is complete only when:

- All MUST and SHOULD checks were executed with evidence.
- Required report artifacts were written.
- History was updated for every reviewed instruction.
- Reasoning package entries are present for failed and advisory findings.
- Source-catalog freshness was checked and source-sensitive findings are grounded in a current source evaluation.
