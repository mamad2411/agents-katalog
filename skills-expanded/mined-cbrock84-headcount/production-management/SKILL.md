---
name: production-management
description: Runs the production schedule — sequencing and releasing work, managing work in process and changeovers, and holding the promised date when the floor and the order book disagree. Use this to build or fix a production schedule, decide what to run next, diagnose why lead times are growing while machines look busy, set up OEE or throughput measurement, or choose between make-to-stock and make-to-order for a product line.
---

# Production management

The schedule is a promise made to a customer using capacity you do not fully control. Most plants
that miss dates are not short of machine hours. They are running a sequence that maximizes
utilization on each machine and no one is accountable for the order.

## Sequence is the decision, not the loading

Loading answers how much work a resource has. Sequence answers what the customer gets and when, and
it is the part usually left to whoever is standing at the machine.

Two sequences with identical total hours produce very different outcomes:

- **Grouped by setup** — run everything in the same color, material or die together. Maximizes
  machine output, and pushes any order that does not fit the current group to the back.
- **Grouped by due date** — run what is owed soonest. Protects dates, and pays for it in changeovers.

Neither is correct in general. What is not acceptable is the choice being made implicitly, shift by
shift, by someone with no view of the order book. Decide the rule, write it down, and state what
overrides it — because something always will, and an unstated override is how a schedule quietly
stops meaning anything.

## Work in process is the lead time

Little's Law is the whole of it: lead time equals work in process divided by throughput. Releasing
more work into a plant that is already full does not make anything come out sooner. It lengthens
every job on the floor, including the one that was on time.

The practical consequence is that **release is a control and most plants do not use it as one**.
Work is released when the order arrives or when the paperwork clears, and the floor absorbs it.
Capping releases against a work-in-process target feels like doing less and shortens quoted lead
times measurably.

The tell that release is uncontrolled: expediting works. If pushing a job to the front reliably
gets it out, there is enough queue on the floor to hide the cost, and someone else's date moved.

## Changeover is capacity you can buy back

Setup time is usually treated as fixed, so the response to losing capacity to it is longer runs,
which raises inventory and lengthens lead times for everything else.

Attack the setup instead. Separate the work that can be done while the machine is still running —
staging material, pre-setting tooling, moving the next die to the press — from the work that
genuinely requires it stopped. Most first attempts find that a third or more of the setup did not
need the machine idle. That recovered time is real capacity, and it costs nothing.

The second-order effect matters more than the recovered hours: cheaper changeovers make small runs
viable, which makes due-date sequencing affordable, which is what protects the promise.

## OEE tells you where, not whether

Overall equipment effectiveness multiplies availability, performance and quality. Its value is the
decomposition — a line at 60% for three different reasons needs three different fixes.

Two ways it misleads:

- **On a non-bottleneck it is noise.** Improving OEE on a resource that is not constraining output
  produces inventory, not throughput. Measure it where the constraint is.
- **It rewards running.** A line kept running to protect the number, making parts nobody ordered,
  scores well. Pair it with schedule adherence or it will quietly optimize for the wrong thing.

Throughput at the constraint, plus on-time delivery, answers the business question. OEE answers the
engineering question underneath it.

## Make-to-stock and make-to-order are a lead-time decision

The choice is between holding inventory and holding the customer waiting, and it is made per product
family rather than per plant.

Make-to-stock where demand is predictable, the item is standard, and the customer's tolerance for
waiting is shorter than the production lead time. Make-to-order where variety is high, the item
carries customer-specific content, or obsolescence risk is real.

The hybrid is usually the right answer and rarely stated: hold the common part as stock, finish to
order. That moves the decoupling point as late as possible, which is where inventory is cheapest and
most flexible. `operations:capacity-and-demand-planning` holds the demand side of this decision.

## Tooling

Scheduling and shop-floor execution is where an ERP is either doing the work or being worked around.
SAP, Oracle NetSuite, Epicor Kinetic, Infor CloudSuite Industrial, Odoo and similar carry the order
book, routings and material availability, and the schedule should come from the same system that
knows whether the material is there.

Finite-capacity scheduling — PlanetTogether, Preactor, Opcenter APS and similar — earns its place
where sequence-dependent setups, shared tooling or constrained labor make the ERP's infinite-capacity
plan fiction. Below that complexity a well-maintained spreadsheet with a stated sequencing rule beats
a scheduler nobody trusts.

Machine-level data collection sits underneath OEE. At scale, a manufacturing execution system;
below it, a tablet at the line and an honest downtime reason code list are enough to find the top
three causes, which is all the first year needs.

## Never

- Release work into a full plant because the order arrived.
- Let sequence be decided at the machine by whoever is standing there.
- Improve utilization on a resource that is not the constraint and call it capacity.
- Quote a lead time from routed hours rather than from observed work in process.
- Report a schedule as met after the dates were moved to match what shipped.
