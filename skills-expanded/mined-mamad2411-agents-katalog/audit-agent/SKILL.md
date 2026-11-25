---
name: audit-agent
description: Use when evaluating one or more workspace .agent.md files for agent-role quality, invocation boundary precision, and platform-currency alignment, then recording remediation recommendations.
---

# Audit Agent

## Specialization

Evaluate `.agent.md` artifacts against agent-governance standards and produce review outcomes (Pass, Pass With Advisories, Fail, Blocked) focused on role boundaries, invocation behavior, and platform fit. Scope is singular: agent quality review and follow-up governance.

## Normative Language

- MUST: Mandatory requirement. Failure means the reviewed agent fails.
- SHOULD: Advisory requirement. Failure does not auto-fail, but requires recommendation and tracking.

## Review Standards

Use these standards exactly:

| ID | Standard | Type | Pass Criteria | Failure Action |
|---|---|---|---|---|
| AGR-M1 | Specialization | MUST | Agent scope is singular: one specialist role with no mixed responsibilities. | Mark as failed and recommend scope split or role refocus. |
| AGR-M2 | Valid format | MUST | Valid YAML frontmatter (`name`, `description`) and `.agent.md` extension. Body contains at minimum the `## Specialization` section. | Mark as failed and provide exact formatting fix. |
| AGR-M3 | Invocation description | MUST | `description` is third-person, invocation-focused, states what the agent does and when to call it, and is not a workflow summary. | Mark as failed and provide rewrite with role and invocation context. |
| AGR-M4 | Hard constraints present | MUST | An explicit `## Hard Constraints` section is present and defines what the agent will not do. | Mark as failed and provide minimum viable hard constraints draft. |
| AGR-S1 | Required sections | SHOULD | Required body sections are present: `## Specialization`, `## Focus Areas`, `## Standards`, `## Hard Constraints`, `## Preferred Companion Skills`. | Record advisory finding and list missing sections with minimum viable drafts. |
| AGR-S2 | No cross-agent delegation | SHOULD NOT | Agent body contains no hardcoded invocations, delegation chains, or required-sub-agent directives to named sibling agents. | Record advisory finding and recommend removing or routing delegation through an orchestrator. |
| AGR-S3 | No conflict | SHOULD NOT conflict | No harmful role overlap or contradictory behavior with other agents. | Start conflict workflow and document resolution plan. |
| AGR-S4 | Growth governance alignment | SHOULD | Agent changes follow growth discipline: reuse-before-create, anti-duplication, delta-first edits, and explicit auditability. | Record advisory finding and recommend minimal, self-contained consolidation. |
| AGR-S5 | Platform currency | SHOULD | Frontmatter fields are aligned with the current VS Code custom agent specification. No deprecated fields (`infer`) used without acknowledged migration path. New platform fields (`handoffs`, `hooks`, `disable-model-invocation`, `agents`, `model`) are considered where they improve role clarity or capability boundaries. | Record advisory finding, reference source-catalog entry and current spec state, and recommend concrete field updates. |

## Trigger Conditions

Invoke this skill when any condition below is true:

- A new `.agent.md` file is created.
- An existing `.agent.md` file is modified.
- A periodic quality audit of workspace agents is requested.
- An agent fails discovery, invocation, or behavior expectations.
- Two agents appear to overlap or contradict each other.
- A source-catalog freshness check triggers a platform-currency review.

## Inputs

Required inputs:

- Target agent name or explicit list of target agents.
- Workspace agent root path (default: `.github/agents/`).
- Review date in ISO format (`YYYY-MM-DD`).

Optional inputs:

- Previous review artifact path if already known.
- Change request or incident context.
- Source catalog file path (default: `./references/source-catalog.md`).
- Maximum age threshold in days for source freshness (default: 30).

## Source Governance Rules

- **BLOCKING**: Read [source-catalog.md](./references/source-catalog.md) BEFORE producing any findings. Platform-specific assessments — including allowed frontmatter fields, deprecated fields, and available capability expansions — MUST be grounded in the source catalog, not inferred from workspace scripts or local tooling whose contracts may be stale.
- Keep the source catalog in Markdown grid format.
- Every source row MUST include: Source, What It Provides, Why It Is Valuable, In Use (Yes or No), Last Evaluated (YYYY-MM-DD), Current Status (Current, Needs Review, Deprecated).
- Mark a source as Needs Review when Last Evaluated exceeds the freshness threshold.
- Mark a source as Deprecated when it is no longer maintained or no longer relevant to agent review.
- Do not remove historical sources without adding a short deprecation note in the Notes column.
- Re-evaluate sources before finalizing AGR-S5 (Platform Currency) findings. If any source is Needs Review, resolve it before issuing platform-currency recommendations.

