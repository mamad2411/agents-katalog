---
name: wayfinder
description: "Lay out a scope larger than one session as a map of decision tickets on the tracker, solved one at a time until the route to the goal clears. Plan, do not build. Trigger words (RU+EN): разложи на тикеты, карта решений, маршрут, больше одной сессии, спланируй эпик / break into tickets, decision map, route, larger than one session, plan the epic."
disable-model-invocation: true
---

# Wayfinder

A large idea arrives — too big for one session, in fog: the path from here to the **goal** is not
yet visible. Wayfinding is finding that path, not lunging at the goal. The skill draws the path as a
**shared map** on the repository tracker, then works its **decision tickets** (questions whose
resolution is a decision, not a piece of the build) one at a time, until the route clears.

## Plan, do not build

By default this is **planning**: each ticket resolves a decision, the map is done when the path is
clear — nothing left to decide before someone goes and builds. The urge to just start building is
usually a signal that the edge of the map is reached and it is time to hand off to execution. The
product of wayfinder is **decisions, not artifacts** (unless the map's Notes explicitly allow
otherwise).

## Reference by name

Each ticket is an issue; it has a **name** (the title). In everything a human reads, reference by
name, not by a bare number. A wall of `#42, #43, #44` is unreadable; names read at a glance. The
number/URL does not vanish — it is inside the named link, but not instead of it.

## The map

One issue on the tracker, labeled `wayfinder:map` — the canonical artifact. Its tickets are child
issues. The map is an **index, not a store**: it lists accepted decisions and points to the tickets
with the details; a decision lives in one place — its own ticket. The map body (loaded once per
session):

```markdown
## Goal
<what the end of the path looks like — a spec, a decision or a change we head to. 1–2 lines.>

## Notes
<the domain; skills every session must check against; standing preferences>

## Decided so far
- <title of the closed ticket> — <link> — <one-line gist of the answer>

## Not yet specified
<fog in the scope that cannot yet be ticketed; comes out of the fog as the frontier advances>

## Out of scope
<work beyond the goal; closed, does not come out of the fog>
```

## Tickets

Each decision ticket resolves ONE decision question. Open tickets are open child issues, found by a
query, not listed in the map body. Resolved a ticket → close it, the gist to "Decided so far".

Maps well onto Gitea + Milestone (the epic = the map, sub-issues = the tickets). Pairs with
[[task-cycle]]: once the route is clear — plan and execution.

## Seams and the spec's altitude (donor to-spec)

When the map's goal is a **spec** (a high-level design, see "Goal") and not just a set of decisions,
hold two disciplines.

**The test seam — sketch it in advance.** This is the same **seam** from the [[task-cycle]] design
vocabulary (a boundary where behavior can be substituted and a decision checked — per Feathers);
here it is the discipline of CHOOSING it. Prefer an EXISTING seam to a new one; take the HIGHEST one
possible (closer to the system boundary — fewer couplings to check); **the ideal number of seams =
one**. More than one — check with the owner: each extra seam is an extra checking boundary and
coupling.

**A spec — without paths and snippets.** File paths and code snippets in a spec rot faster than
prose: a refactor tears them, a decision it does not. The exception is a snippet that encodes a
DECISION more precisely than prose (a state machine, a schema, a type): keep it. Do not mix
altitudes: an **execution ticket** [[task-cycle]] carries a "Files:" block (it is about the build) —
unlike the wayfinder **decision ticket** above (that is about a decision, carries no "Files:"); a
**spec** carries no paths at all. A spec with paths ages into a dead artifact.

## When NOT to apply

- **The scope fits one session.** A map of three tickets costs more than the work itself: take the
  task and do it by [[task-cycle]].
- **The path is already clear.** Wayfinding seeks a route; when there is nothing to decide, the map
  turns into an inventory of the upcoming build — and that is a task plan, not a map.
- **Not for execution.** A decision ticket and a build ticket live at different altitudes, and
  mixing them turns the map into a backlog.
- **Not for the urgent.** Resolving decisions one at a time takes as long as it takes; what is on
  fire is fixed, not mapped.
