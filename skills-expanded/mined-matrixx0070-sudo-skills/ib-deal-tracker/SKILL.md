---
name: ib-deal-tracker
version: 1.0.0
description: Maintain a multi-deal M&A pipeline view — stage, milestones, next steps, and overdue items — so the deal team always knows what is moving, what is stuck, and what needs action today.
author: matrixx0070
tags: [investment-banking, m&a, pipeline, deal-management, productivity]
capabilities: []
---

## When to use
Use this when you are running or supporting several live mandates at once and need a single view of where each stands, what the next milestone is, and what has slipped. A deal tracker turns scattered status into one prioritized list: it maps each deal to its process stage, flags overdue items, and surfaces the actions that unblock progress this week.

**Not for:** the analytical work inside a single deal (use ib-datapack-builder / ib-merger-model), external buyer instructions (use ib-process-letter), or the pitch to win a mandate (use ib-pitch-deck). This tracks status; it does not do the deal work.

## Method
1. List every live and pipeline mandate with a codename, client, deal type (sell-side, buy-side, financing), and lead banker.
2. Tag each deal with its current process stage (pitch/mandate, preparation, marketing, first-round bids, management meetings, diligence, final bids, exclusivity, signing, closing).
3. Record the next milestone and its due date for each deal, plus the single owner responsible.
   **Decision point:** if a milestone due date has passed with no completion, mark it OVERDUE and escalate — overdue items are the tracker's primary output, not a footnote.
4. Capture the immediate next action per deal (what unblocks the next milestone) so the list is actionable, not just descriptive.
5. Note deal health: on-track, at-risk (slipping timeline, buyer drop-off, diligence issue), or stalled.
6. Sort the view by urgency: overdue and at-risk first, then upcoming milestones by date.
7. Refresh on a fixed cadence (e.g., start of each day/week) and circulate to the team; stale trackers are worse than none.

## Example
> A four-deal desk. Project Atlas (sell-side) was in final bids with an LOI due Friday — on track. Project Boreas (buy-side) had a diligence Q&A response overdue by three days — flagged OVERDUE, escalated to the lead, next action "chase seller counsel on rep-and-warranty schedule." Project Cirrus (financing) was at-risk after two lenders passed — next action "expand lender list." Project Delta was a live pitch. Tracker sorted overdue/at-risk to the top; refreshed each morning.

## Pitfalls
- Letting the tracker go stale so it no longer reflects reality — an out-of-date pipeline view actively misleads the team.
- Recording status without a next action, producing a description no one can act on.
- Burying overdue and at-risk items in a flat list instead of surfacing them first.
- Assigning a milestone to "the team" rather than one named owner, so nothing gets chased.

## Output format
```
DEAL PIPELINE — updated <date/time>

>>> NEEDS ACTION (overdue / at-risk)
Codename | Client | Type | Stage | Milestone (due) | Status | Next action | Owner
<...>    | ...    | ...  | ...   | ... (OVERDUE 3d) | at-risk| ...         | ...

ON TRACK
Codename | Client | Type | Stage | Next milestone (due) | Next action | Owner
<...>    | ...    | ...  | ...   | ...                  | ...         | ...

PIPELINE / PITCHES
Codename | Client | Type | Status | Next step | Owner

Summary: live <n> | at-risk <n> | overdue items <n> | closing this month <n>
```

## Reference
- Standard sell-side stages the tracker maps against: pitch/mandate -> preparation (teaser, CIM, datapack) -> marketing/outreach -> first-round bids (IOI) -> management meetings -> due diligence / data room -> final bids (LOI) -> exclusivity -> signing (SPA) -> closing.
- Buy-side and financing mandates have parallel milestone chains (target approach, IOI, diligence, financing commitment, close) and belong in the same view.
- The tracker's value is prioritization: overdue and at-risk deals surface first, each with one owner and one next action; a milestone without an owner does not move.
- Refresh cadence and single-source discipline matter more than tool choice — one current tracker beats several stale ones.
