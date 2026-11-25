---
name: aov-growth
description: Use when average order value is the objective and the lever is not yet chosen — ranking thresholds, bundling, merchandising, tier moves and cross-category attachment against each other by revenue effect and margin cost. Owns free-shipping and gift threshold design. Answers "raise our average order value" and "where is our basket losing value?". Use upsell once the chosen lever is an upward move onto a premium tier, larger size or subscription, and cross-sell once it is attachment in another category.
license: MIT
metadata:
  targetbay.display_name: AOV Growth
  targetbay.version: "2.0.0"
  targetbay.category: revenue
  targetbay.requires: email_sms.order_intelligence, email_sms.customer_intelligence, email_sms.product_intelligence, email_sms.segmentation, email_sms.campaign_analytics
  targetbay.composes: upsell, cross-sell, audience-discovery
  targetbay.risk_level: recommendation
  targetbay.execution_mode: plan_then_execute
  targetbay.status: foundation
---

# AOV Growth

## Purpose

Decide which AOV lever this store should pull, for which customers, and what it costs in margin.

AOV is the third term of the revenue equation and usually the least worked. The failure this skill
exists to prevent is reaching for the mechanism someone already had in mind: a lever aimed at the wrong
cluster suppresses conversion, and the loss appears as fewer orders rather than as an obvious AOV
failure.

## When to Use

- AOV is flat or declining and the cause is unknown
- Choosing between threshold, bundle, tier and attachment mechanics
- A revenue target needs an AOV contribution
- Setting or re-setting a free-shipping or gift threshold
- Reviewing whether existing AOV mechanics still earn their margin cost

## When Not to Use

- The lever is already decided and it moves a customer upward — premium tier, larger size, bundle,
  subscription. Use [upsell](../upsell/SKILL.md).
- The lever is already decided and it is attachment in another category. Use
  [cross-sell](../cross-sell/SKILL.md).
- Thresholds are **not** an exception to those two: threshold design stays here.
- The goal is more orders. Use [customer-retention](../customer-retention/SKILL.md).
- The store's pricing strategy itself is the question — outside this package.

## Required Context

| Context | Why it is needed | Without it |
|---|---|---|
| The AOV distribution, not the average | The average hides where movement is possible | Blocked |
| Basket composition: items per order, category mix | Which lever applies | Blocked |
| Threshold response history | Whether thresholds work here, and at what level | Partial |
| Product tiers, bundles and sizes | What customers can be moved to | Partial |
| Margin posture by product and tier | Whether a bigger order is actually worth more | Partial; state the caveat |
| Discount dependence per segment | Who must not be pushed upward | Partial |

## Required MCP Capabilities

Defined in [../../capabilities.yaml](../../capabilities.yaml); mappings **TODO**.

| Capability | Used for |
|---|---|
| `email_sms.order_intelligence` | AOV distribution, basket composition, threshold behaviour |
| `email_sms.customer_intelligence` | Value bands, price sensitivity, headroom |
| `email_sms.product_intelligence` | Tiers, bundles, attachment candidates, margin signals |
| `email_sms.segmentation` | Sizing each lever's audience |
| `email_sms.campaign_analytics` | Prior AOV mechanic performance |

## Decision Process

```
1. Read the distribution, not the average
2. Locate the dense clusters and the gaps between them
3. Decompose AOV               ← items per order × average item value
4. Choose the lever per cluster:
      items per order low   → attachment, bundling, thresholds
      item value low        → tier moves, premium mix, merchandising
5. Exclude the price-sensitive from upward pushes
6. Cost each lever in margin, not only revenue
7. Rank by net effect, and say what conversion risk each carries
```

Step 3 matters: two stores with identical AOV and opposite problems need opposite levers.

## Decision Rules

Binding: [../../rules/campaign-rules.md](../../rules/campaign-rules.md),
[../../knowledge/marketing-principles.md](../../knowledge/marketing-principles.md),
[../../rules/audience-rules.md](../../rules/audience-rules.md).

