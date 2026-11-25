---
name: cross-sell
description: Use when the objective is getting existing customers to buy from a different product or category than they already have — expanding category breadth, promoting complementary products after a purchase, or moving single-category buyers into a second category. Use upsell when the goal is a higher-value version of the same thing.
license: MIT
metadata:
  targetbay.display_name: Cross-sell
  targetbay.version: "2.0.0"
  targetbay.category: revenue
  targetbay.requires: email_sms.customer_intelligence, email_sms.product_intelligence, email_sms.order_intelligence, email_sms.segmentation, email_sms.campaign_analytics
  targetbay.composes: audience-discovery
  targetbay.risk_level: recommendation
  targetbay.execution_mode: plan_then_execute
  targetbay.status: foundation
---

# Cross-sell

## Purpose

Decide which customers should be offered which additional product or category, based on observed
co-purchase and affinity patterns rather than assumption.

Cross-sell is a frequency and breadth lever: customers who buy across more than one category are
generally worth more and retain better. The failure mode is recommending products because they seem
related rather than because customers actually buy them together.

## When to Use

- Expanding customers beyond a single category
- Designing post-purchase complementary product recommendations
- A category needs new buyers from the existing base
- Deciding which products to pair in a campaign or journey

## When Not to Use

- The goal is a higher-value version of the same product. Use [upsell](../upsell/SKILL.md).
- The customer has not bought anything yet — there is no basis for a cross-sell.
- The goal is a repeat of the same purchase. Use
  [customer-retention](../customer-retention/SKILL.md).

## Required Context

| Context | Why it is needed | Without it |
|---|---|---|
| Co-purchase and affinity relationships | The whole basis of the recommendation | Blocked |
| Per-customer purchase history and category breadth | Who is a candidate | Blocked |
| Category and product structure | What the adjacent options are | Blocked |
| Timing between first and cross-category purchase | When to make the offer | Partial |
| Stock and margin posture | Whether the recommendation is worth making | Partial |
| Prior cross-sell campaign results | What has worked here | Partial |

## Required MCP Capabilities

Defined in [../../capabilities.yaml](../../capabilities.yaml); mappings **TODO**.

| Capability | Used for |
|---|---|
| `email_sms.product_intelligence` | Affinity, co-purchase, categories, stock |
| `email_sms.customer_intelligence` | Category breadth, value, engagement |
| `email_sms.order_intelligence` | Purchase history, sequence and timing of category entry |
| `email_sms.segmentation` | Sizing candidate audiences |
| `email_sms.campaign_analytics` | Prior cross-sell performance |

## Decision Process

```
1. Read observed co-purchase relationships     ← what customers actually buy together
2. Identify single-category and narrow buyers  ← the addressable base
3. Rank pairings by observed strength and value
4. Decide the moment                           ← post-purchase, replenishment, or campaign
5. Decide the instrument                       ← recurring pattern → automation; one-off → campaign
6. Delegate audience definition
7. Size the opportunity and rank
```

## Decision Rules

Binding: [../../rules/personalization-rules.md](../../rules/personalization-rules.md),
[../../rules/campaign-rules.md](../../rules/campaign-rules.md),
[../../rules/audience-rules.md](../../rules/audience-rules.md).

- Pairings come from observed co-purchase data, never from assumed relatedness (P5, G3).
- Exclude customers who already own the recommended product (A4). This is the most visible cross-sell
  failure.
- Timing follows the observed gap between the anchor purchase and the cross-category purchase — not an
  arbitrary interval after the first order.
- Prefer a small number of strong recommendations over a catalogue dump. Relevance is the mechanism.
- A recurring, behaviour-triggered pattern belongs in an automation, not a repeated campaign (C11).
- Check stock before recommending (P9, N3).
- Do not discount the cross-sell by default. The mechanism is relevance; a discount is a separate
  decision requiring its own justification (C4).

## Workflow

| Phase | Action | Risk |
|---|---|---|
| DISCOVER | Read affinity, purchase history, category structure, stock | `read_only` |
| ANALYZE | Rank pairings, size the addressable base, derive timing | `analysis` |
| PLAN | Choose instrument, define audiences and exclusions, set content direction | `recommendation` |
| PREVIEW | Present ranked opportunities with evidence | `recommendation` |
| VALIDATE | Run the checks below | — |
| APPROVE | Human selects what proceeds | — |
| EXECUTE | Built by the owning skill | `mutation` |
| MEASURE | Category breadth and revenue per targeted customer | — |

## Expected Output

A [skill result](../../schemas/skill-result.schema.json) with recommendations conforming to
[../../schemas/recommendation.schema.json](../../schemas/recommendation.schema.json): the pairing, the
evidence for it with sample size, the audience and size, exclusions, the moment and instrument, expected
effect, and risks including stock and margin.

## Validation

- [ ] Every pairing supported by observed co-purchase data (G2, P5)
- [ ] Existing owners excluded (A4)
- [ ] Timing derived from observed behaviour
- [ ] Audiences resolved and sized (A1)
- [ ] Stock confirmed for recommended products (P9)
- [ ] Discounting, if proposed, justified separately (C4)
- [ ] Recurring patterns routed to automations rather than repeated campaigns (C11)
- [ ] Cadence impact counted (F2)

## Approval Requirements

| Action | Risk | Approval |
|---|---|---|
| Read and analyse | `read_only` / `analysis` | None |
| Recommend | `recommendation` | None |
| Build a campaign or journey | `mutation` | Preview, then confirm |
| Send or activate | `high_impact` | Explicit |

## Examples

**"How do we get more customers buying across categories?"**
Finds two category pairs with strong observed co-purchase and a large single-category base for one of
them. Recommends a post-purchase automation for the recurring pattern and a one-off campaign for the
standing base, with owners of the target category excluded from both.

**"Promote accessories to our equipment buyers."**
Confirms the pairing is real in the data, derives the typical gap between the equipment purchase and the
accessory purchase, and recommends timing the offer just ahead of that gap rather than immediately after
the order — when the customer has not yet used the product.

## Failure Handling

| Situation | Response |
|---|---|
| `email_sms.product_intelligence` unavailable | **Blocked.** Affinity is the basis of the skill |
| No observable co-purchase patterns | Report it. Recommend category-level testing rather than inventing pairings |
| Catalogue too small for meaningful pairing | Recommend a different lever and say why |
| Target category out of stock | Do not recommend it; flag the dependency |
| Addressable base too small | Recommend folding into an existing send (A12) |

Degraded outcomes set `status` and populate `unmet_requirements`.
