---
name: audit-skill
description: Use when evaluating one or more workspace skills for skill-specific quality signals such as trigger clarity, self-containment, and reference integrity, then recording remediation recommendations.
---

# Audit Skill

## Specialization

Evaluate skills against skill-governance standards and produce review outcomes (Pass, Pass With Advisories, Fail, Blocked) centered on reusable workflow quality. Scope is singular: skill quality review and follow-up governance.

## Normative Language

- MUST: Mandatory requirement. Failure means the reviewed skill fails.
- SHOULD: Advisory requirement. Failure does not auto-fail, but requires recommendation and tracking.

## Review Standards

Use these standards exactly:

| ID | Standard | Type | Pass Criteria | Failure Action |
|---|---|---|---|---|
| SKR-M1 | Specialization | MUST | Skill scope is hyper-specialized to one objective only. | Mark as failed and recommend scope split or refocus. |
| SKR-M2 | Valid format | MUST | Valid YAML front matter and valid Markdown structure for Copilot skill loading. | Mark as failed and provide exact formatting fix. |
| SKR-M3 | Triggers | MUST | Clear discovery triggers in description and body with concrete use conditions. | Mark as failed and provide trigger rewrite guidance. |
| SKR-M4 | No cross-skill references | MUST | Skill guidance body contains no invocations, delegations, required-sub-skill directives, or workflow steps that call a named sibling skill. All execution content must be self-contained, with explicit inputs, outputs, and process. | Mark as failed; inline required content directly or introduce a dedicated orchestrator skill as the indirection layer. Do not cross-reference to resolve shared logic. |
| SKR-S1 | Assets | SHOULD | Skill uses concrete references or reusable assets when they materially improve execution support; a `references/` directory is optional when the skill is already self-contained. | Record advisory finding only when missing assets cause ambiguity, duplication, or weak reuse. |
| SKR-S3 | Link integrity | SHOULD | Markdown links are resolvable, non-placeholder, and aligned with referenced assets/docs, including valid fragment anchors when present. Validate from the on-disk workspace file context. | Record advisory finding and recommend target fixes or valid replacements. |
| SKR-S4 | Growth governance alignment | SHOULD | Skill changes follow growth discipline: reuse-before-create, anti-duplication, delta-first edits, and explicit auditability. | Record advisory finding and recommend minimal, self-contained consolidation. |
| SKR-S5 | Brevity | SHOULD | Skill wording is economical for context efficiency, avoids obvious duplication or narrative padding, and preserves clarity without unnecessary verbosity. | Record advisory finding and recommend concise reductions through the appropriate authoring skill. |

## Trigger Conditions

Invoke this skill when any condition below is true:

- A new skill is created.
- An existing skill is modified.
- Periodic quality audit of skills is requested.
- A skill fails discovery, invocation, or behavior expectations.
- Two skills appear to overlap or contradict each other.

## Inputs

Required inputs:

- Target skill name or explicit list of target skills.
- Workspace skill root path.
- Review date.

Optional inputs:

- Previous review artifact path if already known.
- Change request or incident context.
- Evaluation date in ISO format (`YYYY-MM-DD`) for review freshness tracking.
- Source catalog file path (default: `./references/source-catalog.md`).
- Maximum age threshold in days for source freshness (default: 30).

## Source Governance Rules

- **BLOCKING**: Read [source-catalog.md](./references/source-catalog.md) BEFORE producing any findings. Platform-specific assessments — including skill structural expectations, format requirements, and tooling behavior — MUST be grounded in the source catalog, not inferred from workspace scripts or local tooling whose contracts may be stale.
- Keep the source catalog in Markdown grid format.
- Every source row MUST include: Source, What It Provides, Why It Is Valuable, In Use (Yes or No), Last Evaluated (YYYY-MM-DD), Current Status (Current, Needs Review, Deprecated).
- Mark a source as Needs Review when Last Evaluated exceeds the freshness threshold.
- Mark a source as Deprecated when it is no longer maintained or no longer relevant to skill review.
- Do not remove historical sources without adding a short deprecation note in the Notes column.
- Re-evaluate sources before finalizing recommendations for skill standards and review guidance.

## Required Outputs

