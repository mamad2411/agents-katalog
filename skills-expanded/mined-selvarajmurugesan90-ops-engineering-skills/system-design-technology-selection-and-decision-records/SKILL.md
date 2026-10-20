---
name: system-design-technology-selection-and-decision-records
description: >
  Guides architect-level engineering work: system-wide architecture
  design spanning multiple teams/services, technology evaluation and
  selection using a real framework (requirements, tradeoffs,
  proof-of-concept criteria, total cost of ownership — not "pick the
  popular one"), writing and maintaining Architecture Decision Records
  (ADRs) that capture context and reasoning for future readers, and
  balancing architectural ideals against organizational and team-maturity
  constraints. Use when an architect (or an agent acting as one) is asked
  to "design the architecture for X across these teams," "evaluate/select
  a technology (database, messaging system, framework)," "write an ADR
  for this decision," or "decide the right architecture given our team's
  actual constraints, not the textbook-ideal one."
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: role-based-engineering-practices
  maturity: stable
---

# System Design, Technology Selection, and Decision Records

## Purpose

Architect-level work operates one level above sequencing a single team's
roadmap (the lead-level work in
[technical-roadmap-ownership-and-cross-team-coordination](../technical-roadmap-ownership-and-cross-team-coordination/SKILL.md)):
it sets the constraints multiple teams design within, chooses the
technologies those teams will live with for years, and is responsible for
whether those choices actually fit the organization that has to operate
them — not just whether they look correct on a whiteboard. A technology
picked because it's popular, or an architecture designed to the textbook
ideal while ignoring the team's actual operational maturity, both fail in
the same way: they work in the proof-of-concept and then become an
expensive, hard-to-reverse mismatch once real teams have to run them at
scale. An Architecture Decision Record (ADR) written honestly, at the
time a decision is made, is what makes that decision legible and
reversible-in-principle for whoever inherits it later — an ADR written
after the fact to justify a decision already made is not a decision
record, it's a rationalization, and it fails the one job an ADR actually
has. This skill covers system-wide design across team/service
boundaries, a real technology-selection framework, writing ADRs that
capture genuine reasoning, and deliberately weighing organizational
constraints against architectural ideals rather than picking one and
ignoring the other.

## When to use

- Designing an architecture that spans multiple teams or services — a
  new system's service boundaries, a major cross-cutting change (e.g.
  introducing an event bus, splitting a monolith), or resolving a
  structural conflict between teams' existing systems.
- Evaluating and selecting a significant technology (a database, a
  messaging system, a framework, a cloud provider) where the choice will
  be expensive to reverse and needs a defensible, repeatable evaluation
  rather than a preference.
- Writing or reviewing an Architecture Decision Record for a consequential
  technical decision, especially one that's contested or non-obvious in
  hindsight.
- A design looks architecturally "correct" in isolation but doesn't
  actually fit the team(s) who will build and operate it — under-skilled
  for the chosen technology, understaffed for the operational burden it
  implies, or organizationally unable to sustain the coordination the
  design requires.
- Revisiting an old architectural decision to understand why it was made,
  and the only record is a Slack thread or nothing at all.

## Prerequisites & environment

- A clearly scoped problem and its actual requirements — the specific
  scale, latency, consistency, and failure-tolerance needs of the system
  being designed — gathered from the teams and stakeholders who will
  build and operate it, not assumed from a generic "how big companies do
  it" reference.
- Visibility into the organization's actual operational maturity for a
  given technology choice: existing team skills, on-call capacity,
  observability tooling maturity, and appetite for operating a new class
  of system — this is what "total cost of ownership" and "team maturity"
  mean concretely in the selection framework below, not an abstract
  concern.
- A shared, versioned place to store ADRs (a `docs/adr/` directory in the
  relevant repo, an architecture wiki with version history) that the
  whole organization — not just the authoring team — can find and read.
- Standing or ad hoc access to a cross-team architecture review forum
  (an architecture review board, a staff/principal engineering group, or
  equivalent) where a system-wide design or a significant technology
  choice gets peer-reviewed before being finalized, not decided in
  isolation.
- Enough time and organizational buy-in to run an actual
  proof-of-concept for a significant technology choice — a selection
  framework that's supposed to include PoC criteria doesn't work if
  there's no room ever budgeted to run one.

## Step-by-step guidance

