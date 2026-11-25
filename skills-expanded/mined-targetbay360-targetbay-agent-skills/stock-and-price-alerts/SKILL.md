---
name: stock-and-price-alerts
description: Use when a change in availability or price should reach specific customers rather than the whole list — a back-in-stock alert to the people who asked for one, a low-stock nudge on an item already sitting in a cart, a price-drop notice to people who viewed or saved something, or collecting a waitlist before a product exists. Decides who is notified and in what order, whether the units available justify notifying anyone at all, and when price-drop messaging starts teaching customers to wait for a discount instead of buying. Answers "set up back-in-stock alerts" and "should we announce that a price dropped?". Use product-launch when a product, collection or restock is being announced as a campaign, and product-replenishment for products bought again on a consumption cycle.
license: MIT
metadata:
  targetbay.display_name: Stock and Price Alerts
  targetbay.version: "1.0.0"
  targetbay.category: revenue
  targetbay.requires: email_sms.product_intelligence, email_sms.customer_intelligence, email_sms.order_intelligence, email_sms.segmentation, email_sms.event_tracking, email_sms.automation, email_sms.suppression_and_consent
  targetbay.composes: audience-discovery, automation-architect
  targetbay.risk_level: recommendation
  targetbay.execution_mode: plan_then_execute
  targetbay.status: foundation
---

# Stock and Price Alerts

## Purpose

Decide whether a change in availability or price is worth a message, who receives it and in what
order, and where price-drop messaging stops being a conversion lever and starts being a discount
habit.

Notifying a waitlist larger than the stock converts demand into complaints: everyone arriving after
the units are gone has been given a reason to be disappointed. Repeatedly telling the same viewers a
price has fallen teaches them that waiting works, and the margin does not recover. Decide both before
the alert is built — neither shows up in the alert's own conversion rate.

## When to Use

- Setting up back-in-stock alerts for people who asked to be told
- Deciding whether a price drop should be messaged, and to whom
- A low-stock nudge on an item already in someone's cart
- Collecting a waitlist before a product is available to buy
- Reviewing whether existing availability or price alerts are eroding margin

## When Not to Use

- A product, collection or restock is being announced as a campaign to a broad audience. Use
  [product-launch](../product-launch/SKILL.md) — a restock announcement is a launch, not an alert.
- The product is bought again on a consumption cycle and the trigger is elapsed time rather than a
  stock or price change. Use [product-replenishment](../product-replenishment/SKILL.md).
- The question is which products to recommend alongside one another. Use
  [cross-sell](../cross-sell/SKILL.md).
- The question is how deep a discount should be for a segment. Use
  [aov-growth](../aov-growth/SKILL.md); this skill decides whether the change is worth a message.

## Required Context

| Context | Why it is needed | Without it |
|---|---|---|
| Units actually available for the product | Decides whether anyone should be notified at all | Blocked |
| Who requested an alert, and when they requested it | The waitlist and its order | Blocked |
| Consent and suppression state for those contacts | Reachability | Blocked |
| Price history for the product | Whether this is a drop, a promotion or a correction | Blocked for price alerts |
| Margin position at the new price | Whether the drop is worth amplifying | Partial; margin risk unstated |
| View, save or cart signal per contact | The audience for a price alert, where there is no explicit waitlist | Partial; price alerts fall back to prior purchasers |
| How often each contact has already received an alert | The discount-habit bound | Partial; the bound cannot be enforced |
| Prior alert performance | Whether the instrument works for this store | Partial |

## Required MCP Capabilities

Defined in [../../capabilities.yaml](../../capabilities.yaml); mappings **TODO**.

| Capability | Used for |
|---|---|
| `email_sms.product_intelligence` | Availability, price history, margin position, variant structure |
| `email_sms.customer_intelligence` | Who asked, who viewed or saved, prior alert history per contact |
| `email_sms.order_intelligence` | Prior purchase of the product or its category, and what the contact paid |
| `email_sms.segmentation` | Sizing and materialising the waitlist and the alert audience |
| `email_sms.event_tracking` | Recording alert requests and alert sends against the contact |
| `email_sms.automation` | The journey that carries the alert |
| `email_sms.suppression_and_consent` | Reachability per channel before any alert is sent |

## Decision Process

```
1. Establish the units actually available          ← the gate, before any audience work
2. If the waitlist exceeds the units, decide the notify count, not the whole list
3. Decide the serving order and say which it is
     request order — fair · expected value — not fair, sometimes right
4. For a price change: is it a drop, a promotion, or a correction?
5. Check the contact's alert history against the discount-habit bound
6. Confirm consent and suppression per contact
7. Decide the channel — urgency argues for SMS, cost and consent often argue against
8. Define the expiry: an alert with no deadline is a newsletter
9. Produce the plan, with the margin position stated for price alerts
```

## Decision Rules

Binding: [../../rules/audience-rules.md](../../rules/audience-rules.md),
[../../rules/campaign-rules.md](../../rules/campaign-rules.md),
[../../rules/personalization-rules.md](../../rules/personalization-rules.md),
[../../rules/frequency-rules.md](../../rules/frequency-rules.md).

- Units available gate the audience, not the other way round. Notifying a waitlist larger than the
  stock manufactures disappointment; size the notify group to the units and state the rule used (A2).
- The serving order is a decision, stated rather than defaulted. Request order is fair and is what
  the customer expects; expected value earns more and is not fair. Say which was chosen and why.
