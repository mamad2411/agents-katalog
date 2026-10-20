---
name: governance-health-overview
description: Use when you need a reconciled governance health view that synthesizes governance, skill-quality, customization-quality, and optimization evidence into one disposition.
---

# Governance Health Overview

## Specialization

Produce one reconciled governance health view across core governance, skill quality, and customization quality by synthesizing outputs from specialized review skills, including optimize-customizations.

This skill is hyper-specialized for governance health reconciliation only.

This skill aggregates and reconciles evidence streams within one governance disposition workflow.

## Trigger Conditions

Invoke this skill when any of the following is true:

- Multiple governance-related audits were run and their results need one unified disposition.
- A governance report appears inconsistent with skill/customization review outputs.
- A monthly cadence report must include both policy-level and artifact-level review status.

## Required Inputs

- Audit date (`YYYY-MM-DD`).
- Target scope (full workspace or constrained scope when explicitly requested).
- Optional override paths only when rerun is explicitly blocked; otherwise generate fresh artifacts in this invocation.

## Required Outputs

- Reconciled report at `.docs/changes/governance/audits/governance-executive-audit.md`.
- Report Navigation Grid with three levels and drill-down links:
	- Level 1 Executive (workspace summary)
	- Level 2 Type (skills/prompts/agents/instructions aggregates)
	- Level 3 Item (individual customization findings)
- Coverage Grid.
- Standards Health Grid including GOV-M*, GOV-S*, plus aggregated GOV-SK, GOV-CUS, and GOV-OPT outcomes.
- Aggregate Metrics Grid including check pass/fail totals, asset counts, and overlap-threshold metrics.
- Failure Detail Grid with one row per open failure (or explicit `None` row when all are closed).
- Failure Detail Grid must include a `Check` column mapped to canonical check IDs and an `Evidence` column referencing the source script.
- Delta vs Prior Report Grid using standardized metrics with `Prior`, `Current`, `Delta`, and `Trend` columns (`Increase`, `Decrease`, `Flat`).
- Responsibility overlap summary sourced from `test-responsibility-overlap.ps1` including duplicate-pair count, threshold, and top overlap pairs.
- Docs Corpus Hygiene Grid sourced from this skill Self-containment checks and `.docs` corpus metrics.
- Ranked Recommendations Grid.
- Explicit final disposition (`PASSED` or `FAILED`) based on MUST failures and open conflicts.

#### Violation Code Legend

| Code Prefix | Standard | Type | Skill Source |
|---|---|---|---|
| GOV-M* | Mandatory governance check | MUST | governance health overview |
| GOV-S* | Advisory governance check | SHOULD | governance health overview |
| GOV-SK | Skill quality aggregate | Aggregate | governance health overview |
| GOV-CUS | Customization quality aggregate | Aggregate | governance health overview |
| GOV-OPT | Optimization factor coverage | Aggregate | governance health overview |
| SKR-M* | Mandatory skill quality check | MUST | governance health overview |
| SKR-S* | Advisory skill quality check | SHOULD | governance health overview |
| INR-M* | Mandatory instruction quality check | MUST | governance health overview |
| INR-S* | Advisory instruction quality check | SHOULD | governance health overview |
| AGR-M* | Mandatory agent quality check | MUST | governance health overview |
| AGR-S* | Advisory agent quality check | SHOULD | governance health overview |
| PRR-M* | Mandatory prompt quality check | MUST | governance health overview |
| PRR-S* | Advisory prompt quality check | SHOULD | governance health overview |
| OPR-M* | Mandatory optimization quality check | MUST | governance health overview |
| OPR-S* | Advisory optimization quality check | SHOULD | governance health overview |

## Workflow

0. Run `invoke-governance-health-overview.ps1` to collect evidence in one non-interactive execution when tooling permits.
1. Produce a fresh core governance artifact under `.docs/changes/governance/audits/` for the audit date.
2. Produce a fresh skill-quality aggregate artifact under `.docs/changes/skill/reviews/` for the audit date.
3. Produce a fresh customization-quality aggregate artifact under `.docs/changes/customization/reviews/` for the audit date.
4. Produce a fresh optimization-factor artifact under `.docs/changes/customization/reviews/` for the audit date.
5. Verify all four artifacts are generated in the current invocation and capture their paths in report metadata.
6. Reconcile the four fresh sources into one coherent set of metrics.
7. If any MUST failures or open conflicts exist in any source, set disposition to `FAILED`.
8. Produce ranked remediation recommendations mapped to evidence artifacts.
9. Include the `responsibility-overlap` output payload in reconciled report metadata and standards evidence.
10. Include the `Metrics` payload in report metadata and use it as the canonical source for aggregate metrics grids.
11. Assess `.docs` corpus growth, redundancy candidates, and stale candidates; include results in the Docs Corpus Hygiene Grid.
12. Compute and publish a standardized Delta vs Prior Report Grid in the reconciled report.
13. Run `test-governance-must-traceability.ps1` before finalizing the report; if it fails, block report publication and return `PROVISIONAL-FAILED` with violations.

## Freshness Policy

- Default behavior is `fresh-run required`.
- Do not aggregate from previously existing artifacts when reruns are possible.
- If reruns are blocked (tooling failure, permissions, or explicit user override), report `stale-input mode` in metadata and list the blocking reason.
- In `stale-input mode`, prefer latest-dated artifacts and mark disposition as provisional until fresh routines complete.

## Execution Efficiency Policy

- Target one terminal approval for the full workflow by batching phase evidence collection.
- Avoid interactive commands and prompts; pass required parameters explicitly.
- If one-approval execution is blocked by environment limits, document the blocker and the minimal extra approvals required.

## Decision Rules

- Core governance pass does not override failing skill/customization quality outcomes.
- Open conflict artifacts from customization review force overall `FAILED` until resolved.
- If source artifacts disagree, cite each artifact and prefer latest-dated output.

### Partial-Run Decision Table

| Evidence Segments Completed | Disposition | Action Required |
|---|---|---|
| 4 of 4 | Normal PASSED or FAILED based on MUST/conflict rules | None |
| 3 of 4 | PROVISIONAL-FAILED | Report which segment failed; cite its blocker; do not aggregate from missing output |
| 2 of 4 | PROVISIONAL-FAILED | Same as above; escalate if core governance is the missing segment |
| 1 of 4 | PROVISIONAL-FAILED | Triage environment issue before retry |
| 0 of 4 | Not reported | Abort run; report tool failure to user before producing any output |

- A PROVISIONAL-FAILED disposition does not imply quality failure; it signals incomplete evidence.
- Retry with `fresh-run required` after resolving the blocker before promoting to a final disposition.
- If this skill fails, the overall run always emits PROVISIONAL-FAILED regardless of other segment outcomes.

## Done Criteria

- Core, skill, customization, and optimization governance routines were executed in this invocation.
- Report metadata records the four freshly generated source artifact paths.
- Report includes reconciled metrics from all four source evidence segments.
- All source paths are cited in evidence rows.
- Final disposition matches MUST/conflict decision rules.

## Inputs

- User request context and target scope for this skill invocation.




