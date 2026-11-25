---
name: pa-schedule-optimizer
version: 1.0.0
description: Plan and optimize a day or week around the owner's priorities, energy rhythms, and fixed meetings.
author: matrixx0070
tags: [scheduling, calendar, planning, productivity, personal-assistant]
capabilities: []
---

## When to use

Use this when the owner wants a realistic plan for a day or week — fitting priority work, errands, and rest around meetings that cannot move. Good for a Sunday week-plan, a chaotic day with too many commitments, or reclaiming focus time.

**Not for:** long-term goal setting, multi-person meeting coordination (that needs polling attendees), or booking/rescheduling meetings with others on your own — you propose, the owner commits.

## Method

1. Gather three inputs: fixed commitments (meetings, appointments with set times), the priority list (what must progress), and energy profile (when the owner focuses best — default: deep work in the morning unless told otherwise).
2. Lock fixed commitments onto the timeline first; these are immovable anchors.
3. Decision point — do priorities fit the free gaps? If demand exceeds supply, surface the overflow and ask the owner to cut or defer rather than silently overpacking.
4. Place the highest-cognitive-load task in the peak-energy window; batch shallow tasks (email, errands, calls) into low-energy troughs.
5. Insert buffers: 10-15 min between meetings, a real lunch, and one flex block for the unexpected.
6. Decision point — any task depends on another or on someone's reply? Sequence it after the dependency; do not schedule blocked work.
7. Present the plan with a one-line rationale per block. Confirm before sending calendar invites or messaging anyone to move a meeting.

## Example

Inputs: 10am standup (fixed), 2pm dentist (fixed), priorities = finish report (deep), pay bills (shallow), gym.
Plan: 8:00-9:45 report (peak focus), 10:00 standup, 10:30-11:00 bills + buffer, 11:00-12:00 report cont., 12:00 lunch, 1:00 flex, 2:00 dentist, 4:30 gym. Rationale: report gets the pre-standup peak; bills batched into a low block.

## Pitfalls

- Packing 100% of hours. Leave 15-20% slack or the first surprise breaks the whole plan.
- Ignoring energy — scheduling the hardest task at 3pm slump guarantees it slips.
- Silently overcommitting when priorities exceed available time; make the owner choose.
- Auto-sending invites or reschedule requests. Confirm first — moving a meeting messages other people.

## Output format

```
SCHEDULE — [day/week] — [date range]

[HH:MM]-[HH:MM]  [block]   ([fixed | priority | buffer | flex])
...
OVERFLOW (did not fit): [items] — cut or defer?
NOTES: [energy/dependency rationale]

Next: reply YES to send invites / reschedule requests, or edit blocks first.
```
