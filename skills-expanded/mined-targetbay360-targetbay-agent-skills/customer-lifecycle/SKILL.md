---
name: customer-lifecycle
description: Use when the whole customer journey needs designing or reviewing rather than one stage — mapping where customers actually sit, deriving the store's own stage boundaries, finding which transitions have no coverage, and sequencing the lifecycle programme by where value leaks. Use customer-retention or customer-winback when one stage is already the agreed focus.
license: MIT
metadata:
  targetbay.display_name: Customer Lifecycle
  targetbay.version: "2.0.0"
  targetbay.category: lifecycle
  targetbay.requires: email_sms.store_profile, email_sms.customer_intelligence, email_sms.order_intelligence, email_sms.segmentation, email_sms.automation, email_sms.automation_analytics
  targetbay.composes: customer-retention, customer-winback, automation-strategy, audience-discovery
  targetbay.risk_level: recommendation
  targetbay.execution_mode: plan_then_execute
  targetbay.status: foundation
---

# Customer Lifecycle

## Purpose

Map where the store's customers actually are, derive the boundaries between stages from the store's own
data, and decide which transitions are worth building a programme around.

Lifecycle stages are not universal. A subscription store's "dormant" and a furniture retailer's are
months apart. This skill derives them rather than importing them.

## When to Use

- Designing or reviewing a full lifecycle programme
- Establishing the store's own stage definitions
- Finding which lifecycle transitions have no coverage at all
- Understanding where customers concentrate and where they leak
- Onboarding a store and needing its lifecycle shape first

## When Not to Use

- One stage is already the agreed focus. Use
  [customer-retention](../customer-retention/SKILL.md) or
  [customer-winback](../customer-winback/SKILL.md).
- The question is the automation portfolio. Use
  [automation-strategy](../automation-strategy/SKILL.md), which this skill composes for the build side.
- Targeting for one campaign. Use [audience-discovery](../audience-discovery/SKILL.md).

## Required Context

| Context | Why it is needed | Without it |
|---|---|---|
| Order history long enough to observe repeat behaviour | Stage boundaries are derived from it | Blocked |
| Customer distribution across recency, frequency, value | The map itself | Blocked |
| Purchase intervals, per customer and per category | Where "late" begins | Blocked |
| Existing automation coverage by stage | Which transitions are already served | Blocked |
| Engagement recency per channel | Who is still reachable at each stage | Partial |
| Value concentration | Which stages carry the money | Partial |

## Required MCP Capabilities

Defined in [../../capabilities.yaml](../../capabilities.yaml); mappings **TODO**.

| Capability | Used for |
|---|---|
| `email_sms.store_profile` | Vertical and scale context for stage shape |
| `email_sms.customer_intelligence` | Distribution across stages, engagement, value |
| `email_sms.order_intelligence` | Intervals, cohorts, transition rates |
| `email_sms.segmentation` | Sizing each stage and transition |
| `email_sms.automation` / `email_sms.automation_analytics` | Coverage and performance per stage |

## Decision Process

```
1. Derive the store's repeat interval distribution
2. Set stage boundaries from it        ← never from a generic template
3. Map the current distribution        ← how many customers sit in each stage
4. Measure transition rates            ← which crossings leak
5. Read existing coverage per transition
6. Size each gap                       ← population × value × leak rate
7. Rank the transitions worth building
8. Delegate each to the owning skill
```

## Decision Rules

Binding: [../../knowledge/customer-lifecycle.md](../../knowledge/customer-lifecycle.md),
[../../rules/audience-rules.md](../../rules/audience-rules.md),
[../../rules/automation-rules.md](../../rules/automation-rules.md).

- **Stage boundaries are derived, never imported.** Two stores in the same vertical can differ; one store's
  boundaries move over time.
- Where possible, "at risk" is relative to the *individual's* interval, not a store-wide number.
- Transitions matter more than states. Build around the crossings, not the labels.
- Size each gap before recommending it. An uncovered transition affecting a handful of customers is not a
  priority (G7).
- Coverage before sophistication. A store missing first-to-second entirely does not need a VIP micro-stage.
- Check existing coverage before proposing anything (G6).
- Stages must partition the base: every customer falls in exactly one. Report anyone who falls in none —
  that is a definition bug, not an empty segment.
- Do not invent a stage the store has no customers in.

## Workflow

| Phase | Action | Risk |
|---|---|---|
| DISCOVER | Read orders, customers, intervals, existing coverage | `read_only` |
| ANALYZE | Derive boundaries, map distribution, measure transitions, size gaps | `analysis` |
| PLAN | Rank transitions and assign owning skills | `recommendation` |
| PREVIEW | Present the map, the gaps and the ranked programme | `recommendation` |
| VALIDATE | Run the checks below | — |
| APPROVE | Human selects what proceeds | — |
| EXECUTE | Delegated to the owning skills | `plan` → `mutation` |
| MEASURE | Re-map after at least one full interval | — |

## Expected Output

A [skill result](../../schemas/skill-result.schema.json) containing: derived stage boundaries with the
evidence for each; the current distribution with counts and value per stage; transition rates and where
they leak; a coverage map marking each transition covered, partial or absent; a ranked programme with
owning skills; and the customers who fall outside every stage definition, if any.

## Validation

- [ ] Stage boundaries derived from this store's data, with the derivation shown (G3)
- [ ] Distribution sums to the full customer base; unassigned customers reported
- [ ] Transition rates measured, not assumed
- [ ] Every gap sized (A1)
- [ ] Existing coverage checked per transition (G6)
- [ ] Programme ranked with criteria stated (G14)
- [ ] No stage proposed that has no customers in it
- [ ] Observation window at least one full repeat interval

## Approval Requirements

| Action | Risk | Approval |
|---|---|---|
| Read and analyse | `read_only` / `analysis` | None |
| Recommend a programme | `recommendation` | None |
| Build anything | `mutation` | In the owning skill; preview then confirm |
| Activate or send | `high_impact` | Explicit |

## Examples

**"Map our customer lifecycle."**
Derives boundaries from the repeat-interval distribution and finds the store's natural "at risk" point is
substantially earlier than the generic default it had been using — meaning its win-back campaigns were
firing long after the recoverable window. The map shows the largest population and the largest leak both
at first-to-second purchase. Ranks that transition first, at-risk detection second.

**"Which stages are we not covering?"**
Coverage map shows welcome and abandonment covered, post-purchase generic, and at-risk, dormant and
second-purchase absent. Sizes each and recommends second-purchase first — largest population, largest
value, no coverage.

## Failure Handling

| Situation | Response |
|---|---|
| Order history shorter than one repeat interval | **Partial.** Report what is observable; boundaries are provisional |
| `email_sms.customer_intelligence` unavailable | **Blocked** |
| No repeat purchases at all | Report it as the finding — this is an acquisition or product problem |
| Intervals too variable to cluster | Use per-customer deviation instead of store-wide boundaries and say so |
| Customers fall outside all stages | Report the count; fix the definitions before building on them |
| Store supplies boundaries that contradict its data | Use the store's, state the contradiction and its consequence |

Degraded outcomes set `status` and populate `unmet_requirements`.
