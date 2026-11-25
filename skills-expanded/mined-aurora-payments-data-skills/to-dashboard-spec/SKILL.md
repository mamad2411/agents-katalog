---
name: to-dashboard-spec
description: Turn the current conversation into a dashboard build spec covering audience, metric map, control map, freshness SLA and logic placement, then publish it to the project issue tracker. No interview, just synthesis of what you've already discussed.
disable-model-invocation: true
---

This skill takes the current conversation context, warehouse understanding, and BI-surface understanding and produces a dashboard build spec, the contract the surface is built against and reviewed against. Do NOT interview the user; just synthesize what you already know.

The issue tracker, triage label, and dashboards vocabulary (`docs/agents/dashboards.md`, covering BI tool, rubric and registry) should have been provided to you. Run `/setup-data-skills` if not.

## Process

1. Explore the warehouse and the BI surface to understand the current state, if you haven't already. For every metric the spec touches, verify the feeding model exists and carries the metric's grain and the freshness columns the surface will report; check the registry (`docs/agents/dashboards.md`) for an existing surface that already answers part of the question, because a rebuild has a basis and the basis changes the spec. Use the project's domain glossary vocabulary throughout the spec, taking metric definitions from the glossary rather than from chart titles, and respect any ADRs in the area you're touching.

2. Sketch the dashboard contract, the pre-agreements that are expensive to change after the build starts. Pin five things, per the org's dashboard rubric:

- **Audience and type**: strategic (exec skim), operational (monitor and act), or analytical (drill and explore). One artifact trying to be two types fails as both. Name the busiest reader.
- **Metric map**: for each headline metric, give the glossary definition it points at, the governed model it reads (its named source of truth), the grain, the comparison (period-over-period, trailing average, or a real target, never an invented one), and whether the card is static or trend.
- **Freshness SLA**: the source-anchored columns the surface reports freshness from (the latest business period and the source load time, never a rebuild timestamp), and how stale the data may be before the surface must say so. A feeding model missing those columns is a pipeline gap the spec names as a blocking dependency, not a reason to fake freshness downstream.
- **Control map**: every control, its targets, its default, which elements deliberately ignore it, and every dimension feeding a synced control, with the models that must agree on its values (each gets a dimension-parity test in the warehouse).
- **Logic placement**: every calculation assigned to a layer. Warehouse model by default; BI data model only with a recorded reason; BI-element SQL never.

Check with the user that this contract (audience, metric map, freshness SLA, control map, logic placement) matches their expectations.

3. Write the spec using the template below, then publish it to the project issue tracker. Apply the `ready-for-agent` triage label - no need for additional triage.

<spec-template>

## Problem Statement

The problem that the user is facing, from the user's perspective.

## Solution

The solution to the problem, from the user's perspective.

## User Stories

A LONG, numbered list of user stories. Each user story should be in the format of:

1. As an <actor>, I want a <feature>, so that <benefit>

<user-story-example>
1. As a CFO skimming before the Monday exec meeting, I want volume against last month on one screen, so that I can say "on track or not" in five seconds
</user-story-example>

This list of user stories should be extremely extensive and cover all aspects of the feature.

## Dashboard Contract

The five pre-agreements from step 2, recorded. This is the section review scores against; every later disagreement resolves here.

- **Audience and type**, and the busiest reader
- **Metric map**: one row per headline metric, giving glossary term, source-of-truth model, grain, comparison type, static or trend
- **Freshness SLA**: the freshness columns per feeding model, and the staleness thresholds at which the surface must say so
- **Control map**: one row per control, giving targets, default and exempt elements; synced dimensions listed with the models that must agree on their values
- **Logic placement**: one row per calculation that is not a plain column read, saying where it lives, and for anything outside the warehouse, the recorded reason

## Tie-Out Basis

For rebuilds and overlapping surfaces only: the basis workbook and governed sources the new surface must tie to, the headline cells and 2-3 drill paths per major metric that will be compared, and what the basis does well, each carried forward or waived explicitly. Omit this section for green-field surfaces with no overlapping numbers.

## Implementation Decisions

A list of implementation decisions that were made. This can include:

- The pages or tabs, and the one question each answers
- Which models feed which elements, and any BI data-model forks (a TopN subset, a pre-aggregation) named by purpose
- Composite-card decisions: which rates absorb their components into a sub-line, which stage counts become one funnel element instead of a row of cards
- Theme, and any waiver of a rubric rule: recorded, with the reason
- Architectural decisions

Do NOT include specific file paths or code snippets. They may end up being outdated very quickly. Model, table, workbook, and element names are not file paths; they are the vocabulary the contract depends on.

Exception: if a prototype produced a snippet that encodes a decision more precisely than prose can (a transformation query, a data-model fork, a schema contract), inline it within the relevant decision and note briefly that it came from a prototype. Trim to the decision-rich parts: not a working demo, just the important bits.

## Testing Decisions

A list of acceptance decisions that were made. Include:

- The tie-out plan: basis and governed sources, the cells compared (headline KPIs plus 2-3 drill paths per major metric), identical filter state frozen on both sides, every cell classified TIE / EXPECTED-MISMATCH (a named, documented definition change) / UNEXPLAINED-MISMATCH, where an unexplained headline mismatch blocks ship
- The dimension-parity tests backing each synced control, and where they run (the warehouse, not the BI tool)
- The freshness checks: the surface's freshness element reads the contracted columns and says so at the SLA thresholds
- The review gate: the build ships only on an approving verdict from /dashboard-review

## Out of Scope

A description of the things that are out of scope for this spec.

## Further Notes

Any further notes about the feature.

</spec-template>
