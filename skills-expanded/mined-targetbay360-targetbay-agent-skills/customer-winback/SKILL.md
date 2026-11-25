---
name: customer-winback
description: Use when targeting customers who have already lapsed — dormant or churned contacts who have stopped buying and largely stopped engaging. Decides who is worth recovering, what would actually bring them back, how many attempts are justified, and when continued sending should stop in favour of suppression. Answers "should we keep emailing our dormant list?" and "can we win these customers back?". Use customer-retention for customers who are still active, and channel-optimization when the question is which channel to reach them on rather than whether to reach them at all.
license: MIT
metadata:
  targetbay.display_name: Customer Win-back
  targetbay.version: "2.2.0"
  targetbay.category: retention
  targetbay.requires: email_sms.customer_intelligence, email_sms.order_intelligence, email_sms.product_intelligence, email_sms.segmentation, email_sms.campaign_analytics, email_sms.suppression_and_consent
  targetbay.composes: audience-discovery, list-hygiene, offer-strategy
  targetbay.risk_level: recommendation
  targetbay.execution_mode: plan_then_execute
  targetbay.status: foundation
---

# Customer Win-back

## Purpose

Decide which lapsed customers are worth recovering, what would plausibly bring them back, and where the
attempt should stop.

Win-back has an unusual property: the cost of doing it badly is not just a wasted send but a
deliverability cost, because it means repeatedly mailing people who no longer engage. Knowing when to
stop is part of the skill, not an afterthought.

## When to Use

- A dormant or churned cohort needs a recovery attempt
- Deciding whether a lapsed segment is worth continued sending
- Designing a win-back sequence or journey
- Reviewing list health and deciding what to suppress

## When Not to Use

- Customers are still active or only just going quiet. Use
  [customer-retention](../customer-retention/SKILL.md) — intervention there is cheaper and works better.
- The goal is reactivating engagement without a purchase objective — that is a deliverability and list
  hygiene exercise. Use [list-hygiene](../list-hygiene/SKILL.md), which owns who leaves the sending
  population and by which route.
- The contacts never purchased. They are prospects, not win-back.
- The falling engagement is programme-wide rather than confined to the lapsed base. Use
  [deliverability-qa](../deliverability-qa/SKILL.md) — a win-back sequence launched onto a failing
  sending programme fails with it.

## Required Context

| Context | Why it is needed | Without it |
|---|---|---|
| Lapse definition derived from the store's own intervals | "Lapsed" is store-specific | Blocked |
| Prior purchase history and value per lapsed customer | Determines who is worth recovering | Blocked |
| Engagement recency per channel | Determines who is still reachable | Blocked |
| Prior win-back attempts and their results | Prevents repeating a failed approach | Partial |
| What changed since they left — new products, categories, fixes | The reason to return | Partial; weaker offer strategy |
| Suppression and complaint history | Where sending must stop | Blocked |

## Required MCP Capabilities

Defined in [../../capabilities.yaml](../../capabilities.yaml); mappings **TODO**.

| Capability | Used for |
|---|---|
| `email_sms.customer_intelligence` | Lapse state, prior value, engagement recency |
| `email_sms.order_intelligence` | Purchase history, intervals, what they used to buy |
| `email_sms.product_intelligence` | What is new or relevant to their prior affinity |
| `email_sms.segmentation` | Sizing win-back audiences by value and reachability |
| `email_sms.campaign_analytics` | Prior win-back results |
| `email_sms.suppression_and_consent` | Reachability, complaint risk, suppression state |

## Decision Process

```
1. Derive the lapse definition from this store's intervals
2. Classify the lapsed base into dormancy classes  ← derived here, never a fixed set of windows
     recently lapsed · long lapsed · engaged but not buying · neither engaged nor buying
3. Segment each class by prior value and current reachability
3a. Discard the unreachable                     ← hand to list-hygiene, not another send
4. Identify the reason to return per segment    ← new products, prior affinity, what changed
5. Decide attempt count and escalation          ← bounded, evidence-led
6. Decide channel per attempt                   ← a different channel often beats a louder one
7. Define the stop condition and suppression handover
8. Produce the plan
```

## Decision Rules

Binding: [../../rules/audience-rules.md](../../rules/audience-rules.md),
[../../rules/frequency-rules.md](../../rules/frequency-rules.md),
[../../knowledge/email-principles.md](../../knowledge/email-principles.md).

- Prior value and reachability decide who is worth recovering — not lapse duration alone.
- Contacts with no engagement for long enough to be a deliverability risk are suppressed, not mailed. The
  revenue from mailing a dead list is smaller than the cost it imposes on every other send.
- Bound the attempt count in advance, and define the stop condition before the first send.
- Escalating incentive is legitimate here in a way it is not for at-risk customers — but it still starts
  with relevance, not with the deepest discount.
- A different channel beats a louder one (F6). If email has been ignored for a long time, an SMS attempt
  where consent exists is a stronger move than another email.
- Personalise on what they previously bought, using verified data only (P1, P5).
- A recovered customer re-enters the normal lifecycle and must exit the win-back sequence immediately.
- Never re-add suppressed or unsubscribed contacts (S7).
- **Dormancy classes are derived from this store's own purchase and engagement intervals**, never
  from fixed windows (G2, A6). A store whose customers buy twice a year and one whose customers buy
  weekly do not share a definition of lapsed, and a borrowed window puts active customers in the
  win-back sequence.
