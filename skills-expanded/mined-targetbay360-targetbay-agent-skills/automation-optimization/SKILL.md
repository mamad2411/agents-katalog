---
name: automation-optimization
description: Use when a live automation is underperforming and needs tuning rather than redesign — a welcome series that is not converting, an abandoned cart flow whose revenue is down, a drip sequence with falling completion, or a journey that used to work and has declined. Finds which node loses people, whether the timing is wrong, whether the wrong contacts are entering, and whether the journey has decayed through expired offers, dead links or discontinued products. Use automation-architect instead when the journey's shape itself is wrong.
license: MIT
metadata:
  targetbay.display_name: Automation Optimization
  targetbay.version: "2.0.0"
  targetbay.category: optimization
  targetbay.requires: email_sms.automation, email_sms.automation_analytics, email_sms.customer_intelligence, email_sms.order_intelligence, email_sms.segmentation, email_sms.experimentation
  targetbay.composes: ab-testing
  targetbay.risk_level: recommendation
  targetbay.execution_mode: plan_then_execute
  targetbay.status: foundation
---

# Automation Optimization

## Purpose

Find where an existing automation loses people and fix that specific point.

The rule this skill exists to enforce: improve the node that is losing people, not the end of a journey
people already abandoned.

## When to Use

- A live automation underperforms against its goal
- A journey that used to work has declined
- Reviewing automations on a scheduled cadence
- Deciding what to test inside an existing journey
- Entry volume, completion rate or revenue per entrant has moved

## When Not to Use

- The journey's structure is wrong — wrong variants, wrong topology. Use
  [automation-architect](../automation-architect/SKILL.md).
- The store needs a portfolio view. Use [automation-strategy](../automation-strategy/SKILL.md).
- The underperformer is a scheduled campaign. Use
  [campaign-optimization](../campaign-optimization/SKILL.md).
- The journey has too little volume to diagnose. Say so and stop.

## Required Context

| Context | Why it is needed | Without it |
|---|---|---|
| Current topology: nodes, timing, conditions, channels | What is being diagnosed | Blocked |
| Per-node performance and drop-off | Locates the failure | Blocked |
| Entry volume and entry audience composition | Whether the wrong people are entering | Blocked |
| Goal attainment and revenue per entrant | Whether the journey works at all | Blocked |
| Historical performance of the same journey | Whether this is decay or a persistent flaw | Partial |
| Content and offer validity: stock, links, prices | Decayed journeys usually fail here first | Partial |

## Required MCP Capabilities

Defined in [../../capabilities.yaml](../../capabilities.yaml); mappings **TODO**.

| Capability | Used for |
|---|---|
| `email_sms.automation` | Current topology; applying changes after approval |
| `email_sms.automation_analytics` | Per-node drop-off, completion, revenue per entrant |
| `email_sms.customer_intelligence` | Who enters and who completes |
| `email_sms.order_intelligence` | Whether conversion happens outside the attributed window |
| `email_sms.segmentation` | Entry audience composition and size |
| `email_sms.experimentation` | Testing a change inside the journey |

## Decision Process

```
1. Read the current topology and its intent
2. Read per-node performance              ← find the largest drop
3. Check entry first                      ← the wrong entrants make every node look broken
4. Check timing                           ← is the gap right for the customer's decision window?
5. Check content validity                 ← dead links, discontinued products, expired offers
6. Check competition                      ← another journey or campaign contacting the same people
7. Form one hypothesis about the largest loss point
8. Propose the smallest change that tests it
```

## Decision Rules

Binding: [../../rules/automation-rules.md](../../rules/automation-rules.md),
[../../knowledge/experimentation-principles.md](../../knowledge/experimentation-principles.md),
[../../rules/safety-rules.md](../../rules/safety-rules.md).

- Fix the node with the largest loss (R18). Adding nodes after the drop-off point changes nothing.
- Diagnose entry before content. A journey receiving the wrong audience cannot be fixed with copy.
- Timing is the most commonly wrong variable and the cheapest to change (R13).
- Journeys decay. Check for expired offers, discontinued products and dead links before concluding the
  strategy is wrong.
- Removing a node is a legitimate optimisation, and often the correct one (R9).
- Changing a live journey affects contacts already in it. Always state what happens to them (S5).
- One variable at a time, with a stated hypothesis. Test design is delegated to
  [ab-testing](../ab-testing/SKILL.md).
- If volume cannot resolve a test, make the change on reasoning and say that is what was done.

## Workflow

| Phase | Action | Risk |
|---|---|---|
| DISCOVER | Read topology, per-node performance, entry composition | `read_only` |
| ANALYZE | Locate the largest loss; check entry, timing, content validity, competition | `analysis` |
| PLAN | Hypothesis and the smallest change that tests it | `recommendation` |
| PREVIEW | Present diagnosis, evidence, proposed change, effect on in-flight contacts | `recommendation` |
| VALIDATE | Run the checks below | — |
| APPROVE | Human approves the change | — |
| EXECUTE | Apply to the live journey | `mutation` → `high_impact` |
| MEASURE | Re-read per-node performance after enough volume | `read_only` |

## Expected Output

A [skill result](../../schemas/skill-result.schema.json) containing: the per-node loss profile; the
diagnosis with evidence; the hypothesis; the proposed change stated as a topology or parameter delta; the
effect on contacts currently in the journey; the measurement plan and the volume needed to read it; and
risks.

## Validation

- [ ] Per-node performance examined, not just the headline metric
- [ ] Entry audience checked before content is blamed
- [ ] Timing assessed against the customer's actual interval
- [ ] Content validity checked — stock, links, offers, products
- [ ] Competing journeys and campaigns checked (R16)
- [ ] One variable changed
- [ ] Effect on in-flight contacts stated (S5)
- [ ] Volume sufficient to read the result, or the limitation stated
- [ ] Node removal considered, not only addition (R9)

## Approval Requirements

| Action | Risk | Approval |
|---|---|---|
| Read and diagnose | `read_only` / `analysis` | None |
| Recommend a change | `recommendation` | None |
| Modify a live automation | `mutation` → `high_impact` | **Explicit**; state the effect on in-flight contacts |
| Remove a node | `destructive` | Explicit, after reporting what is lost (S6) |
| Pause or deactivate a journey | `high_impact` | Explicit |

## Examples

**"Our welcome series isn't converting."**
Per-node data shows healthy engagement through the first message and a large drop at the second, which
fires three days later. Entry composition is correct. The second message promotes a category most
entrants have no affinity with. Recommends replacing its content selection with affinity-based
personalisation rather than adding a fourth message, and states what happens to the contacts currently
between nodes one and two.

**"Abandoned cart revenue is down."**
Finds entry volume unchanged but conversion halved since a date that coincides with an offer expiry
inside the second node. Diagnosis is decay, not strategy. Recommends refreshing the offer and adding a
validity check to the review cadence.

## Failure Handling

| Situation | Response |
|---|---|
| `email_sms.automation_analytics` unavailable | **Blocked.** Node-level diagnosis needs node-level data |
| Journey volume too low to diagnose | Report that plainly; recommend leaving it alone or consolidating it |
| Topology unreadable | **Blocked** |
| Loss is spread evenly, no single failure point | Report that the structure may be wrong and hand to [automation-architect](../automation-architect/SKILL.md) |
| Change would disrupt in-flight contacts | Surface it, and offer a staged alternative |
| Journey duplicated by another | Report the overlap; consolidation is the fix, not tuning |

Degraded outcomes set `status` and populate `unmet_requirements`.
