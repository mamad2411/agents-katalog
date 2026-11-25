---
name: customer-retention
description: Use when the objective is keeping existing customers active — improving repeat purchase rate, reducing churn, strengthening the first-to-second purchase transition, or intervening with customers who are going quiet relative to their own pattern. Works on customers who are still reachable and still buying; use customer-winback once they have stopped.
license: MIT
metadata:
  targetbay.display_name: Customer Retention
  targetbay.version: "2.0.0"
  targetbay.category: retention
  targetbay.requires: email_sms.customer_intelligence, email_sms.order_intelligence, email_sms.product_intelligence, email_sms.segmentation, email_sms.automation, email_sms.automation_analytics, email_sms.campaign_analytics
  targetbay.composes: audience-discovery, automation-architect, product-replenishment
  targetbay.risk_level: recommendation
  targetbay.execution_mode: plan_then_execute
  targetbay.status: foundation
---

# Customer Retention

## Purpose

Find where the store is losing customers it still has, and decide what keeps them.

Retention is the highest-leverage term in the revenue equation for an established store, and the
first-to-second purchase transition is usually where most of the loss happens. This skill locates the
leak before proposing a remedy.

## When to Use

- Repeat purchase rate is flat or declining
- A large cohort bought once and has not returned
- Customers are going quiet relative to their own purchase interval
- Retention coverage needs establishing or reviewing
- A retention programme needs designing across lifecycle stages

## When Not to Use

- Customers have already lapsed and stopped engaging. Use
  [customer-winback](../customer-winback/SKILL.md).
- The goal is a larger basket rather than another purchase. Use [upsell](../upsell/SKILL.md) or
  [cross-sell](../cross-sell/SKILL.md).
- The store needs a full revenue strategy. Use [revenue-growth](../revenue-growth/SKILL.md).

## Required Context

| Context | Why it is needed | Without it |
|---|---|---|
| Cohort repeat rates and purchase intervals | Locates where retention breaks | Blocked |
| Lifecycle distribution | Sizes each stage's retention problem | Blocked |
| Existing lifecycle automations | What already addresses this | Blocked |
| Product replenishment patterns | Timing for reorder-driven retention | Partial |
| Engagement recency and channel preference | Who is still reachable, and how | Partial |
| Historical retention campaign performance | What has worked here before | Partial; lower confidence |

## Required MCP Capabilities

Defined in [../../capabilities.yaml](../../capabilities.yaml); mappings **TODO**.

| Capability | Used for |
|---|---|
| `email_sms.customer_intelligence` | Lifecycle stage, churn signals, engagement, value |
| `email_sms.order_intelligence` | Cohort repeat rates, intervals, frequency |
| `email_sms.product_intelligence` | Replenishables, affinity for the next purchase |
| `email_sms.segmentation` | Sizing retention audiences |
| `email_sms.automation` / `email_sms.automation_analytics` | Existing coverage and its performance |
| `email_sms.campaign_analytics` | Prior retention campaign results |

## Decision Process

```
1. Measure retention by cohort and stage     ← where does it actually break?
2. Derive the store's own intervals          ← "late" is relative to this store, and to this customer
3. Identify the largest leak                 ← usually first-to-second purchase
4. Read existing coverage                    ← what already runs against that leak
5. Decide the instrument                     ← automation for recurring, campaign for a one-off cohort
6. Delegate audiences and topology           ← audience-discovery, automation-architect
7. Size the expected effect from own data
8. Rank and produce recommendations
```

## Decision Rules

Binding: [../../rules/global-rules.md](../../rules/global-rules.md),
[../../rules/automation-rules.md](../../rules/automation-rules.md),
[../../rules/frequency-rules.md](../../rules/frequency-rules.md).

- Derive "at risk" from the customer's own interval, not a store-wide fixed number
  ([../../knowledge/customer-lifecycle.md](../../knowledge/customer-lifecycle.md)).
- Fix the largest leak first. Coverage before sophistication.
- Prefer automations over campaigns: retention is continuous, and a triggered journey catches every cohort.
- Where products are consumable, reorder timing is delegated to
  [product-replenishment](../product-replenishment/SKILL.md), which derives intervals per product and size.
- Intervene early. An at-risk intervention is cheaper and more effective than a win-back later.
- Do not open with a discount for customers who have not yet lapsed — it trains the behaviour it is meant
  to prevent (C4, C5).
- Relevance and timing beat incentive for still-active customers.
- Increasing frequency to a quieting customer is the wrong direction (F6).
- Check that existing journeys are not already covering the leak before proposing new ones (G6).

## Workflow

| Phase | Action | Risk |
|---|---|---|
| DISCOVER | Read cohorts, lifecycle, intervals, existing automations | `read_only` |
| ANALYZE | Measure retention, locate and size the leak | `analysis` |
| PLAN | Choose instruments, delegate audience and topology | `recommendation` |
| PREVIEW | Present ranked recommendations with evidence | `recommendation` |
| VALIDATE | Run the checks below | — |
| APPROVE | Human selects what proceeds | — |
| EXECUTE | Built by the owning skill; activation is `high_impact` | `mutation` |
| MEASURE | Re-measure cohort repeat rate after a full interval has elapsed | — |

## Expected Output

A [skill result](../../schemas/skill-result.schema.json) with recommendations conforming to
[../../schemas/recommendation.schema.json](../../schemas/recommendation.schema.json), each stating: the
leak addressed, audience and size, the instrument, expected effect with evidence, effort, and risks.

Plus: retention measured by cohort and stage, the existing coverage map, and what was rejected.

## Validation

- [ ] Retention measured from this store's data, not assumed (G3)
- [ ] Intervals derived, not fixed
- [ ] Largest leak identified and sized
- [ ] Existing coverage checked before recommending new journeys (G6)
- [ ] Every audience resolved and sized (A1)
- [ ] Cadence impact counted against existing contact (F2, F3)
- [ ] Discount-led recommendations justified (C4)
- [ ] Measurement window at least one full repeat interval

## Approval Requirements

| Action | Risk | Approval |
|---|---|---|
| Read and analyse | `read_only` / `analysis` | None |
| Recommend | `recommendation` | None |
| Build a journey or campaign | `mutation` | In the owning skill; preview then confirm |
| Activate or send | `high_impact` | Explicit |

## Examples

**"Our repeat rate is dropping."**
Cohort analysis shows first-purchase volume steady but second-purchase conversion falling over three
quarters, concentrated in one acquisition channel's cohort. No second-purchase journey exists.
Recommends building one, targeted at the transition rather than at everyone, with timing derived from the
observed gap between first and second orders.

**"Keep our VIPs from lapsing."**
Finds VIP lapse is preceded by a lengthening purchase interval rather than an engagement drop.
Recommends an interval-based at-risk trigger rather than an engagement-based one, and recognition rather
than discount as the intervention.

## Failure Handling

| Situation | Response |
|---|---|
| Order history too short for cohorts | **Partial.** Report what can be measured, state the horizon limitation |
| Customer intelligence unavailable | **Blocked.** Lifecycle work needs lifecycle data |
| Automations unreadable | **Blocked.** Would risk duplicating existing coverage (G6) |
| No repeat purchases at all | Report it as the finding. This is an acquisition-quality or product problem, not a messaging one |
| Intervals too variable to derive | Use per-customer deviation instead of a store-wide threshold, and say so |
| Cadence has no headroom | Recommend replacing existing low-value sends rather than adding |

Degraded outcomes set `status` and populate `unmet_requirements`.
