---
name: review-request-program
description: Use when a store needs to collect more reviews — designing or fixing how and when it asks customers, choosing the trigger and the delay, deciding which products to prioritise, adding or removing a follow-up, or working out why submissions are low despite requests going out. Covers photo and video asks as well as text.
license: MIT
metadata:
  targetbay.display_name: Review Request Programme
  targetbay.version: "2.0.0"
  targetbay.category: outreach
  targetbay.requires: reviews.store_profile, reviews.product_coverage, reviews.review_requests, reviews.request_analytics, reviews.order_intelligence, reviews.suppression_and_consent, reviews.ugc_media, reviews.messaging
  targetbay.composes: review-coverage
  targetbay.risk_level: plan
  targetbay.execution_mode: plan_then_execute
  targetbay.status: foundation
---

# Review Request Programme

## Purpose

Decide how a store asks for reviews: on what trigger, after how long, for which products, on which
channel, and with how many reminders.

Most stores that "need more reviews" are already asking. The problem is usually timing, coverage of the
ask, or friction in the submission — not the absence of a request
([../../knowledge/review-programme-principles.md](../../knowledge/review-programme-principles.md)).

## When to Use

- No request programme exists and one is needed
- Requests go out but submissions are low
- New products are not acquiring proof automatically
- The request delay was set once and never revisited
- Photo or video coverage is short and needs its own ask
- A backlog of past customers could be asked

## When Not to Use

- The question is which products are short of proof. Use
  [review-coverage](../review-coverage/SKILL.md) — this skill composes it.