1. **State the actual requirements before comparing options** — scale
   (current and a realistic multi-year projection, not an aspirational
   one), consistency/availability needs, latency budget, data volume and
   growth rate, and any hard compliance/data-residency constraints.
   Requirements gathered after a preferred technology is already chosen
   tend to describe that technology's strengths rather than the
   system's actual needs.

2. **Use a real technology-selection framework**, not a preference vote:
   ```markdown
   # Technology selection: event streaming for order-events

   ## Requirements
   - Sustained throughput: ~2,000 events/sec, burst to 8,000/sec during
     sales events.
   - At-least-once delivery acceptable; consumers are idempotent.
   - Retention: 7 days for replay during consumer outages.
   - Must integrate with existing AWS infrastructure (no new cloud
     provider).

   ## Options considered
   | Option | Fit to requirements | Team familiarity | Operational burden | Est. 3-yr TCO |
   |---|---|---|---|---|
   | Amazon MSK (managed Kafka) | Strong (throughput, retention) | Low — no team has run Kafka | Medium (managed, but still needs Kafka expertise) | $$$ (infra + ramp-up time) |
   | Amazon SQS + SNS fan-out | Adequate (meets throughput, weaker replay semantics) | High — already used elsewhere | Low | $ |
   | Self-hosted Kafka on EKS | Strong | Low | High (full operational ownership) | $$$$ |

   ## Proof-of-concept criteria (defined before running the PoC)
   - Sustain 8,000 events/sec burst for 10 minutes with <1% consumer lag
     growth.
   - Consumer restart after a 30-minute outage catches up within 15
     minutes from retained events.
   - Team can stand up a working producer/consumer pair within 2 days
     using only public documentation (a proxy for operational
     learnability).

   ## Decision
   Amazon MSK, contingent on the PoC criteria above passing. SQS/SNS
   rejected on replay semantics (no real retention/replay); self-hosted
   Kafka rejected on operational burden — no team currently has the
   on-call capacity to run Kafka's own operational surface (broker
   failure, partition rebalancing) on top of everything else they own.
   ```
   Total cost of ownership must include the ongoing operational burden
   (on-call load, expertise the team needs to build or hire, upgrade/
   patching overhead) — not just licensing or infrastructure spend —
   since an operationally expensive choice shows up as toil and incidents
   long after the initial build cost is forgotten.

3. **Run the proof-of-concept against criteria defined in advance**
   (step 2), not criteria adjusted afterward to fit whichever option
   already "won" internally — a PoC whose success criteria are decided
   after seeing the results isn't evidence, it's a formality.

4. **Explicitly weigh organizational and team-maturity constraints
   against the architecturally "ideal" choice**, and say so in the
   decision. The textbook-best architecture for a problem, run by a team
   that doesn't yet have the operational maturity to run it safely, is
   frequently the worse real-world choice than a simpler design the team
   can actually operate reliably — state this trade-off explicitly rather
   than silently picking the "correct" answer and letting the
   operational gap surface later as recurring incidents.

5. **Design system boundaries around team/service ownership that will
   actually hold**, not an idealized decomposition that ignores which
   team can realistically own which piece — a beautifully decomposed set
   of microservices that no team is staffed to operate individually is a
   worse outcome than a coarser boundary matched to real team
   capacity, echoing the "thinnest viable" sizing discipline in
   [platform-engineering-team-topology-and-operating-model](../../../internal-developer-platform/skills/platform-engineering-team-topology-and-operating-model/SKILL.md).

