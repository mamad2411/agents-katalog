---
name: offer-strategy
description: Use when deciding what incentive a message should carry, if any — whether a discount is needed at all, and if it is, whether a percentage, a fixed amount, free shipping, a spend threshold, a bundle, a gift, early access or exclusivity fits this audience and this objective better, and how deep it should go. Answers "what offer should we use?", "how much discount is right here?" and "do we need to discount at all?". Use aov-growth when the lever itself is still open between thresholds and merchandising, and campaign-optimization when a campaign has already run.
license: MIT
metadata:
  targetbay.display_name: Offer Strategy
  targetbay.version: "1.0.0"
  targetbay.category: revenue
  targetbay.requires: email_sms.order_intelligence, email_sms.customer_intelligence, email_sms.product_intelligence, email_sms.campaign_analytics, email_sms.segmentation, email_sms.store_profile
  targetbay.composes: audience-discovery
  targetbay.risk_level: recommendation
  targetbay.execution_mode: recommend_only
  targetbay.status: foundation
---

# Offer Strategy

## Purpose

Decide what a message offers — including offering nothing — and at what depth, from what this store's
own customers have actually responded to rather than from what discounting generally achieves.

The failure this skill exists to prevent: the reflex discount. A percentage off is the first thing
reached for, the easiest to justify in the moment, and the most expensive habit a store can acquire,
because it trains customers to wait. The second failure is its mirror — refusing every incentive on
principle, when a threshold or a shipping offer would have moved a specific, identifiable group.