- Engagement and purchase are separate axes. A contact still opening but no longer buying is a
  different problem from one who has stopped both, and collapsing them into one "dormant" group
  sends the wrong message to at least one of them.
- The sunset decision is **not made here**. Where the conclusion is that a contact should leave the
  sending population, hand it to [list-hygiene](../list-hygiene/SKILL.md) with the recovery evidence
  attached, so suppression happens in one place with its blast radius reported (G7, S6).
- Win-back is bounded by the same contact budget as everything else (F2, F3). A sequence that
  escalates while a campaign is also reaching the same contacts is escalation to a non-responder
  twice over (F6).
- The offer ladder across attempts is [offer-strategy](../offer-strategy/SKILL.md)'s decision, not a
  default escalation of depth. Each attempt should be a distinct instrument rather than the same
  discount getting deeper (C4, C5).
- Measure recovery by the second purchase, not the first. A discount that buys one transaction from a
  lapsed customer has recovered a sale, not a customer (G1).

## Workflow

| Phase | Action | Risk |
|---|---|---|
| DISCOVER | Read lapse state, prior value, engagement, suppression, prior attempts | `read_only` |
| ANALYZE | Segment by value and reachability; identify what changed | `analysis` |
| PLAN | Attempt count, channel sequence, offer escalation, stop condition | `recommendation` |
| PREVIEW | Present the plan, including the suppression recommendation | `recommendation` |
| VALIDATE | Run the checks below | — |
| APPROVE | Human approves the sequence and the suppression | — |
| EXECUTE | Create campaigns or a journey | `mutation` |
| — | **Sending each attempt** | `high_impact`, explicit approval |
| — | **Suppressing contacts** | `destructive`, explicit approval after reporting what is lost |
| MEASURE | Recovery rate by segment; feed the next cycle | — |

## Expected Output

A [skill result](../../schemas/skill-result.schema.json) containing: win-back audiences ranked by
expected recovery value with sizes; the attempt sequence with channel, offer and spacing per attempt;
the stop condition; the suppression recommendation with its size and rationale; expected recovery with
evidence; and risks including complaint and deliverability exposure.

## Validation

- [ ] Lapse definition derived from this store's intervals, not a fixed number
- [ ] Audiences segmented by prior value **and** reachability (A1)
- [ ] Unreachable contacts routed to suppression, not to more sending
- [ ] Attempt count bounded and the stop condition stated before sending
- [ ] Recovered-customer exit defined
- [ ] Channel choices consent-checked (A10)
- [ ] Escalation starts with relevance, not maximum discount (C4)
- [ ] Complaint and deliverability risk stated
- [ ] Dormancy classes derived from this store's intervals, not fixed windows (G2, A6)
- [ ] Engagement and purchase treated as separate axes, not collapsed
- [ ] Sunset and suppression handed to list-hygiene rather than decided here (G7)
- [ ] Offer ladder delegated to offer-strategy, not a default escalation of depth (C4)
- [ ] Sequence contact counted against campaigns reaching the same contacts (F2, F3)
- [ ] Success defined on the second purchase, not the first (G1)
- [ ] No suppressed contacts targeted (S7)

## Approval Requirements

| Action | Risk | Approval |
|---|---|---|
| Read and analyse | `read_only` / `analysis` | None |
| Recommend the sequence | `recommendation` | None |
| Create campaigns or a journey | `mutation` | Preview, then confirm |
| **Send any attempt** | `high_impact` | **Explicit, per attempt** |
| **Suppress contacts** | `destructive` | **Explicit**, after reporting count and prior value (S6) |

## Examples

**"Win back our lapsed customers."**
Finds three groups: high prior value and still opening, moderate value with no engagement for a long
period, and a large unreachable tail. Recommends a three-attempt sequence for the first group with
escalating relevance rather than escalating discount, a single low-cost attempt for the second, and
suppression for the third with the count and prior value stated so the trade-off is visible.

**"Should we keep emailing our dormant list?"**
Measures engagement and complaint rates for the dormant segment and reports the deliverability cost it
imposes on the rest of the programme. Recommends one final bounded attempt, then suppression, with the
expected revenue and expected cost both stated.

Full trace: [../../examples/customer-winback.md](../../examples/customer-winback.md).

## Failure Handling

| Situation | Response |
|---|---|
| Suppression and consent data unavailable | **Blocked.** Win-back without reachability data risks a deliverability incident |
| Engagement history unavailable | **Partial.** Segment on prior value only; be more conservative on attempt count |
| No prior win-back attempts on record | Proceed with a shorter sequence and treat it as the baseline test |
| Lapsed base very small | Recommend inclusion in an existing campaign rather than a dedicated sequence (A12) |
| Complaint rate already elevated | Recommend suppression first; do not add sends to a reputation problem |
| Store refuses suppression | Proceed with the recovery plan, restate the deliverability cost plainly, and record it as a risk |
| Purchase intervals too sparse to derive a lapse definition | **Partial.** State that the classes are provisional, keep the sequence short, and recommend the measurement before the second attempt (G15) |
| Engagement and purchase cannot be separated | **Partial.** Treat the base as one class, say so, and be more conservative on attempt count |
| Second-purchase data unavailable | **Partial.** Measure on first purchase, and state plainly that recovery cannot be distinguished from a one-off discounted sale (G1) |
| Offer strategy unavailable for the ladder | Design the attempts with instruments unset rather than defaulting to escalating discount depth |

Degraded outcomes set `status` and populate `unmet_requirements`.
