---
name: automation-strategy
description: Use when the question is which automations a store should have at all — auditing the whole automation portfolio, finding lifecycle stages with no coverage, deciding which existing journeys should be split, consolidated, extended or retired, and sequencing them by expected value. Use opportunity-discovery instead when no one has said the problem is automation. Use this before automation-architect, which designs the topology of a single objective once this skill has decided the objective is worth building.
license: MIT
metadata:
  targetbay.display_name: Automation Strategy
  targetbay.version: "2.0.0"
  targetbay.category: automation
  targetbay.requires: email_sms.store_profile, email_sms.customer_intelligence, email_sms.product_intelligence, email_sms.order_intelligence, email_sms.segmentation, email_sms.automation, email_sms.automation_analytics, email_sms.campaign_analytics
  targetbay.composes: automation-architect, audience-discovery
  targetbay.risk_level: plan
  targetbay.execution_mode: plan_then_execute
  targetbay.status: foundation
---

# Automation Strategy

## Purpose

Decide the store's automation portfolio: what exists, what is missing, what is redundant, and what to
build first.

This is the portfolio view. It answers *which journeys should exist* and in what order they are worth
building. [automation-architect](../automation-architect/SKILL.md) then answers *what each one should
look like*.

## When to Use

- A store asks what automations it should have, or whether its current set is adequate
- Onboarding a store and establishing its automation baseline
- A periodic review of automation coverage and performance
- Revenue is flat and the suspicion is structural gaps rather than campaign quality
- Several automations appear to overlap and someone must decide what to merge
- Another skill needs the automation landscape before planning

## When Not to Use

- One objective is already agreed and needs a topology. Use
  [automation-architect](../automation-architect/SKILL.md).
- One journey underperforms and needs tuning. Use
  [automation-optimization](../automation-optimization/SKILL.md).
- The question is about scheduled sends rather than triggered journeys. Use
  [monthly-marketing-planner](../monthly-marketing-planner/SKILL.md).

## Required Context

| Context | Why it is needed | Without it |
|---|---|---|
| Complete list of existing automations with topology and status | The entire audit rests on it | Blocked |
| Automation performance: entry, completion, revenue per entrant | Ranks existing journeys | Partial; coverage only, no value ranking |
| Lifecycle distribution and stage thresholds | Locates gaps and sizes them | Blocked |
| Order history: repeat interval, frequency, AOV | Reveals which transitions leak | Partial |
| Product and category structure | Identifies product-driven journey needs | Product journeys not proposed |
| Campaign performance | Shows where manual sends are simulating a trigger | Partial |
| Store objectives and constraints | Orders the roadmap | Ranking defaults to expected revenue |

## Required MCP Capabilities

Defined in [../../capabilities.yaml](../../capabilities.yaml); tool mappings **TODO** —
[../../docs/mcp-integration.md](../../docs/mcp-integration.md).

| Capability | Used for |
|---|---|
| `email_sms.store_profile` | Vertical, scale, sending posture |
| `email_sms.customer_intelligence` | Lifecycle distribution, transition leakage, value concentration |
| `email_sms.product_intelligence` | Catalogue shape, categories, replenishable products |
| `email_sms.order_intelligence` | Repeat intervals, frequency, AOV distribution |
| `email_sms.segmentation` | Sizing candidate journey audiences |
| `email_sms.automation` | Reading the existing portfolio |
| `email_sms.automation_analytics` | Per-journey and per-node performance |
| `email_sms.campaign_analytics` | Detecting manual sends that should be automations |

## Decision Process

```
Understand business             ← objectives, vertical, constraints
        ↓
Understand customers            ← lifecycle distribution, where the leaks are
        ↓
Understand products             ← replenishable, seasonal, high-consideration
        ↓
Understand existing automations ← topology, status, performance
        ↓
Identify lifecycle gaps         ← which transitions have no coverage
        ↓
Identify audience differences   ← which groups need their own journeys
        ↓
Determine automation variants   ← delegate topology questions to automation-architect
        ↓
Determine topology / timing / channels   ← per selected journey
        ↓
Validate                        ← overlap, cadence, capacity
        ↓
Produce roadmap                 ← ordered by expected value, with dependencies
```

## Decision Rules

Binding: [../../rules/automation-rules.md](../../rules/automation-rules.md),
[../../rules/global-rules.md](../../rules/global-rules.md),
[../../rules/frequency-rules.md](../../rules/frequency-rules.md).

**Finding gaps**

- Walk the lifecycle transitions in
  [../../knowledge/customer-lifecycle.md](../../knowledge/customer-lifecycle.md) and mark each as covered,
  partially covered, or absent.
