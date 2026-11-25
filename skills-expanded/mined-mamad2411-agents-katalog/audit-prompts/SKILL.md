---
name: audit-prompts
description: Use when evaluating one or more workspace .prompt.md files for prompt execution-contract quality, invocation safety, and prompt-specific remediation guidance.
---

# Audit Prompts

## Specialization

Evaluate `.prompt.md` artifacts against prompt-governance standards and produce review outcomes (Pass, Pass With Advisories, Fail, Blocked) focused on trigger clarity, output contract quality, and safe invocation behavior. Scope is singular: prompt quality review and follow-up governance.

This skill exists as a dedicated specialization for prompt-file audits so prompt review can use prompt-specific sources, storage, and outputs without sharing a mixed review workflow with instructions or agents.

## Review Mode

- Default mode is report-only.
- Do not modify prompt artifacts during review unless the user explicitly asks for remediation edits.

## Normative Language

- MUST: Mandatory requirement. Failure means the reviewed prompt fails.
- SHOULD: Advisory requirement. Failure does not auto-fail, but requires recommendation and tracking.

## Review Standards

Use these standards exactly:

| ID | Standard | Type | Pass Criteria | Failure Action |
|---|---|---|---|---|
| PRR-M1 | Singular purpose | MUST | Prompt targets one repeatable workflow task only. | Mark failed; recommend purpose split. |
| PRR-M2 | Valid frontmatter | MUST | `name` and `description` are present when required by the workspace contract; YAML is valid and aligned with current VS Code prompt-file behavior for supported metadata such as `agent`, `tools`, `model`, and `argument-hint`. | Mark failed; provide exact frontmatter fix. |
| PRR-M3 | Output format declared | MUST | Required output structure is explicitly defined in the prompt body. | Mark failed; recommend adding output requirements section. |
| PRR-M4 | Skill routing present | MUST | Prompt explicitly routes to a named skill via `Load and follow [SKILL.md]` or equivalent when the prompt is intended to drive a reusable workflow rather than a lightweight inline task. | Mark failed; recommend adding a skill routing directive or simplifying the prompt purpose. |
| PRR-S1 | No conflict with other prompts | SHOULD NOT conflict | No harmful overlap or duplicate trigger conditions with other active prompts. | Record advisory finding and recommend escalation to type-governance audit for conflict resolution. |
| PRR-S2 | Brevity | SHOULD | Wording is economical; no narrative padding beyond routing and output clarity. | Record advisory finding; recommend concise reductions. |
| PRR-S3 | Growth governance alignment | SHOULD | Prompt changes follow growth discipline: reuse-before-create, anti-duplication, delta-first edits, and explicit auditability. | Record advisory finding and recommend minimal, self-contained consolidation. |

## Trigger Conditions

Invoke this skill when any condition below is true:

- A new `.prompt.md` file is created.
- An existing `.prompt.md` file is modified.
- A periodic quality audit of workspace prompt files is requested.
- A prompt file fails discovery, invocation, or behavior expectations.
- A source-catalog freshness check is needed to verify current prompt-file behavior, locations, and supported frontmatter.

## Inputs

Required inputs:

- Target prompt name or explicit list of target prompt files.
- Workspace prompts root path (default: `.github/prompts/`).
- Review date in ISO format (`YYYY-MM-DD`).

Optional inputs:

- Previous review artifact path if already known.
- Change request or incident context.
- Source catalog file path (default: `./references/source-catalog.md`).
- Maximum age threshold in days for source freshness (default: 30).

## Source Governance Rules

- **BLOCKING**: Read [source-catalog.md](./references/source-catalog.md) BEFORE producing any findings. Platform-specific assessments — including supported frontmatter metadata, prompt invocation behavior, and tool or agent field availability — MUST be grounded in the source catalog, not inferred from workspace scripts or local tooling whose contracts may be stale.
- Keep the source catalog in Markdown grid format.
- Every source row MUST include: Source, What It Provides, Why It Is Valuable, In Use (Yes or No), Last Evaluated (YYYY-MM-DD), Current Status (Current, Needs Review, Deprecated).
- Mark a source as Needs Review when Last Evaluated exceeds the freshness threshold.
- Mark a source as Deprecated when it is no longer maintained or no longer relevant to prompt review.
- Do not remove historical sources without adding a short deprecation note in the Notes column.
- Re-evaluate sources before finalizing frontmatter, location, and prompt-behavior recommendations. If any source is Needs Review, resolve it before issuing source-sensitive recommendations.

