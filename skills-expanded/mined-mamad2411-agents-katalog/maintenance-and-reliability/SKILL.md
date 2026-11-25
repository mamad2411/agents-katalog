---
name: maintenance-and-reliability
description: Keeps production assets available — ranking equipment by consequence of failure, setting preventive and predictive intervals, sizing spares, and moving a plant off reactive maintenance. Use this to build or fix a maintenance program, decide what to put on a PM schedule, diagnose repeat failures on one asset, justify spares inventory, or work out why a plant that maintains everything still has unplanned downtime.
---

# Maintenance and reliability

A plant that maintains everything equally maintains the wrong things. Maintenance effort is finite,
and spending it evenly across assets means the machine whose failure stops the line gets the same
attention as the one with three spares in the cabinet.

## Rank by consequence, not by age or cost

The question is not how likely a machine is to fail. It is what happens when it does.

Rank every asset on what its failure costs: production stopped, product scrapped, a safety event, a
regulatory exposure, or nothing anyone notices before the next shift. That ranking, not the capital
value, decides where preventive effort goes.

Two things this exposes immediately in most plants:

- **Assets with no redundancy and no spare** — the ones that will stop the plant and keep it stopped
  while a part ships. These are the whole list worth arguing about.
- **Assets on a PM schedule for no reason** — inherited from a manual, consuming hours, preventing
  nothing that would have mattered.

## Not everything wears out

The intuition behind interval-based maintenance is that failure probability rises with age, so
replacing on a schedule beats waiting. That holds for things that genuinely wear — belts, bearings,
seals, tooling, anything in contact.

It does not hold for most electronics, instrumentation and control systems, where failure rate is
roughly flat with age and intervention is itself a source of failure. Scheduled replacement of a
component that does not wear out converts a stable asset into one that gets disturbed on a cycle,
and introduces the installation errors that follow every disturbance.

So the interval has to be chosen by failure mode:

1. **Wears predictably** → interval-based replacement, set from observed life rather than the
   manual's default.
2. **Degrades observably** → condition-based. Vibration, thermal, oil analysis, current draw. Replace
   on the signal rather than the calendar.
3. **Fails randomly, consequence low** → run to failure, deliberately, with the decision recorded so
   it does not read as neglect.
4. **Fails randomly, consequence high** → redundancy or detection, because no interval helps.

Option 3 is a legitimate strategy and it is the one nobody writes down, which is why it gets
mistaken for the program failing.

## The backlog is the leading indicator

Downtime is a lagging measure. By the time it moves, the condition that produced it has been present
for months.

The honest leading indicator is the state of the planned-work backlog: how much identified work is
waiting, how old the oldest item is, and what fraction of the week's hours went to work that was
planned before the week started. A plant doing 80% planned work is in a different regime from one
doing 30%, and the second cannot schedule production reliably no matter how good its scheduler is.

The reactive trap is self-sustaining. Unplanned failures consume the hours that would have prevented
the next ones, so the ratio degrades on its own. Breaking it costs a deliberate, temporary
over-allocation to planned work while the backlog is worked down, and that is a decision someone has
to fund rather than a habit the team can adopt.

## Spares are an availability decision priced as inventory

A spare is bought against a downtime cost, not against a usage rate, which is why usage-based
reorder logic gets critical spares wrong in both directions. The part used twice a year sits at zero
and the plant waits six weeks for it.

Size the critical few on lead time and consequence: what it costs per day stopped, multiplied by the
realistic days to obtain. Everything else can run on consumption. Say which list each part is on,
because the finance conversation about slow-moving inventory will otherwise delete the critical
ones first — they are, by design, the parts that never move.

## Tooling

A computerized maintenance management system is the asset register, the work order history and the
PM schedule in one place. Fiix, Limble, UpKeep, eMaint, IBM Maximo and similar differ mostly in how
much configuration they demand; the failure mode is identical across all of them, which is a system
populated with assets and never with completed work orders. History is the entire value — without it
there is no observed failure interval and every PM stays at the manual's default.

Condition monitoring is a sensor and analysis decision before it is a software one. Portable
vibration and thermal instruments on a route cover most plants. Permanently installed monitoring on
a machine ranked at the top of the consequence list pays; installed everywhere it becomes a data
stream nobody reads.

Where the ERP holds the asset master — SAP PM, Oracle, Infor and similar — keep one register rather
than two. A maintenance system with its own asset list diverges from the financial one within a
year, and then neither is trusted.

## Never

- Put an asset on a preventive schedule without naming the failure mode it prevents.
- Treat repeat failures on one asset as bad luck rather than as an unfixed cause.
- Let unplanned work consume the hours allocated to planned work and call the ratio a result.
- Judge a maintenance program on downtime alone, which moves months after the cause does.
- Cut a critical spare because it has not moved.