6. **Write the ADR at decision time, not after the fact**, using a
   consistent template:
   ```markdown
   # ADR 0007: Use Amazon MSK for order-events streaming

   ## Status
   Accepted (2026-07-28)

   ## Context
   order-events currently fan out via direct service-to-service HTTP
   calls, causing cascading failures when a downstream consumer is slow
   or down. We need durable, replayable, at-least-once delivery for
   ~2,000 events/sec sustained, 8,000/sec burst, with 7-day retention for
   consumer-outage recovery.

   ## Decision
   Adopt Amazon MSK (managed Kafka) as the event-streaming backbone for
   order-events, replacing direct HTTP fan-out.

   ## Alternatives considered
   - SQS + SNS fan-out: rejected — no real replay/retention semantics
     for a 30+ minute consumer outage.
   - Self-hosted Kafka on EKS: rejected — no team currently has on-call
     capacity for broker/partition operational burden; revisit if a
     platform team forms with that capacity.

   ## Consequences
   - Producers/consumers must implement idempotent processing (at-least-
     once delivery, not exactly-once).
   - Introduces a new operational dependency (MSK) requiring on-call
     familiarity; a Kafka fundamentals runbook and on-call training are
     required before this ships to production (tracked in
     `PLAT-4821`).
   - Reversible in principle by migrating consumers back to direct calls
     or another queue, but at real migration cost — this is not a
     trivially reversible decision, factored into the confidence level
     of this ADR.

   ## Confirmed by proof-of-concept
   Burst throughput, consumer-lag-recovery, and team-learnability
   criteria (see technology-selection note) all passed on `<PoC date>`.
   ```
   An ADR's **Context** section should describe the situation as it
   actually was when the decision was made — including uncertainty, the
   alternatives seriously considered, and what wasn't yet known —
   because that is exactly the information a future reader needs and the
   thing "after the fact" writing loses.

7. **Store ADRs where they'll actually be found later** (a versioned
   `docs/adr/` directory, numbered sequentially, indexed) and mark
   superseded ADRs explicitly (`Status: Superseded by ADR 0014`) rather
   than deleting or silently ignoring them — an ADR trail with gaps or
   silent overwrites is nearly as unhelpful as no ADRs at all.