- A per-skill review report in workspace docs using template path: [audit-skill-report-template.md](./references/audit-skill-report-template.md).
- A conflict report is not produced by this skill; conflict detection across skills is a type-governance concern.
- Updated per-skill history at: `.docs/changes/skill/history/<skill-name>-history.md`.
- Review result summaries MUST be returned in Markdown grid format (tables), not prose lists.
- Aggregate multi-skill results MUST include at least one consolidated grid with per-skill outcomes.
- Per-skill review files MUST be stored under .docs/changes/skill/reviews/<skill-name>/.
- Reasoning package per reviewed skill: assumptions, trade-offs, blockers, and one recommendation.
- Source-governance summary when maintenance validation is requested.
- Updated [source-catalog.md](./references/source-catalog.md) when source tracking changes are made.

#### Violation Code Legend

| Code Prefix | Standard | Type | Skill Source |
|---|---|---|---|
| SKR-M* | Mandatory skill quality check | MUST | audit-skill |
| SKR-S* | Advisory skill quality check | SHOULD | audit-skill |

## Assets

- Script assets are available at path: [README.md](./references/scripts/README.md).
- Source catalog is available at path: [source-catalog.md](./references/source-catalog.md).
- A dedicated `references/` folder is optional for reviewed skills; do not recommend it by default when the artifact is already self-contained.
- For concision-focused remediation, include exact rewrite recommendations directly in the report.
- Use script assets as follows: `generate-audit-skill-baseline.ps1` (full baseline + history), `get-audit-skill-metadata.ps1` (quick metadata checks), `generate-audit-skill-targeted.ps1` (targeted reruns), `refresh-audit-skill-history.ps1` (history index + aggregate grid).

## Workflow

1. Resolve target skills and collect current SKILL.md files and related assets.
2. Load the per-skill history file from `.docs/changes/skill/history/` before analysis.
3. Build a recommendation deny-list from history entries marked Rejected, Removed, or Illegitimate.
4. Re-evaluate tracked sources in [source-catalog.md](./references/source-catalog.md) for freshness and relevance.
5. Build coverage across mandatory branches: format, triggers, self-containedness, links, and history alignment.
6. Verify growth-governance alignment: duplication control, reuse-before-create, delta-first edits, and explicit review outputs.
7. Re-evaluate maintenance assumptions against active standards and source context when requested.
8. Evaluate all SKR-M* and SKR-S* checks with evidence.
9. Validate markdown link integrity in SKILL.md from on-disk context (reject placeholder `#` and unresolved local paths).
10. Prefer workspace-root-relative markdown links to reduce virtual-buffer resolution mismatch in IDE diagnostics.
11. Validate self-containedness semantically: required execution context must be explicit and not rely on unstated assumptions, using canonical sections or clearly labeled equivalents.
12. Validate brevity: wording should be economical, without obvious duplication or narrative padding.
13. Produce pass or fail for MUST standards and advisory outcome for SHOULD standards.
14. For each failed or advisory check, record assumptions, trade-offs, blockers, and one recommendation.
15. If advisory findings are primarily concision-related, include rewrite-ready text in the report before finalizing remediation wording.
16. Update the skill history file with findings, decisions, and recommendation statuses.
17. Confirm deterministic coverage: each requested outcome is mapped to a report artifact or explicit decision.

## Output Format Rules

- MUST return review outcomes in Markdown grid format.
- MUST present aggregate results using a single consolidated grid with these columns:
   - Skill
   - Outcome
   - MUST Failures
   - SHOULD Advisories
   - Report
- SHOULD include a small aggregate metrics grid for totals (Pass, Pass With Advisories, Fail, Blocked).
- SHOULD keep narrative concise and place it after the grids.

## Storage Rules

- Store each skill review under .docs/changes/skill/reviews/<skill-name>/.
- Use descriptive file names: `review.md`. Use versioned names (for example, `review-v2.md`) to disambiguate repeated runs.
- Keep aggregate cross-skill summaries in .docs/changes/skill/reviews/.

## History Management Rules

- Keep one history file per reviewed skill at `.docs/changes/skill/history/<skill-name>-history.md`.
- Append new review entries; never rewrite prior decisions.
- Track each recommendation with status: Proposed, Accepted, Rejected, Removed, Implemented.
- Before publishing recommendations, remove any item that matches prior Rejected or Removed entries unless the user explicitly re-opens it.

## Done Criteria

A review is complete only when:

- All MUST and SHOULD checks were executed with evidence.
- Required report artifacts were written.
- History was updated for every reviewed skill.
- Conflicts were either resolved with user confirmation or explicitly marked Blocked.
- Reasoning package entries are present for failed and advisory findings.
- Maintenance assumptions are freshness-checked when maintenance validation is in scope.
- Source-catalog freshness was checked before final recommendations were issued.