- Size every gap before recommending it. An uncovered transition affecting a handful of contacts is not a
  priority.
- A manual campaign repeatedly sent to simulate a behavioural trigger is a gap (C11).

**Deciding what to build**

- Rank by expected value: audience size × expected effect × durability, against build and maintenance cost.
- Prefer fixing a leaking existing journey over adding a new one — the audience is already flowing through it.
- Coverage before sophistication. A store missing post-purchase entirely does not need a VIP micro-journey.

**Splitting and consolidating**

- Split only when [../../rules/automation-rules.md#R4](../../rules/automation-rules.md) passes.
- Consolidate when two journeys trigger on the same event with near-identical content (R6).
- Retire journeys that no longer earn their maintenance, after reporting what is lost (S6).

**Sequencing**

- Order by value, but respect dependencies: segments before journeys that need them, data before
  personalisation that depends on it.
- Cap concurrent work at what the store can actually build and measure.

## Workflow

| Phase | Action | Risk |
|---|---|---|
| DISCOVER | Read portfolio, lifecycle, orders, products, campaigns | `read_only` |
| ANALYZE | Map coverage, size gaps, rank existing journeys, find overlaps | `analysis` |
| PLAN | Select and order journeys to build, fix, merge or retire | `plan` |
| PREVIEW | Present the roadmap with evidence per item | `plan` |
| VALIDATE | Run the checks below | `plan` |
| APPROVE | Human selects what proceeds | — |
| EXECUTE | Delegate each selected journey to [automation-architect](../automation-architect/SKILL.md) | `plan` → `mutation` |
| MEASURE | Re-run after the built journeys accumulate volume | — |

## Expected Output

A [skill result](../../schemas/skill-result.schema.json) containing:

1. **Coverage map** — each lifecycle transition marked covered / partial / absent, with audience size
2. **Existing portfolio assessment** — per journey: performance, verdict (keep, fix, split, merge, retire), evidence
3. **Ranked roadmap** — ordered recommendations conforming to
   [../../schemas/recommendation.schema.json](../../schemas/recommendation.schema.json), each with expected
   outcome, dependencies and risks
4. **Explicitly rejected journeys** — considered and not recommended, with reasons

No fixed number of recommendations. A store with good coverage may correctly receive two.

## Validation

- [ ] Every existing automation read and assessed, none silently ignored
- [ ] Every gap sized against `email_sms.segmentation` (A1)
- [ ] Every recommendation carries evidence with period and sample size (G2, G14)
- [ ] No recommendation duplicates an existing journey (G6)
- [ ] Overlaps between recommended journeys identified with precedence (R16)
- [ ] Combined cadence of the roadmap checked against existing contact volume (F2, F3)
- [ ] Roadmap ordered, with dependencies stated
- [ ] Rejected candidates recorded
- [ ] No invented performance figures (G3)

## Approval Requirements

| Action | Risk | Approval |
|---|---|---|
| Audit the portfolio | `read_only` | None |
| Produce the roadmap | `plan` | None |
| Build a recommended journey | `mutation` | Per journey, via automation-architect |
| Activate any journey | `high_impact` | Explicit, per journey |
| Merge or retire an existing journey | `destructive` | Explicit, after reporting what is lost (S6) |

## Examples

**"What automations do we need?"**
Finds five live automations, three of them effectively duplicates of each other triggering on the same
event. Coverage map shows first-time → repeat entirely uncovered, which is also where the largest
customer leak sits. Roadmap: merge the three duplicates, build a second-purchase journey, then
replenishment for the two replenishable categories. Four other candidates rejected on size.

**"Should we split our abandoned cart automation by price?"**
Sizes the high-value tail, checks whether treatment would genuinely differ, and finds it would — the
high-value band justifies SMS follow-up that the rest does not. Recommends a split with the threshold
derived from the store's own AOV distribution, not a round number.

Full trace: [../../examples/automation-strategy.md](../../examples/automation-strategy.md).

## Failure Handling

| Situation | Response |
|---|---|
| `email_sms.automation` unavailable | **Blocked.** The audit is the skill |
| Automation analytics unavailable | **Partial.** Coverage map only; say the ranking is structural, not performance-based |
| New store, no automations | Return a coverage-first baseline roadmap ordered by lifecycle, marked as pre-data |
| Lifecycle data thin | **Partial.** Use order recency directly and say the stage boundaries are provisional |
| Very large portfolio | Assess all, report the ranked subset, and state how many were reviewed |
| Store constraints unknown | Ask once for capacity; otherwise rank on value and flag the assumption |

Degraded outcomes set `status` accordingly and populate `unmet_requirements`.