8. **Revisit and mark ADRs as superseded when circumstances genuinely
   change** (team maturity grows, requirements shift, the chosen
   technology's vendor deprecates it) — an ADR is a record of the
   reasoning at the time, not a permanent commitment; the record's value
   is in showing *why* the original call made sense then, which is
   exactly what lets a future architect evaluate whether it still does.

## Best practices

- Gather requirements from the people who will operate the system, not
  only the people who requested it — operational reality (on-call
  capacity, existing tooling, team skill) is as much a real requirement
  as throughput and latency.
- Define PoC success criteria before running the PoC, in writing, and
  hold to them — adjusting criteria after seeing results turns
  validation into confirmation bias.
- Include operational total cost of ownership (on-call burden, expertise
  to build/hire, upgrade overhead) in every technology comparison, not
  just build/license/infra cost.
- State the organizational-maturity trade-off explicitly when it changes
  the decision — "we chose the operationally simpler option because no
  team currently has capacity to run the more powerful one" is a
  legitimate, honest architectural decision, not a compromise to hide.
- Write the ADR's Context section as it genuinely was at decision time,
  including real uncertainty and rejected alternatives — a future reader
  needs to know what wasn't known yet, not just what was eventually
  chosen.
- Version and index ADRs somewhere durable and organization-visible;
  mark superseded ADRs explicitly rather than deleting them.
- Route a design decision through a cross-team review forum before it's
  finalized when it affects multiple teams — a system-wide design
  decided in isolation by one architect is exactly the kind of decision
  most likely to need reworking once other teams' real constraints
  surface.

## Common pitfalls

- **Symptom:** A technology is selected because it's the most popular
  choice in the industry or a well-known reference architecture, without
  a documented comparison against the system's actual requirements or
  the team's operational maturity.
  **Fix:** Popularity is evidence of ecosystem support, not of fit —
  run the actual comparison (step 2) including operational TCO and team
  familiarity; "everyone uses it" is one input to a decision, not the
  decision itself.

- **Symptom:** An ADR is written weeks after a technology was already
  chosen and partially implemented, and reads as a justification for the
  existing choice — every "alternative considered" is dismissed in one
  line, and there's no real record of what was actually uncertain at
  decision time.
  **Fix:** This is a significant, if quiet, failure mode — an ADR written
  after the fact to rationalize a decision already made loses the one
  thing an ADR is for: capturing genuine reasoning and real
  uncertainty for a future reader. Write ADRs at decision time, before
  or immediately alongside implementation starting, not as retroactive
  documentation.

- **Symptom:** A system is decomposed into a textbook-ideal set of
  fine-grained microservices, but no individual team has the staffing to
  own more than one or two of them, and cross-service coordination
  overhead ends up slower than the monolith it replaced.
  **Fix:** Design service boundaries around what teams can realistically
  own and operate (step 5), not around the theoretically cleanest
  decomposition — an architecturally elegant design that no team can
  actually run well is a worse outcome in practice than a coarser one
  matched to real team capacity.

- **Symptom:** A proof-of-concept "passes" but its success criteria were
  written or adjusted after the results were already in, and the chosen
  technology later struggles in production exactly where the original,
  unadjusted criteria would have caught the gap.
  **Fix:** Define PoC criteria in writing before running it (step 3) and
  hold to them regardless of outcome; if a criterion turns out to be the
  wrong bar after the fact, revise it for the *next* decision's process,
  not retroactively for this one.

- **Symptom:** An architecture decision from three years ago is still
  being followed literally, even though the team's operational maturity,
  scale, or the chosen technology's vendor support has changed
  substantially since — and nobody has revisited whether it still makes
  sense because the original ADR (if one exists at all) is undated,
  unindexed, or lost.
  **Fix:** Store ADRs durably and indexed (step 7), and treat a
  materially changed circumstance (team maturity, scale, vendor
  deprecation) as a trigger to write a new ADR that explicitly supersedes
  the old one (step 8) — an ADR is a record of reasoning at a point in
  time, not a decision that self-updates.

## Worked example

**Scenario:** An architect is asked to design the event-streaming
backbone for `order-events` across three teams (checkout, fulfillment,
notifications) that currently communicate via brittle direct HTTP calls.

1. **Requirements gathered from all three teams** (not just checkout,
   who requested the change): checkout needs durable publish; fulfillment
   needs at-least-once delivery with idempotent consumption; notifications
   needs replay capability for a planned backfill feature. Combined:
   ~2,000 events/sec sustained, 8,000/sec burst, 7-day retention.
2. **Technology selection** run per step 2: Amazon MSK, SQS+SNS, and
   self-hosted Kafka on EKS compared on fit, team familiarity, operational
   burden, and 3-year TCO (the table above). PoC criteria defined in
   writing beforehand.
3. **PoC run against those pre-defined criteria**: MSK sustains the burst
   target with acceptable consumer lag recovery; a two-day
   documentation-only ramp-up test confirms a team unfamiliar with Kafka
   can stand up a working producer/consumer pair, addressing the
   operational-maturity concern directly rather than assuming it away.
4. **Organizational constraint made explicit**: self-hosted Kafka would
   give more operational control, but no team currently has on-call
   capacity for broker-level operations — the decision explicitly names
   this trade-off rather than defaulting to the "more powerful" option
   or silently picking the "safe" one without saying why.
5. **Service boundaries designed around real ownership**: rather than
   each team also standing up its own Kafka-adjacent tooling, a single
   shared "event infrastructure" ownership sits with the platform team
   (see
   [platform-engineering-team-topology-and-operating-model](../../../internal-developer-platform/skills/platform-engineering-team-topology-and-operating-model/SKILL.md)),
   with checkout/fulfillment/notifications as X-as-a-Service consumers.
6. **ADR 0007 written at decision time** (the template in step 6), stored
   in `docs/adr/0007-order-events-streaming.md`, reviewed by the
   cross-team architecture forum before being marked Accepted.
7. **Eighteen months later**, notification volume has grown 5x and a
   follow-up review confirms MSK still fits; a separate, smaller decision
   (a new consumer group's partition strategy) gets its own ADR
   (`0014`) rather than being silently folded into the original one,
   keeping each decision's reasoning traceable independently.

## Cross-references

- [technical-roadmap-ownership-and-cross-team-coordination](../technical-roadmap-ownership-and-cross-team-coordination/SKILL.md) — the lead-level work that sequences and resources implementation of the architecture and technology decisions made here across individual teams' roadmaps.
- [independent-solution-design-and-technical-review](../independent-solution-design-and-technical-review/SKILL.md) — the senior-level design work that operates within the architectural constraints and technology choices this skill sets, and the escalation source when a senior engineer's design can't be met within existing constraints.
- [cloud-well-architected-framework-review](../../../standards-and-compliance-frameworks/skills/cloud-well-architected-framework-review/SKILL.md) — a structured, pillar-based way to audit an existing workload's architecture against reliability/cost/security/performance trade-offs, complementary to this skill's forward-looking design and technology-selection focus.
- [platform-engineering-team-topology-and-operating-model](../../../internal-developer-platform/skills/platform-engineering-team-topology-and-operating-model/SKILL.md) — the team-ownership and "thinnest viable platform" sizing discipline this skill's service-boundary design (step 5) should align with.
