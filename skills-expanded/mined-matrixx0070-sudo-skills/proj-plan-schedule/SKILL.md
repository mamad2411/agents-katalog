---
name: proj-plan-schedule
version: 1.0.0
description: Build a project plan and schedule with milestones, a critical path, and realistic buffers.
author: matrixx0070
tags: [project-management, scheduling, critical-path, milestones, estimation]
---

## When to use

Use this once scope is agreed (see `proj-charter`) and you need a credible timeline: what gets done in what order, which dates are load-bearing, and where the plan will break if something slips. Reach for it when someone asks "when will this ship?" and you want an answer backed by dependencies, not a guess.

**Not for:** deciding feature priority or roadmap sequencing by value (that is product-management — the plan takes the prioritized scope as input). Not for standing team cadence, ceremonies, or process documentation (that is operations). This is a delivery schedule for one project's actual work.

## Method

1. Decompose scope into deliverables, then into tasks small enough to estimate (roughly 0.5-5 days each). Decision point: any task over 5 days gets split — big tasks hide risk.
2. Estimate each task in effort (person-days), not calendar time, and record who does it.
3. Map dependencies: for each task list what must finish before it can start (finish-to-start by default).
4. Set milestones — externally meaningful checkpoints (demo, integration done, launch), not every task.
5. Compute the critical path: the longest dependency chain to the end date. Decision point: only tasks on the critical path move the finish date — protect those first.
6. Add buffers where uncertainty lives, not uniformly. Put a project buffer at the end and feeding buffers where side chains join the critical path. Decision point: high-novelty or external-dependency tasks get a bigger buffer; routine tasks get little.
7. Convert effort to calendar dates using real availability (meetings, PTO, part-time allocation), then publish milestone dates.
8. Re-baseline when scope changes via `proj-change-control`; track slippage against milestones in `proj-status-update`.

## Example

Tasks: design (3d) → build API (5d) → build UI (4d, needs API) → integrate (2d) → launch. Critical path = design+API+UI+integrate = 14 effort-days. At 80% availability that is ~18 calendar days; add a 3-day end buffer → 21 days. Milestones: "API done" day 8, "integrated" day 16, "launch" day 21.

## Pitfalls

- **Effort read as calendar.** 14 person-days is not 14 days on the wall. Divide by real availability.
- **Buffer smeared everywhere.** Padding every task invites Parkinson's law. Concentrate buffer at the end and at merge points.
- **No critical path.** Without it you protect the wrong tasks. Identify the longest chain explicitly.
- **Milestone-per-task.** Fifty milestones mean none. Reserve milestones for externally meaningful checkpoints.

## Output format

```
# Plan: <project>  BASELINE <date>
MILESTONES: M1 <name> <date> | M2 <name> <date> | ...
TASKS:
| id | task | owner | effort(d) | depends-on |
CRITICAL PATH: <task ids in order> = <n> days
BUFFERS: project=<n>d | feeding: <chain>=<n>d
AVAILABILITY: <n>%   FINISH: <date>
```
