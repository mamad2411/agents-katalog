---
name: prioritize-a-backlog
domain: business
locale: [generic]
interface: web
difficulty: intermediate
est_time: 30min
risk: low
prerequisites: []
status: draft
last_verified: 2026-08-17
---

## Goal

Prioritize a backlog so the most valuable and time-sensitive work is visible at the top.

## Preconditions

- You can view and reorder the backlog.
- Current goals, capacity, deadlines, and customer commitments are known.
- Backlog items have enough detail to compare.

## Steps

1. **Open the backlog.** [BRANCH: Jira | Asana | Linear | generic] open the backlog, project list, Linear backlog, or generic unscheduled work view. → *Expect:* unplanned work items are visible.
2. **Remove obvious noise.** Close duplicates, archive stale items, and flag unclear items for refinement. → *Expect:* the backlog contains active candidates.
3. **Group by outcome.** Cluster items by goal, customer impact, product area, or milestone. → *Expect:* related work can be compared together.
4. **Assess value and urgency.** Consider customer impact, revenue, risk reduction, deadlines, and strategic fit. → *Expect:* each high item has a reason.
5. **Assess effort and dependency.** Note size, blockers, sequencing, and required teams. → *Expect:* priority accounts for feasibility.
6. **Rank the top items.** Move the highest-priority items to the top or assign priority fields. → *Expect:* the top backlog reflects the next likely work.
7. **Document priority rationale.** Add short notes for major choices, tradeoffs, and deferred items. → *Expect:* stakeholders can understand the order.

## Decision points

- If two items have similar value → prefer the one with clearer scope or stronger deadline.
- If a high-value item is blocked → mark the blocker and prioritize the unblocker.
- If stakeholders disagree → record options and ask the decision owner to choose.

## Failure modes & recovery

- **F1 Priority without rationale:** detect top items with no reason → recover by adding value, urgency, or dependency notes.
- **F2 Stale backlog dominates:** detect old unclear items near the top → recover by closing, refining, or lowering them.
- **F3 Hidden dependency:** detect a top item cannot start → recover by prioritizing the dependency or moving the item below ready work.

## Verification

The backlog has a clear top set, each top item has a priority reason, and blocked or stale items are marked rather than silently ranked.

## Variations

- Sprint planning: prioritize only items that can fit in the next sprint.
- Support backlog: weigh customer severity, recurrence, and SLA risk.
- Product backlog: include discovery confidence and strategic fit.

## Safety & privacy

Low risk. Priority notes may reveal customer commitments or commercial strategy, so limit visibility where appropriate.
