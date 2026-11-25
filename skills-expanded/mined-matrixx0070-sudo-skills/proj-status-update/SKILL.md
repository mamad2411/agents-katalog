---
name: proj-status-update
version: 1.0.0
description: Write a project status update with RAG health, progress against plan, blockers, and specific asks.
author: matrixx0070
tags: [project-management, status, reporting, rag, communication]
---

## When to use

Use this for the recurring update that tells stakeholders whether the project is on track, what moved since last time, what is stuck, and what you need from them. Reach for it on your reporting cadence, or any time health changes materially (green to red) between cadences.

**Not for:** pitching a new feature or arguing roadmap direction (that is product-management). Not for authoring the standing reporting template or governance process itself (that is operations). This is a concrete, this-period update on one project's delivery.

## Method

1. Set overall RAG health with a rule, not a mood. Green = on plan; Amber = at risk, recoverable with action; Red = will miss a committed milestone without intervention. Decision point: if any critical-path milestone is threatened, the project is at least Amber regardless of overall vibe.
2. State progress against the plan: milestones hit since last update, and next milestone with its date and confidence (see `proj-plan-schedule`).
3. List blockers — only things actively stopping progress — each with an owner and what unblocks it (pull from `proj-raid-log`).
4. Make asks explicit and actionable: who, what, by when. Decision point: an ask with no named person and date is noise — either assign it or drop it.
5. Note changes to scope, date, or budget and point to the `proj-change-control` record.
6. Keep it skimmable: health and asks at the top, detail below. Decision point: if a busy sponsor reads only the first three lines, do they know the state and what you need? If not, rewrite the top.
7. Send on cadence even when green — silence reads as trouble.

## Example

Health: AMBER. Since last week: API milestone hit (day 8, on time). Next: integration by day 16, confidence medium. Blocker: waiting on auth service from Platform, owner Lee, unblocks integration — need it by day 12. Ask: Sponsor to escalate auth priority with Platform lead by Thu. Scope: unchanged. Budget: on track.

## Pitfalls

- **Watermelon status.** Green outside, red inside. Tie RAG to committed milestones, not optimism.
- **Activity as progress.** "The team worked hard" is not a milestone. Report against the plan's checkpoints.
- **Blockers with no owner.** Listing a problem nobody owns changes nothing. Name who and what unblocks it.
- **Vague asks.** "Need more support" is unactionable. Specify person, action, and deadline.

## Output format

```
# Status: <project>  <date>  HEALTH: 🟢/🟡/🔴
SUMMARY: <2 lines: state + top ask>
ASKS: <who> — <what> — by <when>
PROGRESS: hit=<milestones> | next=<milestone> <date> conf=<H/M/L>
BLOCKERS: <blocker> — owner <name> — unblocks by <date>
CHANGES: scope/date/budget → <ref to change-control or "none">
```