## Required Outputs

- A per-agent review report stored using template: [audit-agent-report-template.md](./references/audit-agent-report-template.md).
- A conflict report is not produced by this skill; conflict detection across agents is a type-governance concern.
- Updated per-agent history at: `.docs/changes/agent/history/<agent-name>-history.md`.
- Review result summaries MUST be returned in Markdown grid format (tables), not prose lists.
- Aggregate multi-agent results MUST include at least one consolidated grid with per-agent outcomes.
- Per-agent review files MUST be stored under `.docs/changes/agent/reviews/<agent-name>/`.
- Reasoning package per reviewed agent: assumptions, trade-offs, blockers, and one recommendation.
- Source-governance summary when platform-currency validation is requested.
- Updated [source-catalog.md](./references/source-catalog.md) when source tracking changes are made.

## Workflow

1. Resolve target agents and collect current `.agent.md` files.
2. Load the per-agent history file from `.docs/changes/agent/history/` before analysis.
3. Build a recommendation deny-list from history entries marked Rejected, Removed, or Illegitimate.
4. Re-evaluate tracked sources in [source-catalog.md](./references/source-catalog.md) for freshness and platform-currency changes. Update status fields before proceeding to AGR-S5 checks.
5. Build coverage across all mandatory branches: format, invocation trigger, specialization, hard constraints, companion skills, conflict risk, cross-agent delegation, platform currency, and history alignment.
6. Verify growth-governance alignment: duplication control, reuse-before-create, delta-first edits, and explicit review outputs.
7. Evaluate all AGR-M* and AGR-S* checks with evidence.
8. Evaluate platform currency against the current source-catalog state: flag deprecated fields (`infer`), note new available fields that could improve the agent's role clarity or capability boundary.
9. Produce Pass or Fail for MUST standards and advisory outcome for SHOULD standards.
10. For each failed or advisory check, record assumptions, trade-offs, blockers, and one recommendation.
11. If conflict is detected: document it at `.docs/changes/agent/conflicts/`, recommend resolution options, and collaborate with the user to confirm resolution.
12. Update the agent history file with findings, decisions, and recommendation statuses.
13. Confirm deterministic coverage: each requested outcome is mapped to a report artifact or explicit decision.

## Output Format Rules

- MUST return review outcomes in Markdown grid format.
- MUST present aggregate results using a single consolidated grid with columns: Agent, Outcome, MUST Failures, SHOULD Advisories, Report.
- SHOULD include a small aggregate metrics grid for totals (Pass, Pass With Advisories, Fail, Blocked).
- SHOULD keep narrative concise and place it after the grids.

## Storage Rules

- Store each agent review under `.docs/changes/agent/reviews/<agent-name>/`.
- Use descriptive file names: `review.md`. Use versioned names (for example, `review-v2.md`) to disambiguate repeated runs.
- Keep aggregate cross-agent summaries in `.docs/changes/agent/reviews/`.

## Conflict Workflow (Mandatory When Conflict Exists)

When a conflict exists, this skill MUST:

1. Document the conflict in a workspace document at `.docs/changes/agent/conflicts/` using the conflict template.
2. Provide recommendations to resolve the conflict.
3. Collaborate with the human user to select and confirm the final resolution.

Do not auto-resolve without explicit user direction.

## History Management Rules

- Keep one history file per reviewed agent at `.docs/changes/agent/history/<agent-name>-history.md`.
- Append new review entries; never rewrite prior decisions.
- Track each recommendation with status: Proposed, Accepted, Rejected, Removed, Implemented.
- Before publishing recommendations, remove any item that matches prior Rejected or Removed entries unless the user explicitly re-opens it.

#### Violation Code Legend

| Code Prefix | Standard | Type | Skill Source |
|---|---|---|---|
| AGR-M* | Mandatory agent quality check | MUST | audit-agent |
| AGR-S* | Advisory agent quality check | SHOULD | audit-agent |

## Done Criteria

A review is complete only when:

- All MUST and SHOULD checks were executed with evidence.
- Required report artifacts were written.
- History was updated for every reviewed agent.
- Conflicts were either resolved with user confirmation or explicitly marked Blocked.
- Reasoning package entries are present for failed and advisory findings.
- Source-catalog freshness was checked and AGR-S5 findings are grounded in a current source evaluation.

