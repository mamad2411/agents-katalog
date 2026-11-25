---
name: product-replenishment
description: Use when products are consumed and rebought on a measurable cycle and the store should be reminding customers before they run out — deriving reorder intervals per product and size, deciding which products qualify, and timing the reminder ahead of run-out rather than after it. Use automation-architect for journey topology once the intervals are derived.
license: MIT
metadata:
  targetbay.display_name: Product Replenishment
  targetbay.version: "2.0.0"
  targetbay.category: lifecycle
  targetbay.requires: email_sms.product_intelligence, email_sms.order_intelligence, email_sms.customer_intelligence, email_sms.segmentation, email_sms.automation, email_sms.automation_analytics
  targetbay.composes: automation-architect, audience-discovery
  targetbay.risk_level: recommendation
  targetbay.execution_mode: plan_then_execute
  targetbay.status: foundation
---

# Product Replenishment

## Purpose

Decide which products have a real reorder cycle, derive that cycle from the store's own order data, and
time a reminder to arrive before the customer runs out.

Replenishment is the highest-return automation in consumable categories and worthless in durable ones. The
work is mostly in telling those apart honestly, per product, rather than applying one store-wide interval.

## When to Use

- The catalogue contains consumables with observable repeat purchase
- A replenishment journey needs building or its timing needs fixing
- Deciding which products qualify for reorder reminders
- Reorder reminders exist but fire at the wrong time

## When Not to Use

- Products are durable with no consumption cycle. Say so and stop.
- The goal is a different product rather than the same one again. Use
  [cross-sell](../cross-sell/SKILL.md).
- The customer has already lapsed. Use [customer-winback](../customer-winback/SKILL.md).
- Journey topology is the question and intervals are already known. Use
  [automation-architect](../automation-architect/SKILL.md).

## Required Context

| Context | Why it is needed | Without it |
|---|---|---|
| Repeat purchase history per product and size | The interval is derived from it | Blocked |
| Product attributes: size, format, consumable or durable | Which products qualify | Blocked |
| Delivery time | The reminder must arrive before run-out, allowing for shipping | Partial; state the buffer as assumed |
| Existing replenishment coverage | Prevents duplicate reminders | Blocked |
| Per-customer purchase history | Individual intervals beat product averages | Partial; use product-level |
| Gift and bulk order signals, where available | Those orders pollute interval derivation | Partial; note the caveat |

## Required MCP Capabilities

Defined in [../../capabilities.yaml](../../capabilities.yaml); mappings **TODO**.

| Capability | Used for |
|---|---|
| `email_sms.product_intelligence` | Attributes, size, format, stock |
| `email_sms.order_intelligence` | Repeat intervals per product and per customer |
| `email_sms.customer_intelligence` | Individual patterns, engagement, value |
| `email_sms.segmentation` | Sizing each replenishment audience |
| `email_sms.automation` / `email_sms.automation_analytics` | Existing coverage and its performance |

## Decision Process

```
1. Identify candidate products      ← consumable, with observed repeat purchase
2. Derive the interval per product AND size   ← a large and a small format differ
3. Discard products with insufficient repeat evidence
4. Prefer the individual's own interval where the data supports it
5. Subtract a lead buffer            ← delivery time, so it arrives before run-out
6. Group products with clustered intervals into journeys
7. Decide channel                    ← reorder reminders are a strong SMS candidate
8. Delegate topology to automation-architect
```

## Decision Rules

Binding: [../../rules/automation-rules.md](../../rules/automation-rules.md),
[../../rules/personalization-rules.md](../../rules/personalization-rules.md),
[../../rules/frequency-rules.md](../../rules/frequency-rules.md).

- **Never use one store-wide interval.** Derive per product and per size; this is the single most common
  way this lever is wasted.
- Prefer the individual customer's own interval over the product average where their history supports it.
- The reminder fires **before** run-out, not after. Lead time is delivery time plus a buffer (R13).
- A product with no observable repeat pattern does not qualify. Exclude it and say so rather than assigning
  a default interval (G3).
- Separate gift and bulk orders from interval derivation where the data allows; they inflate intervals.
- Do not discount a reorder by default. The customer is already buying this — a discount here is margin
  given away (C4).
- Exit immediately on reorder. A reminder after purchase is the failure mode customers notice.
- Check existing coverage before building; a duplicate reminder is worse than none (G6).
- One reminder, then at most one follow-up. Repeated nagging on a consumable trains people to ignore it.

## Workflow

| Phase | Action | Risk |
|---|---|---|
| DISCOVER | Read products, repeat history, existing coverage, delivery time | `read_only` |
| ANALYZE | Derive intervals per product and size; qualify or exclude each product | `analysis` |
| PLAN | Group products, set timing, choose channel, delegate topology | `recommendation` |
| PREVIEW | Present qualifying products with their derived intervals and evidence | `recommendation` |
| VALIDATE | Run the checks below | — |
| APPROVE | Human approves | — |
| EXECUTE | Built by [automation-architect](../automation-architect/SKILL.md) | `mutation` |
| — | **Activation** | `high_impact`, explicit approval |
| MEASURE | Reorder rate among reminded customers, against unreminded where possible | — |

## Expected Output

A [skill result](../../schemas/skill-result.schema.json) containing: qualifying products with derived
interval, size variant, sample size and confidence; excluded products with the reason; interval clusters
and the journeys they imply; the lead buffer and how it was derived; channel recommendation per journey;
and audience sizes.

## Validation

- [ ] Intervals derived per product **and** size, never store-wide
- [ ] Every interval carries its sample size
- [ ] Products with insufficient evidence excluded, not defaulted (G3)
- [ ] Lead buffer stated and derived from delivery time
- [ ] Individual intervals used where the data supports them
- [ ] Reorder exit defined
- [ ] Existing coverage checked (G6)
- [ ] Cadence counted against other journeys (F2, F3)
- [ ] Channel consent checked (A10)

## Approval Requirements

| Action | Risk | Approval |
|---|---|---|
| Read and analyse | `read_only` / `analysis` | None |
| Recommend | `recommendation` | None |
| Build journeys | `mutation` | Via automation-architect; preview then confirm |
| Activate | `high_impact` | Explicit, per journey |

## Examples

**"Set up reorder reminders."**
Scans the catalogue and finds a subset with clear repeat patterns. Intervals cluster into two groups, and
the same product in two sizes shows materially different intervals — so size becomes part of the key
rather than an afterthought. Four products are excluded for insufficient repeat evidence, listed with
their sample sizes. Recommends two journeys, SMS for the reminder itself where consent exists.

**"Our reorder reminders aren't working."**
Finds the reminder fires at a single store-wide interval applied to every product, which is early for some
and late for most. The fix is derivation, not copy.

## Failure Handling

| Situation | Response |
|---|---|
| `email_sms.order_intelligence` unavailable | **Blocked.** Intervals cannot be derived |
| No products show repeat patterns | Report it. This catalogue does not support replenishment |
| Repeat sample too small for a product | Exclude it with its sample size; never assign a default |
| Delivery time unknown | **Partial.** State the buffer as assumed and mark it testable |
| Gift and bulk orders indistinguishable | Note that intervals may be inflated and lower confidence |
| Existing reminders already running | Propose fixing their timing rather than adding a second journey |

Degraded outcomes set `status` and populate `unmet_requirements`.
