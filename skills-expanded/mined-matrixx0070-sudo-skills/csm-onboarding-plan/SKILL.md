---
name: csm-onboarding-plan
version: 1.0.0
description: Build a customer onboarding plan that drives a new account to its first measurable value.
author: matrixx0070
tags: [customer-success, onboarding, time-to-value, retention, adoption]
capabilities: []
---

## When to use

Use this when a newly closed account needs a structured path from kickoff to first value, and you own the outcome. Reach for it whenever you must define what "first value" means for a specific customer, sequence enablement, and set milestones the account will actually hit.

**Not for:** reactive ticket triage or bug resolution (that is customer-support); closing the original deal or negotiating price (that is sales); renewal or expansion planning on an already-adopted account (see csm-renewal-prep and csm-expansion-play).

## Method

1. Capture the customer's stated business goal and the metric that proves it. If the goal is vague, ask one scoping question before proceeding.
2. Define the **first-value event** — the smallest concrete outcome that proves the product works for them (e.g., "first report shared with their exec"). Decision point: if you cannot name a single event, the account is under-scoped — pause and align with the buyer.
3. Identify roles: executive sponsor, admin/implementer, and end users. Decision point: if there is no sponsor, escalate before building the plan; sponsorless onboarding stalls.
4. Work backward from the first-value event into 3-5 milestones with owners and target dates.
5. Map enablement (training, docs, config) to each milestone. Decision point: if a milestone depends on the customer's IT/data, add a dependency owner and a slack buffer.
6. Set a cadence (weekly check-ins during onboarding) and a single success metric to review each time.
7. Define exit criteria: onboarding is "done" only when the first-value event fires and the sponsor confirms it.

## Example

Account: mid-market SaaS, bought your analytics tool. Goal: "cut weekly reporting time." First-value event: finance lead auto-generates the Monday revenue report instead of building it by hand. Milestones: (1) data source connected — day 3, admin; (2) report template built — day 7, CSM+admin; (3) finance lead trained — day 10; (4) first auto-report shared with CFO — day 14. Success metric: hours spent on the Monday report (baseline 6h → target <1h). Exit: sponsor confirms the day-14 report shipped.

## Pitfalls

- **Feature tours instead of outcomes.** Teaching every feature delays value; teach only what the first-value event requires.
- **No named sponsor.** Onboarding without an accountable executive drifts and silently churns.
- **Dates with no owners.** A milestone without a single owner is a wish, not a plan.
- **Declaring "done" at go-live.** Provisioning is not value; exit only on the confirmed first-value event.

## Output format

```
ONBOARDING PLAN — <account>
Business goal: <goal> | Success metric: <metric> (baseline → target)
First-value event: <single concrete outcome>
Sponsor: <name> | Admin: <name> | End users: <segment>

Milestones
1. <milestone> — owner: <name> — due: <date> — enablement: <what>
2. ...
Cadence: <weekly check-in day/time>
Dependencies/risks: <item — owner>
Exit criteria: first-value event fired AND sponsor confirmed
```