- A price alert is bound by how often that contact has already received one. Repeated drop notices to
  the same viewers train discount-waiting, and the effect shows up in margin rather than in the
  alert's conversion rate (C4, C5).
- Distinguish a genuine price drop from a promotion and from a correction. Messaging a correction as
  a drop is a claim the store cannot support (N3 in
  [../../rules/content-rules.md](../../rules/content-rules.md)).
- Alert on verified availability and verified price only. A stale availability read that says
  "in stock" is worse than no alert, because the customer acts on it (P1, P9, G3).
- Variant matters. Back in stock in one size is not back in stock for the person who wanted another;
  alert on the variant the contact asked for, or say plainly which variant returned.
- Every alert carries an expiry, and the expiry is real. An alert with no deadline gives no reason to
  act today (C4).
- Alerts spend from the same frequency budget as everything else, and a contact on several waitlists
  can receive several alerts in a day — resolve that collision explicitly (F2, F8).
- Consent is checked per channel at send time, not at request time — someone who asked to be told
  months ago may have unsubscribed since (A10, A13).
- Where there is no explicit waitlist, an inferred audience from views or saves is weaker evidence.
  Say so, and do not present inference as a request (A9).

## Workflow

| Phase | Action | Risk |
|---|---|---|
| DISCOVER | Read availability, price history, margin, waitlist, alert history, consent | `read_only` |
| ANALYZE | Gate on units; size and order the notify group; classify the price change | `analysis` |
| PLAN | Notify count and order, channel, expiry, discount-habit bound, collision handling | `recommendation` |
| PREVIEW | Present the audience with its size against the units, and the margin position | `recommendation` |
| VALIDATE | Run the checks below | — |
| APPROVE | Human approves the alert and the serving order | — |
| EXECUTE | Create the alert journey or campaign | `mutation` |
| — | **Sending the alert** | `high_impact`, explicit approval |
| MEASURE | Conversion per alert, and margin per order against the pre-alert baseline | — |

## Expected Output

A [skill result](../../schemas/skill-result.schema.json) containing: the units available and the
notify count derived from them; the serving order and the reason for it; the audience with its size
and how it was assembled; the channel and the expiry; the margin position for a price alert; the
discount-habit bound applied; collision handling where a contact qualifies for several alerts; and
the risks, including what happens to the people not notified.

## Validation

- [ ] Units available established before any audience is sized (A2)
- [ ] Notify count derived from the units, not from the waitlist size
- [ ] Serving order stated explicitly, with the reason
- [ ] Price change classified as drop, promotion or correction before messaging it
- [ ] Margin position stated for any price alert (C4)
- [ ] Per-contact alert frequency bounded against the discount habit (C5, F2)
- [ ] Availability and price verified at send time, not at plan time (P9)
- [ ] Variant-level accuracy confirmed, or the returning variant stated plainly
- [ ] Expiry set and real (C4)
- [ ] Consent confirmed per channel at send time, not request time (A10, A13)
- [ ] Inferred audiences labelled as inference rather than presented as requests (A9)
- [ ] Collision with other alerts and campaigns resolved explicitly (F8)

## Approval Requirements

| Action | Risk | Approval |
|---|---|---|
| Read availability, price and waitlist | `read_only` / `analysis` | None |
| Recommend the alert and its audience | `recommendation` | None |
| Create the alert journey or campaign | `mutation` | Preview, then confirm |
| **Send the alert** | `high_impact` | **Explicit**, with the notify count against units shown (S4) |
| **Notify a waitlist larger than the units available** | `high_impact` | **Explicit**, with the expected disappointment count stated |

## Examples

**"Set up back-in-stock alerts for the people who asked."**
Finds the waitlist substantially larger than the returning units, and the units concentrated in two
of five sizes. Recommends alerting only the contacts who asked for the sizes that actually returned,
sized to the units, in request order — and holding the rest on the list rather than telling them
something came back that did not come back for them. Rejected: alerting the whole waitlist, which
would have converted a good demand signal into complaints from most of it.

**"The price dropped — should we tell people?"**
Checks the price history and finds two drops on the same product within a short period, with a
material overlap in the audience that received the first. Recommends messaging only contacts who did
not receive the previous notice, and flags that a third drop to the same group would be training
rather than converting. States the margin position at the new price, which the store had not looked
at. Rejected: messaging everyone who viewed the product, which is the version that erodes the price
the fastest.

## Failure Handling

| Situation | Response |
|---|---|
| Availability data unavailable or stale | **Blocked.** An alert on unverified stock sends customers to an out-of-stock page, which is worse than no alert (P9, S12) |
| No waitlist and no view or save signal | **Blocked** for back-in-stock. There is no audience that asked; a broad announcement is [product-launch](../product-launch/SKILL.md) instead |
| Price history unavailable | **Blocked** for price alerts. A drop cannot be distinguished from a correction |
| Margin position unavailable | **Partial.** Proceed with the alert and state that the margin impact is unquantified (G15) |
| Per-contact alert history unavailable | **Partial.** The discount-habit bound cannot be enforced; recommend a conservative cadence and say why |
| Variant-level availability not recorded | **Partial.** Alert at product level and state plainly which variant returned, rather than implying all did |
| No platform availability or price trigger exists | **Partial.** The trigger is store-pushed or polled externally; placement is decided by [automation-orchestration](../automation-orchestration/SKILL.md) |

Degraded outcomes set `status` and populate `unmet_requirements`.