## Required Outputs

- A per-prompt review report stored using template: [audit-prompts-report-template.md](./references/audit-prompts-report-template.md).
- A conflict report is not produced by this skill; conflict detection across prompts or with other customization types is a type-governance concern.
- Updated per-prompt history at: `.docs/changes/prompt/history/<prompt-name>-history.md`.
- Review result summaries MUST be returned in Markdown grid format (tables), not prose lists.
- Aggregate multi-prompt results MUST include at least one consolidated grid with per-prompt outcomes.
- Per-prompt review files MUST be stored under `.docs/changes/prompt/reviews/<prompt-name>/`.
- Reasoning package per reviewed prompt: assumptions, trade-offs, blockers, and one recommendation.
- Source-governance summary when source validation is requested.
- Updated [source-catalog.md](./references/source-catalog.md) when source tracking changes are made.

#### Violation Code Legend

| Code Prefix | Standard | Type | Skill Source |
|---|---|---|---|
| PRR-M* | Mandatory prompt quality check | MUST | audit-prompts |
| PRR-S* | Advisory prompt quality check | SHOULD | audit-prompts |

## Workflow

1. Resolve target prompts and collect current `.prompt.md` files.
2. Load the per-prompt history file from `.docs/changes/prompt/history/` before analysis.
3. Build a recommendation deny-list from history entries marked Rejected, Removed, or Illegitimate.
4. Re-evaluate tracked sources in [source-catalog.md](./references/source-catalog.md) for freshness and current `.prompt.md` behavior before source-sensitive checks.
5. Build coverage across all mandatory branches: purpose scope, frontmatter validity, output contract, skill routing, prompt conflicts, brevity, source alignment, and history alignment.
6. Verify growth-governance alignment: duplication control, reuse-before-create, delta-first edits, and explicit review outputs.
7. Evaluate all PRR-M* and PRR-S* checks with evidence.
8. Evaluate source alignment against the current source-catalog state: file locations, supported frontmatter metadata, prompt invocation behavior, tool and agent metadata, and Markdown reference expectations.
9. Produce Pass or Fail for MUST standards and advisory outcome for SHOULD standards.
10. For each failed or advisory check, record assumptions, trade-offs, blockers, and one recommendation.
11. Update the prompt history file with findings, decisions, and recommendation statuses.
12. Confirm deterministic coverage: each requested outcome is mapped to a report artifact or explicit decision.

## Output Format Rules

- MUST return review outcomes in Markdown grid format.
- MUST present aggregate results using a single consolidated grid with columns: Prompt, Outcome, MUST Failures, SHOULD Advisories, Report.
- SHOULD include a small aggregate metrics grid for totals (Pass, Pass With Advisories, Fail, Blocked).
- SHOULD keep narrative concise and place it after the grids.

## Storage Rules

- Store each prompt review under `.docs/changes/prompt/reviews/<prompt-name>/`.
- Use descriptive file names: `review.md`. Use versioned names (for example, `review-v2.md`) to disambiguate repeated runs.
- Keep aggregate cross-prompt summaries in `.docs/changes/prompt/reviews/`.

## History Management Rules

- Keep one history file per reviewed prompt at `.docs/changes/prompt/history/<prompt-name>-history.md`.
- Append new review entries; never rewrite prior decisions.
- Track each recommendation with status: Proposed, Accepted, Rejected, Removed, Implemented.
- Before publishing recommendations, remove any item that matches prior Rejected or Removed entries unless the user explicitly re-opens it.

## Done Criteria

A review is complete only when:

- All MUST and SHOULD checks were executed with evidence.
- Required report artifacts were written.
- History was updated for every reviewed prompt.
- Reasoning package entries are present for failed and advisory findings.
- Source-catalog freshness was checked and source-sensitive findings are grounded in a current source evaluation.
