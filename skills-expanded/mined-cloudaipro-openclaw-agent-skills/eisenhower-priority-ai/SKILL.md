---
name: eisenhower-priority-ai
description: Eisenhower prioritization engine that classifies tasks into urgency-importance quadrants and outputs a 50/40/5/5 action allocation. Use when users feel overloaded and need a decisive execution order with rationale.
---

# Eisenhower Priority AI

## Objective
Transform unstructured task lists into quadrant-based execution order with explicit tradeoffs.

## Trigger Rules
Use when users need prioritization clarity, not calendar orchestration.

Positive cues:
- "I have too many tasks."
- "Help me prioritize now."
- "Use Eisenhower matrix."

Do not use when:
- User asks for full day scheduling (use executive-assistant).
- User asks for course or marketing design.
- User asks for research-only persona analysis.

## Inputs
Required:
- Task list.

Optional:
- Deadlines.
- Impact metrics.
- Owner/dependency notes.

## Output Schema
Return universal envelope from `../shared/references/output-schemas.md`.

Artifacts order:
1. Prioritization summary brief.
2. Quadrant classification table.
3. 50/40/5/5 action plan.
4. Anti-overload checklist.

## Workflow
1. Score urgency and importance signals.
2. Place tasks into Q1/Q2/Q3/Q4.
3. Rank tasks within each quadrant.
4. Allocate effort using 50/40/5/5 split.
5. Return execute/delegate/drop recommendations.

## Quality Bar
- Classification rationale must be visible.
- Q2 strategic tasks must not be crowded out.
- Q4 tasks should default to eliminate/defer.

## Safety Rules
- Avoid fabricated deadlines.
- Mark assumptions where metadata is missing.
- Keep recommendations actionable and reversible.

## Resources
- Domain framework: `references/domain.md`
- Envelope validator: `scripts/validate_output.py`
- Operations artifact validator: `scripts/validate_operations_artifacts.py`
