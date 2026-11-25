---
name: proj-dependency-map
version: 1.0.0
description: Map cross-team dependencies and sequence them so no team is blocked waiting on another.
author: matrixx0070
tags: [project-management, dependencies, sequencing, cross-team, coordination]
---

## When to use

Use this when your project needs work, decisions, or artifacts from teams you do not control, and the order of hand-offs determines whether you ship on time. Reach for it whenever "we're blocked on another team" is a recurring phrase, or before committing a date that depends on someone else's delivery.

**Not for:** deciding which capabilities to build or their business value (that is product-management). Not for the org chart or the standing RACI of who-owns-what across the company (that is operations). This maps the specific inter-team hand-offs for one project and puts them in a workable order.

## Method

1. List every external need: for each, the providing team, the exact artifact/decision, and the date you need it. Decision point: if you cannot name a concrete artifact, it is not yet a dependency — clarify the ask first.
2. Classify direction: inbound (you need from them) and outbound (they need from you). Outbound matters — other teams are planning around you too.
3. Build the sequence: order needs by when each must land, working backward from your milestones (see `proj-plan-schedule`).
4. Find the chains and the circular waits. Decision point: if Team A waits on you while you wait on Team A, break the cycle by splitting one deliverable into a smaller unblocking piece.
5. Confirm each dependency with the providing team — get an owner and a committed date on their side, not your assumed date. Decision point: unconfirmed dependencies are risks, not plans — log them in `proj-raid-log`.
6. Identify the single longest cross-team chain; that is your coordination critical path — review it every status cycle.
7. Publish the map and the needed-by dates so every team sees its slot.

## Example

Needs: (inbound) auth service from Platform by day 10; design tokens from Design by day 5. (outbound) API contract to Mobile by day 6. Backward from launch day 21: UI needs auth by 10, auth needs the contract Platform agreed to by day 3. Circular wait found: Platform wanted final UI before building auth — broke it by giving them the contract stub on day 3 so both proceed in parallel.

## Pitfalls

- **Inbound-only view.** Ignoring what others need from you makes you the blocker. Map outbound too.
- **Assumed dates.** "They'll have it by day 10" without their confirmation is fiction. Get a committed owner and date.
- **Hidden circular waits.** Two teams each waiting on the other stall silently. Trace chains and split to break cycles.
- **Vague asks.** "We need help from Data" cannot be scheduled. Name the exact artifact and date.

## Output format

```
# Dependency Map: <project>
INBOUND:  | id | need (artifact) | from-team | needed-by | confirmed-by | status |
OUTBOUND: | id | deliverable | to-team | their-need-by | status |
SEQUENCE: <ordered ids by needed-by date>
COORDINATION CRITICAL PATH: <chain of ids>
CYCLES BROKEN: <how>
```
