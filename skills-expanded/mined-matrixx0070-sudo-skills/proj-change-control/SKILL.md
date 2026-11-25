---
name: proj-change-control
version: 1.0.0
description: Run change control on a scope, schedule, or budget change — assess impact, decide, and re-baseline.
author: matrixx0070
tags: [project-management, change-control, scope, impact, governance]
---

## When to use

Use this when something wants to change the committed baseline: new scope requested, a date slips, budget shifts, or a dependency changes what is possible. Reach for it the moment a change is proposed — before the team quietly absorbs it. The point is a traceable decision, not a veto.

**Not for:** deciding whether a feature is worth building on its merits (that is product-management — change control assesses the *delivery impact* of that decision, not the product value). Not for the organization's standing change-approval policy (that is operations). This runs one specific change against one project's baseline.

## Method

1. Log the change request: what is changing, who requested it, and why now. Give it an id.
2. Assess impact across all three axes — scope, schedule, budget — even if only one is requested. Decision point: a "small scope add" almost always moves schedule; compute the knock-on before deciding.
3. Recompute the critical path and milestones with the change applied (see `proj-plan-schedule`). Quantify: +N days, +$X, +M scope items.
4. List options, not just yes/no: absorb (find slack), extend (move the date), trade (cut something to fit), or reject. Decision point: if absorbing means overtime or eroding buffer, name that cost explicitly — hidden absorption is how projects go red.
5. Route to the decision authority — the Sponsor for baseline-moving changes, the Owner for within-tolerance ones. Decision point: define tolerance up front (e.g. Owner decides < 2 days / < $1k; above that goes to Sponsor).
6. Record the decision, rationale, and new baseline. Update the charter, plan, and RAID log.
7. Communicate the re-baseline in the next `proj-status-update` — everyone plans off the same dates.

## Example

CR-4: "Add SSO to launch scope," requested by Sales. Impact: +6 effort-days, pushes launch from day 21 to day 27, +$0. Options: (a) extend to day 27, (b) trade — drop the reporting dashboard to hold day 21, (c) reject, ship SSO in fast-follow. Sponsor picks (c): launch holds, SSO becomes v1.1. Baseline unchanged; RAID gets a follow-on dependency. Logged and announced in Friday status.

## Pitfalls

- **Silent absorption.** Team eats the change without re-baselining; the plan lies until it slips. Log and decide every change.
- **One-axis tunnel vision.** Approving scope without computing schedule/budget knock-on. Assess all three.
- **Yes/no framing.** Forcing accept-or-reject hides better trades. Always present absorb/extend/trade/reject.
- **Wrong approver.** Owner rubber-stamping a date-moving change bypasses the Sponsor. Enforce the tolerance rule.

## Output format

```
# Change Request <id>: <title>  <date>
REQUESTED-BY: <name>  WHY: <reason>
CHANGE: <what changes>
IMPACT: scope +<items> | schedule +<n>d (new finish <date>) | budget +<$>
OPTIONS: absorb <cost> | extend <date> | trade <cut> | reject <fallback>
DECISION: <chosen> by <authority> on <date>  RATIONALE: <one line>
NEW BASELINE: <finish/budget/scope>   UPDATED: charter|plan|RAID
```
