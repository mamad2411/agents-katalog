---
name: proj-retrospective
version: 1.0.0
description: Facilitate a project retrospective and convert it into owned, dated action items.
author: matrixx0070
tags: [project-management, retrospective, lessons-learned, actions, facilitation]
---

## When to use

Use this at a milestone, phase end, or project close to turn the team's raw experience into a small set of changes that actually get made. Reach for it when the same problems keep recurring, or when a phase just ended and the lessons are still fresh. The output is action items with owners — not a feelings session.

**Not for:** deciding what to build next or reprioritizing the roadmap (that is product-management). Not for maintaining the permanent lessons-learned repository or the retro template as a standing artifact (that is operations). This facilitates one retro for one team and produces concrete follow-through.

## Method

1. Set safety and scope first: this is about the system, not blame; time-box it (45-60 min). Decision point: if trust is low, gather input anonymously before the meeting so real issues surface.
2. Gather data across three buckets: what went well (keep), what hurt (stop), what to try (start). Get specifics with examples, not generalities.
3. Cluster into themes and vote to focus. Decision point: pick the top 3 themes — a retro that tries to fix everything fixes nothing.
4. For each chosen theme, ask "why" until you reach a changeable cause, not a symptom.
5. Convert to action items: each has an owner, a concrete first step, and a due date. Decision point: if an item has no owner or is not doable in the next cycle, cut or reshape it — unowned actions never happen.
6. Close the loop: review last retro's actions at the start of this one. Decision point: if prior actions did not happen, fix the follow-through mechanism before adding new items.
7. Feed systemic risks into `proj-raid-log` and process changes to the owning team.

## Example

Keep: pairing sped up the API build. Stop: last-minute scope adds broke the schedule twice. Start: enforce change control. Top theme = uncontrolled scope. Why → no gate on requests → requests went straight to devs. Action: "Owner routes all new requests through `proj-change-control`; first CR logged by next Mon" — owner: you, due Mon. Reviewed at next retro: it stuck, scope-slip incidents dropped to zero.

## Pitfalls

- **Blame over system.** Naming people shuts down honesty. Frame every issue as a process or condition to change.
- **Actionless catharsis.** A good vent that changes nothing. End with owned, dated items or it was wasted time.
- **Boiling the ocean.** Twenty actions, zero done. Pick three; ship them.
- **No follow-through check.** New retro, ignored old actions. Always open by reviewing the previous list.

## Output format

```
# Retro: <project/phase>  <date>
PRIOR ACTIONS REVIEW: <done / not-done + why>
WENT WELL (keep): <items>
HURT (stop): <items>
TRY (start): <items>
TOP THEMES: 1) <> 2) <> 3) <>
ACTIONS:
- [ ] <action> — owner <name> — due <date>
ESCALATED: <systemic risk → RAID / process → team>
```