- Work from the distribution. A single average conceals whether the problem is basket size or item value.
- Thresholds are usually the lowest-risk lever: they raise value without repositioning the customer, and
  they are set just above the dense part of the distribution — never at a round number.
- A threshold set too high is worse than none; it is visible, ignored, and signals the store misread its
  own customers.
- Bundles must carry genuine value at protected margin, not a discount renamed (C4).
- Do not push premium at customers whose price-band history shows no headroom (C5).
- Always state margin effect alongside revenue effect. A larger order at a worse margin can be a loss.
- Always state conversion risk. AOV mechanics that suppress order count usually lose overall.
- Prefer levers that do not spend margin before those that do.

## Workflow

| Phase | Action | Risk |
|---|---|---|
| DISCOVER | Read distribution, basket composition, tiers, margin, prior mechanics | `read_only` |
| ANALYZE | Decompose AOV, locate clusters, match levers, exclude the price-sensitive | `analysis` |
| PLAN | Rank levers with revenue, margin and conversion effects | `recommendation` |
| PREVIEW | Present ranked levers with their trade-offs | `recommendation` |
| VALIDATE | Run the checks below | — |
| APPROVE | Human selects | — |
| EXECUTE | Delegated to [upsell](../upsell/SKILL.md), [cross-sell](../cross-sell/SKILL.md) or campaign work | `mutation` |
| MEASURE | AOV **and** order count together, per targeted segment | — |

## Expected Output

A [skill result](../../schemas/skill-result.schema.json) containing: the AOV distribution with its dense
clusters; the decomposition into items per order and item value; ranked levers, each with audience, size,
expected revenue effect, margin cost, conversion risk and the owning skill; threshold levels derived from
the distribution with the derivation shown; and the levers rejected with reasons.

## Validation

- [ ] Distribution examined, not only the average
- [ ] AOV decomposed into items per order and item value
- [ ] Threshold levels derived from the distribution, never rounded (G3)
- [ ] Price-sensitive segments excluded from upward pushes (C5)
- [ ] Margin effect stated alongside revenue effect
- [ ] Conversion risk stated per lever
- [ ] Audiences resolved and sized (A1)
- [ ] Measurement plan includes order count, not just AOV
- [ ] Rejected levers recorded

## Approval Requirements

| Action | Risk | Approval |
|---|---|---|
| Read and analyse | `read_only` / `analysis` | None |
| Recommend levers | `recommendation` | None |
| Build campaigns or journeys | `mutation` | In the owning skill; preview then confirm |
| Send or activate | `high_impact` | Explicit |
| Change a live threshold | `mutation` | Confirm; state the margin exposure at current volume |

## Examples

**"Raise our average order value."**
Decomposition shows item value is healthy and items per order is low — a basket-size problem, not a
premium problem. The distribution has a dense cluster just below a natural bundle price. Recommends a
free-shipping threshold set just above that cluster plus attachment recommendations, and explicitly
rejects a premium-tier push, which would target customers whose history shows no headroom.

**"Should we lower our free shipping threshold?"**
Finds the current threshold sits well above the dense part of the distribution, so most customers never
approach it and it changes no behaviour. Recommends moving it down to just above the cluster and states
the shipping-margin exposure at current volume, so the trade-off is explicit rather than implied.

## Failure Handling

| Situation | Response |
|---|---|
| `email_sms.order_intelligence` unavailable | **Blocked.** The distribution is the input |
| Margin data unavailable | **Partial.** State that levers are ranked on revenue only and margin is unverified |
| No evidenced headroom in any segment | Recommend threshold and attachment levers only, and say why tier pushes are unsupported |
| Catalogue has no tiers, bundles or attachments | Report it as a merchandising constraint, not a messaging one |
| Distribution too flat to site a threshold | Say so; a threshold with no cluster to sit above will not move behaviour |
| Store insists on a broad premium push | Plan it, state the conversion risk, and recommend testing on a subset first |

Degraded outcomes set `status` and populate `unmet_requirements`.
