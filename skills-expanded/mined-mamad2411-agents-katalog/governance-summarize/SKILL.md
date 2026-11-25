---
name: governance-summarize
description: Use when you need one concise, single-page governance briefing that aggregates the most important points across workspace governance artifacts.
---

# Summarize Governance

## Specialization

Produce a concise, single-page governance briefing that surfaces only the most salient findings, risks, decisions, and next actions from existing governance artifacts.

This skill is an aggregation-and-compression workflow. It does not perform full audits or create new governance standards.

## Trigger Conditions

Invoke this skill when any of the following is true:

- Governance documentation has grown and stakeholders need a fast executive readout.
- A periodic checkpoint needs one page instead of multi-file audit narratives.
- You need a pre-implementation governance brief to align planning and execution teams.
- A review meeting requires a short disposition with evidence links and clear priorities.

## Required Inputs

- Target date or reporting window.
- Source artifact scope, defaulting to:
  - `.docs/changes/governance/audits/`
  - `.docs/changes/skill/reviews/`
  - `.docs/changes/customization/reviews/`
  - `.github/instructions/`
  - `.github/agents/`
  - [README.md](./../../../README.md), [README.md](./../../../README.md), [README.md](./../../../README.md)
- Optional audience mode: `Executive`, `Engineering Leads`, or `Customization Maintainers`.

## Required Outputs

- One markdown briefing at `.docs/changes/governance/audits/governance-one-pager.md`.
- Grid-first output with the sections below, in this order:
  1. `Disposition Snapshot`
  2. `Top Salient Findings`
  3. `Risk and Impact`
  4. `Decision and Action Matrix`
  5. `Evidence Index`

## Single-Page Constraints

- Keep output to one page equivalent (target 450 to 700 words excluding tables).
- Limit to the top 5 salient findings.
- Limit to the top 5 actions.
- Prefer short, high-information table cells over narrative paragraphs.
- Use one final disposition line only: `PASSED`, `PASSED WITH ADVISORIES`, or `FAILED`.

## Salience Selection Rules

Prioritize evidence in this order:

1. Any MUST failures or unresolved conflicts.
2. Repeated advisories across multiple source artifacts.
3. Lane coverage or catalog integrity issues that can block delivery.
4. High-impact hygiene gaps (frontmatter validity, stale indexes, routing drift).
5. Near-term corrective actions with clear owners and due dates.

Exclude low-impact detail unless required to explain a top finding.

## Output Format Rules

- Start with tables; place narrative after tables only if needed.
- Include explicit counts where possible (for example, `3 of 14 MUST checks failing`).
- Every finding row must include at least one evidence reference.
- Action rows must include owner, priority, and target date.
- Keep narrative to 5 lines maximum.

## Workflow

1. Collect source governance artifacts for the target window.
2. Extract findings, advisories, and dispositions from each source.
3. Deduplicate overlapping findings and merge equivalent issues.
4. Rank by severity, recurrence, and delivery impact.
5. Build the one-page grid set using the required section order.
6. Validate that word count and limits satisfy single-page constraints.
7. Publish briefing to the required output path.

## Self-Containment

This workflow is self-contained and performs evidence collection, ranking, and briefing generation without delegating to other skills.

## Done Criteria

- Output exists at the required one-pager path.
- The briefing is one page equivalent and grid-first.
- Only high-salience findings are included.
- Disposition is explicit and traceable to evidence.

## Inputs

- User request context and scope for governance summarization.