Whether a discount is justified at all is already a rule
([../../rules/campaign-rules.md#C4](../../rules/campaign-rules.md)). This skill is where the
justification gets constructed or fails.

## When to Use

- A campaign or automation needs an incentive decided before it is built
- Someone has proposed a discount and the depth has not been examined
- Deciding whether an offer is needed at all for a given objective
- Choosing between instruments — percentage, fixed, shipping, threshold, bundle, gift, access
- A store's offers have become uniform and their effect is flattening
- Setting the incentive ladder for a multi-stage sequence

## When Not to Use

- The lever is still open between thresholds, bundling, merchandising and attachment. Use
  [aov-growth](../aov-growth/SKILL.md), which owns free-shipping and gift threshold *design*; this
  skill decides which instrument a given message carries.
- The campaign has run and the question is why it underperformed. Use
  [campaign-optimization](../campaign-optimization/SKILL.md).
- The question is which products the offer applies to. Use
  [product-recommendation-strategy](../product-recommendation-strategy/SKILL.md).
- The question is who receives the offer. Use
  [audience-discovery](../audience-discovery/SKILL.md).
- The offer is a loyalty programme benefit rather than a marketing incentive — that belongs to the
  loyalty product, not here.
- Two campaigns are offering the same audience competing incentives. Use
  [campaign-conflict-resolver](../campaign-conflict-resolver/SKILL.md).

## Required Context

| Context | Why it is needed | Without it |
|---|---|---|
| Discount usage history per customer | Who already buys only on discount, and who has never needed one | Blocked |
| Prior offers and what each produced | This store's own response curve rather than a general one | Blocked |
| Order value distribution | Where a spend threshold would sit to move behaviour rather than reward it | Partial; thresholds cannot be derived |
| Customer value and lifecycle stage | Offer depth follows value, not urgency | Partial |
| Product price bands and catalogue position | Whether a fixed amount or a percentage reads as meaningful | Partial |
| Shipping cost structure | Whether free shipping is an offer or a cost absorbed invisibly | Partial; shipping offers become guesses |
| Margin, where the platform supplies it | The cost side of the trade | Partial; cost stated as unquantified |
| Objective and its timeframe | An acquisition offer and a clearance offer are different instruments | Blocked |

## Required MCP Capabilities

Defined in [../../capabilities.yaml](../../capabilities.yaml); mappings **TODO**.

| Capability | Used for |
|---|---|
| `email_sms.order_intelligence` | Discount usage, order value distribution, repeat behaviour after a discounted purchase |
| `email_sms.customer_intelligence` | Value band, lifecycle stage and price sensitivity of the target audience |
| `email_sms.product_intelligence` | Price bands, catalogue position, and margin signals where the platform carries them |
| `email_sms.campaign_analytics` | What prior offers produced here — revenue, conversion and what happened afterwards |
| `email_sms.segmentation` | Sizing the audience each candidate offer would reach |
| `email_sms.store_profile` | Currency, shipping posture and the store's own commercial constraints |

## Decision Process

```
1. State the objective and what would count as it working
2. Test the null offer first              <- can this message work with no incentive at all?
3. Read this store's own discount history <- who needs one, who never has, who only buys on one
4. Shortlist instruments that fit the objective and the audience
5. Derive depth from value and prior response, never from a round number
6. Price the cost side                    <- margin where it exists, cancelled full-price sales where it does not
7. Check the habit effect                 <- what does repeating this teach the audience?
8. Choose, and state what the alternatives would have cost
9. Define the ladder if the sequence has more than one stage
```

## Decision Rules

Binding: [../../rules/campaign-rules.md](../../rules/campaign-rules.md),
[../../rules/global-rules.md](../../rules/global-rules.md),
[../../rules/content-rules.md](../../rules/content-rules.md),
[../../knowledge/marketing-principles.md](../../knowledge/marketing-principles.md),
[../../knowledge/campaign-principles.md](../../knowledge/campaign-principles.md).

- Every discount is justified explicitly (C4). "It is a sale period" is an occasion, not a
  justification. The null offer is the default and has to be argued away.
- Offer depth follows customer value, not urgency (C5). A deadline is a reason to communicate, never
  a reason to discount further.
- Never assume margin data exists (G3). Where the platform does not supply it, state the cost side
  as unquantified and present the trade in units the store can price itself — full-price sales
  likely displaced, and to how many customers.
- Depth is derived from this store's own response history, never a round number chosen because it
  sounds standard (G2). A figure with no derivation is invented data.
- Account for the customers who would have bought anyway. An offer to an audience already converting
  is margin given away, and that is the cost that never appears in the campaign report.
- Consider the habit effect over the horizon, not just the send. Repeating an instrument to the same
  audience teaches them to wait for it, and that cost lands on later campaigns
  ([../../knowledge/marketing-principles.md](../../knowledge/marketing-principles.md)).
- Offers are stated exactly, with their terms, exclusions and expiry (N7). An offer the store cannot
  honour as written is a claim it cannot support (N3).
- Non-monetary instruments are first-class candidates, not consolation prizes. Early access,
  exclusivity and a gift move different audiences than a percentage does, and cost differently.
- A threshold offer is derived from where this store's order values actually sit — above the mode,
  reachable by the target audience — never from a round figure (G2).
- Where the audience is already price-sensitive by observed behaviour, a deeper discount is the
  expensive answer; state the alternative instruments before recommending depth (G7).
- Recommend, never configure. Setting up the promotion belongs to the campaign skill.

## Workflow

| Phase | Action | Risk |
|---|---|---|
| DISCOVER | Read discount history, prior offer results, value distribution, price bands, margin if present | `read_only` |
| ANALYZE | Test the null offer; shortlist instruments; derive depth; price the cost side | `analysis` |
| PLAN | The recommended offer with its depth, terms, expected effect and cost, plus the rejected alternatives | `recommendation` |
| PREVIEW | Present the offer, the audience it reaches, the cost, and the habit effect over the horizon | `recommendation` |
| VALIDATE | Run the checks below | — |
| MEASURE | Revenue, margin where available, and the next purchase behaviour of those who redeemed | — |

## Expected Output

A [skill result](../../schemas/skill-result.schema.json) whose recommendations follow
[recommendation.schema.json](../../schemas/recommendation.schema.json): the recommended instrument
and depth with the derivation shown; the exact terms, exclusions and expiry; the audience and its
size; the cost side, quantified where margin exists and stated as unquantified where it does not;
the habit effect over the stated horizon; the instruments rejected and what each would have cost;
and, where the answer is no offer, the argument for it.

## Validation

- [ ] The null offer was tested and either chosen or argued away (C4)
- [ ] Depth derived from this store's own response history, not a round number (G2)
- [ ] Depth matched to customer value rather than to urgency (C5)
- [ ] Non-monetary instruments considered alongside monetary ones
- [ ] Customers who would have converted anyway accounted for in the cost
- [ ] Margin used only where the platform supplied it; otherwise cost stated as unquantified (G3)
- [ ] Threshold, where used, derived from the store's actual order value distribution
- [ ] Habit effect stated over a horizon longer than this send
- [ ] Terms, exclusions and expiry stated exactly (N7)
- [ ] Nothing offered the store cannot honour as written (N3)
- [ ] Rejected instruments recorded with their reason
- [ ] What could not be checked is declared (G15)

## Approval Requirements

| Action | Risk | Approval |
|---|---|---|
| Read order, customer and offer history | `read_only` / `analysis` | None |
| Recommend the offer and its depth | `recommendation` | None |
| Configure a promotion or discount code | `mutation` | Out of scope; owned by the campaign skill |
| **Send a message carrying the offer** | `high_impact` | **Explicit**, owned by the sending skill |

## Examples

**"We need 20% off for the spring campaign."**
Tests the null offer first and finds a third of the intended audience has never used a discount code
and is converting at full price, so the campaign would be paying them to do what they already do.
Reads the store's own history and finds that its last three offers at that depth produced revenue
indistinguishable from its offers a tier shallower, which makes the extra depth unpriced cost rather
than unpriced benefit. Recommends splitting: no offer for the full-price converters with the
campaign carrying the product story instead, and a shipping-threshold offer for the
discount-responsive group derived from where their order values actually sit. States the cost side
as displaced full-price sales, because the platform supplies no margin data, and labels it as
unquantified rather than estimating it. Rejected: the flat 20% to everyone, and a deeper offer for
the lapsed group, which would be the third time this year and is how a store teaches people to wait.

**"What should we offer to win back customers who haven't bought in a year?"**
Finds that prior win-back offers at increasing depth produced redemptions whose second purchase rate
was materially worse than the store's baseline — the discount recovered a transaction, not a
customer. Recommends leading the first attempt with early access to a new collection rather than a
price cut, because it tests interest without setting a price anchor, and reserving a monetary offer
for the final attempt where the alternative is suppression anyway. Defines the ladder so each stage
is a distinct instrument rather than the same discount getting deeper. Rejected: opening at the
deepest discount, which is the common pattern and leaves nothing to escalate to.

## Failure Handling

| Situation | Response |
|---|---|
| Discount usage history unavailable | **Blocked.** Without knowing who already buys on discount, every recommendation is a guess about the cost |
| Prior offer results unavailable | **Blocked.** Depth derived from no response history is an invented number (G2) |
| Objective not stated | **Blocked.** Acquisition, clearance, reactivation and loyalty call for different instruments |
| Margin data absent | Proceed. State the cost side in displaced full-price sales and label it unquantified (G3) |
| Order value distribution unavailable | **Partial.** Threshold instruments drop off the shortlist; say why rather than picking a round figure |
| Shipping cost structure unavailable | **Partial.** Shipping offers are presented with their cost unknown, not recommended as cheap |
| Customer value bands unavailable | **Partial.** Recommend one offer for the whole audience and state that depth could not be matched to value (C5) |
| Store insists on a depth the evidence does not support | Record the objection with the habit cost stated, proceed with their decision, and log it as an accepted risk |
| No instrument clears the cost test | Recommend no offer, and say what the campaign should carry instead |

Degraded outcomes set `status` and populate `unmet_requirements`.
