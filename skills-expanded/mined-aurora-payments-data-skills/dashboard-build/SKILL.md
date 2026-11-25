---
name: dashboard-build
description: Build a dashboard from an approved build spec. Verify the feeding models carry the contract, build thin, then hand off to review. Use when a dashboard build spec exists and the surface needs building or amending.
---

Build the dashboard the spec describes. The spec (from /to-dashboard-spec) is the contract; the org's dashboard rubric is the canon. Read both before touching the BI tool. `docs/agents/dashboards.md` resolves the tool, the rubric, the registry, and where artifacts land. Run `/setup-data-skills` if it's missing. Load the tool-mechanics reference named there before the first tool action.

## 1. Contract gate

Before building anything, verify every feeding model against the spec's metric map:

- The model exists, and its declared grain matches the metric's grain.
- The freshness columns the spec names exist and are source-anchored: the latest business period and the source load time, not the mart's rebuild timestamp.
- Every dimension feeding a synced control has a warehouse assertion that its values agree across the models that consume it.

A gap is a pipeline defect, not a build obstacle: file it upstream (the repo's issue conventions), record it against the spec, and either block on it or proceed with a recorded waiver from the user. Never patch a pipeline gap inside the BI tool. A calculated column that fakes freshness or repairs a join is transformation logic in the wrong layer.

## 2. Data models, thin

- One data model per source table minimum; fork models for TopN subsets, pre-aggregations, and filtered views; name forks by purpose.
- The BI data model carries presentation only: display names, formats, last-mile forks. Any calculated column needs the recorded reason from the spec's logic-placement table; if the reason is missing, the calculation belongs in the warehouse, so propose the mart change instead of building the column.
- Element-level SQL is banned. No exceptions: it is invisible to lineage and untestable upstream.

## 3. Elements

Build to the rubric: card anatomy, layout order, control wiring per the spec's control map, scratch elements on a hidden staging page, and the freshness element wired to the contracted freshness columns. Where the rubric and the spec disagree, stop and ask. The spec may carry a recorded waiver; do not invent one.

## 4. Review handoff

The build is not done when it looks right. Run /dashboard-review against the spec: tie-out to the governed sources (and the basis workbook, for rebuilds), verdict per the rubric. Ship only on an approving verdict; carry conditional-approval items as filed issues with owners.

Register the shipped surface in the registry (workbook, feeding models, freshness columns, owner) so blast-radius checks see it.
