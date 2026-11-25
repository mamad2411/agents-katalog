---
name: upsell
description: Use when the mechanism is already chosen and it is a move upward — promoting a premium tier, a larger size, a bundle or a subscription to customers whose price-band behaviour shows headroom. Answers "promote our premium tier" and "who can we move up?". Use cross-sell when the goal is a purchase in a different category, and aov-growth when the lever is not yet chosen — it owns thresholds, merchandising and ranking the levers against each other.
license: MIT
metadata:
  targetbay.display_name: Upsell
  targetbay.version: "2.0.0"
  targetbay.category: revenue
  targetbay.requires: email_sms.customer_intelligence, email_sms.product_intelligence, email_sms.order_intelligence, email_sms.segmentation, email_sms.campaign_analytics
  targetbay.composes: audience-discovery
  targetbay.risk_level: recommendation
  targetbay.execution_mode: plan_then_execute
  targetbay.status: foundation
---

# Upsell

## Purpose

Move customers to a higher-value version of what they already buy — a premium tier, a larger size, a
bundle or a subscription — targeting only those whose price-band behaviour shows headroom.

The failure this skill exists to prevent: pushing premium at the price-sensitive. The loss shows up as
fewer orders, not as an obvious upsell failure, so it is easy to miss and easy to repeat.

## When to Use

- A premium tier, bundle, larger size or subscription needs adoption
- Post-purchase or pre-checkout messaging that moves a customer upward
- Identifying which customers have evidenced headroom, and which must be left alone

## When Not to Use

- The lever is not yet chosen, or the question is thresholds, merchandising or which mechanic to use at
  all. Use [aov-growth](../aov-growth/SKILL.md), which ranks the levers and owns threshold design.
- The goal is a different category. Use [cross-sell](../cross-sell/SKILL.md).
- The goal is more orders. Use [customer-retention](../customer-retention/SKILL.md).
- The store's pricing strategy itself is the question — that is outside this package.

## Required Context

| Context | Why it is needed | Without it |
|---|---|---|
| AOV distribution, not just the average | The average hides the distribution that matters | Blocked |
| Per-customer price-band behaviour | Who has demonstrated headroom | Blocked |
| Product tiers, bundles, sizes, subscription options | What there is to move customers to | Blocked |
| Discount dependence per customer | Who is price-sensitive and must not be pushed | Partial |
| Margin posture by tier | Whether a higher order value is actually worth more | Partial |

## Required MCP Capabilities

Defined in [../../capabilities.yaml](../../capabilities.yaml); mappings **TODO**.

| Capability | Used for |
|---|---|
| `email_sms.order_intelligence` | Price-band distribution and what each customer has bought before |
| `email_sms.customer_intelligence` | Price-band behaviour, value, discount dependence |
| `email_sms.product_intelligence` | Tiers, bundles, sizes, subscriptions, margin signals |
| `email_sms.segmentation` | Sizing candidate audiences |
| `email_sms.campaign_analytics` | Prior upsell results, and what the same audience already refused |

## Decision Process

```
1. Read the AOV distribution, not the average
2. Identify customers with demonstrated headroom   ← prior higher-band purchases, rising basket value
3. Identify price-sensitive customers              ← exclude them from premium pushes
4. Match mechanism to segment                      ← tier, size, bundle, subscription
5. Decide the moment                               ← pre-purchase, in-basket, post-purchase, replenishment
6. Delegate audience definition
7. Size the effect on revenue and on margin
```

## Decision Rules

Binding: [../../rules/personalization-rules.md](../../rules/personalization-rules.md),
[../../rules/campaign-rules.md](../../rules/campaign-rules.md),
[../../knowledge/marketing-principles.md](../../knowledge/marketing-principles.md).

- Only target customers whose behaviour shows headroom. Pushing premium at the price-sensitive costs
  conversion (C5).
- An upward move repositions the customer; a threshold does not. If a threshold would achieve the same
  value, it is the cheaper instrument — hand it to [aov-growth](../aov-growth/SKILL.md) rather than
  designing one here.
- Bundles must offer genuine value at protected margin, not a discount wearing a different name (C4).
- Subscription upsell is a retention mechanism as much as an AOV one; evaluate it on both.
- Check margin, not only revenue. A higher order value at a lower margin can be a loss.
- Never misrepresent the value of the higher option (N3, N7).

## Workflow

| Phase | Action | Risk |
|---|---|---|
| DISCOVER | Read AOV distribution, price-band behaviour, product tiers, margin | `read_only` |
| ANALYZE | Locate headroom, exclude price-sensitive, match mechanisms | `analysis` |
| PLAN | Choose mechanism, audience, moment and content direction | `recommendation` |
| PREVIEW | Present ranked opportunities with revenue and margin effect | `recommendation` |
| VALIDATE | Run the checks below | — |
| APPROVE | Human selects what proceeds | — |
| EXECUTE | Built by the owning skill | `mutation` |
| MEASURE | AOV by targeted segment, and conversion rate alongside it | — |

## Expected Output

A [skill result](../../schemas/skill-result.schema.json) with recommendations conforming to
[../../schemas/recommendation.schema.json](../../schemas/recommendation.schema.json): the mechanism, the
audience and size, the moment, expected AOV effect with evidence, margin effect, and risks — including
the conversion risk of pushing value at the wrong segment.

## Validation

- [ ] Headroom read from price-band behaviour, not assumed
- [ ] Headroom evidenced per targeted segment (G2)
- [ ] Price-sensitive customers excluded from premium pushes (C5)
- [ ] Margin effect stated alongside revenue effect
- [ ] Conversion risk stated
- [ ] Audiences resolved and sized (A1)
- [ ] No misrepresented value claims (N3)

## Approval Requirements

| Action | Risk | Approval |
|---|---|---|
| Read and analyse | `read_only` / `analysis` | None |
| Recommend | `recommendation` | None |
| Build a campaign or journey | `mutation` | Preview, then confirm |
| Send or activate | `high_impact` | Explicit |

## Examples

**"Push everyone onto the annual subscription."**
Finds that only the repeat cohort with two or more full-price orders has evidenced headroom. Recommends
the subscription offer to that cohort alone, and reports that a broad push would trade order count for
order value — a net loss at this store's margins. Notes the cheaper alternative it did not choose: if the
goal is simply a larger basket, [aov-growth](../aov-growth/SKILL.md) owns threshold design.

**"Promote our premium tier."**
Identifies the subset with prior higher-band purchases or rising basket values as the only audience with
evidenced headroom, and recommends targeting them rather than the whole base. States that a broad push
would likely depress conversion among the price-sensitive majority.

## Failure Handling

| Situation | Response |
|---|---|
| `email_sms.order_intelligence` unavailable | **Blocked.** AOV work needs the distribution |
| No higher-value options in the catalogue | Report it. This is a merchandising problem, not a messaging one |
| No evidenced headroom in any segment | Report that no upward move is supported, and defer to [aov-growth](../aov-growth/SKILL.md) for levers that do not reposition the customer |
| Margin data unavailable | **Partial.** State that the recommendation optimises revenue, and that margin is unverified |
| Store insists on a broad premium push | Plan it, state the conversion risk explicitly, and recommend testing on a subset first |

Degraded outcomes set `status` and populate `unmet_requirements`.