- The rating is falling. More requests do not fix a cause
  ([../../rules/response-rules.md#P8](../../rules/response-rules.md)); use
  [rating-diagnosis](../rating-diagnosis/SKILL.md).
- Reviews exist but appear nowhere useful. Use
  [proof-placement](../proof-placement/SKILL.md).
- The whole programme needs assessing. Use
  [review-program-audit](../review-program-audit/SKILL.md).

## Required Context

| Context | Why it is needed | Without it |
|---|---|---|
| Existing request configuration | What already runs; a second flow competes with the first | Blocked |
| Request performance by trigger and delay | Whether the current timing works | Partial; lower confidence |
| Fulfilment or delivery timing | The delay anchors to possession, not order date | Partial; confidence lowered, gap recorded |
| Coverage gap and its ranking | Which products the ask should prioritise | Blocked |
| Consent and suppression state | Who may be contacted, and on what channel | Blocked |
| Order composition | One order, one ask | Partial |
| Media presence per product | Whether a separate media ask is warranted | Partial |

## Required MCP Capabilities

Defined in [../../capabilities.yaml](../../capabilities.yaml); mappings **TODO**.

| Capability | Used for |
|---|---|
| `reviews.store_profile` | Volume, vertical and plan limits that bound the programme |
| `reviews.product_coverage` | Which products the ask should prioritise |
| `reviews.review_requests` | Reading existing configuration; creating or amending it |
| `reviews.request_analytics` | Submission and abandonment by trigger, delay and product |
| `reviews.order_intelligence` | Fulfilment timing, order composition, return and refund state |
| `reviews.suppression_and_consent` | Eligibility, channel and frequency headroom |
| `reviews.ugc_media` | Whether a media ask is warranted and where |
| `reviews.messaging` | Dispatch — only after explicit approval |

## Decision Process

```
1. Read the existing programme               ← extend before adding (G7)
2. Delegate the coverage gap                 ← review-coverage ranks what matters
3. Measure current request performance       ← where does the funnel actually leak
4. Anchor the delay to possession            ← per product, derived not defaulted
5. Decide the trigger and the channel        ← consent first, preference second
6. Decide the follow-up, if any              ← evidence that reminders convert here
7. Decide whether media needs its own ask
8. Size the eligible population and the cadence cost
9. Stage the plan so the first cohort informs the rest
```

## Decision Rules

Binding: [../../rules/global-rules.md](../../rules/global-rules.md),
[../../rules/request-rules.md](../../rules/request-rules.md),
[../../rules/safety-rules.md](../../rules/safety-rules.md).

- Anchor the delay to delivery, not to order date (R1). Where fulfilment data is unavailable, say so,
  lower confidence, and record the gap rather than pretending order date is equivalent.
- Derive the delay per product from category, price band and usage interval (R2). Never state a fixed
  number of days as a universal (G3).
- One order, one ask (R3). A five-item order does not generate five requests.
- Propose at most one reminder, and only where `reviews.request_analytics` shows reminders convert in this
  store (R4).
- Suppress the ask where a return, refund, cancellation or open complaint is visible (R5).
- Prioritise by coverage gap, not by order recency (R6).
- Channel follows consent and engagement, never store preference (R7).
- Media is a later, separate ask to customers who already reviewed (R8).
- Never route customers differently by expected sentiment (R9, [#S3](../../rules/safety-rules.md)). If a
  proposal only works by filtering who gets asked based on predicted happiness, reject it.
- Extend the existing programme before adding a parallel one (G7).
- Dispatch is `high_impact`: staged, sized and approved per cohort
  ([#S5](../../rules/safety-rules.md), [#S7](../../rules/safety-rules.md),
  [#S10](../../rules/safety-rules.md)).

## Workflow

| Phase | Action | Risk |
|---|---|---|
| DISCOVER | Read existing requests, performance, consent, orders, coverage | `read_only` |
| ANALYZE | Locate the funnel leak; derive delays per product group | `analysis` |
| PLAN | Trigger, delay, channel, follow-up, prioritisation, staging | `plan` |
| PREVIEW | State eligible population per stage, channel and window | `plan` |
| VALIDATE | Run the checks below | — |
| APPROVE | Human approves the first cohort specifically | — |
| EXECUTE | Create or amend request configuration | `mutation` |
| EXECUTE | Dispatch to the approved cohort | `high_impact` |
| VERIFY | Confirm what was created matches what was approved | `read_only` |
| MEASURE | Submission rate by cohort after a full request cycle | `read_only` |

## Expected Output

A [skill result](../../schemas/skill-result.schema.json) containing a staged request plan: per stage, the
trigger, the derived delay and the evidence for it, the product set, the channel, the eligible population
size, the follow-up decision, and the measurement that decides whether the next stage runs.

Each proposal conforms to [../../schemas/recommendation.schema.json](../../schemas/recommendation.schema.json).

Plus: the existing programme as read, the funnel leak identified, and what was rejected — particularly any
ask that was suppressed and why.

## Validation

- [ ] Existing programme read before anything new is proposed (G7)
- [ ] Delay derived per product group from store data, never a fixed default (R2, G3)
- [ ] Delay anchored to possession, or the substitution explicitly declared (R1)
- [ ] One ask per order (R3)
- [ ] Follow-up justified by this store's own reminder performance, or omitted (R4)
- [ ] Return, refund and complaint suppression applied (R5)
- [ ] Channel derived from consent and engagement (R7)
- [ ] No routing by predicted sentiment anywhere in the plan (R9, S3)
- [ ] Every stage states its population size before approval (S7)
- [ ] Stages approved individually, not as a batch (S10)
- [ ] Media ask, if proposed, is separate and later (R8)

## Approval Requirements

| Action | Risk | Approval |
|---|---|---|
| Read and analyse | `read_only` / `analysis` | None |
| Produce the plan | `plan` | None |
| Create or amend request configuration | `mutation` | Preview, then confirm |
| Dispatch requests to real customers | `high_impact` | Explicit, per cohort, with the count shown |

## Examples

**"We're not getting enough reviews."**
Finds requests are going out on order confirmation, days before delivery. Re-anchors the delay to
fulfilment, derives separate windows for consumables and durables from the store's own repeat intervals,
and stages the change on one category first so the submission-rate change is attributable. Rejects adding
a second reminder because the existing reminder converts near zero here.

**"Can we ask our whole customer list from last year?"**
Sizes the backlog, then splits it: customers whose orders are recent enough for a request to make sense,
and those for whom the ask would be about a product they may no longer own. Suppresses the second group,
suppresses everyone with an open return, stages the remainder so the first cohort's opt-out rate is
observed before the rest goes out, and states the count at each stage.

## Failure Handling

| Situation | Response |
|---|---|
| `reviews.review_requests` unavailable | **Blocked.** Cannot read what exists; proposing a programme blind risks duplicating one (G7) |
| `reviews.suppression_and_consent` unavailable | **Blocked.** Contacting customers without eligibility data is not permitted (S11) |
| Fulfilment timing unavailable | **Partial.** Anchor to order date, declare the substitution, lower confidence, record in `unmet_requirements` (R1) |
| `reviews.request_analytics` unavailable | **Partial.** Propose timing from product characteristics only; do not claim the current programme's leak is known |
| `reviews.messaging` unavailable | **Partial.** Produce the plan and the configuration; state that dispatch is owned elsewhere and stop before it |
| Coverage gap unavailable | **Blocked.** Composed skill blocked; prioritisation would be arbitrary |
| Plan limits cap the eligible population | Report the cap, prioritise within it by coverage value, and say what was left out |
| Store has no orders in scope | Report it as the finding rather than producing an empty programme |

Degraded outcomes set `status` and populate `unmet_requirements`.
